@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "DOCS_ROOT=%%~fI"

node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js was not detected.
    echo Please install Node.js ^(>=14^) and rerun this script.
    goto :END
) else (
    docsify --version >nul 2>&1
    if errorlevel 1 (
        echo Installing docsify-cli...
        npm install -g docsify-cli
    )

    echo Launching Docsify server...
    pushd "%DOCS_ROOT%"
    docsify serve . --port 3000
    popd
)

pause

:END
endlocal
