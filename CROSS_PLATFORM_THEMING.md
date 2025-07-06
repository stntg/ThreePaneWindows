# Cross-Platform Theming System

This document describes the enhanced cross-platform theming system implemented in ThreePaneWindows.

## Overview

The enhanced theming system provides comprehensive cross-platform support with native appearance integration for Windows, macOS, and Linux. It includes automatic system theme detection, platform-specific color schemes, typography handling, and real-time theme updates.

## Features

### 🎨 Platform-Native Themes

- **Windows**: Integrates with Windows 10/11 design system
  - Fluent Design colors and typography
  - System accent color detection
  - Dark/Light mode detection via registry
  - Segoe UI font family with fallbacks

- **macOS**: Integrates with macOS design system
  - System appearance detection (Light/Dark/Auto)
  - Dynamic accent color support
  - SF Pro Display typography
  - Native macOS color schemes

- **Linux**: Supports major desktop environments
  - GNOME, KDE, XFCE integration
  - Desktop environment detection
  - System theme detection via gsettings/kreadconfig
  - Platform-appropriate fonts (Cantarell, Noto Sans, Ubuntu)

### 🔄 Dynamic Theme Management

- **System Theme Detection**: Automatically detects OS dark/light mode
- **Real-time Updates**: Monitors system theme changes
- **Accent Color Integration**: Uses system accent colors when available
- **Fallback Support**: Graceful degradation when platform features unavailable

### 🎯 Enhanced Theme Types

```python
class ThemeType(Enum):
    LIGHT = "light"           # Standard light theme
    DARK = "dark"             # Standard dark theme
    BLUE = "blue"             # Blue professional theme
    GREEN = "green"           # Green theme
    PURPLE = "purple"         # Purple theme
    CUSTOM = "custom"         # Custom user theme
    SYSTEM = "system"         # Follows OS theme
    NATIVE = "native"         # Platform-native adaptive
    NATIVE_LIGHT = "native_light"  # Platform-native light
    NATIVE_DARK = "native_dark"    # Platform-native dark
```

### 🔧 Platform-Specific Implementations

#### Windows Platform Handler
- Registry-based dark mode detection
- DWM accent color extraction
- Windows-specific color schemes
- Segoe UI typography with fallbacks

#### macOS Platform Handler
- NSUserDefaults integration for appearance
- System accent color detection
- SF Pro Display font support
- macOS-specific color palettes

#### Linux Platform Handler
- Desktop environment detection
- gsettings/kreadconfig integration
- Font detection per DE (GNOME, KDE, etc.)
- Compositor transparency detection

### 🎨 Enhanced Color Management

- **Alpha Channel Handling**: Proper Tkinter color compatibility
- **Color Utilities**: Brightness adjustment and lightening functions
- **Platform Colors**: Native color scheme extraction
- **Fallback Colors**: Graceful degradation for unsupported platforms

### 🔤 Typography System

```python
@dataclass
class Typography:
    font_family: str = "Segoe UI"
    font_family_fallback: str = "Arial"
    font_size_small: int = 9
    font_size_normal: int = 10
    font_size_large: int = 12
    font_size_title: int = 14
    font_weight_light: str = "normal"
    font_weight_normal: str = "normal"
    font_weight_medium: str = "bold"
    font_weight_bold: str = "bold"
```

## Usage Examples

### Basic Theme Management

```python
from threepanewindows.themes import ThemeManager, ThemeType

# Initialize with native theme
theme_manager = ThemeManager(theme=ThemeType.NATIVE)

# Switch themes
theme_manager.set_theme(ThemeType.NATIVE_DARK, window=root)

# Refresh system theme
theme_manager.refresh_system_theme()

# Get platform information
platform_info = theme_manager.get_platform_info()
```

### Platform Detection

```python
from threepanewindows.platform import platform_handler

# Check system dark mode
is_dark = platform_handler.is_dark_mode()

# Get system accent color
accent_color = platform_handler.get_system_accent_color()

# Get platform-native colors
colors = platform_handler.get_platform_native_colors(is_dark=True)

# Get platform typography
typography = platform_handler.get_platform_typography()
```

### Custom Theme Application

```python
# Apply theme to TTK widgets
style = ttk.Style()
theme_manager.apply_ttk_theme(style)

# Apply theme to TK widgets
text_style = theme_manager.get_tk_widget_style("text")
text_widget.configure(**text_style)

listbox_style = theme_manager.get_tk_widget_style("listbox")
listbox.configure(**listbox_style)
```

