# 🎨 Enhanced Three-Pane Windows - Complete Feature Guide

## 🎯 **Major Improvements & New Features**

The enhanced dockable module now provides a sophisticated, highly customizable
three-pane window with **automatic theme management**, **perfect detached window
support**, and **platform-specific optimizations**.

### ✨ Key Improvements

#### 1. **Professional Theming System**

- **Multiple Built-in Themes**: Light, Dark, Blue Professional
- **Consistent Color Schemes**: Carefully designed color palettes
- **Typography Control**: Professional font choices and sizing
- **Visual Consistency**: Unified styling across all components

#### 2. **Advanced Drag & Drop Interface**

- **Intuitive Drag Handles**: Professional grip indicators in panel headers
- **Visual Feedback**: Real-time visual cues during drag operations
- **Smart Detaching**: Drag panel headers to detach (no more buttons!)
- **Professional Detached Windows**: Beautifully styled floating panels

#### 3. **Highly Customizable Panels**

- **Panel Configuration**: Title, icon, size constraints, and behavior
- **Cross-Platform Icons**: Support for .ico, .png, .gif, .bmp, .xbm formats
  with automatic fallback
- **Flexible Sizing**: Min/max width constraints with intelligent defaults
- **Optional Features**: Detachable, closable, resizable panels
- **Professional Headers**: Icons, titles, and control buttons

#### 4. **Enhanced User Experience**

- **Smooth Animations**: Optional smooth transitions and effects
- **Professional Visual Feedback**: Hover effects, active states
- **Context-Aware UI**: Smart positioning and behavior
- **Responsive Design**: Adapts to different screen sizes

## 🚀 Quick Start

### Basic Usage

```python
import tkinter as tk
from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

# Create pane configurations
left_config = PaneConfig(
    title="File Explorer",
    icon="📁",
    default_width=250,
    min_width=200,
    max_width=400,
    detachable=True
)

right_config = PaneConfig(
    title="Properties",
    icon="🔧",
    default_width=200,
    detachable=True
)

# Create the enhanced window
window = EnhancedDockableThreePaneWindow(
    root,
    left_config=left_config,
    right_config=right_config,
    left_builder=build_left_panel,
    center_builder=build_center_panel,
    right_builder=build_right_panel,
    theme_name="blue"  # Professional blue theme
)
```

### Panel Configuration Options

```python
config = PaneConfig(
    title="Panel Title",           # Display title
    icon="📁",                     # Icon (emoji or text) for header
    window_icon="icons/panel.png", # File icon for detached windows
    default_width=250,             # Default width in pixels
    min_width=200,                 # Minimum width constraint
    max_width=400,                 # Maximum width constraint
    detachable=True,               # Can be detached
    closable=False,                # Can be closed
    resizable=True                 # Can be resized
)
```

### Cross-Platform Icon Support

The enhanced system supports multiple icon formats with automatic platform optimization:

```python
from threepanewindows.enhanced_dockable import (
    get_recommended_icon_formats,
    validate_icon_path
)

# Get recommended formats for current platform
formats = get_recommended_icon_formats()
print(f"Recommended: {formats}")  # e.g., ['.ico', '.png', '.bmp', '.gif'] on Windows

# Validate icon compatibility
is_valid, message = validate_icon_path("my_icon.png")
if is_valid:
    config = PaneConfig(window_icon="my_icon.png")
else:
    print(f"Icon issue: {message}")
```

**Supported Formats by Platform:**

- **Windows**: `.ico` (best), `.png`, `.bmp`, `.gif`
- **macOS**: `.png` (best), `.gif`, `.bmp`, `.ico` (limited)
- **Linux**: `.png`, `.xbm` (best), `.gif`, `.bmp`, `.ico` (limited)

## 🎨 Theming System

### Available Themes

1. **Light Theme** (`"light"`)
    - Clean, bright interface
    - Professional white/gray color scheme
    - Perfect for daytime use

2. **Dark Theme** (`"dark"`)
    - Modern dark interface
    - Easy on the eyes
    - Great for extended coding sessions

3. **Blue Professional** (`"blue"`)
    - Corporate-friendly design
    - Professional blue accents
    - Ideal for business applications

### Changing Themes

```python
# Set theme during creation
window = EnhancedDockableThreePaneWindow(
    root,
    theme_name="dark"
)

# Change theme at runtime
window.set_theme("blue")

# Global theme setting
from threepanewindows import set_global_theme
set_global_theme("light")
```

### Custom Themes

```python
from threepanewindows import ThemeManager, Theme, ColorScheme

# Create custom color scheme
custom_colors = ColorScheme(
    primary_bg="#f8f9fa",
    secondary_bg="#e9ecef",
    accent_bg="#d1ecf1",
    primary_text="#212529",
    accent_text="#0c5460",
    button_bg="#17a2b8",
    button_fg="#ffffff"
)

# Create custom theme
custom_theme = Theme(
    name="Custom",
    colors=custom_colors
)

# Register and use
theme_manager = get_theme_manager()
theme_manager.register_theme(custom_theme)
window.set_theme("custom")
```

## 🖱️ User Interaction

### Detaching Panels

1. **Drag Method**: Drag the panel header to detach
    - Grab the grip area in the panel header
    - Drag away from the main window
    - Panel automatically detaches when threshold is reached

