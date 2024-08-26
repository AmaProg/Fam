@REM @echo off
@REM REM Configuration

@REM set SCRIPT_NAME=src\fam\main.py
@REM set STATIC_DIR=src\fam\static
@REM set DOWNLOAD_DIR=downloads\windows
@REM set EXEC_NAME=fam
@REM set NOFOLLOW_IMPORT=--nofollow-import-to=*tests* --nofollow-import-to=*testing* --nofollow-import-to=*test* --nofollow-import-to=*conftest*
@REM set NUITKA_OPTIONS= --standalone --include-package=passlib --enable-plugin=numpy --include-data-files=alembic_app.ini=alembic_app.ini --include-data-files=alembic_users.ini=alembic_users.ini %NOFOLLOW_IMPORT% --include-data-dir=%STATIC_DIR%="static" --output-filename=%EXEC_NAME%

@REM cd 

@REM nuitka %NUITKA_OPTIONS% %SCRIPT_NAME%

@REM pause

@echo off
REM Configuration

set SCRIPT_NAME=src\fam\main.py
set STATIC_DIR=src\fam\static
set DOWNLOAD_DIR=downloads\windows
set EXEC_NAME=fam
set NOFOLLOW_IMPORT=--nofollow-import-to=*tests* --nofollow-import-to=*testing* --nofollow-import-to=*test* --nofollow-import-to=*conftest*
set NUITKA_OPTIONS= --standalone --include-package=passlib %NOFOLLOW_IMPORT% --include-data-files=alembic_app.ini=alembic_app.ini --include-data-files=alembic_users.ini=alembic_users.ini --include-data-dir=%STATIC_DIR%="static" --output-filename=%EXEC_NAME%

REM Change to the directory containing your script
cd /d "K:\Projects\Fam"

REM Activate virtual environment if needed
REM call path\to\venv\Scripts\activate

call .venv\Scripts\activate

nuitka %NUITKA_OPTIONS% %SCRIPT_NAME%

pause
