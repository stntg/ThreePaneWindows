# ThreePaneWindows Logging Guide

ThreePaneWindows includes a comprehensive logging system that remains completely
silent by default, following Python logging best practices for libraries. This
guide shows you how to enable and configure logging to help with debugging and
monitoring.

## Quick Start

### Enable Basic Console Logging

```python
import threepanewindows

# Enable console logging for the entire library
threepanewindows.enable_console_logging()

# Now create your windows - you'll see log messages
window = threepanewindows.EnhancedDockableThreePaneWindow(root)
```

### Disable Logging

```python
# Disable all logging (back to silent mode)
threepanewindows.disable_logging()
```

## Logging Levels

The library uses standard Python logging levels:

- **DEBUG**: Detailed diagnostic information
- **INFO**: General information about library operations
- **WARNING**: Something unexpected happened, but the library continues
- **ERROR**: A serious problem occurred
- **CRITICAL**: A very serious error occurred

### Set Logging Level

```python
import logging
import threepanewindows

# Enable console logging with specific level
threepanewindows.enable_console_logging(level=logging.DEBUG)  # Show everything
threepanewindows.enable_console_logging(
    level=logging.WARNING
)  # Only warnings and errors
```

## Advanced Configuration

### Custom Console Logging

```python
import logging
import threepanewindows

# Get the main ThreePaneWindows logger
logger = logging.getLogger('threepanewindows')

# Create custom handler with your preferred format
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

# Add handler to logger
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.propagate = True
```

### File Logging

```python
import threepanewindows

# Add file logging (includes detailed information)
threepanewindows.add_file_logging('threepanewindows.log', level=logging.DEBUG)

# You can combine console and file logging
threepanewindows.enable_console_logging(level=logging.INFO)  # Less verbose console
threepanewindows.add_file_logging('debug.log', level=logging.DEBUG)  # Detailed file
```

### Selective Module Logging

```python
import logging

# Enable logging only for specific modules
enhanced_logger = logging.getLogger('threepanewindows.enhanced_dockable')
themes_logger = logging.getLogger('threepanewindows.themes')

# Configure handlers for specific modules
handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

enhanced_logger.addHandler(handler)
enhanced_logger.setLevel(logging.DEBUG)
enhanced_logger.propagate = False

themes_logger.addHandler(handler)
themes_logger.setLevel(logging.INFO)
themes_logger.propagate = False
```

## Logger Hierarchy

ThreePaneWindows uses a hierarchical logger structure:

```text
threepanewindows                    # Main logger
├── threepanewindows.enhanced_dockable
├── threepanewindows.dockable
├── threepanewindows.fixed
├── threepanewindows.themes
├── threepanewindows.examples
├── threepanewindows.cli
└── threepanewindows.utils
    ├── threepanewindows.utils.windows
    ├── threepanewindows.utils.macos
    └── threepanewindows.utils.linux
```

You can configure logging for any level of this hierarchy.

## What Gets Logged

### INFO Level Messages

- Theme changes and applications
- Panel detaching/attaching operations
- Platform detection results
- Successful icon loading
- Demo and example operations

### WARNING Level Messages

- Failed icon loading (with fallback)
- Platform-specific feature failures
- Theme application issues (non-critical)
- TTK styling problems

### ERROR Level Messages

- Critical theme application failures
- Serious widget creation problems
- Platform integration errors

### DEBUG Level Messages

- Detailed function entry/exit information
- Internal state changes
- Platform compatibility checks
- Resource cleanup operations

## Example Usage Patterns

### Development and Debugging

```python
import logging
import threepanewindows

# Enable detailed logging during development
threepanewindows.enable_console_logging(level=logging.DEBUG)

# Your application code
root = tk.Tk()
window = threepanewindows.EnhancedDockableThreePaneWindow(root)
# ... you'll see detailed logs of what's happening
```

### Production with File Logging

