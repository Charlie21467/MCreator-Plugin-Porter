\
        @echo off
        REM One-click installer for Windows (requires Python 3.11+)
        setlocal

        REM detect python
        where python >nul 2>&1
        if errorlevel 1 (
          echo Python not found on PATH. Please install Python 3.11+ from https://www.python.org/downloads/ and check "Add to PATH".
          pause
          exit /b 1
        )

        python -c "import sys
if sys.version_info < (3,11):
    print('Python 3.11+ is required. Found', sys.version.split()[0])
    raise SystemExit(2)
print('Python OK')"

        if errorlevel 2 (
          echo Python 3.11+ required.
          pause
          exit /b 2
        )

        REM create venv
        set VENV_DIR=%LOCALAPPDATA%\mcreator_porter_venv
        if not exist "%VENV_DIR%" (
          echo Creating virtual environment in %VENV_DIR% ...
          python -m venv "%VENV_DIR%"
        ) else (
          echo Virtual environment already exists at %VENV_DIR%
        )

        echo Activating venv and installing requirements...
        call "%VENV_DIR%\Scripts\activate.bat"
        python -m pip install --upgrade pip
        python -m pip install -r requirements.txt

        REM create a simple launcher script on Desktop
        set LAUNCHER_DIR=%USERPROFILE%\AppData\Local\MCreatorPluginPorter
        if not exist "%LAUNCHER_DIR%" mkdir "%LAUNCHER_DIR%"

        REM copy src to launcher dir
        xcopy /E /I /Y src "%LAUNCHER_DIR%\\src" >nul

        REM create run_porter.bat to launch the app using the venv
        > "%LAUNCHER_DIR%\\run_porter.bat" echo @echo off
        >> "%LAUNCHER_DIR%\\run_porter.bat" echo call "%VENV_DIR%\\Scripts\\activate.bat"
        >> "%LAUNCHER_DIR%\\run_porter.bat" echo python "%LAUNCHER_DIR%\\src\\main.py"

        REM create Desktop shortcut using PowerShell
        powershell -NoProfile -Command ^
          "$W = New-Object -ComObject WScript.Shell; ^
           $Shortcut = $W.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\\\\MCreator Plugin Porter.lnk'); ^
           $Shortcut.TargetPath = '%SYSTEMROOT%\\\\System32\\\\cmd.exe'; ^
           $Shortcut.Arguments = '/c start \"\" \"%LOCALAPPDATA%\\\\MCreatorPluginPorter\\\\run_porter.bat\"'; ^
           $Shortcut.WorkingDirectory = '%LOCALAPPDATA%\\\\MCreatorPluginPorter'; ^
           $Shortcut.Save()"

        echo Installation complete. Use the shortcut on your Desktop to run the app.
        pause
