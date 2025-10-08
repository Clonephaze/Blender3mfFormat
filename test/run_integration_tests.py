#!/usr/bin/env python3
"""
Integration tests for the Blender 3MF addon.

These tests run inside Blender to test the actual addon functionality.
Run with: blender --background --python test/run_integration_tests.py -- --verbose

Copyright (C) 2025 Jack
Licensed under GPL v2+
"""

import sys
import os
import tempfile
import unittest
from pathlib import Path

# Add the parent directory path so we can import the addon
SCRIPT_DIR = Path(__file__).parent
ADDON_DIR = SCRIPT_DIR.parent / "io_mesh_3mf"
sys.path.insert(0, str(ADDON_DIR.parent))

import bpy


class TestBlenderEnvironment(unittest.TestCase):
    """Test that Blender environment is set up correctly."""

    def test_blender_version(self):
        """Verify we're running in Blender 4.2+."""
        version = bpy.app.version
        # Allow 4.x or newer (including 5.0+)
        self.assertGreaterEqual(version[0], 4, f"Expected Blender 4.x+, got {version}")
        if version[0] == 4:
            self.assertGreaterEqual(version[1], 2, f"Expected Blender 4.2+, got {version}")
        print(f"[OK] Running in Blender {version[0]}.{version[1]}.{version[2]}")

    def test_addon_available(self):
        """Verify the 3MF addon can be imported."""
        try:
            import io_mesh_3mf
            print(f"✓ Addon imported from: {io_mesh_3mf.__file__}")
        except ImportError as e:
            self.fail(f"Failed to import addon: {e}")


class TestAddonRegistration(unittest.TestCase):
    """Test addon registration and operator availability."""

    @classmethod
    def setUpClass(cls):
        """Enable the addon before running tests."""
        # Register the addon (only if not already registered)
        import io_mesh_3mf
        try:
            io_mesh_3mf.register()
            print("[OK] Addon registered")
        except ValueError as e:
            if "already registered" in str(e):
                print("[OK] Addon already registered")
            else:
                raise

    @classmethod
    def tearDownClass(cls):
        """Disable the addon after tests."""
        import io_mesh_3mf
        try:
            io_mesh_3mf.unregister()
            print("[OK] Addon unregistered")
        except Exception:
            pass  # Ignore if already unregistered

    def test_export_operator_exists(self):
        """Verify export operator is registered."""
        self.assertTrue(
            hasattr(bpy.ops.export_mesh, "threemf"),
            "Export operator 'export_mesh.threemf' not found",
        )
        print("✓ Export operator registered")

    def test_import_operator_exists(self):
        """Verify import operator is registered."""
        self.assertTrue(
            hasattr(bpy.ops.import_mesh, "threemf"),
            "Import operator 'import_mesh.threemf' not found",
        )
        print("✓ Import operator registered")


