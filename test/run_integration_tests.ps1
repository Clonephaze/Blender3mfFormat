<#
.SYNOPSIS
    Run Blender 3MF addon integration tests

.DESCRIPTION
    This script runs the integration tests for the Blender 3MF addon.
    It can test against a single Blender version or all installed versions.

.PARAMETER Verbose
    Show verbose test output

.PARAMETER BlenderPath
    Path to Blender executable (auto-detected if not specified)

.PARAMETER AllVersions
    Test against all installed Blender versions

.EXAMPLE
    .\test\run_integration_tests.ps1
    Run tests with default Blender (from repository root)

.EXAMPLE
    .\test\run_integration_tests.ps1 -AllVersions
    Run tests against all installed Blender versions

.EXAMPLE
    .\test\run_integration_tests.ps1 -Verbose
    Run tests with verbose output

.EXAMPLE
    .\test\run_integration_tests.ps1 -BlenderPath "C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"
    Run tests with specific Blender version
#>

param(
    [switch]$Verbose,
    [string]$BlenderPath = "",
    [switch]$AllVersions
)

# Function to find all Blender installations
function Find-AllBlender {
    Write-Host "Searching for all Blender installations..." -ForegroundColor Cyan
    $allBlenders = @()

    # Check PATH first
    $blenderCmd = Get-Command blender -ErrorAction SilentlyContinue
    if ($blenderCmd) {
        $allBlenders += $blenderCmd.Source
    }

    # Common installation paths
    $searchPaths = @(
        "C:\Program Files\Blender Foundation\Blender*\blender.exe",
        "C:\Program Files (x86)\Blender Foundation\Blender*\blender.exe",
        "$env:LOCALAPPDATA\Programs\Blender*\blender.exe",
        "$env:ProgramFiles\Blender*\blender.exe"
    )

    foreach ($pattern in $searchPaths) {
        $found = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue
        foreach ($blender in $found) {
            if ($allBlenders -notcontains $blender.FullName) {
                $allBlenders += $blender.FullName
            }
        }
    }

    # Sort by version (newest first)
    $allBlenders = $allBlenders | Sort-Object -Descending

    if ($allBlenders.Count -gt 0) {
        Write-Host "Found $($allBlenders.Count) Blender installation(s):" -ForegroundColor Green
        foreach ($blender in $allBlenders) {
            Write-Host "  - $blender" -ForegroundColor White
        }
    }

    return $allBlenders
}

# Function to find single Blender executable (latest version)
function Find-Blender {
    $allBlenders = Find-AllBlender
    if ($allBlenders.Count -gt 0) {
        return $allBlenders[0]
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

# Function to invoke tests against a single Blender version
function Invoke-TestsForBlender {
    param(
        [string]$BlenderExe,
        [bool]$VerboseOutput
    )

    # Get Blender version
    $versionOutput = & $BlenderExe --version 2>&1 | Select-Object -First 1
    Write-Host ""
    Write-Host ("=" * 70) -ForegroundColor Cyan
    Write-Host "Testing: $versionOutput" -ForegroundColor Cyan
    Write-Host ("=" * 70) -ForegroundColor Cyan
    Write-Host "Path: $BlenderExe" -ForegroundColor White
    Write-Host ("=" * 70) -ForegroundColor Cyan
    Write-Host ""

    # Build command
    $blenderArgs = @(
        "--background",
        "--python", $testScript,
        "--"
    )

    if ($VerboseOutput) {
        $blenderArgs += "--verbose"
    }

    # Run tests
    Write-Host "Running tests..." -ForegroundColor Cyan
    Write-Host ""

    # Capture output and display it, but preserve exit code
    $output = & $BlenderExe @blenderArgs 2>&1
    $exitCode = $LASTEXITCODE
    
    # Display output
    $output | ForEach-Object { Write-Host $_ }

    return $exitCode
}

# Determine which Blender versions to test
$blendersToTest = @()

if ($AllVersions) {
    # Test all installed versions
    Write-Host ""
    $blendersToTest = Find-AllBlender
    if ($blendersToTest.Count -eq 0) {
        Write-Host "Error: No Blender installations found." -ForegroundColor Red
        Write-Host "Please install Blender or specify the path with -BlenderPath parameter." -ForegroundColor Yellow
        exit 1
    }
    Write-Host ""
} else {
    # Test single version
    if ($BlenderPath -eq "") {
        $BlenderPath = Find-Blender
        if ($null -eq $BlenderPath) {
            Write-Host "Error: Could not find Blender installation." -ForegroundColor Red
            Write-Host "Please specify the path with -BlenderPath parameter." -ForegroundColor Yellow
            Write-Host "Example: .\test\run_integration_tests.ps1 -BlenderPath 'C:\Path\To\blender.exe'" -ForegroundColor Yellow
            exit 1
        }
    } else {
        if (-not (Test-Path $BlenderPath)) {
            Write-Host "Error: Blender not found at: $BlenderPath" -ForegroundColor Red
            exit 1
        }
    }
    $blendersToTest = @($BlenderPath)
}

# Run tests for each Blender version
$totalTests = 0
$passedTests = 0
$failedTests = 0
$results = @()

foreach ($blender in $blendersToTest) {
    $exitCode = Invoke-TestsForBlender -BlenderExe $blender -VerboseOutput $Verbose
    
    $versionStr = & $blender --version 2>&1 | Select-Object -First 1
    
    if ($exitCode -eq 0) {
        Write-Host ""
        Write-Host "✅ PASSED: $versionStr" -ForegroundColor Green
        $passedTests++
        $results += @{Version = $versionStr; Status = "PASSED"; ExitCode = $exitCode}
    } else {
        Write-Host ""
        Write-Host "❌ FAILED: $versionStr (exit code: $exitCode)" -ForegroundColor Red
        $failedTests++
        $results += @{Version = $versionStr; Status = "FAILED"; ExitCode = $exitCode}
    }
    
    $totalTests++
    
    if ($totalTests -lt $blendersToTest.Count) {
        Write-Host ""
        Write-Host ("-" * 70) -ForegroundColor DarkGray
    }
}

# Print summary if testing multiple versions
if ($totalTests -gt 1) {
    Write-Host ""
    Write-Host ("=" * 70) -ForegroundColor Cyan
    Write-Host "TEST SUMMARY" -ForegroundColor Cyan
    Write-Host ("=" * 70) -ForegroundColor Cyan
    Write-Host "Total Blender versions tested: $totalTests" -ForegroundColor White
    Write-Host "Passed: $passedTests" -ForegroundColor Green
    Write-Host "Failed: $failedTests" -ForegroundColor $(if ($failedTests -gt 0) { "Red" } else { "Green" })
    Write-Host ""
    
    foreach ($result in $results) {
        $color = if ($result.Status -eq "PASSED") { "Green" } else { "Red" }
        $icon = if ($result.Status -eq "PASSED") { "✅" } else { "❌" }
        Write-Host "$icon $($result.Version)" -ForegroundColor $color
    }
    Write-Host ("=" * 70) -ForegroundColor Cyan
}

# Exit with appropriate code
if ($failedTests -gt 0) {
    exit 1
} else {
    exit 0
}
