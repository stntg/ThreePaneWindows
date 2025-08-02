# Development Logging System - Summary

This document provides a quick overview of the development logging system created
for ThreePaneWindows.

## Files Created

### Core Development Tools

- **`dev_logger.py`** - Main development logger driver with CLI interface
- **`setup_dev_logging.py`** - Quick import-and-go logging setup
- **`example_with_logging.py`** - Complete example demonstrating logging usage
- **`start_dev_logging.bat`** - Windows batch file for easy access

### Documentation & Examples

- **`DEVELOPMENT_LOGGING.md`** - Comprehensive development logging guide
- **`dev_files/logging_examples.py`** - Various logging scenario examples
- **`DEV_LOGGING_SUMMARY.md`** - This summary file

### Enhanced Library Features

- **Updated `threepanewindows/logging_config.py`** - Added UTF-8 support for Windows
- **Updated `README.md`** - Added development logging section

## Quick Start Options

### Option 1: Automatic Setup (Easiest)

```python
import setup_dev_logging  # Automatically enables logging
# Your development code here
```

### Option 2: Command Line Driver

```bash
python dev_logger.py --level DEBUG --file logs/dev.log
```

### Option 3: Windows Batch File

```bash
start_dev_logging.bat
```

### Option 4: Manual Setup

```python
from threepanewindows.logging_config import enable_console_logging, DEBUG
enable_console_logging(DEBUG)
```

## Available Commands

```bash
# Basic usage
python dev_logger.py                          # INFO level console
python dev_logger.py --level DEBUG            # DEBUG level console
python dev_logger.py --file logs/dev.log      # Console + file logging

# Examples and testing
python dev_logger.py --example basic          # Run basic example
python dev_logger.py --interactive            # Interactive mode
python dev_logger.py --test-levels            # Test all log levels

# Complete example
python example_with_logging.py                # Full logging demo
```

## Logging Levels

| Level | Console | File | Use Case |
|-------|---------|------|----------|
| DEBUG | Optional | ✅ | Detailed debugging |
| INFO | ✅ | ✅ | General development |
| WARNING | ✅ | ✅ | Potential issues |
| ERROR | ✅ | ✅ | Error conditions |

## Key Features

### What Works

- **UTF-8 Support** - Handles Unicode characters properly on Windows
- **Automatic File Creation** - Creates `logs/` directory and timestamped files
- **Multiple Setup Methods** - Choose what works best for your workflow
- **Interactive Mode** - Real-time testing with REPL
- **Example Integration** - See logging in action with GUI examples
- **Cross-Platform** - Works on Windows, macOS, and Linux

### 🔧 Development Benefits

- **Silent by Default** - Library doesn't spam logs unless you enable them
- **Component-Specific** - Log only what you need to debug
- **File + Console** - Dual output for immediate feedback and later analysis
- **Error Tracking** - Full stack traces with `exc_info=True`
- **Performance Monitoring** - Time operations and track performance

## Common Usage Patterns

### Debugging a Specific Issue

```python
import setup_dev_logging
from threepanewindows.logging_config import get_logger

logger = get_logger(__name__)
logger.debug("Starting problematic operation")
# Your code here
logger.debug("Operation completed")
```

### GUI Development

```python
import setup_dev_logging  # Auto-enable logging
import tkinter as tk
from threepanewindows import FixedThreePaneWindow

logger = get_logger(__name__)
root = tk.Tk()
logger.info("Creating window")
window = FixedThreePaneWindow(root)
logger.debug("Window created successfully")
```

### Error Handling

```python
try:
    # Potentially problematic code
    window = SomeWindow(root)
except Exception as e:
    logger.error(f"Failed: {e}", exc_info=True)
```

## Benefits for Development

1. **Faster Debugging** - See exactly what's happening inside components
2. **Better Error Tracking** - Full stack traces and context
3. **Performance Analysis** - Time operations and identify bottlenecks
4. **Component Understanding** - Learn how ThreePaneWindows works internally
5. **Issue Reporting** - Detailed logs help with bug reports

## Next Steps

1. **Try the Quick Start** - Run `python dev_logger.py --interactive`
2. **Run the Example** - Execute `python example_with_logging.py`
3. **Read the Guide** - Check out `DEVELOPMENT_LOGGING.md` for details
4. **Integrate in Your Code** - Add `import setup_dev_logging` to your projects

---

Happy developing! The logging system will help you understand and debug
ThreePaneWindows components effectively.
