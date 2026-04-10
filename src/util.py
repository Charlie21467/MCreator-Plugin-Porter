from pathlib import Path
import json
import re

def version_str_to_int(version):
    try:
        # Accept formats like "2025.3" or "2025.3.45720"
        base = version.strip().split(".")
        if len(base) < 2:
            return 0
        year = int(base[0])
        minor = int(base[1])
        return year * 1000 + minor
    except Exception:
        return 0

def version_int_to_str(value):
    try:
        year = value // 1000
        minor = value % 1000
        return f"{year}.{minor}"
    except Exception:
        return ""

def clean_version_string(version):
    # Convert something like 2025.3.45720 to 2025.3
    parts = version.strip().split(".")
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return version.strip()

def _read_version_from_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key in ("mcreatorVersion", "version", "appVersion"):
            if key in data:
                return str(data[key])
    except Exception:
        pass
    return None

def detect_installed_mcreator_version():
    base = Path.home() / ".mcreator"
    if not base.exists():
        return None

    # Try known config files
    for file in ("settings.json", "mcreator.json", "workspaces.json"):
        path = base / file
        if path.exists():
            v = _read_version_from_json(path)
            if v:
                return clean_version_string(v)

    # Try plain text version files
    for file in ("version.txt", "mcreator.version"):
        path = base / file
        if path.exists():
            try:
                return clean_version_string(path.read_text(encoding="utf-8").strip())
            except Exception:
                pass

    return None

def check_plugin_id_collision(target_folder: Path, plugin_id: str):
    # Check if a plugin with the same ID exists in the plugins folder
    if not target_folder.exists():
        return False

    for f in target_folder.glob("*.zip"):
        try:
            from zipfile import ZipFile
            with ZipFile(f, 'r') as zipf:
                if "plugin.json" in zipf.namelist():
                    data = json.loads(zipf.read("plugin.json").decode("utf-8"))
                    existing_id = data.get("id", "")
                    if existing_id == plugin_id:
                        return True
        except Exception:
            continue
    return False
