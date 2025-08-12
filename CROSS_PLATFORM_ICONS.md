# Cross-Platform Icon Support in Enhanced Dockable

This document explains the cross-platform icon support in the Enhanced
Dockable Three-Pane Window system.

## Requirements

- **Python**: 3.9 to 3.13
- **Platforms**: Windows, macOS, Linux

## Overview

The enhanced_dockable module now supports cross-platform icon display for
detached windows, with automatic format detection and fallback mechanisms.

## Supported Icon Formats

### Windows

- **Primary**: `.ico` (Windows Icon format) - Best support, multiple sizes
- **Secondary**: `.png`, `.bmp`, `.gif` - Good support via PhotoImage

### macOS

- **Primary**: `.png` - Best support, native format
- **Secondary**: `.gif`, `.bmp` - Good support
- **Limited**: `.ico` - May work but not recommended

### Linux

- **Primary**: `.png`, `.xbm` - Best support
- **Secondary**: `.gif`, `.bmp` - Good support
- **Limited**: `.ico` - May work depending on distribution

## Usage

### Basic Usage

```python
from threepanewindows.enhanced_dockable import PaneConfig

# Using a cross-platform PNG icon
config = PaneConfig(
    title="My Panel",
    window_icon="icons/panel_icon.png"  # Will work on all platforms
)

# Using platform-specific icons
config = PaneConfig(
    title="My Panel",
    window_icon="icons/panel_icon.ico"  # Best on Windows
)
```

### Validation and Recommendations

```python
from threepanewindows.enhanced_dockable import (
    get_recommended_icon_formats,
    validate_icon_path
)

# Get recommended formats for current platform
formats = get_recommended_icon_formats()
print(f"Recommended formats: {formats}")

# Validate an icon path
is_valid, message = validate_icon_path("my_icon.png")
print(f"Valid: {is_valid}, Message: {message}")
```

## Icon Resolution Strategy

The system uses the following strategy for setting window icons:

1. **Check file existence**: Verify the icon file exists
2. **Format detection**: Determine file format from extension
3. **Primary method**: Try the best method for the format:
    - `.ico` files: Use `iconbitmap()` first
    - Other formats: Use `iconphoto()` with `PhotoImage`
4. **Fallback**: If primary method fails, try alternative methods
5. **Graceful degradation**: Continue without icon if all methods fail

## Best Practices

### 1. Use PNG for Cross-Platform Compatibility

```python
# Recommended - works everywhere
config = PaneConfig(window_icon="icons/my_icon.png")
```

### 2. Provide Multiple Formats

```python
import platform
import os

def get_platform_icon():
    """Get the best icon for the current platform."""
    system = platform.system()

    if system == "Windows" and os.path.exists("icons/app.ico"):
        return "icons/app.ico"
    elif os.path.exists("icons/app.png"):
        return "icons/app.png"
    else:
        return ""  # No icon

config = PaneConfig(window_icon=get_platform_icon())
```

### 3. Handle Icon Errors Gracefully

The system automatically handles icon loading errors and continues without
icons if they fail to load. You can monitor the console for warning
messages.

### 4. Icon Size Recommendations

- **Windows .ico**: Include multiple sizes (16x16, 32x32, 48x48)
- **PNG files**: Use 32x32 or 48x48 for best results
- **Avoid very large icons**: They may not display properly in title
  bars

## Unicode Icons

You can also use Unicode emoji or symbols as icons:

```python
config = PaneConfig(
    title="Tools",
    icon="🔧",  # This appears in headers
    window_icon=""  # No file icon needed
)
```

## Troubleshooting

### Icons Not Appearing

1. **Check file path**: Ensure the icon file exists and path is
   correct
2. **Check format**: Use recommended formats for your platform
3. **Check console**: Look for warning messages about icon loading
4. **Test with PNG**: Try a simple PNG file to verify basic
   functionality

### Platform-Specific Issues

#### Windows

- `.ico` files work best
- Ensure icon files are not corrupted
- Some antivirus software may block icon loading

#### macOS

- PNG files work best
- `.ico` files may not work on older macOS versions
- Check file permissions

#### Linux

- PNG and XBM work best
- Icon support varies by window manager
- Some distributions may have limited format support

## Example: Complete Cross-Platform Setup

```python
import os
import platform
from threepanewindows.enhanced_dockable import (
    EnhancedDockableThreePaneWindow,
    PaneConfig,
    validate_icon_path
)

def setup_cross_platform_icons():
    """Setup icons with cross-platform compatibility."""

    # Define icon paths for different platforms
    icon_paths = {
        "Windows": "icons/app.ico",
        "Darwin": "icons/app.png",  # macOS
        "Linux": "icons/app.png"
    }

    # Get the best icon for current platform
    system = platform.system()
    icon_path = icon_paths.get(system, "icons/app.png")

    # Validate the icon
    is_valid, message = validate_icon_path(icon_path)
    if not is_valid:
        print(f"Icon validation failed: {message}")
        icon_path = ""  # Use no icon

    # Create pane configuration
    left_config = PaneConfig(
        title="File Explorer",
        icon="📁",  # Unicode icon for header
        window_icon=icon_path,  # File icon for detached window
        detachable=True
    )

    return left_config

# Usage
config = setup_cross_platform_icons()
```sql

## Migration from Old Code

If you have existing code using only `.ico` files:

### Before (Windows-only)

```python
config = PaneConfig(window_icon="app.ico")
```

### After (Cross-platform)

```python
# Option 1: Use PNG for universal compatibility
config = PaneConfig(window_icon="app.png")

# Option 2: Use platform detection
import platform
icon = "app.ico" if platform.system() == "Windows" else "app.png"
config = PaneConfig(window_icon=icon)

# Option 3: Let the system handle it
config = PaneConfig(window_icon="app.ico")  # Will fallback
# gracefully
```

The enhanced system will automatically handle format compatibility and
provide appropriate fallbacks.
