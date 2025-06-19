# GitHub Workflows Monitor PowerShell Script
# For ThreePaneWindows project

param(
    [Parameter(Position=0)]
    [string]$Command = "help",
    
    [Parameter(Position=1)]
    [string]$Workflow = "",
    
    [Parameter(Position=2)]
    [string]$RunId = ""
)

$RepoUrl = "https://github.com/stntg/ThreePaneWindows"
$ActionsUrl = "$RepoUrl/actions"

function Show-Help {
    Write-Host "GitHub Workflows Monitor" -ForegroundColor Cyan
    Write-Host "=========================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\monitor_workflows.ps1 <command> [args]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Green
    Write-Host "  help                - Show this help"
    Write-Host "  status              - Show git status and workflow links"
    Write-Host "  open [workflow]     - Open Actions page in browser"
    Write-Host "  git                 - Show git information"
    Write-Host "  test                - Run local tests"
    Write-Host "  trigger-ci          - Make a commit to trigger CI"
    Write-Host ""
    Write-Host "Workflows: ci, docs, release, test-release, test-pypi-upload" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\monitor_workflows.ps1 open ci"
    Write-Host "  .\monitor_workflows.ps1 status"
    Write-Host "  .\monitor_workflows.ps1 test"
}

function Show-Status {
    Write-Host "🔍 GitHub Workflows Status" -ForegroundColor Cyan
    Write-Host "===========================" -ForegroundColor Cyan
    Write-Host ""
    
    # Git information
    try {
        $branch = git branch --show-current
        $commit = git log --oneline -1
        $status = git status --porcelain
        
        Write-Host "📍 Current Branch: $branch" -ForegroundColor Green
        Write-Host "📝 Latest Commit: $commit" -ForegroundColor Green
        
        if ($status) {
            Write-Host "⚠️  Uncommitted changes detected" -ForegroundColor Yellow
        } else {
            Write-Host "✅ Working tree clean" -ForegroundColor Green
        }
        Write-Host ""
    }
    catch {
        Write-Host "❌ Error getting git information: $_" -ForegroundColor Red
    }
    
    # Workflow links
    Write-Host "🔗 Workflow Links:" -ForegroundColor Cyan
    Write-Host "  All Workflows: $ActionsUrl"
    Write-Host "  CI Workflow: $ActionsUrl/workflows/ci.yml"
    Write-Host "  Docs Workflow: $ActionsUrl/workflows/docs.yml"
    Write-Host "  Release Workflow: $ActionsUrl/workflows/release.yml"
    Write-Host "  Test Release: $ActionsUrl/workflows/test-release.yml"
    Write-Host "  Test PyPI Upload: $ActionsUrl/workflows/test-pypi-upload.yml"
    Write-Host ""
    
    # Check if GitHub CLI is available
    try {
        $ghVersion = gh --version 2>$null
        if ($ghVersion) {
            Write-Host "✅ GitHub CLI available - use 'gh run list' for detailed status" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "❓ GitHub CLI not found - install from https://cli.github.com/" -ForegroundColor Yellow
    }
}

function Open-ActionsPage {
    param([string]$WorkflowName)
    
    $workflows = @{
        "ci" = "ci.yml"
        "docs" = "docs.yml"
        "release" = "release.yml"
        "test-release" = "test-release.yml"
        "test-pypi-upload" = "test-pypi-upload.yml"
    }
    
    if ($WorkflowName -and $workflows.ContainsKey($WorkflowName)) {
        $url = "$ActionsUrl/workflows/$($workflows[$WorkflowName])"
    } else {
        $url = $ActionsUrl
    }
    
    Write-Host "🌐 Opening: $url" -ForegroundColor Cyan
    Start-Process $url
}

function Show-GitInfo {
    Write-Host "📍 Git Information" -ForegroundColor Cyan
    Write-Host "==================" -ForegroundColor Cyan
    Write-Host ""
    
    try {
        $branch = git branch --show-current
        $commit = git log --oneline -3
        $remote = git remote -v
        $status = git status --porcelain
        
        Write-Host "Current Branch: $branch" -ForegroundColor Green
        Write-Host ""
        Write-Host "Recent Commits:" -ForegroundColor Yellow
        $commit | ForEach-Object { Write-Host "  $_" }
        Write-Host ""
        Write-Host "Remote:" -ForegroundColor Yellow
        $remote | ForEach-Object { Write-Host "  $_" }
        Write-Host ""
        
        if ($status) {
            Write-Host "Uncommitted Changes:" -ForegroundColor Yellow
            $status | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
        } else {
            Write-Host "✅ Working tree clean" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "❌ Error getting git information: $_" -ForegroundColor Red
    }
}

function Run-LocalTests {
    Write-Host "🧪 Running Local Tests" -ForegroundColor Cyan
    Write-Host "======================" -ForegroundColor Cyan
    Write-Host ""
    
    $tests = @(
        @{Name="pytest"; Command="python"; Args=@("-m", "pytest", "tests/", "-v")},
        @{Name="flake8"; Command="flake8"; Args=@("threepanewindows/")},
        @{Name="mypy"; Command="mypy"; Args=@("threepanewindows/", "--ignore-missing-imports")},
        @{Name="bandit"; Command="bandit"; Args=@("-r", "threepanewindows/")}
    )
    
    $results = @{}
    
    foreach ($test in $tests) {
        Write-Host "Running $($test.Name)..." -ForegroundColor Yellow
        
        try {
            $process = Start-Process -FilePath $test.Command -ArgumentList $test.Args -Wait -PassThru -NoNewWindow -RedirectStandardOutput "temp_$($test.Name)_out.txt" -RedirectStandardError "temp_$($test.Name)_err.txt"
            
            if ($process.ExitCode -eq 0) {
                Write-Host "✅ $($test.Name) passed" -ForegroundColor Green
                $results[$test.Name] = "PASS"
            } else {
                Write-Host "❌ $($test.Name) failed" -ForegroundColor Red
                $results[$test.Name] = "FAIL"
                
                # Show error output
                if (Test-Path "temp_$($test.Name)_err.txt") {
                    $errorContent = Get-Content "temp_$($test.Name)_err.txt" -Raw
                    if ($errorContent.Trim()) {
                        Write-Host "Error output:" -ForegroundColor Red
                        Write-Host $errorContent -ForegroundColor Red
                    }
                }
            }
            
            # Clean up temp files
            Remove-Item "temp_$($test.Name)_*.txt" -ErrorAction SilentlyContinue
        }
        catch {
            Write-Host "❓ $($test.Name) - Command not found or error: $_" -ForegroundColor Yellow
            $results[$test.Name] = "ERROR"
        }
    }
    
    Write-Host ""
    Write-Host "📊 Test Results Summary:" -ForegroundColor Cyan
    foreach ($result in $results.GetEnumerator()) {
        $icon = switch ($result.Value) {
            "PASS" { "✅" }
            "FAIL" { "❌" }
            "ERROR" { "❓" }
        }
        Write-Host "$icon $($result.Key): $($result.Value)"
    }
}

function Trigger-CI {
    Write-Host "🚀 Triggering CI Workflow" -ForegroundColor Cyan
    Write-Host "=========================" -ForegroundColor Cyan
    Write-Host ""
    
    try {
        # Check if there are any changes to commit
        $status = git status --porcelain
        
        if (-not $status) {
            # No changes, create a small change to trigger CI
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            $triggerFile = "WORKFLOW_TRIGGER.md"
            
            "# Workflow Trigger`n`nLast triggered: $timestamp`n" | Out-File -FilePath $triggerFile -Encoding UTF8
            
            git add $triggerFile
            git commit -m "Trigger CI workflow - $timestamp"
            
            Write-Host "✅ Created trigger commit" -ForegroundColor Green
        } else {
            Write-Host "📝 Found uncommitted changes, committing them..." -ForegroundColor Yellow
            git add .
            git commit -m "Trigger CI workflow with pending changes"
            Write-Host "✅ Committed changes" -ForegroundColor Green
        }
        
        # Push to trigger CI
        $branch = git branch --show-current
        Write-Host "📤 Pushing to $branch..." -ForegroundColor Yellow
        git push origin $branch
        
        Write-Host "🎉 CI workflow triggered successfully!" -ForegroundColor Green
        Write-Host "🔗 Monitor at: $ActionsUrl" -ForegroundColor Cyan
        
        # Optionally open the Actions page
        $openPage = Read-Host "Open Actions page in browser? (y/n)"
        if ($openPage -eq "y" -or $openPage -eq "Y") {
            Start-Process $ActionsUrl
        }
    }
    catch {
        Write-Host "❌ Error triggering CI: $_" -ForegroundColor Red
    }
}

# Main script logic
switch ($Command.ToLower()) {
    "help" { 
        Show-Help 
    }
    "status" { 
        Show-Status 
    }
    "open" { 
        Open-ActionsPage -WorkflowName $Workflow 
    }
    "git" { 
        Show-GitInfo 
    }
    "test" { 
        Run-LocalTests 
    }
    "trigger-ci" { 
        Trigger-CI 
    }
    default { 
        Write-Host "❌ Unknown command: $Command" -ForegroundColor Red
        Write-Host ""
        Show-Help
    }
}