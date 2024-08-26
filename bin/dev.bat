@echo off

REM Stocke le chemin du répertoire contenant le script batch dans une variable
set "SCRIPT_DIR=%~dp0"
set ENV=dev

REM Change temporairement de répertoire vers le répertoire contenant le script
pushd "%SCRIPT_DIR%"

REM Obtiens le répertoire parent
set "PARENT_DIR=%CD%"

REM Remonte d'un niveau pour obtenir le répertoire parent
cd ..

REM Stocke le chemin du répertoire parent dans une variable
set "PARENT_DIR=%CD%"

python %PARENT_DIR%\src\fam\main.py %*