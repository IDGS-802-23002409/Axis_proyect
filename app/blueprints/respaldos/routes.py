import os
import subprocess
from datetime import datetime
from flask import render_template, current_app, redirect, url_for, flash, send_from_directory, request
from flask_security import roles_accepted, login_required
from . import respaldos_bp
from app.utils.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT

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
        env['MYSQL_PWD'] = DB_PASSWORD
        
        cmd = [
            'mysqldump',
            f'--host={DB_HOST}',
            f'--port={DB_PORT}',
            f'--user={DB_USER}',
            DB_NAME
        ]
        
        with open(filepath, 'w') as out_file:
            result = subprocess.run(cmd, stdout=out_file, env=env, stderr=subprocess.PIPE, check=True)
            
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
    resp_dir = get_respaldos_dir()
    filepath = os.path.join(resp_dir, filename)
    
    if not os.path.exists(filepath):
        flash('El archivo de respaldo no existe.', 'danger')
        return redirect(url_for('respaldos.index'))
        
    try:
        env = os.environ.copy()
        env['MYSQL_PWD'] = DB_PASSWORD
        
        cmd = [
            'mysql',
            f'--host={DB_HOST}',
            f'--port={DB_PORT}',
            f'--user={DB_USER}',
            DB_NAME
        ]
        
        with open(filepath, 'r') as in_file:
            subprocess.run(cmd, stdin=in_file, env=env, stderr=subprocess.PIPE, check=True)
            
        flash(f'Base de datos restaurada correctamente desde {filename}.', 'success')
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else str(e)
        flash(f'Error al restaurar: {error_msg}', 'danger')
    except Exception as e:
        flash(f'Error inesperado: {str(e)}', 'danger')
        
    return redirect(url_for('respaldos.index'))
