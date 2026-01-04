@echo off
echo ==========================================
echo Building PolliPaper
echo ==========================================
echo.

REM Check if python is in PATH
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found in PATH, checking common locations...
    if exist "C:\Users\Aaron\AppData\Local\Programs\Python\Python312\python.exe" (
        set "PYTHON_EXE=C:\Users\Aaron\AppData\Local\Programs\Python\Python312\python.exe"
    ) else if exist "C:\Users\Aaron\AppData\Local\Programs\Python\Python314\python.exe" (
        set "PYTHON_EXE=C:\Users\Aaron\AppData\Local\Programs\Python\Python314\python.exe"
    ) else (
        echo ERROR: Python not found! Please install Python or add it to PATH.
        pause
        exit /b 1
    )
) else (
    set "PYTHON_EXE=python"
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    "%PYTHON_EXE%" -m venv venv
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
