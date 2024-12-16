@echo off
REM Batch file to install necessary Python libraries

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b
)

REM Install dependencies
pip install --upgrade pip
pip install dash plotly pandas numpy
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    exit /b
)

echo All libraries installed successfully.
