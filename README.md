<<<<<<< HEAD
MCreator Plugin Porter - Full Repository (Installer-ready)
=========================================================

What this package contains
- A complete Python project that accepts drag & drop .zip MCreator plugins,
  edits plugin.json according to rules, and writes ported zips.
- Build scripts for creating a Windows executable using PyInstaller.
- An installer batch file (`installer.bat`) that performs a one-click install:
  it creates a virtual environment, installs requirements, and places a
  desktop shortcut to run the app. (Requires Windows + Python 3.11+.)
- An optional NSIS script and PowerShell build helpers.

How to "just click to install"
1. On Windows, extract this repository and double-click `installer.bat`.
   The installer will:
     - Check for Python 3.11+. If not found, it will prompt you to install Python.
     - Create a venv in `%LOCALAPPDATA%\mcreator_porter_venv`.
     - Install required Python packages.
     - Create a desktop shortcut that runs the GUI application.
2. After installation, use the desktop shortcut to run the app.

Notes & limitations
- This package does NOT include a pre-built signed .exe installer. Building a
  single-file native installer (PyInstaller + optional NSIS) requires tools
  and elevated permissions that cannot be produced inside this environment.
- The `installer.bat` performs a one-click installation (no admin required).
- If you want a single .exe installer, run the included `scripts/build_exe.ps1`
  on a Windows machine with Python and PyInstaller installed.

Files of interest
- src/main.py           -> GUI + drag/drop entrypoint
- src/converter.py      -> Core conversion logic
- src/fetch_versions.py -> Fetches MCreator release tags from GitHub
- src/util.py           -> Utilities
- installer.bat         -> One-click installer (Windows)
- scripts/build_exe.ps1 -> PowerShell script to build a single-file .exe
- scripts/nsis_installer.nsi -> Example NSIS installer script

=======
# MCreator-Plugin-Porter
This program ports MCreator Plugins to different versions of MCreator
>>>>>>> e5eb79825ec6a2878fbdc2b6741f9bba41198660
