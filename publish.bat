@echo off
REM Configuration

set SCRIPT_NAME=src\fam\main.py
set STATIC_DIR=src\fam\static
set DOWNLOAD_DIR=downloads\windows
set EXEC_NAME=Fam
set NOFOLLOW_IMPORT=--nofollow-import-to=*tests* --nofollow-import-to=*testing*
set NUITKA_OPTIONS= --standalone --include-package=passlib --include-package=alembic --include-data-files=alembic_app.ini=alembic_app.ini --include-data-files=alembic_users.ini=alembic_users.ini %NOFOLLOW_IMPORT% --include-data-dir=%STATIC_DIR%="static" --output-filename=%EXEC_NAME%

cd 

nuitka %NUITKA_OPTIONS% %SCRIPT_NAME%

pause
