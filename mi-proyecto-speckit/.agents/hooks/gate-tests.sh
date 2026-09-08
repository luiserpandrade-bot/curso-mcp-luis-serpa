#!/bin/bash
# agy ejecuta este script con cwd = .agents/ (la carpeta que contiene hooks.json),
# no la raiz del proyecto - por eso subimos un nivel antes de correr pytest.
# Se invoca el Python del entorno virtual directamente: el bash de Git para Windows
# no tiene 'uv' en su PATH.
cd ..
if [ -x ".venv/Scripts/python.exe" ]; then
  PY=".venv/Scripts/python.exe"
else
  PY=".venv/bin/python"
fi
if "$PY" -m pytest --tb=no -q > .gate-tests.log 2>&1; then
  echo '{}'
else
  echo '{"decision":"continue","reason":"Hay tests fallando. No te detengas -- corrige el codigo antes de terminar."}'
fi