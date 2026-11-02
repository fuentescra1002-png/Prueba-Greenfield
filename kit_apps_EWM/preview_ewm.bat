@echo off
title SAP EWM Logistica y Almacen Z101 - Distribuidora Express S.A.
cls
echo =========================================================================
echo   CENTRO DE CONTROL LOGISTICO EWM (ALMACEN Z101)
echo   Distribuidora Express S.A.
echo =========================================================================
echo [1/2] Iniciando servidor EWM en http://localhost:8086
echo [2/2] Abriendo aplicacion en el navegador...
echo.
start http://localhost:8086/standalone_preview.html
echo.
python "%~dp0ewm_bridge_server.py"
pause
