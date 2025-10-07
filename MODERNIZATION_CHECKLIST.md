# Blender 3MF Format Addon - Modernization Checklist

## 📋 Overview
This checklist tracks the modernization of the Blender 3MF addon from Blender 2.8 to 4.2+.

**Estimated Time:** 2-3 weeks  
**Difficulty:** 6/10 (Moderate)

---

## Phase 1: Critical Fixes (Must Complete First) 🔴

### Import/Export Fixes
- [x] Fix reload logic in `__init__.py`
- [x] Add copyright notice for 2025 modernization
- [x] Update README with modernization status
- [x] Replace wildcard imports with explicit imports in all files

#### Files to Fix:
- [x] `io_mesh_3mf/import_3mf.py` - Add `conflicting_mustpreserve_contents`
- [x] `io_mesh_3mf/export_3mf.py` - Replace `from .constants import *`
- [x] `io_mesh_3mf/annotations.py` - Replace `from .constants import *`
- [x] `io_mesh_3mf/metadata.py` - Check for any wildcard imports

### Property Syntax Updates (Blender 4.2+ Compatibility)
- [ ] Fix `export_3mf.py` property annotations
  - [ ] Remove `: ` from `filter_glob` (line 50)
  - [ ] Remove `: ` from `use_selection` (line 51)
  - [ ] Remove `: ` from `global_scale` (line 57)
  - [ ] Remove `: ` from `use_mesh_modifiers` (line 60)
  - [ ] Remove `: ` from `coordinate_precision` (line 65)

- [ ] Fix `import_3mf.py` property annotations
  - [ ] Remove `: ` from `filter_glob`
  - [ ] Remove `: ` from `files`
  - [ ] Remove `: ` from `directory`
  - [ ] Remove `: ` from `global_scale`

### bl_info Updates
- [ ] Update `bl_info` in `__init__.py`
  - [ ] Change `"blender": (2, 80, 0)` to `"blender": (4, 2, 0)`
  - [ ] Update version to `(2, 0, 0)` or similar to indicate major update
  - [ ] Update `"author"` to include contributor info

---

## Phase 2: Blender 4.2+ API Compatibility Testing 🟡

### Initial Testing
- [ ] Install addon in Blender 4.2
- [ ] Test basic loading (does it appear in preferences?)
- [ ] Document all errors that occur

### Export Testing
- [ ] Test exporting a simple cube
  - [ ] Note any errors
  - [ ] Check if file is created
- [ ] Test exporting with materials
  - [ ] Check material color export
  - [ ] Verify shader node access works
- [ ] Test exporting with modifiers
- [ ] Test "Selection Only" option
- [ ] Test scale settings
- [ ] Test precision settings

### Import Testing
- [ ] Test importing `test/resources/only_3dmodel_file.3mf`
  - [ ] Note any errors
  - [ ] Verify mesh appears in scene
- [ ] Test importing file with materials
- [ ] Test importing file with metadata
- [ ] Test scale settings

### Material System Fixes (HIGH RISK AREA)
- [ ] Test `bpy_extras.node_shader_utils.PrincipledBSDFWrapper` compatibility
  - Location: `export_3mf.py` line ~239
  - [ ] Verify `base_color` property access works
  - [ ] Verify `alpha` property access works
  - [ ] Check if color space conversion is correct
- [ ] Test material slot access patterns
- [ ] Verify material index handling

### Mesh API Fixes
- [ ] Test `mesh.calc_loop_triangles()` (export_3mf.py line ~388)
- [ ] Test `mesh.loop_triangles` access
- [ ] Test `blender_object.to_mesh()` (export_3mf.py line ~383)
- [ ] Test `bpy.context.evaluated_depsgraph_get()` (export_3mf.py line ~376)
- [ ] Test `blender_object.evaluated_get()` (export_3mf.py line ~377)

### Context Usage Fixes
- [ ] Replace `bpy.context` with passed `context` parameter in:
  - [ ] `export_3mf.py` line 116 (`scene_metadata.retrieve(bpy.context.scene)`)
  - [ ] `export_3mf.py` line 376 (`bpy.context.evaluated_depsgraph_get()`)
  - [ ] Any other instances found

### Property Storage Fixes
- [ ] Verify `bpy.data.texts` still works for storing annotations
  - Location: `annotations.py` `store()` method
  - Location: `export_3mf.py` `must_preserve()` method
- [ ] Test `textfile.as_string()` method compatibility
- [ ] Check if `idprop.types` import is needed (metadata.py line 2)

