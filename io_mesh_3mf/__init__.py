# Blender add-on to import and export 3MF files.
# Copyright (C) 2020 Ghostkeeper
# Copyright (C) 2025 Jack (modernization for Blender 4.2+)
# This add-on is free software; you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later
# version.
# This add-on is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# Reload functionality.
if "bpy" in locals():
    import importlib
    from . import import_3mf, export_3mf

    importlib.reload(import_3mf)
    importlib.reload(export_3mf)
else:
    from . import import_3mf, export_3mf

import bpy.types  # To (un)register the add-on as an import/export function.
import bpy.utils  # To (un)register the add-on.

from .export_3mf import Export3MF  # Exports 3MF files.
from .import_3mf import Import3MF  # Imports 3MF files.

# IDE and Documentation support.
__all__ = [
    "Export3MF",
    "Import3MF",
    "register",
    "unregister",
]

"""
Import and export 3MF files in Blender.
"""


def menu_import(self, _) -> None:
    """
    Calls the 3MF import operator from the menu item.
    """
    self.layout.operator(Import3MF.bl_idname, text="3D Manufacturing Format (.3mf)")


def menu_export(self, _) -> None:
    """
    Calls the 3MF export operator from the menu item.
    """
    self.layout.operator(Export3MF.bl_idname, text="3D Manufacturing Format (.3mf)")


classes = (Import3MF, Export3MF)


def register() -> None:
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(menu_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_export)


def unregister() -> None:
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.TOPBAR_MT_file_import.remove(menu_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export)


# Allow the add-on to be ran directly without installation.
if __name__ == "__main__":
    register()
