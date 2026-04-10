import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
from tkinterdnd2 import DND_FILES, TkinterDnD

from converter import port_plugin_zip, read_plugin_info
from util import version_str_to_int, detect_installed_mcreator_version, check_plugin_id_collision, clean_version_string

MCREATOR_DIR = Path.home() / ".mcreator" / "plugins"
REQUIRED_FIELDS = ["id", "name", "author", "version"]

class ValidationSeverity:
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, borderwidth=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class App:
    def __init__(self, root):
        self.root = root
        root.title("MCreator Plugin Porter")
        root.geometry("1200x760")
        root.minsize(1200, 760)

        self.plugins = []
        self.updating_fields = False

        self.configure_style()
        self.build_ui()
        self.autodetect_mcreator_version()

    def configure_style(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"))

    def build_ui(self):
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        # === Top main area split into 3 columns ===
        top_frame = ttk.Frame(container)
        top_frame.pack(fill=tk.BOTH, expand=True)

        # --- Left: Plugin selector ---
        left_frame = ttk.LabelFrame(top_frame, text="Plugin ZIPs", padding=8)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10), pady=5)

        self.drop_label = ttk.Label(left_frame, text="Drag ZIP(s) here or Browse", width=30)
        self.drop_label.pack(pady=5)

        ttk.Button(left_frame, text="Browse", command=self.pick_zips).pack(pady=5)

        self.plugin_listbox = tk.Listbox(left_frame, width=40, height=30)
        self.plugin_listbox.pack(pady=5, fill=tk.Y, expand=True)
        self.plugin_listbox.bind("<<ListboxSelect>>", self.on_plugin_select)

        ttk.Button(left_frame, text="Remove Selected", command=self.remove_selected_plugin).pack(pady=5)

        # --- Middle: Override fields (scrollable) ---
        middle_frame = ttk.LabelFrame(top_frame, text="Override plugin.json Fields", padding=8)
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)

        self.scrollable_fields = ScrollableFrame(middle_frame)
        self.scrollable_fields.pack(fill=tk.BOTH, expand=True)

        self.fields = {}
        for field in ["id", "name", "description", "author", "version", "updateJSONURL", "pluginPageID"]:
            row = ttk.Frame(self.scrollable_fields.scrollable_frame)
            row.pack(fill=tk.X, pady=4)
            ttk.Label(row, text=field, width=20).pack(side=tk.LEFT)
            entry = ttk.Entry(row)
            entry.pack(fill=tk.X, expand=True, padx=(0, 15))
            entry.bind("<FocusOut>", self.save_current_overrides)
            self.fields[field] = entry

        # --- Right: Plugin summary + version + validation ---
        right_frame = ttk.LabelFrame(top_frame, text="Plugin Info & Status", padding=8, width=250)
        right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10,0), pady=5)

        self.plugin_info_text = tk.Text(right_frame, height=20, width=30, state="disabled", wrap=tk.WORD)
        self.plugin_info_text.pack(fill=tk.BOTH, expand=False, pady=5)

        ttk.Label(right_frame, text="Target MCreator Version:").pack(pady=(10,0))
        self.version_entry = ttk.Entry(right_frame)
        self.version_entry.pack(fill=tk.X, padx=5, pady=5)

        self.validation_status = ttk.Label(right_frame, text="", foreground="red")
        self.validation_status.pack(pady=10)

        # === Bottom fixed Port button ===
        bottom_frame = ttk.Frame(container)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 8))

        self.port_button = ttk.Button(bottom_frame, text="Port & Install Plugin(s)", command=self.run)
        self.port_button.pack(fill=tk.X)

        # === Console window below bottom frame ===
        console_frame = ttk.LabelFrame(container, text="Console", padding=8)
        console_frame.pack(fill=tk.BOTH, expand=True)

        self.console = tk.Text(console_frame, height=8, state="disabled")
        self.console.pack(fill=tk.BOTH, expand=True)

        # Setup drag and drop
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.on_drop)

    def log(self, msg, severity=ValidationSeverity.INFO):
        prefix = ""
        if severity == ValidationSeverity.ERROR:
            prefix = "[ERROR] "
        elif severity == ValidationSeverity.WARNING:
            prefix = "[WARNING] "
        elif severity == ValidationSeverity.INFO:
            prefix = "[INFO] "
        self.console.configure(state="normal")
        self.console.insert("end", prefix + msg + "\n")
        self.console.see("end")
        self.console.configure(state="disabled")

    def autodetect_mcreator_version(self):
        version = detect_installed_mcreator_version()
        if version:
            self.version_entry.delete(0, tk.END)
            self.version_entry.insert(0, version)
            self.log(f"Detected installed MCreator version: {version}", ValidationSeverity.INFO)
        else:
            self.log("WARNING: Could not detect installed MCreator version", ValidationSeverity.WARNING)

    def load_plugin(self, path):
        info = read_plugin_info(path)
        if info is None:
            self.log(f"Failed to read plugin info from {path}", ValidationSeverity.ERROR)
            return False

        if any(p["path"] == path for p in self.plugins):
            self.log(f"Plugin {path} already loaded", ValidationSeverity.WARNING)
            return False

        self.plugins.append({"path": path, "info": info, "overrides": {}})

        self.plugin_listbox.insert(tk.END, Path(path).name)
        self.drop_label.config(text=f"{len(self.plugins)} plugin(s) loaded")
        self.log(f"Loaded plugin: {Path(path).name}", ValidationSeverity.INFO)
        return True

    def pick_zips(self):
        paths = filedialog.askopenfilenames(filetypes=[("ZIP", "*.zip")])
        for p in paths:
            self.load_plugin(p)

    def on_drop(self, event):
        dropped = event.data.strip("{}").split()
        for path in dropped:
            if path.lower().endswith(".zip"):
                self.load_plugin(path)

    def on_plugin_select(self, event=None):
        selection = self.plugin_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        plugin = self.plugins[index]

        # Update overrides fields
        self.updating_fields = True
        for entry in self.fields.values():
            entry.delete(0, tk.END)

        info = plugin["info"]
        overrides = plugin["overrides"]

        for field, entry in self.fields.items():
            if field in overrides:
                entry.insert(0, overrides[field])
            elif field in info:
                entry.insert(0, info[field])
        self.updating_fields = False

        # Update plugin info text summary
        self.plugin_info_text.configure(state="normal")
        self.plugin_info_text.delete("1.0", tk.END)
        info_lines = [f"{k}: {v}" for k, v in info.items()]
        self.plugin_info_text.insert(tk.END, "\n".join(info_lines))
        self.plugin_info_text.configure(state="disabled")

        self.validation_status.config(text="")

    def save_current_overrides(self, event=None):
        if self.updating_fields:
            return
        selection = self.plugin_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        plugin = self.plugins[index]

        for field, entry in self.fields.items():
            val = entry.get().strip()
            original_val = plugin["info"].get(field, "")
            if val and val != original_val:
                plugin["overrides"][field] = val
            elif field in plugin["overrides"]:
                del plugin["overrides"][field]

    def remove_selected_plugin(self):
        selection = self.plugin_listbox.curselection()
        if not selection:
            return
        index = selection[0]

        removed = self.plugins.pop(index)
        self.plugin_listbox.delete(index)
        self.drop_label.config(text=f"{len(self.plugins)} plugin(s) loaded")

        if not self.plugins:
            for entry in self.fields.values():
                entry.delete(0, tk.END)
            self.plugin_info_text.configure(state="normal")
            self.plugin_info_text.delete("1.0", tk.END)
            self.plugin_info_text.configure(state="disabled")
        else:
            new_index = min(index, len(self.plugins) - 1)
            self.plugin_listbox.selection_set(new_index)
            self.plugin_listbox.event_generate("<<ListboxSelect>>")

        self.log(f"Removed plugin: {Path(removed['path']).name}", ValidationSeverity.INFO)

    def validate(self):
        if not self.plugins:
            self.validation_status.config(text="No plugin ZIP selected")
            return False

        version_raw = self.version_entry.get().strip()
        version_clean = clean_version_string(version_raw)

        if version_str_to_int(version_clean) == 0:
            self.validation_status.config(text="Invalid MCreator version format (expected YYYY.M)")
            return False

        for i, plugin in enumerate(self.plugins):
            info = plugin["info"]
            overrides = plugin["overrides"]
            pid = overrides.get("id", info.get("id", ""))
            if not pid:
                self.validation_status.config(text=f"Plugin {i+1} missing required 'id' field.")
                return False

            if check_plugin_id_collision(MCREATOR_DIR, pid):
                self.log(f"Plugin ID collision detected for '{pid}'. Plugin {i+1}", ValidationSeverity.WARNING)

            for field in REQUIRED_FIELDS:
                val = overrides.get(field, info.get(field, "")).strip()
                if not val:
                    self.validation_status.config(text=f"Plugin {i+1} missing required field '{field}'.")
                    return False

        self.validation_status.config(text="")
        return True

    def run(self):
        if not self.validate():
            self.log("Validation failed. Fix errors before continuing.", ValidationSeverity.ERROR)
            return

        version_raw = self.version_entry.get().strip()
        version = clean_version_string(version_raw)

        MCREATOR_DIR.mkdir(parents=True, exist_ok=True)

        def task():
            for idx, plugin in enumerate(self.plugins):
                path = plugin["path"]
                plugin_name = Path(path).stem
                output_path = MCREATOR_DIR / f"{plugin_name}-ported-{version}.zip"
                overrides = plugin["overrides"]

                try:
                    self.log(f"Porting plugin {idx+1}/{len(self.plugins)}: {plugin_name}", ValidationSeverity.INFO)
                    port_plugin_zip(path, version, output_path, overrides, self.log)
                    self.log(f"Installed to: {output_path}", ValidationSeverity.INFO)
                except Exception as e:
                    self.log(f"Error porting plugin {plugin_name}: {e}", ValidationSeverity.ERROR)

        threading.Thread(target=task, daemon=True).start()

def main():
    root = TkinterDnD.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
