#!/bin/bash
# Script para ejecutar la aplicación Social Media Content Generator API
# Uso: ./run.sh (Linux/Mac) o run.bat (Windows)

# Activar entorno virtual
echo "Activando entorno virtual..."

# En Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    .\.venv\Scripts\Activate.ps1
else
    # En Linux/Mac
    source .venv/bin/activate
fi

# Ejecutar la aplicación
echo ""
echo "=========================================="
echo "Iniciando Social Media Content Generator API"
echo "=========================================="
echo ""
echo "La API estará disponible en:"
echo "  - URL: http://localhost:8000"
echo "  - Documentación Swagger: http://localhost:8000/docs"
echo "  - Documentación ReDoc: http://localhost:8000/redoc"
echo ""
echo "Presiona Ctrl+C para detener la aplicación"
echo ""

python m3_omar_pinzon.py
