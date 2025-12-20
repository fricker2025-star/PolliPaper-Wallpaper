@echo off
echo ==========================================
echo Building PolliPaper
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Build with PyInstaller
echo.
echo Building executable...
pyinstaller build.spec --clean --noconfirm

REM Check if build was successful
if exist "dist\PolliPaper.exe" (
    echo.
    echo ==========================================
    echo Build completed successfully!
    echo Executable: dist\PolliPaper.exe
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo Build failed! Check the output above.
    echo ==========================================
)

echo.
pause
