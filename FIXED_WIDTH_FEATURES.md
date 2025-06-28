# Fixed Width Pane Features

## Overview

All three ThreePaneWindows implementations now support optional fixed width panes and menu bar integration:

- **FixedThreePaneLayout**: Basic fixed layout with optional fixed pane widths
- **DockableThreePaneWindow**: Dockable panes with fixed width support
- **EnhancedDockableThreePaneWindow**: Professional UI with advanced fixed width configuration

## Key Features

### 🔒 Fixed Width Panes
- Left and right panes can be set to fixed widths that don't resize with the window
- Center pane automatically adjusts to fill remaining space
- Mixed configurations: some panes fixed, others resizable

### 📋 Menu Bar Integration
- All window types support optional menu bars
- Menu bars are properly integrated with the window layout
- Compatible with standard Tkinter Menu widgets

### ⚙️ Dynamic Width Control
- Change pane widths at runtime
- Enable/disable fixed width constraints dynamically
- Query current width settings and constraints

## Usage Examples

### FixedThreePaneLayout

```python
import tkinter as tk
from threepanewindows import FixedThreePaneLayout

root = tk.Tk()

# Create menu bar
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="New", command=lambda: print("New"))
menubar.add_cascade(label="File", menu=file_menu)

# Create layout with fixed left pane, resizable right pane
layout = FixedThreePaneLayout(
    root,
    left_fixed_width=200,    # Left pane fixed at 200px
    right_fixed_width=None,  # Right pane resizable (default behavior)
    menu_bar=menubar
)

# Dynamic width control
layout.set_left_width(250)      # Change left width to 250px
layout.set_right_width(180)     # Set right width to 180px (makes it fixed)

# Query width settings
print(f"Left fixed: {layout.is_left_fixed()}")    # True
print(f"Left width: {layout.get_left_width()}")   # 250
```

### DockableThreePaneWindow

```python
import tkinter as tk
from threepanewindows import DockableThreePaneWindow

def build_left(frame):
    tk.Label(frame, text="Fixed Width Panel").pack()

def build_center(frame):
    tk.Label(frame, text="Resizable Center").pack()

def build_right(frame):
    tk.Label(frame, text="Another Fixed Panel").pack()

root = tk.Tk()

# Create menu

menubar = tk.Menu(root)
# ... configure menu ...

# Create dockable window with fixed side panes
window = DockableThreePaneWindow(
    root,
    left_builder=build_left,
    center_builder=build_center,
    right_builder=build_right,
    left_fixed_width=180,   # Left pane fixed at 180px
    right_fixed_width=150,  # Right pane fixed at 150px
    menu_bar=menubar
)

# Dynamic control
window.set_left_fixed_width(220)     # Change to 220px
window.clear_right_fixed_width()     # Make right pane resizable
window.set_right_fixed_width(160)    # Make right pane fixed at 160px

# Query settings
print(f"Left fixed: {window.is_left_fixed()}")   # True
print(f"Right fixed: {window.is_right_fixed()}")  # True
```

### EnhancedDockableThreePaneWindow

```python
import tkinter as tk
from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

def build_sidebar(frame):
    tk.Label(frame, text="File Explorer").pack()

def build_editor(frame):
    tk.Text(frame).pack(fill=tk.BOTH, expand=True)

def build_properties(frame):
    tk.Label(frame, text="Properties Panel").pack()

root = tk.Tk()

# Configure panes with fixed widths
left_config = PaneConfig(
    title="Explorer",
    icon="📁",
    fixed_width=250,  # Fixed at 250px
    detachable=True
)

center_config = PaneConfig(
    title="Editor",
    icon="📝",
    detachable=False
)

right_config = PaneConfig(
    title="Properties",
    icon="🔧",
    fixed_width=200,  # Fixed at 200px
    detachable=True
)

# Create menu

menubar = tk.Menu(root)
# ... configure menu ...

# Create enhanced window
window = EnhancedDockableThreePaneWindow(
    root,
    left_config=left_config,
    center_config=center_config,
    right_config=right_config,
    left_builder=build_sidebar,
    center_builder=build_editor,
    right_builder=build_properties,
    menu_bar=menubar
)

# Dynamic control
window.set_pane_fixed_width("left", 300)      # Change left to 300px
window.clear_pane_fixed_width("right")        # Make right resizable
window.set_pane_fixed_width("right", 180)     # Make right fixed at 180px

# Query settings
print(f"Left fixed: {window.is_pane_fixed_width('left')}")   # True
print(f"Left width: {window.get_pane_width('left')}")        # 300
```

