# Platform Separation Implementation

This document describes the platform-specific functionality separation
implemented in ThreePaneWindows.

## Overview

The platform-specific code has been extracted from the main modules and
organized into a dedicated `platform` package. This provides better
maintainability, testability, and extensibility for platform-specific
features.

## Architecture

### Platform Package Structure

```text
threepanewindows/platform/
├── __init__.py          # Main platform detection and handler selection
├── base.py              # Abstract base class for platform handlers
├── windows.py           # Windows-specific implementation
├── macos.py             # macOS-specific implementation
└── linux.py             # Linux-specific implementation
```

### Platform Handler Interface

All platform handlers implement the `PlatformHandler` abstract base class
with these methods:

- `get_recommended_icon_formats()` - Returns platform-specific icon
  format preferences
- `validate_icon_path(icon_path)` - Validates icon files for the
  platform
- `set_window_icon(window, icon_path)` - Sets window icons using
  platform-optimal methods
- `apply_custom_titlebar(window, theme_colors)` - Applies
  platform-specific titlebar customization

## Platform-Specific Features

### Windows (`WindowsPlatformHandler`)

- **Icon Formats**: Prefers `.ico`, supports `.png`, `.bmp`, `.gif`
- **Icon Handling**: Uses `iconbitmap()` for `.ico` files,
  `iconphoto()` for others
- **Titlebar**: Uses Windows DWM API to set titlebar colors
- **Features**: Native Windows titlebar color customization

### macOS (`MacOSPlatformHandler`)

- **Icon Formats**: Prefers `.png`, supports `.gif`, `.bmp`, `.ico`
- **Icon Handling**: Uses `iconphoto()` primarily, `iconbitmap()` as
  fallback
- **Titlebar**: Creates custom titlebar with macOS-style window
  controls
- **Features**: Custom draggable titlebar with red/yellow/green
  buttons

### Linux (`LinuxPlatformHandler`)

- **Icon Formats**: Prefers `.png`, supports `.xbm`, `.gif`, `.bmp`,
  `.ico`
- **Icon Handling**: Uses `iconphoto()` primarily for better
  compatibility
- **Titlebar**: Basic theming, respects window manager preferences
- **Features**: Desktop environment detection, transparency support
  detection

## Integration Points

### Themes Module

The `themes.py` module now uses the platform handler for titlebar
customization:

```python
from .platform import platform_handler

# In ThemeManager.set_theme()
if window:
    platform_handler.apply_custom_titlebar(window, theme.colors)
```

### Enhanced Dockable Module

The `enhanced_dockable.py` module uses platform handlers for icon
functionality:

```python
from .platform import platform_handler

def get_recommended_icon_formats():
    return platform_handler.get_recommended_icon_formats()

def validate_icon_path(icon_path):
    return platform_handler.validate_icon_path(icon_path)

# In DetachedWindow._set_window_icon()
def _set_window_icon(self, icon_path):
    platform_handler.set_window_icon(self, icon_path)
```

## Benefits

### 1. **Maintainability**

- Platform-specific code is isolated and organized
- Easier to update platform-specific features
- Clear separation of concerns

### 2. **Testability**

- Each platform handler can be tested independently
- Mock handlers can be used for testing
- Platform-specific behavior is predictable

### 3. **Extensibility**

- New platforms can be added by creating new handler classes
- Platform-specific features can be added without affecting other platforms
- Easy to customize behavior for specific environments

### 4. **Code Quality**

- Eliminates platform-specific `if/else` blocks scattered throughout the code
- Reduces code duplication
- Improves type safety with abstract base class

## Usage Examples

### Basic Platform Detection

```python
from threepanewindows.platform import platform_handler

# Get current platform handler
print(f"Platform: {type(platform_handler).__name__}")

# Get recommended icon formats
formats = platform_handler.get_recommended_icon_formats()
print(f"Recommended formats: {formats}")
```

### Icon Validation

```python
from threepanewindows.platform import validate_icon_path

# Validate an icon file
valid, message = validate_icon_path("my_icon.png")
if valid:
    print("Icon is valid for this platform")
else:
    print(f"Icon validation failed: {message}")
```

### Theme Integration

```python
from threepanewindows import ThemeManager
import tkinter as tk

root = tk.Tk()
theme_manager = ThemeManager()

# Set theme with automatic platform-specific titlebar customization
theme_manager.set_theme("dark", window=root)
```

## Migration Notes

### For Existing Code

The public API remains unchanged. Existing code using ThreePaneWindows
will continue to work without modifications.

### For Developers

- Platform-specific customizations should now be implemented in the
  appropriate platform handler
- New platform-specific features should be added to the
  `PlatformHandler` interface
- Testing should include verification of platform-specific behavior

## Future Enhancements

The platform separation architecture enables future enhancements such as:

- Platform-specific keyboard shortcuts
- Native file dialogs integration
- Platform-specific animation preferences
- Advanced window management features
- Better integration with platform-specific UI guidelines

## Testing

The platform separation includes comprehensive tests to verify:

- Correct platform detection
- Platform handler functionality
- Integration with existing modules
- Cross-platform compatibility

Run the platform demo to see the separation in action:

```bash
python example_platform_demo.py
```

This will show platform-specific icon format recommendations, validation
behavior, and titlebar customization in a live ThreePaneWindows application.