---

## Phase 3: Test Suite Modernization 🧪

### Unit Tests (Mock-Based)
- [ ] Fix wildcard imports in test files
  - [ ] `test/annotations.py` - Replace `from io_mesh_3mf.constants import *`
  - [ ] `test/export_3mf.py` - Replace `from io_mesh_3mf.constants import *`
  - [ ] `test/import_3mf.py` - Replace `from io_mesh_3mf.constants import *`
  - [ ] `test/metadata.py` - Check for wildcards

- [ ] Update mock objects for Blender 4.2 API
  - [ ] Update `test/mock/bpy.py` if needed
  - [ ] Verify `PrincipledBSDFWrapper` mock is correct

- [ ] Run existing unit tests
  - [ ] `python -m unittest discover test`
  - [ ] Fix any failures
  - [ ] Document which tests pass/fail

### Integration Tests (Real Blender)
- [ ] Create `test/run_integration_tests.py`
  - [ ] Copy structure from review notes
  - [ ] Add test for simple cube export
  - [ ] Add test for simple cube import
  - [ ] Add test for round-trip (import then export)
  - [ ] Add test for materials
  - [ ] Add test for Blender 4.2 API compatibility

- [ ] Run integration tests
  - [ ] `blender --background --python test/run_integration_tests.py -- --verbose`
  - [ ] Fix any failures
  - [ ] Document results

- [ ] Test with real 3MF files
  - [ ] Export from Blender, import into slicer
  - [ ] Import 3MF from slicer, verify in Blender
  - [ ] Test with complex models (1000+ triangles)

---

## Phase 4: Code Quality Improvements 📝

### Type Hints (Optional but Recommended)
- [ ] Add type hints to `export_3mf.py`
  - [ ] `execute()` method
  - [ ] `create_archive()` method
  - [ ] `write_materials()` method
  - [ ] Other major methods

- [ ] Add type hints to `import_3mf.py`
  - [ ] `execute()` method
  - [ ] `read_archive()` method
  - [ ] `read_materials()` method
  - [ ] Other major methods

- [ ] Add type hints to `annotations.py`
- [ ] Add type hints to `metadata.py`

### Error Reporting Improvements
- [ ] Add `self.report()` calls for user feedback in:
  - [ ] `export_3mf.py` - Replace `log.error()` with `self.report({'ERROR'}, ...)`
  - [ ] `import_3mf.py` - Replace `log.error()` with `self.report({'ERROR'}, ...)`
  - [ ] Add `self.report({'WARNING'}, ...)` for non-critical issues
  - [ ] Add `self.report({'INFO'}, ...)` for successful operations

### String Formatting
- [ ] Convert all string concatenation to f-strings
  - [ ] `export_3mf.py`
  - [ ] `import_3mf.py`
  - [ ] `annotations.py`
  - [ ] `metadata.py`

### Code Documentation
- [ ] Update outdated comments
  - [ ] Remove "Python 3.7" references (export_3mf.py line 110)
  - [ ] Update any Blender 2.8 specific comments

- [ ] Add `__all__` exports to modules
  - [ ] `__init__.py`
  - [ ] `export_3mf.py`
  - [ ] `import_3mf.py`
  - [ ] `annotations.py`
  - [ ] `metadata.py`
  - [ ] `constants.py`
  - [ ] `unit_conversions.py`

---

## Phase 5: CI/CD and Release 🚀

### GitHub Actions Setup
- [ ] Create `.github/workflows/test.yml`
  - [ ] Add unit test job (Python only)
  - [ ] Add integration test job (with Blender download)
  - [ ] Test against Blender 4.2 and 4.3
  - [ ] Add code coverage reporting

### Documentation
- [ ] Update README.md
  - [x] Add modernization notice
  - [x] Update installation instructions
  - [ ] Add testing instructions
  - [ ] Update compatibility information
  - [ ] Add troubleshooting section

- [ ] Create CHANGELOG.md
  - [ ] Document all API changes
  - [ ] List breaking changes from v1.x
  - [ ] Note Blender version compatibility

- [ ] Update inline documentation
  - [ ] Verify all docstrings are accurate
  - [ ] Update parameter descriptions if API changed

### Release Preparation
- [ ] Create release checklist
  - [ ] All tests pass in Blender 4.2
  - [ ] All tests pass in Blender 4.3
  - [ ] Export/import tested with real files
  - [ ] No linter errors
  - [ ] Documentation complete

