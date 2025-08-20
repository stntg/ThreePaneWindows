# Custom Titlebar Integration Guide

This guide explains how to use the new cross-platform custom titlebar system in ThreePaneWindows, which replicates CustomTkinter's functionality without requiring the library.

## Overview

The custom titlebar system provides:

- **Cross-platform compatibility**: Works on Windows, macOS, and Linux
- **Platform-specific optimizations**: Uses native APIs where possible
- **Seamless integration**: Automatically integrates with all ThreePaneWindows modules
- **Theme synchronization**: Automatically updates with theme changes
- **No external dependencies**: Pure Python implementation using only standard libraries

## How It Works

### Platform-Specific Implementations

#### Windows
- Uses Windows DWM API (`ctypes.windll.dwmapi`) to set native titlebar colors
- Supports both light and dark themes
- Maintains native window controls (minimize, maximize, close)
- Provides the best user experience with native OS integration

#### macOS
- Uses system commands to enable dark titlebar support globally
- Replicates CustomTkinter's approach with `NSRequiresAquaSystemAppearance`
- Maintains native macOS window controls and behavior
- Automatically detects system dark mode

#### Linux
- Provides full custom titlebar with window controls
- Removes native window decorations using `overrideredirect(True)`
- Implements custom minimize, maximize, and close buttons
- Supports window dragging and resizing
- Detects desktop environment (GNOME, KDE, XFCE, WSL) for optimizations

## Automatic Integration

The custom titlebar system is automatically integrated into all ThreePaneWindows modules:

### Enhanced Dockable Three-Pane Window
```python
from threepanewindows.enhanced_dockable import EnhancedDockableThreePaneWindow

# Custom titlebar is automatically applied when using a top-level window
root = tk.Tk()
window = EnhancedDockableThreePaneWindow(
    root,
    theme_name="dark"  # Titlebar automatically matches theme
)
```

### Dockable Three-Pane Window
```python
from threepanewindows.dockable import DockableThreePaneWindow

root = tk.Tk()
window = DockableThreePaneWindow(root)
# Custom titlebar automatically applied
```

### Flexible Layout
```python
from threepanewindows.flexible import EnhancedFlexibleLayout

root = tk.Tk()
layout = EnhancedFlexibleLayout(root, container_config)
# Custom titlebar automatically applied
```

## Manual Usage

You can also use the custom titlebar system directly:

### Basic Usage
```python
import tkinter as tk
from threepanewindows.utils import apply_custom_titlebar_direct, get_titlebar_theme

root = tk.Tk()
root.title("My Application")

# Apply custom titlebar with default theme
theme = get_titlebar_theme(is_dark=False)
titlebar = apply_custom_titlebar_direct(root, theme, "My Application")

# Your application content here
content = tk.Frame(root)
content.pack(fill='both', expand=True)

root.mainloop()
```

### Advanced Usage with Custom Theme
```python
import tkinter as tk
from threepanewindows.utils.custom_titlebar import CustomTitleBarManager

root = tk.Tk()

# Create custom theme
custom_theme = {
    'bg': '#2d2d30',           # Titlebar background
    'fg': '#ffffff',           # Title text color
    'btn_bg': '#3e3e42',       # Button background
    'btn_fg': '#ffffff',       # Button text color
    'btn_active_bg': '#007acc', # Button hover color
    'content_bg': '#1e1e1e',   # Window content background
    'font': ('Segoe UI', 10),  # Font
    'height': 30               # Titlebar height
}

# Apply custom titlebar
titlebar = CustomTitleBarManager.create_titlebar(
    root,
    custom_theme,
    "My Custom App",
    force_custom=False  # Use platform-appropriate implementation
)

root.mainloop()
```

## Theme Integration

The custom titlebar automatically synchronizes with ThreePaneWindows themes:

### Theme Switching
```python
from threepanewindows.enhanced_dockable import EnhancedDockableThreePaneWindow

root = tk.Tk()
window = EnhancedDockableThreePaneWindow(root, theme_name="light")

# Switch theme - titlebar automatically updates
window.set_theme("dark")
```

