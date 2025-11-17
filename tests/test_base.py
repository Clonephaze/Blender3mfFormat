"""
Test utilities and base classes for Blender 3MF addon tests.

This file provides reusable test utilities and base classes.
Tests run directly in Blender using: blender --background --python tests/run_tests.py

Uses unittest (built into Python/Blender) - no external dependencies required.
"""

import bpy
import unittest
import tempfile
import shutil
from pathlib import Path


# ============================================================================
# Global Test Configuration
# ============================================================================

# Shared temporary directory for all tests
_temp_test_dir = None
_test_resources_dir = Path(__file__).parent / "resources"


def get_temp_test_dir():
    """Get or create shared temporary directory for tests."""
    global _temp_test_dir
    if _temp_test_dir is None:
        _temp_test_dir = Path(tempfile.mkdtemp(prefix="3mf_test_"))
        print(f"[test utils] Test output directory: {_temp_test_dir}")
    return _temp_test_dir


def get_test_resources_dir():
    """Get test resources directory."""
    return _test_resources_dir


def cleanup_temp_dir():
    """Clean up temporary test directory."""
    global _temp_test_dir
    if _temp_test_dir and _temp_test_dir.exists():
        shutil.rmtree(_temp_test_dir)
        print("[test utils] Cleaned up test directory")
        _temp_test_dir = None


# ============================================================================
# Base Test Classes
# ============================================================================

class Blender3mfTestCase(unittest.TestCase):
    """Base test case for Blender 3MF addon tests with common utilities."""

    @classmethod
    def setUpClass(cls):
        """Set up test class - register addon once for all tests."""
        import io_mesh_3mf
        try:
            io_mesh_3mf.register()
            print(f"[{cls.__name__}] Addon registered")
        except ValueError as e:
            if "already registered" not in str(e):
                raise

    def setUp(self):
        """Set up before each test - clean scene."""
        self.clean_scene()

        # Create temp file path for this test
        import uuid
        self.temp_file = get_temp_test_dir() / f"test_{uuid.uuid4().hex[:8]}.3mf"
        self.test_resources_dir = get_test_resources_dir()

    def tearDown(self):
        """Clean up after each test."""
        self.clean_scene()

    def clean_scene(self):
        """Reset Blender scene to empty state."""
        # Load empty scene
        bpy.ops.wm.read_homefile(use_empty=True)

        # Delete all objects
        if bpy.context.object and bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        # Clear orphan data
        for mesh in bpy.data.meshes:
            bpy.data.meshes.remove(mesh)
        for material in bpy.data.materials:
            bpy.data.materials.remove(material)

    def create_red_material(self):
        """Create a red Principled BSDF material."""
        mat = bpy.data.materials.new(name="RedMaterial")
        mat.use_nodes = True
        principled = mat.node_tree.nodes.get("Principled BSDF")
        if principled:
            principled.inputs["Base Color"].default_value = (1.0, 0.0, 0.0, 1.0)
        return mat

    def create_blue_material(self):
        """Create a blue Principled BSDF material."""
        mat = bpy.data.materials.new(name="BlueMaterial")
        mat.use_nodes = True
        principled = mat.node_tree.nodes.get("Principled BSDF")
        if principled:
            principled.inputs["Base Color"].default_value = (0.0, 0.0, 1.0, 1.0)
        return mat
