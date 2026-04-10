\
        # PowerShell helper to build a single-file exe using PyInstaller
        # Usage: Open PowerShell, cd to repo root, then run:
        #   .\\scripts\\build_exe.ps1
        param(
            [string]$Entry = "src\\main.py",
            [string]$Icon = "src\\assets\\icon.ico",
            [string]$Name = "mcreator_porter.exe"
        )

        Write-Host "Installing build tools..."
        python -m pip install --upgrade pip
        python -m pip install pyinstaller

        Write-Host "Building single-file executable..."
        pyinstaller --onefile --icon=$Icon -n mcreator_porter $Entry

        Write-Host "Done. Check the dist\\ directory for the executable."
