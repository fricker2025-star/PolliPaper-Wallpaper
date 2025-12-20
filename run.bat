@echo off
echo ==========================================
echo Starting PolliPaper (Development Mode)
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies if needed
echo Checking dependencies...
pip install -r requirements.txt --quiet
echo.

REM Generate icon if it doesn't exist
if not exist "icon.ico" (
    echo Generating application icon...
    python create_icon.py
    echo.
)

REM Run the application
echo Starting application...
echo.
python main.py

echo.
pause