2. **Button Method**: Click the detach button (⧉) in the header
    - Professional icon button in panel header
    - One-click detaching

### Reattaching Panels

1. **From Detached Window**: Click "⧈ Reattach" button
2. **Window Close**: Close the detached window
3. **Programmatic**: Call `window._reattach_pane("left")`

### Visual Feedback

- **Hover Effects**: Headers highlight on mouse over
- **Drag Indicators**: Visual feedback during drag operations
- **Professional Cursors**: Context-appropriate cursor changes
- **Smooth Transitions**: Optional animations for state changes

## 📋 Complete Example

```python
# !/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

def build_file_explorer(frame):
    """Build a professional file explorer."""
    tree = ttk.Treeview(frame)
    tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    # Add sample files
    root_item = tree.insert("", "end", text="📁 Project", open=True)
    tree.insert(root_item, "end", text="📄 main.py")
    tree.insert(root_item, "end", text="📄 utils.py")
    tree.insert(root_item, "end", text="📁 assets")

def build_code_editor(frame):
    """Build a professional code editor."""
    text = tk.Text(frame, font=("Consolas", 10), wrap=tk.NONE)
    text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    # Add scrollbars
    v_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text.yview)
    v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    text.config(yscrollcommand=v_scroll.set)

def build_properties(frame):
    """Build a professional properties panel."""
    # Create sections
    sections = [
        ("File Info", [("Name", "main.py"), ("Size", "2.1 KB")]),
        ("Settings", [("Theme", "Blue"), ("Font", "Consolas")])
    ]

    for section_name, properties in sections:
        section = ttk.LabelFrame(frame, text=section_name)
        section.pack(fill="x", padx=8, pady=4)

        for prop_name, prop_value in properties:
            prop_frame = ttk.Frame(section)
            prop_frame.pack(fill="x", padx=8, pady=2)

            ttk.Label(prop_frame, text=f"{prop_name}:").pack(side="left")
            ttk.Label(prop_frame, text=prop_value).pack(side="right")

def main():
    root = tk.Tk()
    root.title("Professional IDE")
    root.geometry("1200x800")

    # Configure panels with cross-platform icons
    left_config = PaneConfig(
        title="Explorer",
        icon="📁",                        # Unicode icon for header
        window_icon="icons/explorer.png", # Cross-platform PNG icon
        default_width=250,
        min_width=200,
        max_width=400,
        detachable=True
    )

    center_config = PaneConfig(
        title="Editor",
        icon="📝",
        window_icon="icons/editor.png",   # Icon for detached editor window
        detachable=False
    )

    right_config = PaneConfig(
        title="Properties",
        icon="🔧",
        window_icon="icons/properties.ico", # Windows .ico with PNG fallback
        default_width=200,
        min_width=150,
        max_width=300,
        detachable=True
    )

    # Create enhanced window
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=build_file_explorer,
        center_builder=build_code_editor,
        right_builder=build_properties,
        theme_name="blue",
        enable_animations=True
    )
    window.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if **name** == "**main**":
    main()
```

## 🔧 Advanced Features

### Animation Control

```python
# Enable/disable animations
window = EnhancedDockableThreePaneWindow(
    root,
    enable_animations=True  # or False
)
```

### Panel State Management

```python
# Check if panel is detached
if window.is_pane_detached("left"):
    print("Left panel is detached")

# Get panel frame (works for attached and detached)
left_frame = window.get_pane_frame("left")
if left_frame:
    # Add widgets to the frame
    tk.Label(left_frame, text="Dynamic content").pack()
```

### Theme Management

```python
from threepanewindows import get_theme_manager

theme_manager = get_theme_manager()

# Get available themes
current_theme = theme_manager.get_current_theme()
print(f"Current theme: {current_theme.name}")

# Get styling for components
button_style = theme_manager.get_style("button", "hover")
```

## 🎯 Best Practices

1. **Panel Sizing**: Use reasonable min/max constraints
2. **Theme Consistency**: Stick to one theme throughout your application
3. **User Experience**: Provide visual feedback for all interactions
4. **Performance**: Disable animations on slower systems if needed
5. **Accessibility**: Use clear icons and descriptive titles

## 🆚 Comparison with Original

| Feature | Original | Enhanced |
|---------|----------|----------|
| Theming | None | Professional themes |
| Detaching | Button-based | Drag & drop + buttons |
| Visual Feedback | Basic | Professional |
| Customization | Limited | Highly configurable |
| Panel Headers | None | Professional with icons |
| Animations | None | Optional smooth transitions |
| Window Positioning | Basic | Smart positioning |
| User Experience | Functional | Professional |

## 🚀 Migration Guide

### From Original to Enhanced

```python
# Original
window = DockableThreePaneWindow(
    root,
    side_width=200,
    left_builder=build_left,
    center_builder=build_center,
    right_builder=build_right
)

# Enhanced
left_config = PaneConfig(title="Left", default_width=200)
right_config = PaneConfig(title="Right", default_width=200)

window = EnhancedDockableThreePaneWindow(
    root,
    left_config=left_config,
    right_config=right_config,
    left_builder=build_left,
    center_builder=build_center,
    right_builder=build_right,
    theme_name="light"
)
```

The enhanced version is designed to be intuitive and professional while maintaining
the flexibility and power that developers need for creating sophisticated
applications.