```python
import logging
import threepanewindows

# Silent console, but log to file for troubleshooting
threepanewindows.add_file_logging('/var/log/myapp/threepanewindows.log',
                                  level=logging.WARNING)

# Your application runs silently but logs issues to file
```

### User Support and Diagnostics

```python
import logging
import threepanewindows

def enable_debug_mode():
    """Enable debug mode for user support."""
    threepanewindows.enable_console_logging(level=logging.DEBUG)
    threepanewindows.add_file_logging('debug_session.log', level=logging.DEBUG)

    # Now user can reproduce issue with full logging
```

## Integration with Application Logging

ThreePaneWindows logging integrates seamlessly with your application's logging:

```python
import logging
import threepanewindows

# Configure your application's root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('myapp.log'),
        logging.StreamHandler()
    ]
)

# ThreePaneWindows will automatically use your configuration
# No need to call enable_console_logging()

# Your app logger
app_logger = logging.getLogger('myapp')
app_logger.info("Application starting")

# Create ThreePaneWindows components - they'll log using your config
window = threepanewindows.EnhancedDockableThreePaneWindow(root)
```

## Performance Considerations

- **Silent by default**: No performance impact when logging is disabled
- **Lazy evaluation**: Log messages use `%s` formatting for efficiency
- **Minimal overhead**: Only active handlers process messages
- **No string concatenation**: Uses proper logging parameter substitution

## Best Practices

1. **Start silent**: Don't enable logging unless you need it
2. **Use appropriate levels**: DEBUG for development, WARNING+ for production
3. **Combine console and file**: Console for immediate feedback, file for history
4. **Module-specific logging**: Enable only the modules you're debugging
5. **Structured logging**: Use consistent formatting for easier parsing

## Troubleshooting

### No Log Messages Appearing

```python
import logging

# Check if any handlers are configured
logger = logging.getLogger('threepanewindows')
print(f"Handlers: {logger.handlers}")
print(f"Level: {logger.level}")
print(f"Propagate: {logger.propagate}")

# Enable basic logging
threepanewindows.enable_console_logging(level=logging.DEBUG)
```

### Too Many Log Messages

```python
# Reduce logging level
threepanewindows.enable_console_logging(level=logging.WARNING)

# Or disable specific modules
logging.getLogger('threepanewindows.enhanced_dockable').setLevel(logging.ERROR)
```

### Log Messages in Wrong Format

```python
# Clear existing handlers and reconfigure
logger = logging.getLogger('threepanewindows')
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Add your custom handler
threepanewindows.enable_console_logging(level=logging.INFO)
```

## Complete Example

Here's a complete example showing various logging configurations:

```python
import tkinter as tk
import logging
import threepanewindows

def main():
    # Method 1: Simple console logging
    threepanewindows.enable_console_logging(level=logging.INFO)

    # Method 2: Add file logging
    threepanewindows.add_file_logging('app.log', level=logging.DEBUG)

    # Method 3: Custom configuration
    logger = logging.getLogger('threepanewindows.themes')
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('THEME: %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create your application
    root = tk.Tk()
    root.title("Logging Example")

    window = threepanewindows.EnhancedDockableThreePaneWindow(
        root,
        left_config=threepanewindows.PaneConfig(title="Left", width=200),
        center_config=threepanewindows.PaneConfig(title="Center"),
        right_config=threepanewindows.PaneConfig(title="Right", width=200),
    )
    window.pack(fill=tk.BOTH, expand=True)

    # Add content
    tk.Label(window.left_pane, text="Left Panel").pack(pady=20)
    tk.Label(window.center_pane, text="Center Panel").pack(pady=20)
    tk.Label(window.right_pane, text="Right Panel").pack(pady=20)

    # Test logging by switching themes
    window.switch_theme("dark")
    window.switch_theme("blue")

    root.mainloop()

if __name__ == "__main__":
    main()
```

This logging system provides complete control over ThreePaneWindows diagnostic
output while maintaining the library's silent-by-default behavior.
