# ThreePaneWindows API Documentation

## Requirements

- **Python**: 3.9 to 3.13
- **Dependencies**: None (uses Python standard library only)
- **Platforms**: Windows, macOS, Linux

## Overview

ThreePaneWindows provides multiple classes for creating three-pane layouts in
Tkinter applications:

- `EnhancedDockableThreePaneWindow`: Professional layout with advanced theming
  and cross-platform icon support
- `DockableThreePaneWindow`: Advanced layout with detachable side panels
- `FixedThreePaneLayout`: Simple fixed layout with customizable panels

## EnhancedDockableThreePaneWindow

### Class: `EnhancedDockableThreePaneWindow(tk.Frame)`

A professional three-pane window with advanced theming, cross-platform icon
support, and sophisticated user interactions.

**Key Features:**

- **Professional Theming**: Multiple built-in themes (light, dark, blue
  professional)
- **Cross-Platform Icons**: Support for .ico, .png, .gif, .bmp, .xbm formats
  with automatic fallback
- **Drag & Drop Interface**: Intuitive panel detaching by dragging headers
- **Advanced Customization**: Configurable panel properties, icons, and
  constraints
- **Smart Layout System (v1.2.0)**: Automatic detection of fixed vs. resizable
  panes for optimal sash behavior
- **Smart Positioning**: Intelligent window placement and sizing

#### Constructor: EnhancedDockableThreePaneWindow

```python
EnhancedDockableThreePaneWindow(
    master=None, left_config=None, center_config=None,
    right_config=None, left_builder=None, center_builder=None,
    right_builder=None, theme_name="light", enable_animations=True,
    menu_bar=None, **kwargs
)
```

**Parameters:**

- `master`: Parent widget (default: None)
- `left_config`: PaneConfig object for left panel configuration
  (default: None)
- `center_config`: PaneConfig object for center panel configuration
  (default: None)
- `right_config`: PaneConfig object for right panel configuration
  (default: None)
- `left_builder`: Function to build left panel content (default: None)
- `center_builder`: Function to build center panel content (default: None)
- `right_builder`: Function to build right panel content (default: None)
- `theme_name`: Theme name ("light", "dark", "blue") (default: "light")
- `enable_animations`: Enable smooth animations (default: True)
- `menu_bar`: Optional menu bar widget (default: None)
- `**kwargs`: Additional arguments passed to tk.Frame

#### PaneConfig Class

```python
@dataclass
class PaneConfig:
    title: str = ""                    # Panel title
    icon: str = ""                     # Icon (emoji or text)
    window_icon: str = ""              # Path to icon file for detached windows
                                       # (.ico, .png, .gif, .bmp, .xbm)
    custom_titlebar: bool = False      # Use custom title bar instead of
                                       # system title bar
    custom_titlebar_shadow: bool = True # Add shadow/border to custom title
                                        # bar windows
    detached_height: int = 0           # Fixed height for detached windows
                                       # (0 = auto)
    detached_scrollable: bool = True   # Add scrollbars if content exceeds
                                       # detached window size
    default_width: int = 200           # Default panel width
    min_width: int = 100               # Minimum panel width
    max_width: int = 0                 # Maximum panel width (0 = no limit)
    fixed_width: Optional[int] = None  # Fixed width (prevents resizing)
    detachable: bool = True            # Panel can be detached
    closable: bool = False             # Panel can be closed
    resizable: bool = True             # Panel can be resized
```

#### Smart Layout System (v1.2.0)

The enhanced window automatically detects the optimal layout system based on
pane configuration:

**Custom Layout (Fixed Panes):**

- Used when any pane has `fixed_width` set or `resizable=False`
- Provides visual sash separators without interactive resize handles
- Fixed panes maintain their specified widths
- Center pane automatically expands to fill remaining space
- Proper handling of detached panes (center expands when others detach)

**TTK PanedWindow Layout (Resizable Panes):**

- Used when all panes are fully resizable (`resizable=True` and no
  `fixed_width`)
- Provides standard TTK PanedWindow with interactive sash handles
- All panes can be resized by dragging sash handles
- Standard TTK PanedWindow behavior for detaching/reattaching

**Configuration Examples:**

```python
# Fixed width left pane - triggers custom layout
left_config = PaneConfig(fixed_width=200)

# Non-resizable right pane - triggers custom layout
right_config = PaneConfig(resizable=False, default_width=150)

# All resizable panes - uses TTK PanedWindow
left_config = PaneConfig(resizable=True)
center_config = PaneConfig(resizable=True)
right_config = PaneConfig(resizable=True)
```

#### Cross-Platform Icon Support

The enhanced window supports cross-platform icon display for detached windows:

**Supported Formats:**

