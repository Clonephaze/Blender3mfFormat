#!/usr/bin/env bash
# Blender 3MF addon integration test runner for macOS/Linux
#
# Usage (from repository root):
#   ./test/run_integration_tests.sh              # Auto-detect Blender
#   ./test/run_integration_tests.sh --verbose    # Show verbose output
#   ./test/run_integration_tests.sh --blender-path /path/to/blender  # Use specific Blender

set -e

# Default values
VERBOSE=""
BLENDER_PATH=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE="--verbose"
            shift
            ;;
        -b|--blender-path)
            BLENDER_PATH="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Run Blender 3MF addon integration tests"
            echo ""
            echo "Options:"
            echo "  -v, --verbose              Show verbose test output"
            echo "  -b, --blender-path PATH    Path to Blender executable (auto-detected if not specified)"
            echo "  -h, --help                 Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0"
            echo "  $0 --verbose"
            echo "  $0 --blender-path /usr/local/blender/blender"
            exit 0
            ;;
        *)
            echo "Error: Unknown option $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Function to find Blender executable
find_blender() {
    echo "Searching for Blender installation..."
    
    # Try PATH first (user's preferred version)
    if command -v blender &> /dev/null; then
        local blender_cmd=$(command -v blender)
        echo "Found Blender in PATH: $blender_cmd"
        echo "$blender_cmd"
        return 0
    fi
    
    # Platform-specific search paths
    local search_paths=()
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS paths
        search_paths=(
            "/Applications/Blender.app/Contents/MacOS/Blender"
            "/Applications/Blender*.app/Contents/MacOS/Blender"
            "$HOME/Applications/Blender.app/Contents/MacOS/Blender"
            "$HOME/Applications/Blender*.app/Contents/MacOS/Blender"
        )
    else
        # Linux paths
        search_paths=(
            "/usr/bin/blender"
            "/usr/local/bin/blender"
            "/opt/blender/blender"
            "/snap/bin/blender"
            "$HOME/.local/bin/blender"
            "$HOME/blender*/blender"
        )
    fi
    
    # Search for Blender in common locations
    for pattern in "${search_paths[@]}"; do
        # Use glob expansion
        for path in $pattern; do
            if [[ -x "$path" ]]; then
                echo "Found Blender: $path"
                echo "$path"
                return 0
            fi
        done
    done
    
    return 1
}

# Get script directory (now in test folder, so go up one level)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_SCRIPT="$SCRIPT_DIR/test/run_integration_tests.py"

# Check if test script exists
if [[ ! -f "$TEST_SCRIPT" ]]; then
    echo "Error: Test script not found: $TEST_SCRIPT" >&2
    echo "Make sure you are running this from the repository root." >&2
    exit 1
fi

# Find or use specified Blender
if [[ -z "$BLENDER_PATH" ]]; then
    BLENDER_PATH=$(find_blender)
    if [[ $? -ne 0 ]] || [[ -z "$BLENDER_PATH" ]]; then
        echo "Error: Could not find Blender installation." >&2
        echo "Please specify the path with --blender-path parameter." >&2
        echo "Example: $0 --blender-path /path/to/blender" >&2
        exit 1
    fi
else
    if [[ ! -x "$BLENDER_PATH" ]]; then
        echo "Error: Blender not found or not executable: $BLENDER_PATH" >&2
        exit 1
    fi
fi

# Get Blender version
VERSION_OUTPUT=$("$BLENDER_PATH" --version 2>&1 | head -n 1)

# Print header
echo ""
echo "======================================================================"
echo "Blender 3MF Addon - Integration Tests"
echo "======================================================================"
echo "Blender: $VERSION_OUTPUT"
echo "Test Script: $TEST_SCRIPT"
echo "======================================================================"
echo ""

# Build command arguments
BLENDER_ARGS=(
    --background
    --python "$TEST_SCRIPT"
    --
)

if [[ -n "$VERBOSE" ]]; then
    BLENDER_ARGS+=("$VERBOSE")
fi

# Run tests
echo "Running tests..."
echo ""

if "$BLENDER_PATH" "${BLENDER_ARGS[@]}"; then
    echo ""
    echo "All tests passed!"
    exit 0
else
    EXIT_CODE=$?
    echo ""
    echo "Tests failed with exit code: $EXIT_CODE"
    exit $EXIT_CODE
fi
