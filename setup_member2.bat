@echo off
REM Setup script for Member 2 directory structure

cd /d "C:\Users\pradheepa jaya shree\Desktop\neww\Time-Table-Scheduler"

echo Creating directory structure...
echo.

mkdir utils 2>nul
echo Created: utils\
type nul > utils\__init__.py
echo Created: utils\__init__.py
echo.

mkdir data 2>nul
echo Created: data\
type nul > data\__init__.py
echo Created: data\__init__.py
echo.

mkdir agent 2>nul
echo Created: agent\
type nul > agent\__init__.py
echo Created: agent\__init__.py
echo.

mkdir tests 2>nul
echo Created: tests\
type nul > tests\__init__.py
echo Created: tests\__init__.py
echo.

echo Directory structure setup complete!
echo.
dir /b /ad
pause
