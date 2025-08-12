# Central Theme Manager

The Central Theme Manager is a powerful new theming system that provides unified,
consistent theming across all ThreePaneWindows components. It serves as a single
source of truth for all visual styling, ensuring cohesive appearance and easy
theme switching.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
- [Available Themes](#available-themes)
- [Theme Colors](#theme-colors)
- [Widget Theming](#widget-theming)
- [Custom Themes](#custom-themes)
- [Integration with Components](#integration-with-components)
- [API Reference](#api-reference)

## Overview

The Central Theme Manager replaces the previous scattered theming approach with
a centralized system that:

- **Unifies Theming**: Single point of control for all visual styling
- **Ensures Consistency**: All components use the same color scheme
- **Simplifies Management**: Easy theme switching and customization
- **Supports All Widgets**: Comprehensive support for Tkinter and TTK widgets
- **Cross-Platform**: Consistent appearance across Windows, macOS, and Linux

## Key Features

### 🎨 Comprehensive Theme Support

- **7 Built-in Themes**: Light, Dark, Blue, Green, Purple, System, Native
- **Custom Theme Support**: Create and register your own themes
- **Dynamic Switching**: Change themes at runtime without restart

### 🔧 Complete Widget Coverage

- **Standard Tkinter**: Button, Label, Entry, Text, Listbox, Menu, etc.
- **TTK Widgets**: Full TTK theming integration
- **Custom Components**: Scrollbars, menubars, and other custom widgets

### 🌐 Platform Integration

- **System Theme Detection**: Automatically detect system dark/light mode
- **Native Styling**: Option to use platform-native appearance
- **Cross-Platform Consistency**: Uniform appearance across platforms

## Getting Started

### Basic Usage

```python
import tkinter as tk
from threepanewindows.central_theme_manager import get_theme_manager, ThemeType

# Get the global theme manager instance
theme_manager = get_theme_manager()

# Set a theme
theme_manager.set_theme(ThemeType.DARK)

# Create your UI - theming is automatic
root = tk.Tk()
theme_manager.apply_window_theme(root)

# Create widgets - they'll be themed automatically
button = tk.Button(root, text="Themed Button")
theme_manager.apply_button_theme(button)
```

### Integration with Layouts

```python
from threepanewindows import EnhancedDockableThreePaneWindow

# Theme is automatically applied to all components
window = EnhancedDockableThreePaneWindow(
    root,
    theme_name="blue"  # Uses central theme manager
)
```

## Available Themes

### Light Theme

Clean, bright interface perfect for daytime use:

- **Background**: Light grays and whites
- **Text**: Dark colors for high contrast
- **Accents**: Subtle blue highlights

```python
theme_manager.set_theme(ThemeType.LIGHT)
```

### Dark Theme

Modern dark interface ideal for low-light environments:

- **Background**: Dark grays and blacks
- **Text**: Light colors for readability
- **Accents**: Bright blue highlights

```python
theme_manager.set_theme(ThemeType.DARK)
```

### Blue Theme

Professional blue theme for business applications:

- **Background**: Blue-tinted grays
- **Text**: High contrast colors
- **Accents**: Professional blue tones

```python
theme_manager.set_theme(ThemeType.BLUE)
```

### Green Theme

Nature-inspired green theme:

- **Background**: Subtle green tints
- **Text**: Natural color palette
- **Accents**: Forest green highlights

```python
theme_manager.set_theme(ThemeType.GREEN)
```

### Purple Theme

Creative purple theme for artistic applications:

- **Background**: Purple-tinted neutrals
- **Text**: High contrast colors
- **Accents**: Rich purple tones

```python
theme_manager.set_theme(ThemeType.PURPLE)
```

### System Theme

Automatically matches system preferences:

- **Windows**: Follows Windows theme settings
- **macOS**: Matches macOS appearance preferences
- **Linux**: Adapts to desktop environment

```python
theme_manager.set_theme(ThemeType.SYSTEM)
```

### Native Theme

Uses platform-native styling:

- **Appearance**: Platform-specific look and feel
- **Behavior**: Native widget behavior
- **Integration**: Perfect OS integration

```python
theme_manager.set_theme(ThemeType.NATIVE)
```

## Theme Colors

Each theme provides a comprehensive color palette:

### Color Categories

```python
@dataclass
class ThemeColors:
    # Window and frame colors
    window_bg: str          # Main window background
    frame_bg: str           # Frame backgrounds
    panel_bg: str           # Panel backgrounds

    # Text colors
    text_fg: str            # Primary text color
    text_bg: str            # Text background
    text_select_bg: str     # Text selection background
    text_select_fg: str     # Text selection foreground

    # Button colors
    button_bg: str          # Button background
    button_fg: str          # Button text
    button_active_bg: str   # Active button background
    button_active_fg: str   # Active button text
    button_hover_bg: str    # Hover button background
    button_hover_fg: str    # Hover button text
    button_disabled_bg: str # Disabled button background
    button_disabled_fg: str # Disabled button text

    # Entry colors
    entry_bg: str           # Entry background
    entry_fg: str           # Entry text
    entry_select_bg: str    # Entry selection background
    entry_select_fg: str    # Entry selection text
    entry_disabled_bg: str  # Disabled entry background
    entry_disabled_fg: str  # Disabled entry text

    # Listbox colors
    listbox_bg: str         # Listbox background
    listbox_fg: str         # Listbox text
    listbox_select_bg: str  # Listbox selection background
    listbox_select_fg: str  # Listbox selection text

    # Menu colors
    menu_bg: str            # Menu background
    menu_fg: str            # Menu text
    menu_active_bg: str     # Active menu background
    menu_active_fg: str     # Active menu text
    menu_disabled_fg: str   # Disabled menu text

    # Scrollbar colors
    scrollbar_bg: str       # Scrollbar background
    scrollbar_fg: str       # Scrollbar foreground
    scrollbar_active_bg: str # Active scrollbar background
    scrollbar_trough_bg: str # Scrollbar trough background

    # Border and accent colors
    border_color: str       # Border color
    accent_color: str       # Accent/highlight color
    highlight_color: str    # Secondary highlight
    shadow_color: str       # Shadow color
```

### Accessing Theme Colors

```python
# Get current theme colors
colors = theme_manager.current_colors

# Use colors in your widgets
my_widget.configure(
    bg=colors.panel_bg,
    fg=colors.text_fg,
    selectbackground=colors.accent_color
)
```

## Widget Theming

### Automatic Theming

The theme manager can automatically theme widgets:

```python
# Theme individual widgets
theme_manager.apply_button_theme(my_button)
theme_manager.apply_label_theme(my_label)
theme_manager.apply_entry_theme(my_entry)

# Theme entire widget hierarchies
theme_manager.apply_theme_to_widget(root_frame, recursive=True)
```

### Manual Theming

For custom styling, access theme colors directly:

```python
colors = theme_manager.current_colors

# Custom button styling
button.configure(
    bg=colors.button_bg,
    fg=colors.button_fg,
    activebackground=colors.button_active_bg,
    activeforeground=colors.button_active_fg,
    relief="flat",
    bd=1,
    highlightthickness=0
)

# Custom text widget styling
text.configure(
    bg=colors.text_bg,
    fg=colors.text_fg,
    selectbackground=colors.text_select_bg,
    selectforeground=colors.text_select_fg,
    insertbackground=colors.text_fg
)
```

### TTK Integration

The theme manager integrates with TTK styling:

```python
# Configure TTK styles
theme_manager.configure_ttk_style()

# Create TTK widgets - they'll use the theme automatically
ttk_button = ttk.Button(root, text="TTK Button")
ttk_entry = ttk.Entry(root)
```

## Custom Themes

### Creating Custom Themes

```python
from threepanewindows.central_theme_manager import ThemeColors

# Define custom colors
custom_colors = ThemeColors(
    window_bg="#2b2b2b",
    frame_bg="#3c3c3c",
    panel_bg="#404040",
    text_fg="#ffffff",
    text_bg="#2b2b2b",
    text_select_bg="#0078d4",
    text_select_fg="#ffffff",
    button_bg="#0078d4",
    button_fg="#ffffff",
    button_active_bg="#106ebe",
    button_active_fg="#ffffff",
    button_hover_bg="#1084d4",
    button_hover_fg="#ffffff",
    button_disabled_bg="#666666",
    button_disabled_fg="#999999",
    entry_bg="#404040",
    entry_fg="#ffffff",
    entry_select_bg="#0078d4",
    entry_select_fg="#ffffff",
    entry_disabled_bg="#333333",
    entry_disabled_fg="#666666",
    listbox_bg="#404040",
    listbox_fg="#ffffff",
    listbox_select_bg="#0078d4",
    listbox_select_fg="#ffffff",
    menu_bg="#3c3c3c",
    menu_fg="#ffffff",
    menu_active_bg="#0078d4",
    menu_active_fg="#ffffff",
    menu_disabled_fg="#666666",
    scrollbar_bg="#404040",
    scrollbar_fg="#666666",
    scrollbar_active_bg="#0078d4",
    scrollbar_trough_bg="#2b2b2b",
    border_color="#666666",
    accent_color="#0078d4",
    highlight_color="#1084d4",
    shadow_color="#1a1a1a"
)

# Register the custom theme
theme_manager.register_custom_theme("my_custom_theme", custom_colors)

# Use the custom theme
theme_manager.set_theme("my_custom_theme")
```

### Theme Inheritance

Create themes based on existing ones:

```python
# Start with dark theme colors
dark_colors = theme_manager.get_theme_colors(ThemeType.DARK)

# Modify specific colors
custom_colors = ThemeColors(
    **dark_colors.__dict__,  # Copy all colors
    accent_color="#ff6b35",  # Override accent color
    button_bg="#ff6b35",     # Override button color
    button_active_bg="#e55a2b"  # Override active button color
)

theme_manager.register_custom_theme("orange_dark", custom_colors)
```

## Integration with Components

### Automatic Integration

All ThreePaneWindows components automatically use the central theme manager:

```python
# All these components will use the current theme
fixed_window = FixedThreePaneWindow(root)
dockable_window = DockableThreePaneWindow(root)
enhanced_window = EnhancedDockableThreePaneWindow(root)
flexible_layout = EnhancedFlexibleLayout(root, layout_config)
```

### Custom Component Integration

Integrate your own components:

```python
class MyCustomWidget(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Get theme manager
        self.theme_manager = get_theme_manager()

        # Apply initial theme
        self.apply_theme()

        # Listen for theme changes (if needed)
        self.theme_manager.bind_theme_change(self.on_theme_changed)

    def apply_theme(self):
        colors = self.theme_manager.current_colors
        self.configure(bg=colors.panel_bg)

        # Theme child widgets
        for child in self.winfo_children():
            self.theme_manager.apply_theme_to_widget(child)

    def on_theme_changed(self, new_theme):
        self.apply_theme()
```

## API Reference

### CentralThemeManager Class

#### Properties

- `current_theme: ThemeType` - Currently active theme
- `current_colors: ThemeColors` - Current theme color palette

#### Theme Management

- `set_theme(theme: ThemeType) -> None` - Set active theme
- `get_theme_colors(theme: ThemeType) -> ThemeColors` - Get colors for specific theme
- `register_custom_theme(name: str, colors: ThemeColors) -> None`
  Register custom theme
- `get_available_themes() -> List[ThemeType]` - Get list of available themes

#### Widget Theming

- `apply_theme_to_widget(widget: tk.Widget, recursive: bool = True) -> None`
  Theme widget and optionally children
- `apply_window_theme(window: tk.Tk) -> None` - Theme main window
- `apply_frame_theme(frame: tk.Frame) -> None` - Theme frame widget
- `apply_button_theme(button: tk.Button) -> None` - Theme button widget
- `apply_label_theme(label: tk.Label) -> None` - Theme label widget
- `apply_entry_theme(entry: tk.Entry) -> None` - Theme entry widget
- `apply_text_theme(text: tk.Text) -> None` - Theme text widget
- `apply_listbox_theme(listbox: tk.Listbox) -> None` - Theme listbox widget
- `apply_menu_theme(menu: tk.Menu) -> None` - Theme menu widget
- `apply_scrollbar_theme(scrollbar: Union[tk.Scrollbar, ttk.Scrollbar]) -> None`
  Theme scrollbar

#### TTK Integration

- `apply_ttk_theme(widget: ttk.Widget) -> None` - Theme TTK widget
- `configure_ttk_style() -> None` - Configure TTK style system

#### Scrollbar Creation

- `create_themed_scrollbar_auto(parent, orient="vertical", command=None, **kwargs)`
  Create automatically themed scrollbar
- `create_themed_scrollbar_native(parent, orient="vertical", command=None, **kwargs)`
  Create native themed scrollbar
- `create_themed_scrollbar_ttk(parent, orient="vertical", command=None, **kwargs)`
  Create TTK themed scrollbar

#### Utility Methods

- `get_contrasting_color(color: str) -> str` - Get contrasting color
- `lighten_color(color: str, factor: float = 0.1) -> str` - Lighten color
- `darken_color(color: str, factor: float = 0.1) -> str` - Darken color
- `is_dark_theme() -> bool` - Check if current theme is dark
- `get_platform_scrollbar_type() -> str` - Get recommended scrollbar type for platform

### Global Functions

```python
# Get global theme manager instance
def get_theme_manager() -> CentralThemeManager

# Convenience functions
def set_global_theme(theme: ThemeType) -> None
def get_current_theme() -> ThemeType
def get_current_colors() -> ThemeColors
```

## Best Practices

### Theme Selection

- Use **Light** theme for bright environments and general use
- Use **Dark** theme for low-light environments and extended use
- Use **Blue** theme for professional/business applications
- Use **System** theme to respect user preferences
- Use **Native** theme for maximum OS integration

### Performance

- Set theme once at application startup when possible
- Avoid frequent theme switching in performance-critical code
- Use `apply_theme_to_widget(recursive=True)` for bulk theming

### Consistency

- Always use the central theme manager for all theming
- Don't mix manual color assignments with themed widgets
- Test themes across different platforms

### Custom Themes

- Base custom themes on existing ones when possible
- Ensure sufficient contrast for accessibility
- Test custom themes with all widget types

The Central Theme Manager provides a powerful, flexible foundation for creating
beautiful, consistent user interfaces across all ThreePaneWindows components.
