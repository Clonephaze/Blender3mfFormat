1.1.0 - Modernization for Blender 4.2+
====
**IMPORTANT: This version requires Blender 4.2 or newer. For Blender 2.8-4.1, use version 1.0.2.**

This release modernizes the addon for Blender 4.2+ and Python 3.11+, ensuring compatibility with current and future Blender versions.

Breaking Changes
----
* **Minimum Blender version is now 4.2** (previously supported 2.8-4.0)
* **Minimum Python version is now 3.11** (previously 3.7+)
* Installation now uses Blender Extensions format (drag-and-drop .zip or install via Preferences)

Features
----
* Full compatibility with Blender 4.2, 4.3, 4.5, and 5.0 Alpha
* Verified compatibility with all modern Blender APIs:
  - `PrincipledBSDFWrapper` for material handling
  - `mesh.loop_triangles` for mesh data
  - `evaluated_depsgraph_get()` for modifier evaluation
* Comprehensive test suite (142 unit tests + 16 integration tests)
* Cross-platform integration test runners (Windows PowerShell, macOS/Linux Bash)
* Multi-version testing support (test against all installed Blender versions)
* Automated CI/CD testing via GitHub Actions
* Updated documentation and contribution guidelines

Technical Improvements
----
* Replaced wildcard imports with explicit imports for better code maintainability
* Removed deprecated `__init__()` methods from operators (Blender 4.2+ requirement)
* Fixed state variable initialization in export/import classes
* Updated manifest format for modern Blender addon structure
* Improved error handling for malformed 3MF files

Bug Fixes
----
* Fixed operator initialization for Blender 4.2+ compatibility
* Fixed material color handling with modern shader node API
* Fixed mesh triangulation with current API patterns
* Corrected depsgraph evaluation for objects with modifiers

Testing
----
* All original unit tests updated and passing (Python 3.11)
* New integration tests verify real-world Blender functionality
* Tested across Blender 4.2 LTS, 4.3, 4.5, and 5.0 Alpha
* Verified export → import round-trip functionality
* Confirmed material preservation through round-trip operations

Contributors
----
* Modernization work by Jack (Clonephaze)
* Original addon by Ghostkeeper

1.0.2 - Bug Fixes
====
* Fix support in newer Blender versions, up to 4.0.
* Run tests using Python 3.10.

1.0.1 - Bug Fixes
====
* Fix the resource ID of exported materials to be integer.

1.0.0 - Big Bang
====
For the first stable release, the full core 3MF specification is implemented.

Features
----
* Support for importing materials, and applying them to triangles of your meshes.
* Support for exporting materials from Blender with a diffuse color.
* Metadata is now retained when editing existing 3MF files.
* Relationships are retained when editing existing 3MF files.
* Content types are retained when editing existing 3MF files.
* Added support for the model types "solidsupport", "support" and "surface".
* Support and solidsupport meshes are hidden from any renders.
* 3MF part numbers are retained when editing existing 3MF files.
* Files marked as MustPreserve are retained when editing existing 3MF files.
* PrintTickets are retained when editing existing 3MF files.
* When metadata, relationships and content types clash when loading multiple 3MF files into one scene, the most common denominator is kept.
* Metadata, relationships, content types and part numbers are retained when the scene is shared through a .blend file.
* The object names are now stored in the 3MF files as metadata.
* Content types are now being read out, allowing for any file type to be anywhere in the archive.
* Automated tests improve stability of the add-on.
* Actions are being logged in Blender's log stream.
* If anything goes wrong, errors and warnings are being logged in Blender's log stream.
* The code is now compliant to Blender's code style requirements.
* Added support for new "Adaptive" units in Blender.
* Transformation matrices are written more compactly.
* Vertex coordinates are written more compactly.
* Warn the user if the 3MF document requires 3MF extensions that are not present.
* When exporting, you can now configure the number of decimals to write.
* Material colors are rendered in Blender with a BSDF node, and converted back to sRGB when exporting.
* The exported 3MF archive is now compressed with the Deflate algorithm.
* Allow installation via .zip file.

Bug Fixes
----
* No longer crash if faces are provided with negative vertex indices.
* Importing multiple 3MF files in succession no longer allows resource objects of old files to be used by new files.
* Exporting multiple 3MF files in succession resets the resource ID counter every time.
* No longer crash if there are no access rights to files to read or write.
* Fix writing of transformations for resource objects that have components.
* Fix writing transformations if multiple transformed objects are written.
* Resource objects that have components can no longer have mesh data of their own.
* No longer create meshes when an object has no vertices or faces.
* Transformation matrices and vertex coordinates will no longer use scientific notation for big or tiny numbers.

0.2.0 - Get Out
====
This is another pre-release where the goal is to implement exporting 3MF files from Blender.

Features
----
* A menu item is added to the export menu to export 3D Manufactoring Format files.
* Saving Open Document formatted archives.
* Support for exporting object resources.
* Support for exporting vertices.
* Support for exporting triangles.
* Support for exporting components.
* Support for exporting build items.
* Support for exporting transformations.
* Support for conversion from Blender's units to millimetres.
* You can now scale the models when importing and exporting.

Bug Fixes
----
* The unit is now applied after the 3MF file's own transformations, so that models end up in the correct position.

0.1.0 - Come On In
====
This is a minimum viable product release where the goal is to reliably import at least the geometry of a 3MF file into Blender.

Features
----
* A menu item is added to the import menu to import 3D Manufactoring Format files.
* Opening 3MF archives.
* Support for importing object resources.
* Support for importing vertices.
* Support for importing triangles.
* Support for importing components.
* Support for importing build items.
* Support for transformations on build items and components.
* Transforming the 3MF file units correctly to Blender's units.
