@echo off
title SAP S/4HANA OData Bridge - Distribuidora Express S.A.
cls
echo =========================================================================
echo   CENTRO DE MANDO Y PUENTE ODATA SAP S/4HANA (MANDANTE 100)
echo   Distribuidora Express S.A.
echo =========================================================================
echo [1/2] Verificando conexion con servidor SAP S/4HANA...
echo [2/2] Iniciando servidor puente en http://localhost:8085
echo.
echo Presione cualquier tecla si desea abrir la aplicacion en el navegador...
start http://localhost:8085/standalone_preview.html?v=16
echo.
python "%~dp0sap_bridge_server.py"
pause
