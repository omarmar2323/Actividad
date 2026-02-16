@echo off
REM Script para ejecutar la aplicación Social Media Content Generator API
REM Uso: run.bat (Windows)

REM Activar entorno virtual
echo Activando entorno virtual...
call .\.venv\Scripts\activate.bat

REM Ejecutar la aplicación
echo.
echo ==========================================
echo Iniciando Social Media Content Generator API
echo ==========================================
echo.
echo La API estara disponible en:
echo   - URL: http://localhost:8000
echo   - Documentacion Swagger: http://localhost:8000/docs
echo   - Documentacion ReDoc: http://localhost:8000/redoc
echo.
echo Presiona Ctrl+C para detener la aplicacion
echo.

python m3_omar_pinzon.py
pause
