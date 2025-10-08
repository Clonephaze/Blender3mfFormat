<#
.SYNOPSIS
    Run Blender 3MF addon integration tests

.DESCRIPTION
    This script runs the integration tests for the Blender 3MF addon.
    It attempts to find your Blender installation automatically.

.PARAMETER Verbose
    Show verbose test output

.PARAMETER BlenderPath
    Path to Blender executable (auto-detected if not specified)

.EXAMPLE
    .\test\run_integration_tests.ps1
    Run tests with default Blender (from repository root)

.EXAMPLE
    .\test\run_integration_tests.ps1 -Verbose
    Run tests with verbose output

.EXAMPLE
    .\test\run_integration_tests.ps1 -BlenderPath "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
    Run tests with specific Blender version
#>

param(
    [switch]$Verbose,
    [string]$BlenderPath = ""
)

# Function to find Blender executable
function Find-Blender {
    Write-Host "Searching for Blender installation..." -ForegroundColor Cyan

    # Try PATH first (user's preferred version)
    $blenderCmd = Get-Command blender -ErrorAction SilentlyContinue
    if ($blenderCmd) {
        Write-Host "Found Blender in PATH: $($blenderCmd.Source)" -ForegroundColor Green
        return $blenderCmd.Source
    }

    # Common installation paths (fallback)
    $searchPaths = @(
        "C:\Program Files\Blender Foundation\Blender*\blender.exe",
        "C:\Program Files (x86)\Blender Foundation\Blender*\blender.exe",
        "$env:LOCALAPPDATA\Programs\Blender*\blender.exe",
        "$env:ProgramFiles\Blender*\blender.exe"
    )

    foreach ($pattern in $searchPaths) {
        $found = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | 
                 Sort-Object LastWriteTime -Descending | 
                 Select-Object -First 1

        if ($found) {
            Write-Host "Found Blender: $($found.FullName)" -ForegroundColor Green
            return $found.FullName
        }
    }

    return $null
}

# Get script directory (now in test folder, so go up one level)
$scriptDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$testScript = Join-Path $scriptDir "test\run_integration_tests.py"

# Check if test script exists
if (-not (Test-Path $testScript)) {
    Write-Host "Error: Test script not found: $testScript" -ForegroundColor Red
    Write-Host "Make sure you are running this from the repository root." -ForegroundColor Yellow
    exit 1
}

# Find or use specified Blender
if ($BlenderPath -eq "") {
    $BlenderPath = Find-Blender
    if ($null -eq $BlenderPath) {
        Write-Host "Error: Could not find Blender installation." -ForegroundColor Red
        Write-Host "Please specify the path with -BlenderPath parameter." -ForegroundColor Yellow
        Write-Host "Example: .\run_tests.ps1 -BlenderPath 'C:\Path\To\blender.exe'" -ForegroundColor Yellow
        exit 1
    }
} else {
    if (-not (Test-Path $BlenderPath)) {
        Write-Host "Error: Blender not found at: $BlenderPath" -ForegroundColor Red
        exit 1
    }
}

# Get Blender version
$versionOutput = & $BlenderPath --version 2>&1 | Select-Object -First 1
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "Blender 3MF Addon - Integration Tests" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "Blender: $versionOutput" -ForegroundColor White
Write-Host "Test Script: $testScript" -ForegroundColor White
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Build command

# Build command
$blenderArgs = @(
    "--background",
    "--python", $testScript,
    "--"
)

if ($Verbose) {
    $blenderArgs += "--verbose"
}

# Run tests
Write-Host "Running tests..." -ForegroundColor Cyan
Write-Host ""

$result = & $BlenderPath @blenderArgs

# Display output
Write-Output $result

# Check exit code
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "All tests passed!" -ForegroundColor Green
    exit 0
} else {
    Write-Host ""
    Write-Host "Tests failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}