## Platform-Specific Features

### Windows
- **Accent Color**: Extracted from `HKEY_CURRENT_USER\Software\Microsoft\Windows\DWM\AccentColor`
- **Dark Mode**: Detected via `AppsUseLightTheme` registry value
- **Typography**: Segoe UI with Tahoma fallback
- **Colors**: Fluent Design-inspired color schemes

### macOS
- **Appearance**: NSUserDefaults `AppleInterfaceStyle` detection
- **Accent Color**: System accent color via NSUserDefaults
- **Typography**: SF Pro Display with Helvetica fallbacks
- **Colors**: macOS Human Interface Guidelines colors

### Linux
- **Desktop Environment**: XDG_CURRENT_DESKTOP detection
- **Theme Detection**: gsettings (GNOME) and kreadconfig (KDE)
- **Typography**: DE-specific fonts (Cantarell, Noto Sans, Ubuntu)
- **Colors**: DE-appropriate color schemes

## Error Handling

The system includes comprehensive error handling:

- **Graceful Degradation**: Falls back to standard themes if native detection fails
- **Color Validation**: Ensures Tkinter-compatible color formats
- **Font Fallbacks**: Multiple fallback fonts per platform
- **Exception Handling**: Catches and logs platform-specific errors

## Dependencies

### Required
- `tkinter` (Python standard library)
- `platform` (Python standard library)

### Optional (for enhanced features)
- `darkdetect` - Cross-platform dark mode detection
- Platform-specific modules for advanced features

## Testing

Run the comprehensive demo:

```bash
python example_cross_platform_theming.py
```

Or test specific functionality:

```bash
python test_enhanced_theming.py
```

## File Structure

```
threepanewindows/
├── themes.py                    # Enhanced theme management
├── platform/
│   ├── __init__.py             # Platform handler interface
│   ├── base.py                 # Base platform handler
│   ├── windows.py              # Windows-specific implementation
│   ├── macos.py                # macOS-specific implementation
│   └── linux.py                # Linux-specific implementation
└── examples/
    ├── example_cross_platform_theming.py
    ├── example_macos_theming.py
    └── test_enhanced_theming.py
```

## Widget Theming

### Automatic Widget Theming

The system now automatically themes both TTK and TK widgets:

```python
# Automatic theming when setting a theme
theme_manager.set_theme(ThemeType.NATIVE, window=root)  # Themes entire window

# Manual theming
theme_manager.apply_theme_to_window(root)  # Themes all widgets in window
theme_manager.apply_theme_to_widget(widget, recursive=True)  # Themes specific widget
```

### Supported Widget Types

**TTK Widgets** (automatically themed):
- TLabel, TButton, TEntry, TCombobox
- TCheckbutton, TRadiobutton, TFrame, TLabelFrame
- TNotebook, TProgressbar, TScale, TScrollbar
- Treeview with headers and selection

**TK Widgets** (automatically themed):
- Text, Listbox, Canvas, Entry
- Label, Button, Frame
- Root windows and Toplevel windows

### Theme Application Methods

1. **Comprehensive Window Theming**:
   ```python
   theme_manager.apply_theme_to_window(window)
   ```

2. **Individual Widget Theming**:
   ```python
   theme_manager.apply_theme_to_widget(widget, recursive=True)
   ```

3. **TTK Style Configuration**:
   ```python
   style = ttk.Style()
   theme_manager.apply_ttk_theme(style)
   ```

4. **TK Widget Styling**:
   ```python
   text_style = theme_manager.get_tk_widget_style("text")
   text_widget.configure(**text_style)
   ```

## Benefits

1. **Complete Widget Coverage**: Both TTK and TK widgets are automatically themed
2. **Native Integration**: Themes match the host OS appearance
3. **Automatic Adaptation**: Follows system theme changes
4. **Cross-Platform Consistency**: Unified API across platforms
5. **Enhanced UX**: Professional, native-looking applications
6. **Developer Friendly**: Simple API with powerful features
7. **Robust Fallbacks**: Works even when platform features unavailable
8. **Real-time Updates**: Themes can be changed dynamically without restart

## Future Enhancements

- High contrast theme support
- Custom accent color themes
- Theme transition animations
- More granular typography control
- Additional platform integrations

This enhanced theming system provides a professional, cross-platform solution for creating native-looking Tkinter applications that adapt to their environment while maintaining consistency across platforms.
