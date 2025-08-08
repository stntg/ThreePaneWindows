# Enhanced Flexible Layout System

The Enhanced Flexible Layout System is a powerful new addition to ThreePaneWindows
that provides weight-based pane distribution with advanced configuration options.
This system allows you to create complex, nested layouts with professional
detached window management.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Core Components](#core-components)
- [Basic Usage](#basic-usage)
- [Advanced Configuration](#advanced-configuration)
- [Nested Layouts](#nested-layouts)
- [Theming Integration](#theming-integration)
- [API Reference](#api-reference)

## Overview

The Enhanced Flexible Layout System introduces a new paradigm for creating
sophisticated UI layouts in Tkinter applications. Unlike traditional fixed
layouts, this system uses weight-based distribution to automatically manage
pane sizes while respecting minimum and maximum constraints.

### Key Benefits

- **Weight-based Distribution**: Panes automatically resize based on their
  assigned weights
- **Nested Layouts**: Create complex hierarchical layouts with containers
- **Professional Detached Windows**: Full-featured detached window management
- **Constraint Management**: Minimum and maximum size constraints
- **Theme Integration**: Seamless integration with the central theme manager
- **Dynamic Reconfiguration**: Runtime layout modifications

## Key Features

### 🎯 Weight-Based Distribution

```python
# Panes automatically distribute space based on weights
explorer_config = FlexPaneConfig(name="explorer", weight=0.2)  # 20%
editor_config = FlexPaneConfig(name="editor", weight=0.6)      # 60%
properties_config = FlexPaneConfig(name="properties", weight=0.2)  # 20%
```

### 🏗️ Nested Container Support

```python
# Create complex nested layouts
bottom_section = FlexContainer(
    direction=LayoutDirection.HORIZONTAL,
    children=[editor_config, console_config]
)

main_layout = FlexContainer(
    direction=LayoutDirection.HORIZONTAL,
    children=[explorer_config, bottom_section, properties_config]
)
```

### 🎨 Professional Detached Windows

- Custom titlebars with theme integration
- Scrollable content support
- Proper window restoration
- Icon and title customization

### 📏 Advanced Constraints

- Minimum and maximum size limits
- Detachable/non-detachable panes
- Custom window dimensions for detached panes

## Core Components

### FlexPaneConfig

Configuration class for individual panes:

```python
@dataclass
class FlexPaneConfig:
    name: str                    # Unique identifier
    title: str                   # Display title
    weight: float = 1.0          # Weight for space distribution
    min_size: int = 100          # Minimum size in pixels
    max_size: Optional[int] = None  # Maximum size (None = unlimited)
    detachable: bool = True      # Can be detached
    builder: Optional[Callable] = None  # Content builder function

    # Detached window properties
    custom_titlebar: bool = True
    default_width: int = 500
    detached_height: int = 400
    min_width: int = 300
    max_width: int = 0          # 0 = no limit
    detached_scrollable: bool = False
    window_icon: str = ""
    icon: str = ""
```

### FlexContainer

Container for organizing panes and sub-containers:

```python
@dataclass
class FlexContainer:
    direction: LayoutDirection   # HORIZONTAL or VERTICAL
    children: List[Union[FlexPaneConfig, FlexContainer]]
    weight: float = 1.0         # Weight within parent container
    min_size: int = 100
    max_size: Optional[int] = None
```

### EnhancedFlexibleLayout

Main layout class:

```python
class EnhancedFlexibleLayout(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        layout_config: FlexContainer,
        theme_name: str = "light",
        **kwargs
    ):
```

## Basic Usage

### Simple Three-Pane Layout

```python
import tkinter as tk
from threepanewindows import (
    EnhancedFlexibleLayout,
    FlexContainer,
    FlexPaneConfig,
    LayoutDirection
)

def build_left(frame):
    tk.Label(frame, text="Left Panel").pack(pady=10)

def build_center(frame):
    tk.Text(frame).pack(fill="both", expand=True)

def build_right(frame):
    tk.Listbox(frame).pack(fill="both", expand=True)

# Configure panes
left_config = FlexPaneConfig(
    name="left",
    title="Navigation",
    weight=0.25,
    builder=build_left
)

center_config = FlexPaneConfig(
    name="center",
    title="Content",
    weight=0.5,
    builder=build_center
)

right_config = FlexPaneConfig(
    name="right",
    title="Properties",
    weight=0.25,
    builder=build_right
)

# Create layout container
layout_config = FlexContainer(
    direction=LayoutDirection.HORIZONTAL,
    children=[left_config, center_config, right_config]
)

# Create and display layout
root = tk.Tk()
layout = EnhancedFlexibleLayout(root, layout_config)
layout.pack(fill="both", expand=True)
root.mainloop()
```

## Advanced Configuration

### IDE-Style Layout with Console

```python
def create_ide_layout():
    # File explorer
    explorer_config = FlexPaneConfig(
        name="explorer",
        title="File Explorer",
        weight=0.2,
        min_size=200,
        max_size=400,
        icon="📁",
        builder=build_file_explorer
    )

    # Code editor
    editor_config = FlexPaneConfig(
        name="editor",
        title="Code Editor",
        weight=0.7,
        min_size=400,
        icon="📝",
        builder=build_code_editor
    )

    # Console (bottom section)
    console_config = FlexPaneConfig(
        name="console",
        title="Console",
        weight=0.3,
        min_size=100,
        icon="💻",
        builder=build_console
    )

    # Properties panel
    properties_config = FlexPaneConfig(
        name="properties",
        title="Properties",
        weight=0.2,
        min_size=150,
        max_size=300,
        icon="🔧",
        builder=build_properties
    )

    # Create nested layout
    # Main editor area with console below
    editor_section = FlexContainer(
        direction=LayoutDirection.VERTICAL,
        children=[editor_config, console_config],
        weight=0.6
    )

    # Complete layout
    main_layout = FlexContainer(
        direction=LayoutDirection.HORIZONTAL,
        children=[explorer_config, editor_section, properties_config]
    )

    return main_layout
```

## Nested Layouts

### Complex Multi-Level Nesting

```python
def create_complex_layout():
    # Top toolbar area
    toolbar_config = FlexPaneConfig(
        name="toolbar",
        title="Toolbar",
        weight=0.1,
        min_size=40,
        max_size=60,
        detachable=False,
        builder=build_toolbar
    )

    # Left sidebar with tabs
    files_config = FlexPaneConfig(name="files", title="Files", weight=0.5,
                                   builder=build_files)
    search_config = FlexPaneConfig(name="search", title="Search", weight=0.3,
                                    builder=build_search)
    git_config = FlexPaneConfig(name="git", title="Git", weight=0.2,
                                 builder=build_git)

    left_sidebar = FlexContainer(
        direction=LayoutDirection.VERTICAL,
        children=[files_config, search_config, git_config],
        weight=0.2
    )

    # Main content area
    editor_tabs = FlexPaneConfig(name="editor", title="Editor", weight=0.7,
                                  builder=build_editor)
    terminal = FlexPaneConfig(name="terminal", title="Terminal", weight=0.3,
                               builder=build_terminal)

    main_content = FlexContainer(
        direction=LayoutDirection.VERTICAL,
        children=[editor_tabs, terminal],
        weight=0.6
    )

    # Right sidebar
    outline_config = FlexPaneConfig(name="outline", title="Outline", weight=0.4,
                                     builder=build_outline)
    problems_config = FlexPaneConfig(name="problems", title="Problems",
                                      weight=0.3, builder=build_problems)
    debug_config = FlexPaneConfig(name="debug", title="Debug", weight=0.3,
                                   builder=build_debug)

    right_sidebar = FlexContainer(
        direction=LayoutDirection.VERTICAL,
        children=[outline_config, problems_config, debug_config],
        weight=0.2
    )

    # Content area (below toolbar)
    content_area = FlexContainer(
        direction=LayoutDirection.HORIZONTAL,
        children=[left_sidebar, main_content, right_sidebar],
        weight=0.9
    )

    # Complete layout
    return FlexContainer(
        direction=LayoutDirection.VERTICAL,
        children=[toolbar_config, content_area]
    )
```

## Theming Integration

The flexible layout system integrates seamlessly with the central theme manager:

```python
from threepanewindows.central_theme_manager import get_theme_manager, ThemeType

# Set global theme
theme_manager = get_theme_manager()
theme_manager.set_theme(ThemeType.DARK)

# Create layout with theme
layout = EnhancedFlexibleLayout(
    root,
    layout_config,
    theme_name="dark"  # Automatically applies theme
)

# Change theme at runtime
layout.apply_theme("blue")
```

### Custom Theme Colors

```python
# Access theme colors for custom styling
colors = theme_manager.current_colors

# Apply to custom widgets
custom_widget.configure(
    bg=colors.panel_bg,
    fg=colors.text_fg,
    selectbackground=colors.accent_color
)
```

## API Reference

### EnhancedFlexibleLayout Methods

#### Layout Management

- `get_pane(name: str) -> Optional[tk.Frame]` - Get pane frame by name
- `get_layout_info() -> Dict[str, Any]` - Get current layout information
- `save_layout_state() -> Dict[str, Any]` - Save current layout state
- `restore_layout_state(state: Dict[str, Any]) -> bool` - Restore layout state

#### Detached Window Management

- `detach_pane(name: str) -> bool` - Detach a pane to separate window
- `reattach_pane(name: str) -> bool` - Reattach a detached pane
- `is_pane_detached(name: str) -> bool` - Check if pane is detached
- `get_detached_windows() -> List[tk.Toplevel]` - Get all detached windows
- `close_all_detached() -> None` - Close all detached windows

#### Configuration Management

- `get_pane_config(name: str) -> Optional[FlexPaneConfig]` - Get pane configuration
- `update_pane_config(name: str, **kwargs) -> bool` - Update pane configuration

#### Theming

- `apply_theme(theme_name: str) -> None` - Apply theme to layout

### Events and Callbacks

The flexible layout system supports various events:

```python
def on_pane_detached(pane_name: str, window: tk.Toplevel):
    print(f"Pane {pane_name} was detached")

def on_pane_reattached(pane_name: str):
    print(f"Pane {pane_name} was reattached")

# Register event handlers (implementation-specific)
layout.bind_event("pane_detached", on_pane_detached)
layout.bind_event("pane_reattached", on_pane_reattached)
```

## Best Practices

### Weight Distribution

- Use weights that sum to 1.0 for predictable behavior
- Reserve larger weights (0.4-0.6) for main content areas
- Use smaller weights (0.1-0.3) for sidebars and toolbars

### Constraint Management

- Always set reasonable minimum sizes to prevent unusable panes
- Use maximum sizes sparingly, mainly for toolbars and status bars
- Consider different screen sizes when setting constraints

### Performance Optimization

- Minimize deep nesting levels (3-4 levels maximum recommended)
- Use lazy loading for pane content when possible
- Implement efficient builder functions

### User Experience

- Make primary content areas non-detachable for stability
- Provide clear visual indicators for detachable panes
- Save and restore layout state for user preferences

## Migration from Traditional Layouts

### From FixedThreePaneWindow

```python
# Old approach
window = FixedThreePaneWindow(root, side_width=200)

# New flexible approach
left_config = FlexPaneConfig(name="left", weight=0.25, min_size=200)
center_config = FlexPaneConfig(name="center", weight=0.5)
right_config = FlexPaneConfig(name="right", weight=0.25, min_size=200)

layout_config = FlexContainer(
    direction=LayoutDirection.HORIZONTAL,
    children=[left_config, center_config, right_config]
)

layout = EnhancedFlexibleLayout(root, layout_config)
```

### From DockableThreePaneWindow

```python
# Old approach
window = DockableThreePaneWindow(
    root,
    left_builder=build_left,
    center_builder=build_center,
    right_builder=build_right
)

# New flexible approach with enhanced detaching
left_config = FlexPaneConfig(
    name="left",
    builder=build_left,
    detachable=True,
    custom_titlebar=True
)
# ... configure other panes

layout = EnhancedFlexibleLayout(root, layout_config)
```

The Enhanced Flexible Layout System represents the future of ThreePaneWindows,
providing unprecedented flexibility while maintaining the ease of use that
makes the library popular.
