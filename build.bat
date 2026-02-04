@echo off
echo ========================================
echo QR Label Printer - Build Script
echo ========================================
echo.

echo Step 1: Creating QR icon...
python build_exe.py
if errorlevel 1 (
    echo Error creating icon!
    pause
    exit /b 1
)
echo.

echo Step 2: Building executable with PyInstaller...
python -m PyInstaller --onefile --windowed --icon=qr_icon.ico --name=QRLabelPrinter --hidden-import=tkinter --collect-all customtkinter main.py
if errorlevel 1 (
    echo Error building executable!
    pause
    exit /b 1
)
echo.

echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo Your executable is located at:
echo dist\QRLabelPrinter.exe
echo.
pause
