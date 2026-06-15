@echo off
setlocal
REM 整个 docsify 站点都在 docs\docsify\ ；内容在 docs\* 。用静态服务器从 docs\ 根起服务，访问 /docsify/。
REM 不要用 `docsify serve`：它要求服务根有 index.html，而我们的 index.html 在子目录。

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..\..") do set "DOCS_ROOT=%%~fI"
set "PORT=3000"

cd /d "%DOCS_ROOT%"
echo Serving: %DOCS_ROOT%
echo -^> Open http://localhost:%PORT%/docsify/

where python >nul 2>&1
if %errorlevel%==0 (
    python -m http.server %PORT%
    goto :END
)
where npx >nul 2>&1
if %errorlevel%==0 (
    npx --yes http-server . -p %PORT% -c-1
    goto :END
)
echo Need python or Node(npx) to start a static server.
pause

:END
endlocal
