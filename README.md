# MCreator Plugin Porter

**MCreator Plugin Porter** is a utility designed to help migrate MCreator plugins between different MCreator versions by updating the `plugin.json` file inside plugin packages.

⚠️ **Important:** This tool does **not** modify plugin code. It only updates metadata. Because of this limitation, compatibility is **not guaranteed**.

---

## To Run

1. Unzip the .zip file and enter the folder
2. Run the .bat files
3. Open the "dist" folder, and the .exe should be there

---

## What This Tool Does

MCreator Plugin Porter:

* Opens an existing MCreator plugin package
* Updates the `plugin.json` file to match a selected MCreator version
* Repackages the plugin for use with another version of MCreator

This can save time when testing plugins across versions that have compatible APIs.

---

## What This Tool Does NOT Do

This tool **does not modify plugin code**.

That means:

* If the plugin uses features that changed or were removed, it may fail.
* If APIs are incompatible, the plugin may not load.
* Some plugins will still require manual fixes.

**Bottom line:**
If the underlying plugin code is incompatible with the target version, this tool will not make it work.

---

## Compatibility Warning

Because only the `plugin.json` file is modified:

* Some plugins will work after porting
* Some plugins will partially work
* Some plugins will fail entirely

This tool is best used for:

* Minor version changes
* Testing compatibility
* Speeding up manual porting workflows

It is **not a guaranteed automatic porting solution**.

---

## Legal and Licensing Notice

Using this tool does **not** give permission to redistribute plugins.

You **must still follow the original plugin's license**.

Do **not**:

* Re-upload plugins created by other developers
* Redistribute modified plugins
* Publish ports of other people's plugins

**Unless you have permission from the original author** or the license explicitly allows it.

Failure to respect licensing terms can result in:

* Repository takedowns
* Copyright violations
* Loss of community trust

Use this tool responsibly.

---

## License

This project is licensed under the **GNU Lesser General Public License v3.0 (LGPLv3)**.

Under LGPLv3:

* You may use this tool freely
* You may modify the source code
* You may redistribute modified versions
* You must include the original license
* Changes to this project must remain open under LGPLv3

See the `LICENSE` file for full details.

---

## Disclaimer

This project is **not affiliated with or endorsed by MCreator or its developers**.

All trademarks and product names belong to their respective owners.

---

## Usage Overview

1. Select an existing plugin package
2. Choose the target MCreator version
3. Run the porter
4. Test the plugin inside MCreator

Always test thoroughly after porting.

---

## Known Limitations

* Does not update Java code
* Does not fix API incompatibilities
* Does not verify plugin functionality
* Cannot guarantee cross-version compatibility

Manual adjustments may still be required.

---

## Intended Use

This tool is intended for:

* Developers maintaining their own plugins
* Testing plugin compatibility
* Learning and experimentation
* Internal plugin migration

It is **not intended for bypassing licensing restrictions**.

---

## Contributions

Contributions are welcome. Improvements that increase reliability, compatibility detection, or usability are encouraged.

Before contributing:

* Ensure your code follows the project's license requirements
* Clearly document changes
* Test modifications where possible

---

## Support

If you encounter problems:

* Verify the plugin version compatibility
* Check the `plugin.json` changes
* Review logs and error messages

Remember: many failures are caused by incompatible plugin code, not the porter itself.
