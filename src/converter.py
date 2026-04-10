import zipfile
import os
import tempfile
import shutil
import json
import re

from util import version_str_to_int


def strip_angle(value):
    if value is None:
        return None
    match = re.search(r"<([^>]*)>", str(value))
    return match.group(1) if match else value


def find_plugin_json(root):
    for r, _, files in os.walk(root):
        if "plugin.json" in files:
            return os.path.join(r, "plugin.json")
    return None


def read_plugin_info(zip_path):
    temp = tempfile.mkdtemp(prefix="mcreator_read_")
    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(temp)

        pj = find_plugin_json(temp)
        if not pj:
            return {}

        with open(pj, "r", encoding="utf-8") as f:
            data = json.load(f)

        info = {}
        for k, v in data.get("info", {}).items():
            info[k] = strip_angle(v)

        info["id"] = strip_angle(data.get("id"))
        return info
    finally:
        shutil.rmtree(temp)


def port_plugin_zip(zip_path, target_version, output_path, overrides, log):
    temp = tempfile.mkdtemp(prefix="mcreator_port_")

    try:
        log("Extracting plugin...")
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(temp)

        pj = find_plugin_json(temp)
        if not pj:
            raise RuntimeError("plugin.json not found")

        with open(pj, "r", encoding="utf-8") as f:
            original = json.load(f)

        info = {}
        for k, v in original.get("info", {}).items():
            info[k] = strip_angle(v)

        for k, v in overrides.items():
            info[k] = v

        plugin_id = overrides.get("id") or strip_angle(original.get("id")) or "plugin"
        plugin_id = f"{plugin_id}_ported"

        new_plugin = {
            "id": plugin_id,
            "supportedversions": [version_str_to_int(target_version)],
            "info": info
        }

        with open(pj, "w", encoding="utf-8") as f:
            json.dump(new_plugin, f, indent=2)

        log("Writing ZIP...")
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as out:
            for r, _, files in os.walk(temp):
                for file in files:
                    full = os.path.join(r, file)
                    out.write(full, os.path.relpath(full, temp))

        log("Port completed.")
    finally:
        shutil.rmtree(temp)
