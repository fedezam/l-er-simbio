@echo off
title Iniciando LER Core - Lenguaje de Entidades Reflexivas
echo.
echo ================================
echo  _ Iniciando sistema LER Core
echo  _ Modo: Reflexivo Simbi_tico
echo ================================
echo.

REM Cambiar al directorio ra_z del proyecto
cd /d %~dp0..

REM Ejecutar entity runner
python core\entity_runner.py

echo.
echo ================================
echo  _ LER finalizado.
echo  Presiona cualquier tecla para salir.
echo ================================
pause >nul
