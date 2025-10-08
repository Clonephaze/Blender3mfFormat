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

"""
This module defines some constants for 3MF's file structure.

These are the constants that are inherent to the 3MF file format.
"""

from typing import Set, Dict

# IDE and Documentation support.
__all__ = [
    "SUPPORTED_EXTENSIONS",
    "conflicting_mustpreserve_contents",
    "MODEL_LOCATION",
    "CONTENT_TYPES_LOCATION",
    "RELS_FOLDER",
    "MODEL_REL",
    "THUMBNAIL_REL",
    "RELS_MIMETYPE",
    "MODEL_MIMETYPE",
    "MODEL_NAMESPACE",
    "MODEL_NAMESPACES",
    "MODEL_DEFAULT_UNIT",
    "CONTENT_TYPES_NAMESPACE",
    "CONTENT_TYPES_NAMESPACES",
    "RELS_NAMESPACE",
    "RELS_NAMESPACES",
    "RELS_RELATIONSHIP_FIND",
]

SUPPORTED_EXTENSIONS: Set[str] = set()  # Set of namespaces for 3MF extensions that we support.
# File contents to use when files must be preserved but there's a file with different content in a previous archive.
# Only for flagging. This will not be in the final 3MF archives.
conflicting_mustpreserve_contents: str = "<Conflicting MustPreserve file!>"

# Default storage locations.
MODEL_LOCATION: str = "3D/3dmodel.model"  # Conventional location for the 3D model data.
CONTENT_TYPES_LOCATION: str = "[Content_Types].xml"  # Location of the content types definition.
RELS_FOLDER: str = "_rels"  # Folder name to store relationships files in.

# Relationship types.
MODEL_REL: str = "http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"  # Relationship type of 3D models.
THUMBNAIL_REL: str = "http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail"

# MIME types of files in the archive.
RELS_MIMETYPE: str = "application/vnd.openxmlformats-package.relationships+xml"  # MIME type of .rels files.
MODEL_MIMETYPE: str = "application/vnd.ms-package.3dmanufacturing-3dmodel+xml"  # MIME type of .model files.

# Constants in the 3D model file.
MODEL_NAMESPACE: str = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
MODEL_NAMESPACES: Dict[str, str] = {
    "3mf": MODEL_NAMESPACE
}
MODEL_DEFAULT_UNIT: str = "millimeter"  # If the unit is missing, it will be this.

# Constants in the ContentTypes file.
CONTENT_TYPES_NAMESPACE: str = "http://schemas.openxmlformats.org/package/2006/content-types"
CONTENT_TYPES_NAMESPACES: Dict[str, str] = {
    "ct": CONTENT_TYPES_NAMESPACE
}

# Constants in the .rels files.
RELS_NAMESPACE: str = "http://schemas.openxmlformats.org/package/2006/relationships"
RELS_NAMESPACES: Dict[str, str] = {  # Namespaces used for the rels files.
    "rel": RELS_NAMESPACE
}
RELS_RELATIONSHIP_FIND: str = "rel:Relationship"
