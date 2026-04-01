@echo off
REM Create directories
mkdir utils
mkdir data
mkdir agent
mkdir tests

REM Create __init__.py files
type nul > utils\__init__.py
type nul > data\__init__.py
type nul > agent\__init__.py
type nul > tests\__init__.py

REM Display structure
echo.
echo ===== Directory Structure Created =====
echo.
dir /B /AD
echo.
for /d %%D in (utils data agent tests) do (
    echo %%D:
    dir %%D /B
    echo.
)
