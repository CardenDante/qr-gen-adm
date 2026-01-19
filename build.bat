@echo off
echo ========================================
echo Building QR Code Label Printer...
echo ========================================
echo.

echo Installing PyInstaller...
pip install pyinstaller
echo.

echo Building executable...
pyinstaller --clean build.spec
echo.

echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Executable location: dist\QR_Label_Printer.exe
echo.
pause
