# PowerShell script for running coverage on ThreePaneWindows
# Usage: .\scripts\run_coverage.ps1 [options]

param(
    [switch]$Basic,
    [switch]$Full,
    [switch]$Branch,
    [switch]$NoGui,
    [switch]$Open,
    [switch]$Clean,
    [switch]$Summary,
    [switch]$Help
)

function Show-Help {
    Write-Host "ThreePaneWindows Coverage Runner" -ForegroundColor Green
    Write-Host "=================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage: .\scripts\run_coverage.ps1 [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Cyan
    Write-Host "  -Basic     Run basic coverage with terminal report"
    Write-Host "  -Full      Run full coverage with all report formats"
    Write-Host "  -Branch    Run coverage with branch analysis"
    Write-Host "  -NoGui     Run coverage excluding GUI components"
    Write-Host "  -Open      Open HTML coverage report in browser"
    Write-Host "  -Clean     Clean coverage files and reports"
    Write-Host "  -Summary   Show summary of coverage files"
    Write-Host "  -Help      Show this help message"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Magenta
    Write-Host "  .\scripts\run_coverage.ps1 -Basic"
    Write-Host "  .\scripts\run_coverage.ps1 -Full"
    Write-Host "  .\scripts\run_coverage.ps1 -NoGui"
    Write-Host "  .\scripts\run_coverage.ps1 -Open"
}

function Run-Command {
    param(
        [string[]]$Command,
        [string]$Description = ""
    )

    if ($Description) {
        Write-Host "`n[RUNNING] $Description" -ForegroundColor Blue
    }

    $cmdString = $Command -join " "
    Write-Host "Running: $cmdString" -ForegroundColor Gray

    try {
        & $Command[0] $Command[1..($Command.Length-1)]
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[SUCCESS] $($Description -or 'Command') completed successfully" -ForegroundColor Green
            return $true
        } else {
            Write-Host "[ERROR] Command failed with exit code $LASTEXITCODE" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "[ERROR] Command failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Run-BasicCoverage {
    $cmd = @("python", "-m", "pytest", "--cov=threepanewindows", "--cov-report=term-missing", "--cov-config=.coveragerc")
    Run-Command -Command $cmd -Description "Running basic coverage"
}

function Run-FullCoverage {
    $cmd = @("python", "-m", "pytest", "--cov=threepanewindows", "--cov-report=term-missing", "--cov-report=html", "--cov-report=xml", "--cov-report=json", "--cov-config=.coveragerc")
    Run-Command -Command $cmd -Description "Running full coverage with all reports"
}

function Run-BranchCoverage {
    $cmd = @("python", "-m", "pytest", "--cov=threepanewindows", "--cov-branch", "--cov-report=term-missing", "--cov-report=html", "--cov-config=.coveragerc")
    Run-Command -Command $cmd -Description "Running coverage with branch analysis"
}

function Run-NoGuiCoverage {
    $cmd = @("python", "-m", "pytest", "--cov=threepanewindows", "--cov-report=term-missing", "--cov-report=html", "--ignore=tests/test_gui_components.py", "--cov-config=.coveragerc")
    Run-Command -Command $cmd -Description "Running coverage (excluding GUI components)"
}

function Open-HtmlReport {
    $htmlFile = "htmlcov\index.html"
    if (Test-Path $htmlFile) {
        Write-Host "[OPENING] Coverage report: $(Resolve-Path $htmlFile)" -ForegroundColor Green
        Start-Process $htmlFile
    } else {
        Write-Host "[ERROR] HTML coverage report not found. Run coverage first." -ForegroundColor Red
    }
}

function Clean-Coverage {
    Write-Host "[CLEANING] Cleaning coverage files..." -ForegroundColor Yellow

    $filesToClean = @(
        ".coverage",
        "coverage.xml",
        "coverage.json",
        "htmlcov"
    )

    foreach ($file in $filesToClean) {
        if (Test-Path $file) {
            try {
                Remove-Item $file -Recurse -Force
                Write-Host "[REMOVED] $file" -ForegroundColor Green
            } catch {
                Write-Host "[WARNING] Could not remove $file`: $($_.Exception.Message)" -ForegroundColor Yellow
            }
        }
    }

    # Clean .coverage.* files
    Get-ChildItem -Path "." -Name ".coverage.*" | ForEach-Object {
        try {
            Remove-Item $_ -Force
            Write-Host "[REMOVED] $_" -ForegroundColor Green
        } catch {
            Write-Host "[WARNING] Could not remove $_`: $($_.Exception.Message)" -ForegroundColor Yellow
        }
    }
}

function Show-CoverageSummary {
    Write-Host "`n[SUMMARY] Coverage Files Summary:" -ForegroundColor Cyan

    $filesToCheck = @(
        @(".coverage", "Coverage data file"),
        @("coverage.xml", "XML coverage report"),
        @("coverage.json", "JSON coverage report"),
        @("htmlcov\index.html", "HTML coverage report")
    )

    foreach ($fileInfo in $filesToCheck) {
        $filePath = $fileInfo[0]
        $description = $fileInfo[1]

        if (Test-Path $filePath) {
            $size = if (Test-Path $filePath -PathType Leaf) { (Get-Item $filePath).Length } else { "N/A" }
            Write-Host "  [OK] $description`: $filePath ($size bytes)" -ForegroundColor Green
        } else {
            Write-Host "  [X] $description`: $filePath (not found)" -ForegroundColor Red
        }
    }
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

# Change to project root directory
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

if ($Clean) {
    Clean-Coverage
} elseif ($Open) {
    Open-HtmlReport
} elseif ($Summary) {
    Show-CoverageSummary
} elseif ($Basic) {
    Run-BasicCoverage
} elseif ($Full) {
    Run-FullCoverage
} elseif ($Branch) {
    Run-BranchCoverage
} elseif ($NoGui) {
    Run-NoGuiCoverage
} else {
    # Default: run basic coverage
    Write-Host "No specific option provided. Running basic coverage..." -ForegroundColor Yellow
    Run-BasicCoverage
}

if (-not ($Clean -or $Open -or $Summary)) {
    Write-Host "`n$('='*60)" -ForegroundColor Gray
    Show-CoverageSummary
    Write-Host "`nTip: Use -Open to view the HTML report in your browser" -ForegroundColor Cyan
}
