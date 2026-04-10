\
        #!/usr/bin/env bash
        set -e
        python -m pip install --user --upgrade pip
        python -m pip install --user pyinstaller
        pyinstaller --onefile --icon=src/assets/icon.ico -n mcreator_porter src/main.py
        echo "Built dist/mcreator_porter"
