# PowerShell script for building ThreePaneWindows documentation
# Usage: .\scripts\build-docs.ps1 [command] [options]

param(
    [Parameter(Position=0)]
    [ValidateSet("build", "serve", "check", "setup", "help")]
    [string]$Command = "help",

    [ValidateSet("html", "pdf", "epub")]
    [string]$Format = "html",

    [switch]$Clean,

    [int]$Port = 8000,

    [switch]$NoBrowser
)

# Colors for output
$Green = "Green"
$Red = "Red"
$Yellow = "Yellow"
$Cyan = "Cyan"

function Write-Status {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Test-Command {
    param([string]$CommandName)
    try {
        Get-Command $CommandName -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Test-PythonModule {
    param([string]$ModuleName)
    try {
        python -c "import $ModuleName" 2>$null
        return $?
    }
    catch {
        return $false
    }
}

function Test-Dependencies {
    Write-Status "🔍 Checking dependencies..." $Cyan

    # Check Python
    if (-not (Test-Command "python")) {
        Write-Status "❌ Python not found. Please install Python 3.8+" $Red
        return $false
    }

    # Check Sphinx
    if (Test-PythonModule "sphinx") {
        $sphinxVersion = python -c "import sphinx; print(sphinx.__version__)" 2>$null
        Write-Status "✅ Sphinx $sphinxVersion found" $Green
    }
    else {
        Write-Status "❌ Sphinx not found. Install with: pip install -r docs/requirements-docs.txt" $Red
        return $false
    }

    # Check ThreePaneWindows package
    if (Test-PythonModule "threepanewindows") {
        Write-Status "✅ ThreePaneWindows package found" $Green
    }
    else {
        Write-Status "⚠️ ThreePaneWindows package not found. Install with: pip install -e ." $Yellow
        Write-Status "   (This is needed for API documentation generation)" $Yellow
    }

    return $true
}

function New-SampleImages {
    Write-Status "📸 Creating sample images..." $Cyan

    $sampleDir = "sample_images"
    if ((Test-Path $sampleDir) -and (Get-ChildItem $sampleDir -ErrorAction SilentlyContinue)) {
        Write-Status "✅ Sample images already exist" $Green
        return $true
    }

    try {
        python -c @"
from threepanewindows.examples import create_example_screenshots
create_example_screenshots('$sampleDir')
print('Sample images created successfully')
"@
        Write-Status "✅ Sample images created" $Green
        return $true
    }
    catch {
        Write-Status "⚠️ Could not create sample images: $($_.Exception.Message)" $Yellow
        # Create minimal directory structure
        New-Item -ItemType Directory -Path $sampleDir -Force | Out-Null
        return $false
    }
}

function Build-Documentation {
    param([string]$Format, [bool]$Clean)

    if (-not (Test-Path "docs")) {
        Write-Status "❌ docs/ directory not found" $Red
        return $false
    }

    Push-Location "docs"

    try {
        if ($Clean) {
            Write-Status "🧹 Cleaning previous build..." $Cyan
            make clean
        }

        Write-Status "📚 Building $Format documentation..." $Cyan
        $result = make $Format

        if ($LASTEXITCODE -eq 0) {
            Write-Status "✅ $($Format.ToUpper()) documentation built successfully" $Green

            # Show output location
            if ($Format -eq "html") {
                $outputPath = Resolve-Path "docs\_build\html\index.html" -ErrorAction SilentlyContinue
                if ($outputPath) {
                    Write-Status "📄 Documentation available at: $outputPath" $Cyan
                }
            }
            elseif ($Format -eq "pdf") {
                $pdfFiles = Get-ChildItem "docs\_build\latex\*.pdf" -ErrorAction SilentlyContinue
                if ($pdfFiles) {
                    Write-Status "📄 PDF available at: $($pdfFiles[0].FullName)" $Cyan
                }
            }

            return $true
        }
        else {
            Write-Status "❌ $($Format.ToUpper()) build failed" $Red
            return $false
        }
    }
    finally {
        Pop-Location
    }
}

function Start-DocumentationServer {
    param([int]$Port, [bool]$OpenBrowser)

    if (-not (Test-Path "docs")) {
        Write-Status "❌ docs/ directory not found" $Red
        return $false
    }

    # Check if sphinx-autobuild is available
    try {
        sphinx-autobuild --version | Out-Null
    }
    catch {
        Write-Status "❌ sphinx-autobuild not found. Install with:" $Red
        Write-Status "   pip install sphinx-autobuild" $Red
        return $false
    }

    Write-Status "🚀 Starting documentation server on port $Port..." $Cyan
    Write-Status "📄 Documentation will be available at: http://localhost:$Port" $Cyan
    Write-Status "🔄 Auto-reload enabled - changes will be reflected automatically" $Cyan
    Write-Status "Press Ctrl+C to stop the server" $Yellow

    # Open browser if requested
    if ($OpenBrowser) {
        Start-Job -ScriptBlock {
            Start-Sleep -Seconds 2
            Start-Process "http://localhost:$using:Port"
        } | Out-Null
    }

    # Start the server
    try {
        sphinx-autobuild docs docs\_build\html --port $Port --host localhost --ignore "*.tmp" --ignore "*~"
    }
    catch {
        Write-Status "`n👋 Documentation server stopped" $Yellow
    }
}

function Invoke-DocumentationChecks {
    if (-not (Test-Path "docs")) {
        Write-Status "❌ docs/ directory not found" $Red
        return $false
    }

    Push-Location "docs"

    try {
        Write-Status "🔍 Running documentation checks..." $Cyan

        # Link check
        Write-Status "`n📎 Checking links..." $Cyan
        make linkcheck
        if ($LASTEXITCODE -eq 0) {
            Write-Status "✅ Link check passed" $Green
        }
        else {
            Write-Status "⚠️ Some links may be broken" $Yellow
        }

        # Doctest
        Write-Status "`n🧪 Running doctests..." $Cyan
        make doctest
        if ($LASTEXITCODE -eq 0) {
            Write-Status "✅ Doctests passed" $Green
        }
        else {
            Write-Status "⚠️ Some doctests failed" $Yellow
        }

        # Coverage
        Write-Status "`n📊 Checking documentation coverage..." $Cyan
        make coverage
        if ($LASTEXITCODE -eq 0) {
            Write-Status "✅ Coverage check completed" $Green
        }
        else {
            Write-Status "⚠️ Coverage check had issues" $Yellow
        }

        return $true
    }
    finally {
        Pop-Location
    }
}

function Initialize-DocumentationEnvironment {
    Write-Status "🔧 Setting up documentation environment..." $Cyan

    # Install dependencies
    Write-Status "📦 Installing documentation dependencies..." $Cyan
    python -m pip install -r docs/requirements-docs.txt

    # Install package in development mode
    Write-Status "📦 Installing GUI Image Studio in development mode..." $Cyan
    python -m pip install -e .

    # Create sample images
    New-SampleImages

    # Build documentation
    Build-Documentation -Format "html" -Clean $true

    Write-Status "✅ Documentation environment setup complete!" $Green
    Write-Status "💡 Try: .\scripts\build-docs.ps1 serve" $Cyan
}

function Show-Help {
    Write-Host @"
GUI Image Studio Documentation Builder

USAGE:
    .\scripts\build-docs.ps1 <command> [options]

COMMANDS:
    build       Build documentation
    serve       Serve documentation with live reload
    check       Run documentation quality checks
    setup       Setup documentation environment
    help        Show this help message

BUILD OPTIONS:
    -Format     Output format: html, pdf, epub (default: html)
    -Clean      Clean previous build before building

SERVE OPTIONS:
    -Port       Port to serve on (default: 8000)
    -NoBrowser  Don't open browser automatically

EXAMPLES:
    .\scripts\build-docs.ps1 build
    .\scripts\build-docs.ps1 build -Format pdf -Clean
    .\scripts\build-docs.ps1 serve -Port 8080
    .\scripts\build-docs.ps1 serve -NoBrowser
    .\scripts\build-docs.ps1 check
    .\scripts\build-docs.ps1 setup

"@ -ForegroundColor White
}

# Main execution
switch ($Command) {
    "build" {
        if (-not (Test-Dependencies)) {
            Write-Status "`n❌ Please install required dependencies first:" $Red
            Write-Status "   pip install -r docs/requirements-docs.txt" $Red
            Write-Status "   pip install -e ." $Red
            exit 1
        }

        New-SampleImages
        $success = Build-Documentation -Format $Format -Clean $Clean

        if ($success -and $Format -eq "html") {
            $outputPath = "docs\_build\html\index.html"
            if (Test-Path $outputPath) {
                $fullPath = Resolve-Path $outputPath
                Write-Status "`n🌐 Open in browser: file:///$($fullPath.Path.Replace('\', '/'))" $Cyan
            }
        }
    }

    "serve" {
        if (-not (Test-Dependencies)) {
            Write-Status "`n❌ Please install required dependencies first:" $Red
            Write-Status "   pip install -r docs/requirements-docs.txt" $Red
            Write-Status "   pip install -e ." $Red
            exit 1
        }

        New-SampleImages
        Start-DocumentationServer -Port $Port -OpenBrowser (-not $NoBrowser)
    }

    "check" {
        if (-not (Test-Dependencies)) {
            Write-Status "`n❌ Please install required dependencies first:" $Red
            Write-Status "   pip install -r docs/requirements-docs.txt" $Red
            Write-Status "   pip install -e ." $Red
            exit 1
        }

        New-SampleImages
        Invoke-DocumentationChecks
    }

    "setup" {
        Initialize-DocumentationEnvironment
    }

    "help" {
        Show-Help
    }

    default {
        Show-Help
    }
}
