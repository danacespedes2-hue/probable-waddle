#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate upload/index.html listing all files in this directory (except this script and index.html).
Run: python3 upload/generate_index.py
"""

import os
from datetime import datetime

HERE = os.path.dirname(__file__)
OUTPUT = os.path.join(HERE, 'index.html')
EXCLUDE = {'index.html', os.path.basename(__file__)}


def human_size(n):
    n = float(n)
    for unit in ['B','KB','MB','GB','TB']:
        if n < 1024.0:
            if unit == 'B':
                return f"{int(n)}{unit}"
            return f"{n:.1f}{unit}"
        n /= 1024.0
    return f"{n:.1f}PB"


files = []
for name in os.listdir(HERE):
    path = os.path.join(HERE, name)
    if not os.path.isfile(path):
        continue
    if name in EXCLUDE:
        continue
    stat = os.stat(path)
    files.append({
        'name': name,
        'size': human_size(stat.st_size),
        'mtime': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    })

files.sort(key=lambda x: x['name'].lower())

rows = []
for f in files:
    rows.append(f"""      <tr>
        <td>{f['name']}</td>
        <td>{f['size']}</td>
        <td>{f['mtime']}</td>
        <td><a class=\"button\" href=\"./{f['name']}\" target=\"_blank\" rel=\"noopener noreferrer\">Abrir</a></td>
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
  <p>Generado por <code>generate_index.py</code> — actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

  <table>
    <thead>
      <tr><th>Nombre</th><th>Tamaño</th><th>Modificado</th><th>Acción</th></tr>
    </thead>
    <tbody>
{rows_html}
    </tbody>
  </table>

  <p class="note">Para regenerar esta página ejecuta: <code>python3 upload/generate_index.py</code></p>
</body>
</html>"""

with open(OUTPUT, 'w', encoding='utf-8') as fh:
    fh.write(html)

print(f'Wrote {OUTPUT} with {len(files)} file(s).')
