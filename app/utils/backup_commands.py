import click
from flask.cli import with_appcontext
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.utils.config import (
    STAGING_DB_USER, STAGING_DB_PASSWORD, STAGING_DB_HOST,
    STAGING_DB_PORT, STAGING_DB_NAME,
    DB_HOST, DB_PORT, DB_NAME,
    BACKUP_DB_USER, BACKUP_DB_PASSWORD
)
import logging

logger = logging.getLogger('backup_axis')

# ── Tablas que no se sincronizan ─────────────────────────────────────────────
SKIP_TABLES = {'security_audit_logs', 'alembic_version'}


def sync_databases(source_engine, target_engine, log_fn=None, restore_mode=False):
    """
    Sincronización conservativa: solo INSERT/UPDATE. Nunca elimina datos en destino.

    Modos:
    - restore_mode=False (Respaldo incremental Prod->Staging):
        Tablas CON fecha_actualizacion: solo registros más nuevos que el máximo en destino.
        Tablas SIN fecha_actualizacion: solo inserta PKs faltantes.
    - restore_mode=True (Restauración Staging->Prod):
        SIEMPRE compara por PK directamente, sin filtro de fecha.
        Inserta registros faltantes (recupera los borrados).
        Actualiza si la versión de staging es más nueva (tiene fecha_actualizacion).

    Args:
        source_engine: Engine de la BD fuente.
        target_engine: Engine de la BD destino.
        log_fn: Función para logging.
        restore_mode: True para restauración, False para respaldo incremental.
    """
    if log_fn is None:
        log_fn = lambda msg: logger.info(msg)

    src_metadata = MetaData()
    src_metadata.reflect(bind=source_engine)

    TargetSession = sessionmaker(bind=target_engine)
    target_session = TargetSession()

    total_synced = 0

    try:
        for table_name in src_metadata.tables:
            if table_name in SKIP_TABLES:
                continue

            table = src_metadata.tables[table_name]

            if not table.primary_key.columns:
                log_fn(f"  [SKIP] {table_name}: sin PK definida.")
                continue

            pk_col = list(table.primary_key.columns)[0].name
            has_fecha = 'fecha_actualizacion' in table.columns

            with source_engine.connect() as src_conn:
                if not restore_mode and has_fecha:
                    # ── MODO RESPALDO: solo registros más nuevos que en destino ──
                    try:
                        res = target_session.execute(
                            text(f"SELECT MAX(fecha_actualizacion) FROM `{table_name}`")
                        )
                        last_sync = res.scalar() or datetime(2000, 1, 1)
                    except Exception:
                        last_sync = datetime(2000, 1, 1)

                    rows = src_conn.execute(
                        table.select().where(table.c.fecha_actualizacion > last_sync)
                    ).fetchall()
                else:
                    # ── MODO RESTAURACIÓN o tabla sin fecha: todos los registros ──
                    rows = src_conn.execute(table.select()).fetchall()

            if not rows:
                log_fn(f"  [OK] {table_name}: sin cambios.")
                continue

            count = 0
            for row in rows:
                data = dict(row._mapping)
                pk_val = data[pk_col]

                exists = target_session.execute(
                    text(f"SELECT 1 FROM `{table_name}` WHERE `{pk_col}` = :pk"),
                    {"pk": pk_val}
                ).scalar()

                if exists:
                    if has_fecha and restore_mode:
                        # ── MODO RESTAURACIÓN: actualiza si staging es más nuevo ──
                        src_fecha = data.get('fecha_actualizacion')
                        if src_fecha:
                            dest_fecha = target_session.execute(
                                text(f"SELECT fecha_actualizacion FROM `{table_name}` WHERE `{pk_col}` = :pk"),
                                {"pk": pk_val}
                            ).scalar()
                            if dest_fecha and src_fecha <= dest_fecha:
                                continue  # El registro en prod es más nuevo, conservamos

                        parts = ", ".join(
                            [f"`{k}` = :{k}" for k in data if k != pk_col]
                        )
                        target_session.execute(
                            text(f"UPDATE `{table_name}` SET {parts} WHERE `{pk_col}` = :{pk_col}"),
                            data
                        )
                        count += 1
                    elif has_fecha and not restore_mode:
                        # ── MODO RESPALDO: actualiza registros con fecha_actualizacion ──
                        parts = ", ".join(
                            [f"`{k}` = :{k}" for k in data if k != pk_col]
                        )
                        target_session.execute(
                            text(f"UPDATE `{table_name}` SET {parts} WHERE `{pk_col}` = :{pk_col}"),
                            data
                        )
                        count += 1
                    # Sin fecha en modo respaldo: no toca registros existentes
                else:
                    cols = ", ".join([f"`{k}`" for k in data])
                    vals = ", ".join([f":{k}" for k in data])
                    target_session.execute(
                        text(f"INSERT INTO `{table_name}` ({cols}) VALUES ({vals})"),
                        data
                    )
                    count += 1

            target_session.commit()
            total_synced += count
            log_fn(f"  [OK] {table_name}: {count} registros sincronizados.")

        log_fn(f"Sincronización completada. Total registros: {total_synced}.")
        return True, total_synced

    except Exception as e:
        target_session.rollback()
        logger.error(f"Error en sync_databases: {e}")
        log_fn(f"  [ERROR] {e}")
        return False, 0
    finally:
        target_session.close()


# ── CLI: Respaldo Incremental (Prod -> Staging) ──────────────────────────────

@click.group()
def backup():
    """Comandos para gestión de respaldos."""
    pass


@backup.command('incremental')
@with_appcontext
def incremental_backup():
    """Realiza un respaldo incremental de Producción hacia Staging."""
    click.echo("Iniciando respaldo incremental (Prod -> Staging)...")

    prod_uri = f"mysql+pymysql://{BACKUP_DB_USER}:{BACKUP_DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    staging_uri = f"mysql+pymysql://{STAGING_DB_USER}:{STAGING_DB_PASSWORD}@{STAGING_DB_HOST}:{STAGING_DB_PORT}/{STAGING_DB_NAME}"

    prod_engine = create_engine(prod_uri, pool_pre_ping=True)
    staging_engine = create_engine(staging_uri, pool_pre_ping=True)

    success, total = sync_databases(prod_engine, staging_engine, log_fn=click.echo)

    if success:
        click.echo(click.style(f"Respaldo incremental completado. {total} registros.", fg='green'))
    else:
        click.echo(click.style("Error durante el respaldo incremental.", fg='red'))


def init_backup_cli(app):
    app.cli.add_command(backup)
