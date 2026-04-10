@echo off
echo Starting the build process with PyInstaller...

:: Run the PyInstaller command
pyinstaller --onefile --windowed -n mcreator_porter src\main.py

:: Check if the build was successful
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Build successful! Your executable is in the "dist" folder.
) else (
    echo.
    echo Something went wrong during the build. Check the errors above.
)

pause