- [ ] Version the release
  - [ ] Update `bl_info["version"]` to `(2, 0, 0)`
  - [ ] Create git tag
  - [ ] Build .zip file

- [ ] Test installation
  - [ ] Install .zip in fresh Blender 4.2
  - [ ] Verify all features work
  - [ ] Test uninstall/reinstall

---

## Testing Matrix 🧪

### Blender Versions to Test
- [ ] Blender 4.2.0 LTS (primary target)
- [ ] Blender 4.3.0 (latest stable)
- [ ] Blender 4.4+ (future compatibility)

### Operating Systems to Test
- [ ] Windows (primary development)
- [ ] macOS (if available)
- [ ] Linux (via CI/CD)

### Test Scenarios
- [ ] **Simple Geometry**
  - [ ] Single cube export/import
  - [ ] Multiple objects
  - [ ] Nested objects (parent/child)

- [ ] **Materials**
  - [ ] Single material
  - [ ] Multiple materials per object
  - [ ] Transparency/alpha
  - [ ] Material-less objects

- [ ] **Modifiers**
  - [ ] Export with modifiers applied
  - [ ] Export without modifiers
  - [ ] Complex modifier stacks

- [ ] **Scale/Units**
  - [ ] Different Blender units (mm, cm, m, inches)
  - [ ] Custom scale factors
  - [ ] Very small/large models

- [ ] **Edge Cases**
  - [ ] Empty scene export
  - [ ] Very large models (100k+ triangles)
  - [ ] Objects with no geometry
  - [ ] Corrupted 3MF import
  - [ ] Unicode characters in names

---

## Known Issues to Address 📌

### High Priority
- [ ] Material system may need complete rewrite for Blender 4.2
- [ ] Shader node access patterns changed in 4.x
- [ ] Property annotation syntax must be updated
- [ ] Context access needs cleanup

### Medium Priority
- [ ] Wildcard imports cause linter issues
- [ ] Missing type hints make maintenance harder
- [ ] Error messages don't reach user UI
- [ ] Outdated comments reference old Python/Blender

### Low Priority
- [ ] No performance benchmarks
- [ ] Test coverage not measured
- [ ] No support for 3MF extensions yet

---

## Quick Start Checklist 🏃

**Complete these in order for fastest results:**

1. [ ] Fix all wildcard imports (30 min)
2. [ ] Fix all property annotations (15 min)
3. [ ] Update bl_info version (5 min)
4. [ ] Try loading in Blender 4.2 (15 min)
5. [ ] Fix immediate errors found (2-4 hours)
6. [ ] Test export of simple cube (30 min)
7. [ ] Test import of test file (30 min)
8. [ ] Document what works/doesn't work (30 min)

**After first 8 steps, you'll know the scope of remaining work!**

---

## Progress Tracking

### Completion Status
- Phase 1 (Critical): ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%
- Phase 2 (API Testing): ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%
- Phase 3 (Tests): ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%
- Phase 4 (Quality): ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%
- Phase 5 (Release): ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%

**Overall Progress: 5%** (3 of 150+ items complete)

---

## Notes and Issues

### Blockers
- None yet

### Questions
- None yet

### Decisions Made
1. Modernizing for Blender 4.2+ only (not maintaining 2.8 compatibility)
2. Using explicit imports instead of wildcards
3. Keeping original GPL v2+ license
4. Offering to contribute back to original author

---

## Resources

### Documentation Links
- [Blender 4.2 API Docs](https://docs.blender.org/api/4.2/)
- [Blender Python API Changes](https://wiki.blender.org/wiki/Reference/Release_Notes)
- [3MF Spec](https://github.com/3MFConsortium/spec_core)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

### Testing Commands
```bash
# Unit tests (no Blender needed)
python -m unittest discover test

# Integration tests (requires Blender)
blender --background --python test/run_integration_tests.py -- --verbose

# Install to Blender
mkdir -p ~/.config/blender/4.2/scripts/addons/
cp -r io_mesh_3mf ~/.config/blender/4.2/scripts/addons/
```

### Helper Scripts
```bash
# Find all wildcard imports
grep -r "from .* import \*" io_mesh_3mf/

# Find all bpy.props with type annotations
grep -r ": bpy.props" io_mesh_3mf/

# Count TODO items
grep -r "TODO\|FIXME\|XXX" io_mesh_3mf/ | wc -l
```

---

**Last Updated:** October 7, 2025  
**Maintained by:** Jack  
**Original Author:** Ghostkeeper
