@echo off
title Subir Proyecto Greenfield a GitHub
cls
echo =========================================================================
echo   SINCRONIZANDO PROYECTO GREENFIELD CON GITHUB
echo   Repositorio: https://github.com/fuentescra1002-png/Prueba-Greenfield
echo =========================================================================
echo.

set "GIT_EXE=C:\Users\Javier\AppData\Local\Programs\MinGit\cmd\git.exe"

echo [1/3] Verificando archivos modificados...
"%GIT_EXE%" add .

echo [2/3] Confirmando cambios locales...
"%GIT_EXE%" commit -m "Actualizacion de respaldo: Greenfield Distribuidora Express S.A."

echo [3/3] Subiendo cambios a GitHub (rama main)...
echo.
"%GIT_EXE%" push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo =========================================================================
    echo   EXITO! Todos los archivos estan respaldados en GitHub correctamente.
    echo =========================================================================
) else (
    echo =========================================================================
    echo   AVISO: Si te solicita usuario y contrasena, recuerda que GitHub requiere
    echo   un "Personal Access Token" (PAT) en lugar de tu contrasena normal.
    echo =========================================================================
)
echo.
pause
