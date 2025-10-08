# Blender 3MF Format - Testing Guide

This directory contains two types of tests for the Blender 3MF addon:

## Unit Tests

**What they are**: Fast, isolated tests that mock the Blender API. They test individual functions and modules without requiring Blender to be installed.

**When to use**: 
- During development to quickly verify changes
- In CI/CD pipelines
- To test specific functions in isolation

**How to run**:
```bash
# From the repository root
python -m unittest test                          # All unit tests
python -m unittest test.export_3mf               # Export tests only
python -m unittest test.import_3mf               # Import tests only
python -m unittest test.annotations              # Annotation tests only
python -m unittest test.metadata                 # Metadata tests only
```

**Requirements**:
- Python 3.11+ (3.10+ should work but 3.11 is tested in CI)
- `mathutils` package: `pip install mathutils`
- `pycodestyle` (optional, for style checking): `pip install pycodestyle`

**Current status**: 142 tests, all passing ✅

## Integration Tests

**What they are**: End-to-end tests that run inside a real Blender instance. They test the full import/export workflow including actual file I/O, material handling, and mesh operations.

**When to use**:
- Before submitting pull requests
- To verify the addon works with your Blender version
- To test real-world import/export scenarios
- To verify Blender API compatibility

**How to run**:

### Windows (PowerShell)
```powershell
# From the repository root
.\test\run_integration_tests.ps1                       # Auto-detect latest Blender
.\test\run_integration_tests.ps1 -AllVersions          # Test ALL installed versions! 🎯
.\test\run_integration_tests.ps1 -Verbose              # Verbose output
.\test\run_integration_tests.ps1 -BlenderPath "C:\Path\To\blender.exe"  # Specific version
```

### macOS/Linux (Bash)
```bash
# From the repository root
./test/run_integration_tests.sh                       # Auto-detect latest Blender
./test/run_integration_tests.sh --all                 # Test ALL installed versions! 🎯
./test/run_integration_tests.sh --verbose             # Verbose output
./test/run_integration_tests.sh --blender-path /path/to/blender  # Specific version
```

**🎯 NEW: Multi-Version Testing!**
Use `-AllVersions` (PowerShell) or `--all` (Bash) to automatically test against all installed Blender versions. This is perfect for ensuring compatibility across Blender 4.2, 4.3, 4.4, 4.5, etc.

Example output:
```
Found 3 Blender installation(s):
  - C:\Program Files\Blender Foundation\Blender 4.5\blender.exe
  - C:\Program Files\Blender Foundation\Blender 4.3\blender.exe
  - C:\Program Files\Blender Foundation\Blender 4.2\blender.exe

Testing: Blender 4.5.0
✅ PASSED: Blender 4.5.0

Testing: Blender 4.3.2
✅ PASSED: Blender 4.3.2

Testing: Blender 4.2.1 LTS
✅ PASSED: Blender 4.2.1 LTS

TEST SUMMARY
Total Blender versions tested: 3
Passed: 3
Failed: 0
```

**Requirements**:
- Blender 4.2+ installed
- The addon must be loadable by Blender (it will be loaded from your working directory)

**Current status**: 16 tests, all passing ✅

Tests include graceful handling of malformed files (verifies no crashes occur).

## Test Structure

```
test/
├── README.md                          # This file
├── __init__.py                        # Test package initialization
├── export_3mf.py                      # Unit tests for export functionality
├── import_3mf.py                      # Unit tests for import functionality
├── annotations.py                     # Unit tests for annotation handling
├── metadata.py                        # Unit tests for metadata handling
├── run_integration_tests.py           # Integration test suite (runs in Blender)
├── run_integration_tests.ps1          # PowerShell runner for integration tests
├── run_integration_tests.sh           # Bash runner for integration tests (macOS/Linux)
├── mock/
│   └── bpy.py                         # Mock Blender Python API for unit tests
└── resources/
    ├── corrupt_archive.3mf            # Test file: Intentionally malformed
    ├── empty_archive.zip              # Test file: Empty archive
    └── only_3dmodel_file.3mf          # Test file: Minimal valid 3MF

```

## Writing Tests

### Adding Unit Tests

1. Add test methods to the appropriate test file (`export_3mf.py`, `import_3mf.py`, etc.)
2. Use the mock Blender API in `mock/bpy.py` 
3. Test should be fast and not require Blender installation
4. Follow the existing pattern: use `unittest.TestCase` and `setUp()`/`tearDown()`

Example:
```python
def test_my_feature(self):
    """Test description."""
    # Arrange
    expected = "some_value"
    
    # Act
    result = self.exporter.my_function()
    
    # Assert
    self.assertEqual(result, expected)
```

### Adding Integration Tests

1. Add test methods to `run_integration_tests.py`
2. Use real Blender API (`bpy`)
3. Tests can create/modify actual Blender objects and files
4. Clean up after yourself in `tearDown()` or `cleanup()` methods

Example:
```python
def test_my_integration(self):
    """Test description."""
    import bpy
    
    # Create test data
    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.active_object
    
    # Test export
    filepath = os.path.join(self.test_dir, "my_test.3mf")
    bpy.ops.export_mesh.threemf(filepath=filepath)
    
    # Verify file exists
    self.assertTrue(os.path.exists(filepath))
```

## Code Style

All code should follow [Blender's Python style guide](https://wiki.blender.org/wiki/Style_Guide/Python):
- PEP-8 compliant
- Single quotes (`'`) for enum-style string constants
- Double quotes (`"`) for other strings
- Maximum line length: 120 characters

Run style checker:
```bash
python -m pycodestyle --ignore=E402 --max-line-length=120 .
```

## Continuous Integration

Unit tests run automatically on GitHub Actions for every push and pull request:
- Python 3.11
- All unit test modules
- Code style validation with pycodestyle

Integration tests must be run locally (they require a Blender installation).