class TestBasicExport(unittest.TestCase):
    """Test basic export functionality."""

    @classmethod
    def setUpClass(cls):
        """Enable the addon and set up test environment."""
        import io_mesh_3mf
        try:
            io_mesh_3mf.register()
        except ValueError:
            pass  # Already registered
        cls.temp_dir = tempfile.mkdtemp(prefix="3mf_test_")
        print(f"[OK] Test directory: {cls.temp_dir}")

    @classmethod
    def tearDownClass(cls):
        """Clean up test files."""
        import shutil
        if hasattr(cls, "temp_dir") and os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)
            print("✓ Cleaned up test files")

    def setUp(self):
        """Clear the scene before each test."""
        bpy.ops.wm.read_homefile(use_empty=True)
        # Delete all objects
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()

    def test_export_simple_cube(self):
        """Test exporting a simple cube."""
        # Create a cube
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        cube = bpy.context.active_object
        cube.name = "TestCube"

        # Export
        filepath = os.path.join(self.temp_dir, "test_cube.3mf")
        result = bpy.ops.export_mesh.threemf(filepath=filepath)

        self.assertIn("FINISHED", result, f"Export failed with result: {result}")
        self.assertTrue(os.path.exists(filepath), f"File not created: {filepath}")
        self.assertGreater(os.path.getsize(filepath), 0, "File is empty")
        print(f"✓ Exported cube to {filepath} ({os.path.getsize(filepath)} bytes)")

    def test_export_multiple_objects(self):
        """Test exporting multiple objects."""
        # Create multiple objects
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        bpy.ops.mesh.primitive_uv_sphere_add(location=(3, 0, 0))
        bpy.ops.mesh.primitive_cone_add(location=(-3, 0, 0))

        # Export all
        filepath = os.path.join(self.temp_dir, "test_multiple.3mf")
        result = bpy.ops.export_mesh.threemf(filepath=filepath)

        self.assertIn("FINISHED", result)
        self.assertTrue(os.path.exists(filepath))
        print(f"✓ Exported multiple objects ({os.path.getsize(filepath)} bytes)")

    def test_export_with_material(self):
        """Test exporting with materials."""
        # Create cube with material
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        cube = bpy.context.active_object

        # Create and assign material
        mat = bpy.data.materials.new(name="RedMaterial")
        mat.use_nodes = True
        principled = mat.node_tree.nodes.get("Principled BSDF")
        if principled:
            principled.inputs["Base Color"].default_value = (1.0, 0.0, 0.0, 1.0)  # Red

        cube.data.materials.append(mat)

        # Export
        filepath = os.path.join(self.temp_dir, "test_material.3mf")
        result = bpy.ops.export_mesh.threemf(filepath=filepath)

        self.assertIn("FINISHED", result)
        self.assertTrue(os.path.exists(filepath))
        print(f"✓ Exported with material ({os.path.getsize(filepath)} bytes)")

    def test_export_selection_only(self):
        """Test exporting selected objects only."""
        # Create two cubes
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        cube1 = bpy.context.active_object
        cube1.name = "Cube1"

        bpy.ops.mesh.primitive_cube_add(location=(3, 0, 0))
        cube2 = bpy.context.active_object
        cube2.name = "Cube2"

        # Select only first cube
        bpy.ops.object.select_all(action="DESELECT")
        cube1.select_set(True)
        bpy.context.view_layer.objects.active = cube1

        # Export with selection only
        filepath = os.path.join(self.temp_dir, "test_selection.3mf")
        result = bpy.ops.export_mesh.threemf(
            filepath=filepath, use_selection=True
        )

        self.assertIn("FINISHED", result)
        self.assertTrue(os.path.exists(filepath))
        print(f"✓ Exported selection only ({os.path.getsize(filepath)} bytes)")

    def test_export_with_modifiers(self):
        """Test exporting with modifiers applied."""
        # Create cube with subdivision modifier
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        cube = bpy.context.active_object

        # Add subdivision modifier
        modifier = cube.modifiers.new(name="Subsurf", type="SUBSURF")
        modifier.levels = 2

        # Export with modifiers
        filepath = os.path.join(self.temp_dir, "test_modifiers.3mf")
        result = bpy.ops.export_mesh.threemf(
            filepath=filepath, use_mesh_modifiers=True
        )

        self.assertIn("FINISHED", result)
        self.assertTrue(os.path.exists(filepath))
        print(f"✓ Exported with modifiers ({os.path.getsize(filepath)} bytes)")


