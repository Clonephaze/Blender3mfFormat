#!/usr/bin/env bash
# Blender 3MF addon integration test runner for macOS/Linux
#
# Usage (from repository root):
#   ./test/run_integration_tests.sh              # Auto-detect Blender
#   ./test/run_integration_tests.sh --all        # Test all installed versions
#   ./test/run_integration_tests.sh --verbose    # Show verbose output
#   ./test/run_integration_tests.sh --blender-path /path/to/blender  # Use specific Blender

set -e

# Default values
VERBOSE=""
BLENDER_PATH=""
ALL_VERSIONS=0

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE="--verbose"
            shift
            ;;
        -a|--all|--all-versions)
            ALL_VERSIONS=1
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
            echo "  -a, --all, --all-versions  Test against all installed Blender versions"
            echo "  -b, --blender-path PATH    Path to Blender executable (auto-detected if not specified)"
            echo "  -h, --help                 Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0"
            echo "  $0 --all"
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

# Function to find all Blender installations
find_all_blender() {
    echo "Searching for all Blender installations..."
    local all_blenders=()
    
    # Try PATH first (user's preferred version)
    if command -v blender &> /dev/null; then
        local blender_cmd=$(command -v blender)
        all_blenders+=("$blender_cmd")
    fi
    
    # Platform-specific search paths
    local search_paths=()
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS paths
        search_paths=(
            "/Applications/Blender*.app/Contents/MacOS/Blender"
            "$HOME/Applications/Blender*.app/Contents/MacOS/Blender"
        )
    else
        # Linux paths
        search_paths=(
            "/usr/bin/blender*"
            "/usr/local/bin/blender*"
            "/opt/blender*/blender"
            "/snap/bin/blender*"
            "$HOME/.local/bin/blender*"
            "$HOME/blender*/blender"
        )
    fi
    
    # Search for Blender in common locations
    for pattern in "${search_paths[@]}"; do
        for path in $pattern; do
            if [[ -x "$path" ]] && [[ ! " ${all_blenders[@]} " =~ " ${path} " ]]; then
                all_blenders+=("$path")
            fi
        done
    done
    
    # Sort and deduplicate
    if [[ ${#all_blenders[@]} -gt 0 ]]; then
        # Sort by path (newer versions typically have higher numbers)
        IFS=$'\n' all_blenders=($(sort -r <<<"${all_blenders[*]}"))
        unset IFS
        
        echo "Found ${#all_blenders[@]} Blender installation(s):"
        for blender in "${all_blenders[@]}"; do
            echo "  - $blender"
        done
    fi
    
    # Return as newline-separated string
    printf '%s\n' "${all_blenders[@]}"
}

# Function to find single Blender executable (latest version)
find_blender() {
    local all_blenders=($(find_all_blender | tail -n +2))  # Skip the "Found X installations" line
    if [[ ${#all_blenders[@]} -gt 0 ]]; then
        echo "${all_blenders[0]}"
        return 0
    fi
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

# Function to run tests for a single Blender version
run_tests_for_blender() {
    local blender_exe="$1"
    local verbose_flag="$2"
    
    # Get Blender version
    local version_output=$("$blender_exe" --version 2>&1 | head -n 1)
    
    echo ""
    echo "======================================================================"
    echo "Testing: $version_output"
    echo "======================================================================"
    echo "Path: $blender_exe"
    echo "======================================================================"
    echo ""
    
    # Build command arguments
    local blender_args=(
        --background
        --python "$TEST_SCRIPT"
        --
    )
    
    if [[ -n "$verbose_flag" ]]; then
        blender_args+=("$verbose_flag")
    fi
    
    # Run tests
    echo "Running tests..."
    echo ""
    
    "$blender_exe" "${blender_args[@]}"
    return $?
}

# Determine which Blender versions to test
declare -a BLENDERS_TO_TEST

if [[ $ALL_VERSIONS -eq 1 ]]; then
    # Test all installed versions
    echo ""
    mapfile -t BLENDERS_TO_TEST < <(find_all_blender | tail -n +2)  # Skip the "Found X installations" line
    
    if [[ ${#BLENDERS_TO_TEST[@]} -eq 0 ]]; then
        echo "Error: No Blender installations found." >&2
        echo "Please install Blender or specify the path with --blender-path parameter." >&2
        exit 1
    fi
    echo ""
else
    # Test single version
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
    BLENDERS_TO_TEST=("$BLENDER_PATH")
fi

# Run tests for each Blender version
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
declare -a RESULTS

for blender in "${BLENDERS_TO_TEST[@]}"; do
    if run_tests_for_blender "$blender" "$VERBOSE"; then
        version_str=$("$blender" --version 2>&1 | head -n 1)
        echo ""
        echo "✅ PASSED: $version_str"
        ((PASSED_TESTS++))
        RESULTS+=("PASSED|$version_str")
    else
        exit_code=$?
        version_str=$("$blender" --version 2>&1 | head -n 1)
        echo ""
        echo "❌ FAILED: $version_str (exit code: $exit_code)"
        ((FAILED_TESTS++))
        RESULTS+=("FAILED|$version_str|$exit_code")
    fi
    
    ((TOTAL_TESTS++))
    
    if [[ $TOTAL_TESTS -lt ${#BLENDERS_TO_TEST[@]} ]]; then
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    fi
done

# Print summary if testing multiple versions
if [[ $TOTAL_TESTS -gt 1 ]]; then
    echo ""
    echo "======================================================================"
    echo "TEST SUMMARY"
    echo "======================================================================"
    echo "Total Blender versions tested: $TOTAL_TESTS"
    echo "Passed: $PASSED_TESTS"
    echo "Failed: $FAILED_TESTS"
    echo ""
    
    for result in "${RESULTS[@]}"; do
        IFS='|' read -r status version exit_code <<< "$result"
        if [[ "$status" == "PASSED" ]]; then
            echo "✅ $version"
        else
            echo "❌ $version (exit code: $exit_code)"
        fi
    done
    echo "======================================================================"
fi

# Exit with appropriate code
if [[ $FAILED_TESTS -gt 0 ]]; then
    exit 1
else
    exit 0
fi
