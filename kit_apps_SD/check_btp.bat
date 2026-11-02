@echo off
chcp 65001 >nul
echo =======================================================
echo   CONSULTANDO ESTADO DE SAP BTP Y DESTINOS CONECTIVIDAD
echo =======================================================
echo 1. Verificando Sesion BTP... > btp_status.txt
btp.exe target >> btp_status.txt 2>&1

echo. >> btp_status.txt
echo 2. Listando Subcuentas... >> btp_status.txt
btp.exe list accounts/subaccount >> btp_status.txt 2>&1

type btp_status.txt
echo =======================================================
echo   Resultado guardado en btp_status.txt
echo =======================================================
pause