## API Reference

### FixedThreePaneLayout

#### Constructor Parameters
- `left_fixed_width: Optional[int]` - Fixed width for left pane (None = resizable)
- `right_fixed_width: Optional[int]` - Fixed width for right pane (None = resizable)
- `menu_bar: Optional[tk.Menu]` - Optional menu bar to integrate

#### Methods
- `set_left_width(width: int)` - Set left pane width (makes it fixed)
- `set_right_width(width: int)` - Set right pane width (makes it fixed)
- `get_left_width() -> int` - Get current left pane width
- `get_right_width() -> int` - Get current right pane width
- `is_left_fixed() -> bool` - Check if left pane has fixed width
- `is_right_fixed() -> bool` - Check if right pane has fixed width

### DockableThreePaneWindow

#### Constructor Parameters
- `left_fixed_width: Optional[int]` - Fixed width for left pane
- `right_fixed_width: Optional[int]` - Fixed width for right pane
- `menu_bar: Optional[tk.Menu]` - Optional menu bar

#### Methods
- `set_left_fixed_width(width: int)` - Set left pane to fixed width
- `set_right_fixed_width(width: int)` - Set right pane to fixed width
- `clear_left_fixed_width()` - Make left pane resizable
- `clear_right_fixed_width()` - Make right pane resizable
- `is_left_fixed() -> bool` - Check if left pane is fixed
- `is_right_fixed() -> bool` - Check if right pane is fixed

### EnhancedDockableThreePaneWindow

#### Constructor Parameters
- `menu_bar: Optional[tk.Menu]` - Optional menu bar

#### PaneConfig
- `fixed_width: Optional[int]` - Fixed width for the pane

#### Methods
- `set_pane_fixed_width(pane_side: str, width: int)` - Set pane to fixed width
- `clear_pane_fixed_width(pane_side: str)` - Make pane resizable
- `is_pane_fixed_width(pane_side: str) -> bool` - Check if pane is fixed
- `get_pane_width(pane_side: str) -> int` - Get current pane width

## Behavior Notes

### Fixed Width Behavior
- Fixed width panes maintain their width regardless of window resizing
- The center pane automatically adjusts to fill remaining space
- Fixed panes have weight=0 in the PanedWindow to prevent resizing
- Resizable panes have weight>0 to allow proportional resizing

### Menu Bar Integration
- Menu bars are automatically attached to the parent window
- Compatible with all standard Tkinter menu features
- Menu bars work with all three window types

### Detachment Behavior (Dockable/Enhanced)
- Fixed width settings are preserved when panes are detached
- Detached windows maintain the configured fixed width
- Width settings are restored when panes are reattached

### Dynamic Changes
- Width changes take effect immediately
- Switching between fixed and resizable modes is seamless
- All changes are compatible with existing content

## Testing

Run the comprehensive test suite:

```bash
python test_fixed_width_features.py
```

Or try the simple examples:

```bash
python simple_fixed_width_example.py
```

## Migration Guide

### Existing Code Compatibility
All existing code continues to work without changes. The new parameters are optional:


```python
# Old code - still works
layout = FixedThreePaneLayout(root, side_width=150)

# New code - with fixed width features
layout = FixedThreePaneLayout(root, side_width=150, left_fixed_width=200)
```

### Upgrading to Fixed Widths
To add fixed width support to existing applications:

1. Add the new parameters to your constructor calls
2. Optionally add menu bar integration
3. Use the new methods for dynamic width control

The center pane automatically adjusts, so no changes are needed for center pane content.