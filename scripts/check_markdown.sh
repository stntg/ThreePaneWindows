#!/bin/bash
# Markdown File Checker - Shell Script
# This script runs the markdown checker with common options

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo
echo "========================================"
echo "  ThreePaneWindows Markdown Checker"
echo "========================================"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python is not installed or not in PATH${NC}"
    echo "Please install Python and try again."
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Change to project directory
cd "$PROJECT_DIR"

# Parse command line arguments
CHECK_ONLY=false
VERBOSE=false
FIX_MODE=false
QUICK_MODE=false
SHOW_HELP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --check-only)
            CHECK_ONLY=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --fix)
            FIX_MODE=true
            shift
            ;;
        --quick)
            QUICK_MODE=true
            shift
            ;;
        --help|-h)
            SHOW_HELP=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            SHOW_HELP=true
            shift
            ;;
    esac
done

# Show help if requested
if [ "$SHOW_HELP" = true ]; then
    echo
    echo "Usage: $0 [options]"
    echo
    echo "Options:"
    echo "  --check-only    Only check files, don't fix them"
    echo "  --verbose, -v   Show detailed output"
    echo "  --fix           Fix issues automatically (quick mode only)"
    echo "  --quick         Use quick checker instead of full checker"
    echo "  --help, -h      Show this help message"
    echo
    echo "Examples:"
    echo "  $0                    # Full check and fix"
    echo "  $0 --check-only       # Check only, no fixes"
    echo "  $0 --quick --fix      # Quick check and fix"
    echo "  $0 --verbose          # Detailed output"
    echo
    exit 0
fi

# Build command based on options
if [ "$QUICK_MODE" = true ]; then
    COMMAND="$PYTHON_CMD scripts/quick_md_check.py"
    if [ "$FIX_MODE" = true ]; then
        COMMAND="$COMMAND --fix"
    fi
    if [ "$VERBOSE" = true ]; then
        COMMAND="$COMMAND --verbose"
    fi
else
    COMMAND="$PYTHON_CMD scripts/check_fix_markdown.py"
    if [ "$CHECK_ONLY" = true ]; then
        COMMAND="$COMMAND --check-only"
    fi
    if [ "$VERBOSE" = true ]; then
        COMMAND="$COMMAND --verbose"
    fi
fi

echo -e "${BLUE}Running: $COMMAND${NC}"
echo

# Run the command
if $COMMAND; then
    EXIT_CODE=0
    echo
    echo -e "${GREEN}✅ Markdown check completed successfully!${NC}"
else
    EXIT_CODE=$?
    echo
    echo -e "${YELLOW}⚠️  Markdown check completed with issues.${NC}"
fi

exit $EXIT_CODE