@echo off
echo Initializing D-Drive Sandbox for DAIN Development...

:: 1. Define a central cache folder inside your D: drive project
set CACHE_DIR=D:\dain_demo\.local_cache

:: 2. Create the necessary cache directories silently
mkdir "%CACHE_DIR%\temp" 2>nul
mkdir "%CACHE_DIR%\appdata" 2>nul
mkdir "%CACHE_DIR%\localappdata" 2>nul
mkdir "%CACHE_DIR%\pip" 2>nul
mkdir "%CACHE_DIR%\npm" 2>nul
mkdir "%CACHE_DIR%\xdg" 2>nul

:: 3. Override Windows Global Temp Variables
set TMP=%CACHE_DIR%\temp
set TEMP=%CACHE_DIR%\temp

:: 4. Override Application Data Variables (Stops IDEs/Agents from saving to C:)
set APPDATA=%CACHE_DIR%\appdata
set LOCALAPPDATA=%CACHE_DIR%\localappdata

:: 5. Override Package Manager and AI Tool Cache Variables
set PIP_CACHE_DIR=%CACHE_DIR%\pip
set NPM_CONFIG_CACHE=%CACHE_DIR%\npm
set XDG_CACHE_HOME=%CACHE_DIR%\xdg
set HF_HOME=%CACHE_DIR%\huggingface

:: 6. Launch your tools within this sandboxed environment
:: (Replace these paths with your actual D: drive installation paths)
start "" "D:\Path\To\Your\IDE.exe"
start "" "D:\Path\To\Puku\puku.exe"
start "" "D:\Path\To\Antigravity\antigravity-agent.exe"

echo Sandbox initialized. You can close this window.
exit