#!/usr/bin/env bash
set -e

echo "=== Iniciando build del backend y frontend ==="

# Instalar dependencias de Python
python -m pip install --upgrade pip
pip install -r requirements.txt

# Instalar dependencias del frontend
npm install --prefix frontend
npm run build --prefix frontend

# Copiar el build del frontend al backend
rm -rf app/static && mkdir -p app/static
cp -r frontend/dist/* app/static/

echo "=== Build completo ==="
ls -la app/static