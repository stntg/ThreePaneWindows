@echo off
REM Development Logging Starter for ThreePaneWindows
REM This batch file provides easy access to development logging tools

echo.
echo ========================================
echo ThreePaneWindows Development Logging
echo ========================================
echo.

:menu
echo Choose an option:
echo 1. Basic console logging (INFO level)
echo 2. Debug console logging (DEBUG level)
echo 3. Console + file logging (DEBUG level)
echo 4. Run basic example with logging
echo 5. Run interactive mode
echo 6. Run example with logging demo
echo 7. Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" (
    echo Starting basic console logging...
    python dev_logger.py --level INFO
    goto menu
)

if "%choice%"=="2" (
    echo Starting debug console logging...
    python dev_logger.py --level DEBUG --test-levels
    goto menu
)

if "%choice%"=="3" (
    echo Starting console + file logging...
    python dev_logger.py --level DEBUG --file logs/development.log --test-levels
    goto menu
)

if "%choice%"=="4" (
    echo Running basic example with logging...
    python dev_logger.py --example basic --level DEBUG
    goto menu
)

if "%choice%"=="5" (
    echo Starting interactive mode...
    python dev_logger.py --interactive --level DEBUG
    goto menu
)

if "%choice%"=="6" (
    echo Running example with logging demo...
    python example_with_logging.py
    goto menu
)

if "%choice%"=="7" (
    echo Goodbye!
    exit /b 0
)

echo Invalid choice. Please try again.
goto menu