- **Windows**: `.ico` (primary), `.png`, `.bmp`, `.gif` (secondary)
- **macOS**: `.png` (primary), `.gif`, `.bmp` (secondary), `.ico` (limited)
- **Linux**: `.png`, `.xbm` (primary), `.gif`, `.bmp` (secondary),
  `.ico` (limited)

**Icon Resolution Strategy:**

1. Check file existence
2. Detect format from extension
3. Use best method for format (iconbitmap for .ico, iconphoto for others)
4. Fallback to alternative methods if primary fails
5. Continue without icon if all methods fail

#### Utility Functions

##### `get_recommended_icon_formats()`

Get recommended icon formats for the current platform.

**Returns:** `List[str]` - List of recommended file extensions

##### `validate_icon_path(icon_path: str)`

Validate an icon path for cross-platform compatibility.

**Parameters:**

- `icon_path`: Path to icon file

**Returns:** `Tuple[bool, str]` - (is_valid, message)

#### Example Usage: EnhancedDockableThreePaneWindow

```python
import tkinter as tk
from threepanewindows.enhanced_dockable import (
    EnhancedDockableThreePaneWindow,
    PaneConfig,
    get_recommended_icon_formats,
    validate_icon_path
)

# Check recommended formats for current platform
formats = get_recommended_icon_formats()
print(f"Recommended formats: {formats}")

# Validate icon before use
is_valid, message = validate_icon_path("icons/app.png")
print(f"Icon validation: {message}")

# Configure panels with icons
left_config = PaneConfig(
    title="File Explorer",
    icon="📁",                          # Unicode icon for header
    window_icon="icons/explorer.png",   # File icon for detached window
    default_width=250,
    min_width=200,
    max_width=400,
    detachable=True
)

center_config = PaneConfig(
    title="Editor",
    icon="📝",
    detachable=False  # Center panel typically not detachable
)

right_config = PaneConfig(
    title="Properties",
    icon="🔧",
    window_icon="icons/properties.ico",  # Windows .ico file
    default_width=200,
    detachable=True
)

def build_left(frame):
    tk.Label(frame, text="File Explorer").pack(pady=10)

def build_center(frame):
    text = tk.Text(frame)
    text.pack(fill='both', expand=True)

def build_right(frame):
    tk.Label(frame, text="Properties").pack(pady=10)

root = tk.Tk()
window = EnhancedDockableThreePaneWindow(
    root,
    left_config=left_config,
    center_config=center_config,
    right_config=right_config,
    left_builder=build_left,
    center_builder=build_center,
    right_builder=build_right,
    theme_name="blue"
)
window.pack(fill='both', expand=True)
root.mainloop()
```

## DockableThreePaneWindow

### Class: `DockableThreePaneWindow(tk.Frame)`

A sophisticated three-pane window with detachable left and right panels.

**Key Features:**

- **Detachable Panels**: Left and right panels can be detached into separate
  windows
- **Center Panel Expansion**: When side panels are detached, the center panel
  automatically expands to fill the available space
- **Automatic Reattachment**: Detached panels can be reattached by closing
  their windows or using reattach buttons
- **Flexible Layout**: Supports both resizable and fixed-width panel
  configurations

#### Constructor: DockableThreePaneWindow

```python
DockableThreePaneWindow(master=None, side_width=150, left_builder=None,
                       center_builder=None, right_builder=None, **kwargs)
```

**Parameters:**

- `master`: Parent widget (default: None)
- `side_width`: Width of side panels in pixels (default: 150)
- `left_builder`: Function to build left panel content (default: None)
- `center_builder`: Function to build center panel content (default: None)
- `right_builder`: Function to build right panel content (default: None)
- `**kwargs`: Additional arguments passed to tk.Frame

**Builder Function Signature:**

```python
def builder_function(frame):
    """
    Args:
        frame: The tkinter Frame to add widgets to
    """
    # Add your widgets here
    tk.Label(frame, text="Content").pack()
```

#### Methods (DockableThreePaneWindow)

##### `get_left_frame()`

Returns the left panel frame widget.

**Returns:** `ttk.Frame` - The left panel frame

##### `get_center_frame()`

Returns the center panel frame widget.

**Returns:** `ttk.Frame` - The center panel frame

##### `get_right_frame()`

Returns the right panel frame widget.

**Returns:** `ttk.Frame` - The right panel frame

#### DockableThreePaneWindow Properties

- `side_width`: Width of side panels
- `left_builder`: Left panel builder function
- `center_builder`: Center panel builder function
- `right_builder`: Right panel builder function
- `left_window`: Reference to detached left window (None if attached)
- `right_window`: Reference to detached right window (None if attached)

#### Example Usage: DockableThreePaneWindow

