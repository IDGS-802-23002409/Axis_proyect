import click
from flask.cli import with_appcontext
from sqlalchemy import create_engine, text, Table, MetaData
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.utils.config import (
    STAGING_DB_USER, STAGING_DB_PASSWORD, STAGING_DB_HOST, 
    STAGING_DB_PORT, STAGING_DB_NAME,
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
)
from app.utils.database_connection import db
import logging

logger = logging.getLogger('backup_axis')

@click.group()
def backup():
    """Comandos para gestión de respaldos."""
    pass

@backup.command('incremental')
@with_appcontext
def incremental_backup():
    """Realiza un respaldo incremental hacia la base de datos de staging."""
    
    prod_engine = db.engine
    
    staging_uri = f"mysql+pymysql://{STAGING_DB_USER}:{STAGING_DB_PASSWORD}@{STAGING_DB_HOST}:{STAGING_DB_PORT}/{STAGING_DB_NAME}"
    staging_engine = create_engine(staging_uri)
    StagingSession = sessionmaker(bind=staging_engine)
    staging_session = StagingSession()

    try:
        metadata = MetaData()
        metadata.reflect(bind=prod_engine)
        
        for table_name in metadata.tables:
            if table_name in ['security_audit_logs', 'alembic_version']:
                continue
                
            table = metadata.tables[table_name]
            
            if 'fecha_actualizacion' not in table.columns:
                logger.warning(f"La tabla {table_name} no tiene campo 'fecha_actualizacion'. Saltando...")
                continue
            
            try:
                res = staging_session.execute(text(f"SELECT MAX(fecha_actualizacion) FROM {table_name}"))
                last_sync = res.scalar() or datetime(2000, 1, 1)
            except Exception:
                last_sync = datetime(2000, 1, 1)

            query = table.select().where(table.c.fecha_actualizacion > last_sync)
            with prod_engine.connect() as conn:
                new_records = conn.execute(query).fetchall()

            if not new_records:
                click.echo(f"Tabla {table_name}: Sin cambios.")
                continue

            count_synced = 0
            for row in new_records:
                data = dict(row._mapping)
                
                pk_col = list(table.primary_key.columns)[0].name
                pk_val = data[pk_col]
                
                check_query = text(f"SELECT 1 FROM {table_name} WHERE {pk_col} = :pk")
                exists = staging_session.execute(check_query, {"pk": pk_val}).scalar()
                
                if exists:
                    update_parts = ", ".join([f"{k} = :{k}" for k in data.keys() if k != pk_col])
                    update_stmt = text(f"UPDATE {table_name} SET {update_parts} WHERE {pk_col} = :{pk_col}")
                    staging_session.execute(update_stmt, data)
                else:
                    cols = ", ".join(data.keys())
                    vals = ", ".join([f":{k}" for k in data.keys()])
                    insert_stmt = text(f"INSERT INTO {table_name} ({cols}) VALUES ({vals})")
                    staging_session.execute(insert_stmt, data)
                
                count_synced += 1
            
            staging_session.commit()
            click.echo(f"Tabla {table_name}: Sincronizados {count_synced} registros.")

        click.echo(click.style("Respaldo incremental completado con éxito.", fg='green'))

    except Exception as e:
        staging_session.rollback()
        logger.error(f"Error en respaldo incremental: {str(e)}")
        click.echo(click.style(f"Error: {str(e)}", fg='red'))
    finally:
        staging_session.close()

def init_backup_cli(app):
    app.cli.add_command(backup)
