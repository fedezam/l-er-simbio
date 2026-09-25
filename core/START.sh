#!/bin/bash

clear
echo "=============================="
echo " _ Iniciando sistema LER Core"
echo " _ Modo: Reflexivo Simbi_tico"
echo "=============================="
echo ""

# Cambiar al directorio ra_z del proyecto
cd "$(dirname "$0")"/..

# Ejecutar el n_cleo simbi_tico
python3 core/entity_runner.py

echo ""
echo "=============================="
echo " _ LER finalizado."
echo " Presiona [Enter] para salir."
echo "=============================="
read
