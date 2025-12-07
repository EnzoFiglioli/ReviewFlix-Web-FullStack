#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Agrega estas líneas para debug
echo "=== Listando archivos del proyecto ==="
ls -la
echo "=== Verificando si existe ReviewFlix ==="
ls -la ReviewFlix/ || echo "No se encuentra ReviewFlix"
echo "=== Contenido de PYTHONPATH ==="
echo $PYTHONPATH
echo "=== Agregando directorio actual a PYTHONPATH ==="
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
