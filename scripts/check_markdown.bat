@echo off
REM Markdown File Checker - Windows Batch Script
REM This script runs the markdown checker with common options

setlocal enabledelayedexpansion

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..

echo.
echo ========================================
echo   ThreePaneWindows Markdown Checker
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and try again.
    pause
    exit /b 1
)

REM Change to project directory
cd /d "%PROJECT_DIR%"

REM Parse command line arguments
set CHECK_ONLY=0
set VERBOSE=0
set FIX_MODE=0
set QUICK_MODE=0

:parse_args
if "%1"=="" goto end_parse
if /i "%1"=="--check-only" set CHECK_ONLY=1
if /i "%1"=="--verbose" set VERBOSE=1
if /i "%1"=="--fix" set FIX_MODE=1
if /i "%1"=="--quick" set QUICK_MODE=1
if /i "%1"=="--help" goto show_help
if /i "%1"=="-h" goto show_help
shift
goto parse_args
:end_parse

REM Show help if requested
if "%1"=="--help" goto show_help
if "%1"=="-h" goto show_help

REM Build command based on options
if %QUICK_MODE%==1 (
    set COMMAND=python scripts/quick_md_check.py
    if %FIX_MODE%==1 set COMMAND=!COMMAND! --fix
    if %VERBOSE%==1 set COMMAND=!COMMAND! --verbose
) else (
    set COMMAND=python scripts/check_fix_markdown.py
    if %CHECK_ONLY%==1 set COMMAND=!COMMAND! --check-only
    if %VERBOSE%==1 set COMMAND=!COMMAND! --verbose
)

echo Running: !COMMAND!
echo.

REM Run the command
!COMMAND!
set EXIT_CODE=!errorlevel!

echo.
if !EXIT_CODE!==0 (
    echo ✅ Markdown check completed successfully!
) else (
    echo ⚠️  Markdown check completed with issues.
)

echo.
echo Press any key to exit...
pause >nul
exit /b !EXIT_CODE!

:show_help
echo.
echo Usage: check_markdown.bat [options]
echo.
echo Options:
echo   --check-only    Only check files, don't fix them
echo   --verbose       Show detailed output
echo   --fix           Fix issues automatically (quick mode only)
echo   --quick         Use quick checker instead of full checker
echo   --help, -h      Show this help message
echo.
echo Examples:
echo   check_markdown.bat                    # Full check and fix
echo   check_markdown.bat --check-only       # Check only, no fixes
echo   check_markdown.bat --quick --fix      # Quick check and fix
echo   check_markdown.bat --verbose          # Detailed output
echo.
pause
exit /b 0