### Custom Theme Colors
The titlebar uses these theme properties:
- `primary_bg` → Titlebar background
- `primary_fg` → Title text color
- `button_bg` → Button background
- `button_fg` → Button text color
- `button_hover_bg` → Button hover color
- `secondary_bg` → Content background

## Platform-Specific Features

### Windows Features
- Native DWM integration
- Automatic dark/light mode detection
- Seamless OS integration
- Native window controls

### macOS Features
- System-wide dark mode support
- Native window controls
- Automatic system theme detection
- Proper macOS styling

### Linux Features
- Full custom window controls
- Desktop environment detection
- WSL support
- Window dragging and resizing
- Custom button styling

## Configuration Options

### Force Custom Titlebar
```python
# Force custom titlebar on all platforms (useful for consistent appearance)
titlebar = apply_custom_titlebar_direct(
    root,
    theme,
    "My App",
    force_custom=True
)
```

### Disable Custom Titlebar
```python
# The system respects platform capabilities
# On Windows/macOS: Uses native titlebar with color theming
# On Linux: Uses full custom titlebar

# To completely disable, don't call the titlebar functions
# or set environment variable
import os
os.environ['THREEPANE_DISABLE_CUSTOM_TITLEBAR'] = '1'
```

## Troubleshooting

### Common Issues

#### Windows: Titlebar not changing color
- Ensure Windows 10 version 2004 or later
- Check that DWM is enabled
- Verify the application has proper window handle

#### macOS: Dark mode not working
- Check Python version (3.10+ recommended)
- Verify Tcl/Tk version (8.6.9+)
- Ensure system permissions for appearance changes

#### Linux: Window controls not working
- Verify window manager compatibility
- Check if compositor is running for transparency
- Test with different desktop environments

### Debug Information
```python
from threepanewindows.utils import platform_handler

print(f"Platform: {platform_handler.__class__.__name__}")
print(f"Dark mode: {platform_handler.is_dark_mode()}")
print(f"Accent color: {platform_handler.get_system_accent_color()}")
```

## Migration from CustomTkinter

If you're migrating from CustomTkinter, the transition is seamless:

### Before (CustomTkinter)
```python
import customtkinter as ctk

ctk.set_appearance_mode("dark")
root = ctk.CTk()
```

### After (ThreePaneWindows)
```python
import tkinter as tk
from threepanewindows.enhanced_dockable import EnhancedDockableThreePaneWindow

root = tk.Tk()
window = EnhancedDockableThreePaneWindow(root, theme_name="dark")
# Custom titlebar automatically applied with dark theme
```

## Performance Considerations

- **Windows**: Minimal overhead, uses native APIs
- **macOS**: One-time system setting, no runtime overhead
- **Linux**: Slight overhead for custom controls, optimized for performance

## Security Notes

- Uses only standard library functions
- No external process execution (except for macOS system commands)
- All Windows API calls are through standard ctypes
- Linux implementation uses secure subprocess calls with timeouts

## Examples

See the following example files:
- `examples/custom_titlebar_demo.py` - Comprehensive demo
- `test_custom_titlebar_integration.py` - Integration tests
- `examples/` directory - Various usage examples

## API Reference

### CustomTitleBarManager
- `create_titlebar(window, theme, title, force_custom)` - Create titlebar
- `get_default_theme(is_dark)` - Get default theme

### Utility Functions
- `apply_custom_titlebar_direct(window, theme, title, force_custom)` - Direct application
- `get_titlebar_theme(is_dark)` - Get theme dictionary

### Platform Handlers
- `WindowsTitleBar` - Windows implementation
- `MacOSTitleBar` - macOS implementation
- `LinuxTitleBar` - Linux implementation

This system provides a robust, cross-platform solution for custom titlebars that integrates seamlessly with ThreePaneWindows while maintaining the flexibility and features of CustomTkinter's approach.
