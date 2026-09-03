@echo off
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel%==0 (
  python metodos_numericos_app.py
  goto :eof
)

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 metodos_numericos_app.py
  goto :eof
)

echo No se encontro Python instalado o disponible en PATH.
echo Instala Python y vuelve a ejecutar este archivo.
pause
