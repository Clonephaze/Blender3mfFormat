Blender 3MF Format
====
This is a Blender add-on that allows importing and exporting 3MF files.

3D Manufacturing Format files (.3mf) are a file format for triangular meshes intended to serve as exchange format for 3D printing applications. They can communicate not only the model, but also the intent and material of a 3D printing job from the CAD software to the CAM software (slicer). In this scenario, Blender serves as the CAD software. To that end, the aim of this add-on is to make Blender a more viable alternative as CAD software for additive manufacturing.

## ✅ Modernization Complete (2025)

**This fork has been successfully modernized for Blender 4.2+ and is production-ready!**

The original repository by Ghostkeeper has been inactive since 2023. The addon no longer functions in modern Blender versions (4.2+) due to API changes. This fork contains complete modernization work with full test coverage.

**Version Guide:**
- **Blender 4.2+**: Use this modernized fork ✅ **Ready for production!**
- **Blender 2.8-3.6**: Use the [original repository](https://github.com/Ghostkeeper/Blender3mfFormat/releases/latest)

**What's Been Modernized:**
- ✅ All Blender 4.2+ API compatibility verified
- ✅ Material system (PrincipledBSDFWrapper) working
- ✅ Import/Export/Round-trip fully functional
- ✅ 142 unit tests + 16 integration tests (all passing)
- ✅ Cross-platform test runners (Windows/macOS/Linux)
- ✅ CI/CD with GitHub Actions

**Credits:**
- **Original Author**: Ghostkeeper (2020-2022)
- **Modernization**: Jack (2025)

**Note to Original Author**: Should Ghostkeeper return to active development, all modernization work will be contributed back to the original repository. This fork exists solely to keep the addon functional for the community while maintaining the original vision and GPL v2+ license.

### Current Modernization Status ✅
- [x] ✅ Fixed reload logic and imports
- [x] ✅ Updated for Blender 4.2+ API
- [x] ✅ Fixed material/shader system compatibility
- [x] ✅ Updated property annotation syntax
- [x] ✅ Added integration tests for Blender 4.2+
- [x] ✅ Verified round-trip import/export functionality
- [x] ✅ 142 unit tests + 16 integration tests all passing

**Status: Production Ready!** All core functionality working in Blender 4.2+

Installation
----
### For Blender 4.2+ (This Modernized Version)

**Option 1: Drag and Drop Installation (Easiest)**
1. Download the repository as a ZIP:
   - Click the green "Code" button → "Download ZIP"
   - Or download from the [releases page](../../releases) (when available)
2. Open Blender 4.2+
3. Drag the `io_mesh_3mf` folder directly into the Blender window
4. Blender will prompt to install - click "OK"
5. The addon will appear in Preferences → Add-ons
6. Enable it by checking the checkbox next to "Import-Export: 3MF format"

**Option 2: Manual Installation via Preferences**
1. Download the repository as a ZIP
2. Extract it to get the `io_mesh_3mf` folder
3. Open Blender → Edit → Preferences → Add-ons
4. Click "Install..." button at the top right
5. Navigate to the `io_mesh_3mf` folder and select it
6. Click "Install Add-on"
7. Search for "3MF" in the add-ons list
8. Enable it by checking the checkbox

**Option 3: Developer Installation (For Development)**
1. Clone or download this repository
2. Create a symbolic link or copy the `io_mesh_3mf` folder to:
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\4.5\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/4.5/scripts/addons/`
   - **Linux**: `~/.config/blender/4.5/scripts/addons/`
3. Restart Blender or reload scripts (F3 → "Reload Scripts")
4. Enable in Preferences → Add-ons → Search "3MF"

### For Blender 2.80-3.6 (Original Version)
Use the [original repository releases](https://github.com/Ghostkeeper/Blender3mfFormat/releases/latest).

### Verifying Installation
After enabling the addon, you should see:
- **File → Import → 3D Manufacturing Format (.3mf)**
- **File → Export → 3D Manufacturing Format (.3mf)**

### Future: Blender Extensions Platform
This addon may at some point be submitted to [Blender Extensions](https://extensions.blender.org), if Ghostkeeper ever comes back and wants to, or if they ever recede their claim to the add-on's current state to an active maintainer. 


Usage
----
When this add-on is installed, a new entry will appear under the File -> Import menu called "3D Manufacturing Format". When you click that, you'll be able to select 3MF files to import into your Blender scene. A new entry will also appear under the File -> Export menu with the same name. This allows you to export your scene to a 3MF file.

![Screenshot](screenshot.png)

The following options are available when importing 3MF files:
* Scale: A scaling factor to apply to the scene after importing. All of the mesh data loaded from the 3MF files will get scaled by this factor from the origin of the coordinate system. They are not scaled individually from the centre of each mesh, but all from the coordinate origin.

The following options are available when exporting to 3MF:
* Selection only: Only export the objects that are selected. Other objects will not be included in the 3MF file.
* Scale: A scaling factor to apply to the models in the 3MF file. The models are scaled by this factor from the coordinate origin.
* Apply modifiers: Apply the modifiers to the mesh data before exporting. This embeds these modifiers permanently in the file. If this is disabled, the unmodified meshes will be saved to the 3MF file instead.
* Precision: Number of decimals to use for coordinates in the 3MF file. Greater precision will result in a larger file size.

Scripting
----
From a script, you can import a 3MF mesh by executing the following function call:

```
bpy.ops.import_mesh.threemf(filepath="/path/to/file.3mf")
```

This import function has two relevant parameters:
* `filepath`: A path to the 3MF file to import.
* `global_scale` (default `1`): A scaling factor to apply to the scene after importing. All of the mesh data loaded from the 3MF files will get scaled by this factor from the origin of the coordinate system.

You can export a 3MF mesh by executing the following function call:

```
bpy.ops.export_mesh.threemf(filepath="/path/to/file.3mf")
```

This export function has five relevant parameters:
* `filepath`: The location to store the 3MF file.
* `use_selection` (default `False`): Only export the objects that are selected. Other objects will not be included in the 3MF file.
* `global_scale` (default `1`): A scaling factor to apply to the models in the 3MF file. The models are scaled by this factor from the coordinate origin.
* `use_mesh_modifiers` (default `True`): Apply the modifiers to the mesh data before exporting. This embeds these modifiers permanently in the file. If this is disabled, the unmodified meshes will be saved to the 3MF file instead.
* `coordinate_precision` (default `4`): Number of decimals to use for coordinates in the 3MF file. Greater precision will result in a larger file size.

Testing
----
This addon has comprehensive test coverage to ensure reliability:

**Unit Tests** (142 tests - mock-based, no Blender required):
```bash
python -m unittest test
```

**Integration Tests** (16 tests - requires Blender 4.2+):
```powershell
# Windows
.\test\run_integration_tests.ps1

# macOS/Linux
./test/run_integration_tests.sh
```

For detailed testing information, see [`test/README.md`](test/README.md).

**CI/CD**: Unit tests run automatically on every push via GitHub Actions.

Support
----
This add-on currently supports the full [3MF Core Specification](https://github.com/3MFConsortium/spec_core/blob/1.2.3/3MF%20Core%20Specification.md) version 1.2.3. However there are a number of places where it deviates from the specification on purpose.

The 3MF specification demands that consumers of 3MF files (i.e. importing 3MF files) must fail quickly and catastrophically when anything is wrong. If a single field is wrong, the entire archive should not get loaded. This add-on has the opposite approach: If something small is wrong with the file, the rest of the file can still be loaded, but for instance without loading that particular triangle that's wrong. You'll get an incomplete file and a warning is placed in the Blender log.

The 3MF specification is also not designed to handle loading multiple 3MF files at once, or to load 3MF files into existing scenes together with other 3MF files. This add-on will try to load as much as possible, but if there are conflicts with parts of the files, it will load neither. One example is the scene metadata such as the title of the scene. If loading two files with the same title, that title is kept. However when combining files with multiple titles, no title will be loaded.

No 3MF format extensions are currently supported. That is a goal for future development.
