# Development Logging for ThreePaneWindows

This document explains how to use the comprehensive logging system while developing the ThreePaneWindows library.

## Quick Start

### Option 1: Automatic Setup (Easiest)
```python
import setup_dev_logging  # Automatically enables logging
import threepanewindows

# Your development code here
# All ThreePaneWindows operations will be logged
```

### Option 2: Development Logger Driver
```bash
# Basic console logging
python dev_logger.py

# Debug level with file logging
python dev_logger.py --level DEBUG --file logs/development.log

# Run an example with logging
python dev_logger.py --example basic --level DEBUG

# Interactive mode for testing
python dev_logger.py --interactive
```

### Option 3: Manual Setup
```python
from threepanewindows.logging_config import enable_console_logging, DEBUG
enable_console_logging(DEBUG)

# Now all ThreePaneWindows operations will be logged
```

## Available Tools

### 1. `dev_logger.py` - Development Logger Driver
The main development tool with multiple features:

```bash
# Show help
python dev_logger.py --help

# Basic usage
python dev_logger.py                           # INFO level console logging
python dev_logger.py --level DEBUG            # DEBUG level console logging
python dev_logger.py --file logs/dev.log      # Console + file logging
python dev_logger.py --example basic          # Run example with logging
python dev_logger.py --interactive            # Interactive testing mode
python dev_logger.py --test-levels            # Test all logging levels
```

### 2. `setup_dev_logging.py` - Quick Setup
Simple import-and-go logging setup:

```python
# Automatic setup (just import)
import setup_dev_logging

# Custom setup
import setup_dev_logging
setup_dev_logging.setup_custom_logging(
    console_level="DEBUG",
    file="logs/my_debug.log",
    file_level="DEBUG"
)
```

### 3. `dev_files/logging_examples.py` - Examples
Comprehensive examples of different logging scenarios:

```bash
python dev_files/logging_examples.py
```

## Logging Levels

| Level | When to Use | Console | File |
|-------|-------------|---------|------|
| `DEBUG` | Detailed debugging info | Optional | Recommended |
| `INFO` | General information | Recommended | Yes |
| `WARNING` | Potential issues | Yes | Yes |
| `ERROR` | Error conditions | Yes | Yes |
| `CRITICAL` | Critical failures | Yes | Yes |

## Common Development Scenarios

### Debugging a Specific Component
```python
from threepanewindows.logging_config import enable_console_logging, get_logger, DEBUG

# Enable debug logging
enable_console_logging(DEBUG)

# Get component-specific logger
logger = get_logger("threepanewindows.dockable")

# Your debugging code
logger.debug("Starting dockable window creation")
# ... your code ...
logger.debug("Dockable window created successfully")
```

### Logging GUI Operations
```python
import setup_dev_logging  # Auto-enable logging
import tkinter as tk
from threepanewindows import FixedThreePaneWindow
from threepanewindows.logging_config import get_logger

logger = get_logger(__name__)

root = tk.Tk()
logger.info("Creating main window")

window = FixedThreePaneWindow(root)
logger.debug("ThreePaneWindow created")

window.pack(fill=tk.BOTH, expand=True)
logger.debug("Window packed and ready")

root.mainloop()
```

### Error Tracking
```python
from threepanewindows.logging_config import enable_console_logging, get_logger, DEBUG

enable_console_logging(DEBUG)
logger = get_logger(__name__)

try:
    # Your potentially problematic code
    window = SomeThreePaneWindow(root)
except Exception as e:
    logger.error(f"Failed to create window: {e}", exc_info=True)
    # exc_info=True includes the full traceback
```

### File Logging for Long Sessions
```python
from threepanewindows.logging_config import enable_console_logging, add_file_logging, INFO, DEBUG

# Console for immediate feedback
enable_console_logging(INFO)

# File for detailed analysis
add_file_logging("logs/development_session.log", DEBUG)

# Now all operations are logged to both console and file
```

## Log File Locations

By default, log files are created in:
- `logs/` directory (created automatically)
- Timestamped files: `logs/dev_YYYYMMDD_HHMMSS.log`
- Custom files: wherever you specify

## Interactive Development

Use the interactive mode for real-time testing:

```bash
python dev_logger.py --interactive
```

This gives you a Python REPL with:
- Logging pre-enabled
- Common imports available
- Helper functions for creating test windows
- Real-time log output

Example interactive session:
```python
>>> logger.info("Starting interactive test")
>>> root, window = create_test_window("dockable")
>>> root.mainloop()  # Test your window
>>> logger.debug("Test completed")
```

## Integration with IDEs

### VS Code
Add to your launch.json:
```json
{
    "name": "ThreePaneWindows Debug",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/dev_logger.py",
    "args": ["--level", "DEBUG", "--file", "logs/vscode_debug.log"],
    "console": "integratedTerminal"
}
```

### PyCharm
1. Create a new run configuration
2. Script path: `dev_logger.py`
3. Parameters: `--level DEBUG --interactive`
4. Working directory: project root

## Tips for Effective Development Logging

1. **Start with INFO level** for general development
2. **Use DEBUG level** when troubleshooting specific issues
3. **Enable file logging** for complex debugging sessions
4. **Use component-specific loggers** to filter messages
5. **Include context** in your log messages
6. **Use exc_info=True** for exception logging

## Example Development Workflow

```python
# 1. Enable logging at start of development session
import setup_dev_logging

# 2. Get a logger for your module
from threepanewindows.logging_config import get_logger
logger = get_logger(__name__)

# 3. Add logging to your development code
logger.info("Starting development test")

# 4. Create and test components
import tkinter as tk
from threepanewindows import EnhancedDockableThreePaneWindow

root = tk.Tk()
logger.debug("Creating enhanced window")

window = EnhancedDockableThreePaneWindow(root)
logger.debug("Window created, configuring...")

# 5. Log important operations
window.pack(fill=tk.BOTH, expand=True)
logger.info("Window ready for testing")

# 6. Run and observe logs
root.mainloop()
logger.info("Development test completed")
```

## Troubleshooting

### No Log Output
- Check that logging is enabled: `enable_console_logging(DEBUG)`
- Verify logger name: use `get_logger(__name__)` or `get_logger("threepanewindows.yourmodule")`

### Too Much Output
- Increase log level: `enable_console_logging(WARNING)`
- Use component-specific loggers instead of root logger

### File Logging Not Working
- Check file path permissions
- Ensure directory exists (or use `Path.mkdir(parents=True, exist_ok=True)`)
- Verify file isn't locked by another process

### Performance Impact
- Logging has minimal impact at INFO level and above
- DEBUG level can be verbose - use only when needed
- File logging is generally faster than console logging

## Advanced Usage

### Custom Log Formatting
```python
import logging
from threepanewindows.logging_config import get_logger

# Create custom formatter
formatter = logging.Formatter(
    '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s'
)

# Apply to console handler
logger = logging.getLogger('threepanewindows')
for handler in logger.handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setFormatter(formatter)
```

### Conditional Logging
```python
from threepanewindows.logging_config import get_logger
import os

logger = get_logger(__name__)

# Only log in development environment
if os.getenv('DEVELOPMENT', 'false').lower() == 'true':
    logger.debug("Development mode - detailed logging enabled")
```

### Performance Logging
```python
import time
from threepanewindows.logging_config import get_logger

logger = get_logger(__name__)

start_time = time.time()
# Your operation here
elapsed = time.time() - start_time
logger.info(f"Operation completed in {elapsed:.3f} seconds")
```

---

Happy developing! 🚀 The logging system will help you track down issues and understand how ThreePaneWindows components work internally.