class TestBasicImport(unittest.TestCase):
    """Test basic import functionality."""

    @classmethod
    def setUpClass(cls):
        """Enable the addon and create test files."""
        import io_mesh_3mf
        try:
            io_mesh_3mf.register()
        except ValueError:
            pass  # Already registered
        cls.temp_dir = tempfile.mkdtemp(prefix="3mf_test_")
        cls.test_file = os.path.join(cls.temp_dir, "test_import.3mf")

        # Create a test file by exporting a cube
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        bpy.ops.export_mesh.threemf(filepath=cls.test_file)
        print(f"[OK] Created test file: {cls.test_file}")

    @classmethod
    def tearDownClass(cls):
        """Clean up test files."""
        import shutil
        if hasattr(cls, "temp_dir") and os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)
            print("✓ Cleaned up test files")

    def setUp(self):
        """Clear the scene before each test."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()

    def test_import_basic(self):
        """Test importing a basic 3MF file."""
        result = bpy.ops.import_mesh.threemf(filepath=self.test_file)

        self.assertIn("FINISHED", result, f"Import failed with result: {result}")
        self.assertGreater(
            len(bpy.data.objects), 0, "No objects imported"
        )
        print(f"✓ Imported {len(bpy.data.objects)} object(s)")

    def test_import_test_resource(self):
        """Test importing the bundled test resource."""
        test_resource = SCRIPT_DIR / "resources" / "only_3dmodel_file.3mf"
        if not test_resource.exists():
            self.skipTest(f"Test resource not found: {test_resource}")

        result = bpy.ops.import_mesh.threemf(filepath=str(test_resource))

        # This test file is minimal (only 3dmodel.model, no [Content_Types].xml)
        # The addon handles this gracefully with a warning
        # This demonstrates robust error handling - import completes even if file is malformed
        self.assertIn("FINISHED", result, 
                     "Should handle minimal test resource gracefully without crashing")
        # Note: This minimal file may not import any objects (missing metadata)
        # but the important thing is it doesn't crash
        print(f"✓ Minimal test resource handled gracefully ({len(bpy.data.objects)} objects imported)")


class TestRoundTrip(unittest.TestCase):
    """Test export followed by import (round-trip)."""

    @classmethod
    def setUpClass(cls):
        """Enable the addon."""
        import io_mesh_3mf
        try:
            io_mesh_3mf.register()
        except ValueError:
            pass  # Already registered
        cls.temp_dir = tempfile.mkdtemp(prefix="3mf_test_")

    @classmethod
    def tearDownClass(cls):
        """Clean up."""
        import shutil
        if hasattr(cls, "temp_dir") and os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)
            print("✓ Cleaned up test files")

    def setUp(self):
        """Clear the scene."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()

    def test_round_trip_cube(self):
        """Test exporting and re-importing a cube."""
        # Create cube
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        original_verts = len(bpy.context.active_object.data.vertices)

        # Export
        filepath = os.path.join(self.temp_dir, "roundtrip_cube.3mf")
        result = bpy.ops.export_mesh.threemf(filepath=filepath)
        self.assertIn("FINISHED", result)

        # Clear scene
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()

        # Import
        result = bpy.ops.import_mesh.threemf(filepath=filepath)
        self.assertIn("FINISHED", result)
        self.assertGreater(len(bpy.data.objects), 0)

        # Check vertices (should be triangulated, so more vertices)
        imported_obj = bpy.data.objects[0]
        imported_verts = len(imported_obj.data.vertices)
        self.assertEqual(
            imported_verts, original_verts, 
            f"Vertex count mismatch: original={original_verts}, imported={imported_verts}"
        )
        print(f"✓ Round-trip successful: {original_verts} verts -> {imported_verts} verts")

    def test_round_trip_with_material(self):
        """Test round-trip with material preservation."""
        # Create cube with red material
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        cube = bpy.context.active_object

        mat = bpy.data.materials.new(name="TestRed")
        mat.use_nodes = True
        principled = mat.node_tree.nodes.get("Principled BSDF")
        if principled:
            principled.inputs["Base Color"].default_value = (1.0, 0.0, 0.0, 1.0)
        cube.data.materials.append(mat)

        # Export
        filepath = os.path.join(self.temp_dir, "roundtrip_material.3mf")
        bpy.ops.export_mesh.threemf(filepath=filepath)

        # Clear and import
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()
        bpy.ops.import_mesh.threemf(filepath=filepath)

        # Check material exists
        self.assertGreater(len(bpy.data.materials), 0, "No materials imported")
        
        imported_mat = bpy.data.materials[0]
        if imported_mat.use_nodes:
            principled = imported_mat.node_tree.nodes.get("Principled BSDF")
            if principled:
                color = principled.inputs["Base Color"].default_value
                # Check if red-ish (allow for rounding)
                self.assertGreater(color[0], 0.9, "Red channel should be high")
                self.assertLess(color[1], 0.1, "Green channel should be low")
                self.assertLess(color[2], 0.1, "Blue channel should be low")
                print(f"✓ Material color preserved: RGB({color[0]:.3f}, {color[1]:.3f}, {color[2]:.3f})")