```python
import tkinter as tk
from threepanewindows import DockableThreePaneWindow

def build_left(frame):
    tk.Label(frame, text="File Explorer").pack(pady=10)
    # Add more widgets...

def build_center(frame):
    text = tk.Text(frame)
    text.pack(fill='both', expand=True)

def build_right(frame):
    tk.Label(frame, text="Properties").pack(pady=10)
    # Add more widgets...

root = tk.Tk()
window = DockableThreePaneWindow(
    root,
    side_width=200,
    left_builder=build_left,
    center_builder=build_center,
    right_builder=build_right
)
window.pack(fill='both', expand=True)
root.mainloop()
```

## FixedThreePaneLayout

### Class: `FixedThreePaneLayout(tk.Frame)`

A simple three-pane layout with fixed panel sizes and customizable appearance.

#### Constructor

```python
FixedThreePaneLayout(master, side_width=150, sash_width=2, **kwargs)
```bash

**Parameters:**

- `master`: Parent widget (required)
- `side_width`: Width of side panels in pixels (default: 150)
- `sash_width`: Width of separator bars in pixels (default: 2)
- `**kwargs`: Additional arguments passed to tk.Frame

#### Methods

##### `set_label_texts(left=None, center=None, right=None)`

Set the text labels for the panels.

**Parameters:**

- `left`: Text for left panel label (optional)
- `center`: Text for center panel label (optional)
- `right`: Text for right panel label (optional)

##### `add_to_left(widget)`

Add a widget to the left panel.

**Parameters:**

- `widget`: Tkinter widget to add

##### `add_to_center(widget)`

Add a widget to the center panel.

**Parameters:**

- `widget`: Tkinter widget to add

##### `add_to_right(widget)`

Add a widget to the right panel.

**Parameters:**

- `widget`: Tkinter widget to add

##### `clear_left()`

Remove all widgets from the left panel (except the label).

##### `clear_center()`

Remove all widgets from the center panel (except the label).

##### `clear_right()`

Remove all widgets from the right panel (except the label).

#### FixedThreePaneLayout Properties

##### `frame_left`

Returns the left panel frame.

**Returns:** `tk.Frame` - The left panel frame

##### `frame_center`

Returns the center panel frame.

**Returns:** `tk.Frame` - The center panel frame

##### `frame_right`

Returns the right panel frame.

**Returns:** `tk.Frame` - The right panel frame

#### Example Usage

```python
import tkinter as tk
from threepanewindows import FixedThreePaneLayout

root = tk.Tk()
layout = FixedThreePaneLayout(root, side_width=180)
layout.pack(fill='both', expand=True)

# Customize labels
layout.set_label_texts(
    left="Navigation",
    center="Workspace",
    right="Properties"
)

# Add content
layout.add_to_left(tk.Button(layout.frame_left, text="Menu 1"))
layout.add_to_center(tk.Text(layout.frame_center))
layout.add_to_right(tk.Label(layout.frame_right, text="Info"))

root.mainloop()
```

## Color Customization

### FixedThreePaneLayout Default Colors

- Left panel: `#3A7CA5` (blue)
- Center panel: `#FFFFFF` (white)
- Right panel: `#F4A261` (orange)
- Sash bars: `#888888` (gray)

You can customize colors by accessing the frame properties:

```python
layout = FixedThreePaneLayout(root)
layout.frame_left.config(bg="#FF0000")  # Red background
layout.frame_center.config(bg="#00FF00")  # Green background
layout.frame_right.config(bg="#0000FF")  # Blue background
```

## Best Practices

1. **Builder Functions**: Use builder functions with `DockableThreePaneWindow`
   for dynamic content that needs to be recreated when panels are
   detached/reattached.

2. **Widget Management**: With `FixedThreePaneLayout`, create widgets with the
   correct parent frame for better performance:

   ```python
   # Good
   widget = tk.Label(layout.frame_left, text="Content")
   layout.add_to_left(widget)

   # Also works, but less efficient
   widget = tk.Label(root, text="Content")
   layout.add_to_left(widget)
   ```

3. **Responsive Design**: Use `fill` and `expand` options appropriately:

   ```python
   # For center content that should resize
   layout.add_to_center(text_widget)  # Automatically uses fill='both',
                                       # expand=True

   # For side content that should stay fixed
   layout.add_to_left(button_widget)  # Uses default packing
   ```

4. **Memory Management**: Use `clear_*()` methods to properly clean up widgets
   when switching content.

## Error Handling

Both classes are designed to be robust, but consider these scenarios:

- **Invalid builder functions**: If a builder function raises an exception, the
  panel will be created but empty
- **Widget reparenting**: The `add_to_*` methods handle widget reparenting
  automatically
- **Window closing**: Detached windows automatically reattach when closed

## Performance Considerations

- `DockableThreePaneWindow` recreates panel content when detaching/reattaching
- `FixedThreePaneLayout` uses absolute positioning for optimal performance
- Both classes are suitable for complex applications with many widgets
