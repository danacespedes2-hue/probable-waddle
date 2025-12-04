#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Flask server to list and serve files from the upload/ directory.
Run: pip install -r requirements.txt && python3 server.py
"""

from flask import Flask, send_from_directory
from markupsafe import escape
import os
import datetime

app = Flask(__name__)
HERE = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(HERE, 'upload')
EXCLUDE = {'index.html', 'generate_index.py'}

def human_size(n):
    n = float(n)
    for unit in ['B','KB','MB','GB','TB']:
        if n < 1024.0:
            if unit == 'B':
                return f"{int(n)}{unit}"
            return f"{n:.1f}{unit}"
        n /= 1024.0
    return f"{n:.1f}PB"

@app.route('/')
def index():
    try:
        names = sorted(os.listdir(UPLOAD_DIR), key=str.lower)
    except Exception as e:
        return f"Error leyendo carpeta upload: {e}", 500

    rows = []
    for name in names:
        path = os.path.join(UPLOAD_DIR, name)
        if not os.path.isfile(path) or name in EXCLUDE:
            continue
        st = os.stat(path)
        mtime = datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        size = human_size(st.st_size)
        rows.append(f"""      <tr>
        <td>{escape(name)}</td>
        <td>{size}</td>
        <td>{mtime}</td>
        <td><a class=\"button\" href=\"/files/{escape(name)}\" target=\"_blank\">Abrir</a></td>
      </tr>""")

    rows_html = "\n".join(rows) if rows else "      <tr><td colspan=\"4\">No hay archivos en esta carpeta.</td></tr>"

    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Archivos subidos</title>
  <style>
    body{{font-family:system-ui,Arial,sans-serif;margin:24px;color:#222}}
    table{{border-collapse:collapse;width:100%;max-width:900px}}
    th,td{{border:1px solid #e1e1e1;padding:8px;text-align:left}}
    a.button{{background:#007bff;color:#fff;padding:6px 10px;text-decoration:none;border-radius:4px}}
    a.button:hover{{background:#0056c8}}
    .note{{color:#555;margin-top:12px}}
  </style>
</head>
<body>
  <h1>Archivos subidos</h1>
  <p>Servido por <code>server.py</code> — actualizado: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

  <table>
    <thead>
      <tr><th>Nombre</th><th>Tamaño</th><th>Modificado</th><th>Acción</th></tr>
    </thead>
    <tbody>
{rows_html}
    </tbody>
  </table>

  <p class=\"note\">Los archivos se sirven desde la carpeta <code>upload/</code>. Para regenerar manualmente index.html (si lo deseas), ejecuta <code>python3 upload/generate_index.py</code>.</p>
</body>
</html>"""

    return html

@app.route('/files/<path:filename>')
def files(filename):
    # Prevent directory traversal
    safe_name = os.path.normpath(filename)
    if safe_name.startswith('..'):
        return "Nombre de archivo inválido", 400
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=False)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)