class TestAPICompatibility(unittest.TestCase):
    """Test Blender 4.2+ API compatibility."""

    @classmethod
    def setUpClass(cls):
        """Enable the addon."""
        import io_mesh_3mf
        try:
            io_mesh_3mf.register()
        except ValueError:
            pass  # Already registered

    def setUp(self):
        """Clear the scene."""
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()

    def test_principled_bsdf_wrapper(self):
        """Test PrincipledBSDFWrapper compatibility."""
        from bpy_extras.node_shader_utils import PrincipledBSDFWrapper

        # Create material
        mat = bpy.data.materials.new(name="TestMat")
        mat.use_nodes = True

        # Wrap it
        wrapper = PrincipledBSDFWrapper(mat, is_readonly=True)
        
        # Test access to properties
        color = wrapper.base_color
        self.assertIsNotNone(color, "base_color should not be None")
        # Blender 4.5 returns 3 components (RGB), older versions may return 4 (RGBA)
        self.assertIn(len(color), [3, 4], "base_color should have 3 or 4 components")

        alpha = wrapper.alpha
        self.assertIsInstance(alpha, (int, float), "alpha should be numeric")

        print(f"✓ PrincipledBSDFWrapper working: color={color[:3]}, alpha={alpha}")

    def test_depsgraph_evaluated_get(self):
        """Test evaluated depsgraph API."""
        # Create object
        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.active_object

        # Get depsgraph
        depsgraph = bpy.context.evaluated_depsgraph_get()
        self.assertIsNotNone(depsgraph, "Depsgraph should not be None")

        # Get evaluated object
        obj_eval = obj.evaluated_get(depsgraph)
        self.assertIsNotNone(obj_eval, "Evaluated object should not be None")

        print("✓ Depsgraph API working")

    def test_mesh_loop_triangles(self):
        """Test mesh.loop_triangles API."""
        # Create object
        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.active_object
        mesh = obj.data

        # Calculate loop triangles
        mesh.calc_loop_triangles()
        
        self.assertGreater(
            len(mesh.loop_triangles), 0, 
            "Should have loop triangles after calc"
        )
        
        # Check triangle structure
        tri = mesh.loop_triangles[0]
        self.assertEqual(len(tri.vertices), 3, "Triangle should have 3 vertices")

        print(f"✓ loop_triangles API working: {len(mesh.loop_triangles)} triangles")


def run_tests(verbose=False):
    """Run all tests and return success status."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBlenderEnvironment))
    suite.addTests(loader.loadTestsFromTestCase(TestAddonRegistration))
    suite.addTests(loader.loadTestsFromTestCase(TestBasicExport))
    suite.addTests(loader.loadTestsFromTestCase(TestBasicImport))
    suite.addTests(loader.loadTestsFromTestCase(TestRoundTrip))
    suite.addTests(loader.loadTestsFromTestCase(TestAPICompatibility))

    # Run tests
    verbosity = 2 if verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == "__main__":
    # Check for --verbose flag
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    print("=" * 70)
    print("Blender 3MF Addon - Integration Tests")
    print(f"Blender version: {bpy.app.version_string}")
    print(f"Python version: {sys.version}")
    print("=" * 70)
    print()

    success = run_tests(verbose=verbose)

    # Exit with appropriate code
    sys.exit(0 if success else 1)
