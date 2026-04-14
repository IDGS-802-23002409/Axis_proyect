import os
import subprocess
import logging
from datetime import datetime
from flask import render_template, current_app, redirect, url_for, flash, send_from_directory, request
from flask_security import roles_accepted, login_required
from sqlalchemy import create_engine
from . import respaldos_bp
from app.utils.config import (
    DB_HOST, DB_NAME, DB_PORT,
    BACKUP_DB_USER, BACKUP_DB_PASSWORD,
    STAGING_DB_HOST, STAGING_DB_PORT, STAGING_DB_NAME,
    STAGING_DB_USER, STAGING_DB_PASSWORD
)
from app.utils.backup_commands import sync_databases

logger = logging.getLogger('backup_axis')


def get_respaldos_dir():
    root_dir = os.path.abspath(os.path.join(current_app.root_path, '..'))
    dst_dir = os.path.join(root_dir, 'respaldos')
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    return dst_dir


@respaldos_bp.route('/')
@login_required
@roles_accepted('admin')
def index():
    resp_dir = get_respaldos_dir()
    files = []
    last_backup_date = "Sin respaldos"
    
    try:
        for f in os.listdir(resp_dir):
            if f.endswith('.sql'):
                path = os.path.join(resp_dir, f)
                stats = os.stat(path)
                created_at = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                files.append({
                    'name': f,
                    'size': f"{stats.st_size / 1024:.2f} KB",
                    'date': created_at
                })
        
        files.sort(key=lambda x: x['date'], reverse=True)
        
        if files:
            last_backup_date = files[0]['date']
    except Exception as e:
        flash(f"Error al listar archivos: {str(e)}", "error")
        
    return render_template('produccion/respaldos.html', files=files, last_backup_date=last_backup_date)


@respaldos_bp.route('/generar', methods=['POST'])
@login_required
@roles_accepted('admin')
def generar_respaldo():
    resp_dir = get_respaldos_dir()
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"backup_{timestamp}.sql"
    filepath = os.path.join(resp_dir, filename)
    
    try:
        env = os.environ.copy()
        env['MYSQL_PWD'] = BACKUP_DB_PASSWORD
        
        cmd = [
            'mysqldump',
            f'--host={DB_HOST}',
            f'--port={DB_PORT}',
            f'--user={BACKUP_DB_USER}',
            '--single-transaction',
            '--skip-lock-tables',
            DB_NAME
        ]
        
        with open(filepath, 'w') as out_file:
            subprocess.run(cmd, stdout=out_file, env=env, stderr=subprocess.PIPE, check=True)
            
        flash(f'Respaldo {filename} generado correctamente.', 'success')
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else str(e)
        flash(f'Error al generar respaldo: {error_msg}', 'danger')
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        flash(f'Error inesperado: {str(e)}', 'danger')
            
    return redirect(url_for('respaldos.index'))


@respaldos_bp.route('/descargar/<filename>')
@login_required
@roles_accepted('admin')
def descargar_respaldo(filename):
    resp_dir = get_respaldos_dir()
    return send_from_directory(resp_dir, filename, as_attachment=True)


@respaldos_bp.route('/restaurar/<filename>', methods=['POST'])
@login_required
@roles_accepted('admin')
def restaurar_respaldo(filename):
    """
    Restauración Incremental Conservativa:
    1. Carga el archivo .sql en la BD de Staging (auxiliar).
    2. Sincroniza Staging -> Producción (solo INSERT/UPDATE, nunca DELETE).
    
    Esto protege los datos actuales en Producción y solo aplica diferencias.
    """
    resp_dir = get_respaldos_dir()
    filepath = os.path.join(resp_dir, filename)
    
    if not os.path.exists(filepath):
        flash('El archivo de respaldo no existe.', 'danger')
        return redirect(url_for('respaldos.index'))
        
    # ── PASO 1: Cargar el respaldo en Staging ──────────────────────────────
    try:
        flash(f'Iniciando restauración incremental de {filename}...', 'info')
        env = os.environ.copy()
        env['MYSQL_PWD'] = BACKUP_DB_PASSWORD
        
        # Limpiamos y recreamos staging para cargar el respaldo limpio
        recreate_staging_cmds = [
            f"DROP DATABASE IF EXISTS `{STAGING_DB_NAME}`",
            f"CREATE DATABASE `{STAGING_DB_NAME}`"
        ]
        
        for sql_cmd in recreate_staging_cmds:
            subprocess.run(
                ['mysql', f'--host={DB_HOST}', f'--port={DB_PORT}',
                 f'--user={BACKUP_DB_USER}', '--execute', sql_cmd],
                env=env, stderr=subprocess.PIPE, check=True
            )
        
        # Cargamos el archivo SQL en staging
        with open(filepath, 'r', encoding='utf-8', errors='replace') as in_file:
            subprocess.run(
                ['mysql', f'--host={DB_HOST}', f'--port={DB_PORT}',
                 f'--user={BACKUP_DB_USER}', STAGING_DB_NAME],
                stdin=in_file, env=env, stderr=subprocess.PIPE, check=True
            )
        
        logger.info(f"Respaldo {filename} cargado en Staging correctamente.")
        
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode(errors='replace') if e.stderr else str(e)
        flash(f'Error al cargar el respaldo en Staging: {error_msg}', 'danger')
        return redirect(url_for('respaldos.index'))
    except Exception as e:
        flash(f'Error inesperado al cargar en Staging: {str(e)}', 'danger')
        return redirect(url_for('respaldos.index'))
    
    # ── PASO 2: Sincronización Conservativa Staging -> Producción ──────────
    try:
        staging_uri = (
            f"mysql+pymysql://{BACKUP_DB_USER}:{BACKUP_DB_PASSWORD}"
            f"@{STAGING_DB_HOST}:{STAGING_DB_PORT}/{STAGING_DB_NAME}"
        )
        prod_uri = (
            f"mysql+pymysql://{BACKUP_DB_USER}:{BACKUP_DB_PASSWORD}"
            f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        
        staging_engine = create_engine(staging_uri, pool_pre_ping=True)
        prod_engine = create_engine(prod_uri, pool_pre_ping=True)
        
        messages = []
        success, total = sync_databases(
            source_engine=staging_engine,
            target_engine=prod_engine,
            log_fn=lambda msg: messages.append(msg),
            restore_mode=True  # Modo restauración: compara por PK, recupera borrados
        )
        
        if success:
            flash(
                f'Restauración incremental completada. '
                f'{total} registros sincronizados desde {filename}.',
                'success'
            )
            logger.info(f"Restauración desde {filename}: {total} registros. Detalles: {messages}")
        else:
            flash(
                f'Error durante la sincronización incremental. '
                f'Revisa los logs para más detalles.',
                'danger'
            )
            
    except Exception as e:
        flash(f'Error inesperado durante la sincronización: {str(e)}', 'danger')
        logger.error(f"Error en restauración incremental: {e}")
        
    return redirect(url_for('respaldos.index'))

