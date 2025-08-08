# ThreePaneWindows

[![PyPI version](https://img.shields.io/pypi/v/threepanewindows.svg)](https://pypi.org/project/threepanewindows/)
[![Python versions](https://img.shields.io/pypi/pyversions/threepanewindows.svg)](https://pypi.org/project/threepanewindows/)
[![CI Status](https://github.com/stntg/threepanewindows/workflows/CI/badge.svg)](https://github.com/stntg/threepanewindows/actions)
[![CodeFactor](https://www.codefactor.io/repository/github/stntg/threepanewindows/badge)](https://www.codefactor.io/repository/github/stntg/threepanewindows)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Professional three-pane window layouts for Tkinter applications with
flexible layouts, advanced theming, custom UI components, and comprehensive logging.**

## Features

### Core Layout Systems

- **FixedThreePaneWindow**: Simple fixed three-pane layout with customizable panels
- **DockableThreePaneWindow**: Sophisticated layout with detachable side panels
- **EnhancedDockableThreePaneWindow**: Professional-grade interface with advanced features
- **🆕 EnhancedFlexibleLayout**: Modern flexible layout system with weight-based distribution
- **🆕 Smart Layout System**: Automatic layout detection for optimal sash behavior

### Advanced Theming & UI Components

- **🆕 Central Theme Manager**: Unified theming system across all components
- **🆕 Custom Scrollbars**: Fully themeable scrollbars with cross-platform support
- **🆕 Custom Menu Bars**: Themeable menu bars that work on all platforms
- **Professional Theming**: Light, Dark, Blue, Green, Purple, System, and Native themes
- **Cross-Platform Icon Support**: Multiple formats (.ico, .png, .gif, .bmp, .xbm)

### Professional Features

- **Flexible Layout Configuration**: Weight-based pane distribution with constraints
- **Drag & Drop Interface**: Intuitive panel detaching by dragging headers
- **Fixed Width Control**: Panes can be set to fixed widths or remain resizable
- **Advanced Customization**: Configurable panel properties, icons, and constraints
- **Smart Positioning**: Intelligent window placement and sizing
- **Visual Feedback**: Professional hover effects and drag indicators
- **🆕 Comprehensive Logging**: Silent by default with configurable debug output
- **Cross-platform compatibility**: Windows, macOS, Linux

> **See [ENHANCED_FEATURES.md](https://github.com/stntg/threepanewindows/blob/main/ENHANCED_FEATURES.md)
> for complete documentation of the enhanced professional features.**
>
> **See [FLEXIBLE_LAYOUT_SYSTEM.md](https://github.com/stntg/threepanewindows/blob/main/FLEXIBLE_LAYOUT_SYSTEM.md)
> for comprehensive documentation of the new flexible layout system.**
>
> **See [CENTRAL_THEME_MANAGER.md](https://github.com/stntg/threepanewindows/blob/main/CENTRAL_THEME_MANAGER.md)
> for detailed documentation of the central theming system.**
>
> **See [CROSS_PLATFORM_ICONS.md](https://github.com/stntg/threepanewindows/blob/main/CROSS_PLATFORM_ICONS.md)
> for detailed cross-platform icon support documentation.**

## Requirements

- **Python**: 3.9 to 3.13
- **Dependencies**: None (uses Python standard library only)
- **Platforms**: Windows, macOS, Linux

## Installation

### From PyPI (Recommended)

```bash
pip install threepanewindows
```

### From Source

```bash
git clone https://github.com/stntg/threepanewindows.git
cd threepanewindows
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

### Dockable Three-Pane Window

```python
import tkinter as tk
from threepanewindows import DockableThreePaneWindow

def build_left(frame):
    tk.Label(frame, text="Left Panel").pack(pady=10)
    tk.Button(frame, text="Button 1").pack(pady=5)

def build_center(frame):
    tk.Label(frame, text="Center Panel").pack(pady=10)
    text = tk.Text(frame)
    text.pack(fill='both', expand=True, padx=10, pady=10)

def build_right(frame):
    tk.Label(frame, text="Right Panel").pack(pady=10)
    tk.Listbox(frame).pack(fill='both', expand=True, padx=10, pady=10)

root = tk.Tk()
root.title("Dockable Three-Pane Example")
root.geometry("900x600")

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

### Enhanced Professional Three-Pane Window (NEW!)

```python
import tkinter as tk
from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

def build_left(frame):
    tk.Label(frame, text="📁 File Explorer").pack(pady=10)
    # Add your file tree here

def build_center(frame):
    tk.Label(frame, text="📝 Code Editor").pack(pady=10)
    # Add your text editor here

def build_right(frame):
    tk.Label(frame, text="🔧 Properties").pack(pady=10)
    # Add your properties panel here

root = tk.Tk()
root.title("Professional IDE")
root.geometry("1200x800")

# Configure panels with professional settings
left_config = PaneConfig(
    title="Explorer",
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

# Create enhanced window with professional theming
window = EnhancedDockableThreePaneWindow(
    root,
    left_config=left_config,
    right_config=right_config,
    left_builder=build_left,
    center_builder=build_center,
    right_builder=build_right,
    theme_name="blue"  # Professional blue theme
)
window.pack(fill='both', expand=True)

root.mainloop()
```

### Enhanced Flexible Layout System (NEW!)

The new flexible layout system provides weight-based pane distribution with advanced configuration:

```python
import tkinter as tk
from threepanewindows import (
    EnhancedFlexibleLayout,
    FlexContainer,
    FlexPaneConfig,
    LayoutDirection
)

def build_explorer(frame):
    tk.Label(frame, text="📁 File Explorer", font=("Arial", 12, "bold")).pack(pady=5)
    # Add your file tree here
    for i in range(5):
        tk.Label(frame, text=f"📄 File {i+1}.py").pack(anchor="w", padx=10)

def build_editor(frame):
    tk.Label(frame, text="📝 Code Editor", font=("Arial", 12, "bold")).pack(pady=5)
    text = tk.Text(frame, wrap="word")
    text.pack(fill="both", expand=True, padx=5, pady=5)
    text.insert("1.0", "# Welcome to the flexible layout system!\nprint('Hello, World!')")

def build_properties(frame):
    tk.Label(frame, text="🔧 Properties", font=("Arial", 12, "bold")).pack(pady=5)
    # Add property controls
    for prop in ["Width", "Height", "Color", "Font"]:
        tk.Label(frame, text=f"{prop}:").pack(anchor="w", padx=10)

def build_console(frame):
    tk.Label(frame, text="💻 Console", font=("Arial", 12, "bold")).pack(pady=5)
    console = tk.Text(frame, height=6, bg="black", fg="green")
    console.pack(fill="both", expand=True, padx=5, pady=5)
    console.insert("1.0", ">>> Ready for input...\n")

root = tk.Tk()
root.title("Flexible Layout IDE")
root.geometry("1400x900")

# Configure flexible panes
explorer_config = FlexPaneConfig(
    name="explorer",
    title="File Explorer",
    weight=0.2,  # 20% of available space
    min_size=200,
    max_size=400,
    detachable=True,
    builder=build_explorer,
    icon="📁"
)

editor_config = FlexPaneConfig(
    name="editor",
    title="Code Editor",
    weight=0.6,  # 60% of available space
    min_size=400,
    detachable=True,
    builder=build_editor,
    icon="📝"
)

properties_config = FlexPaneConfig(
    name="properties",
    title="Properties",
    weight=0.2,  # 20% of available space
    min_size=150,
    max_size=300,
    detachable=True,
    builder=build_properties,
    icon="🔧"
)

console_config = FlexPaneConfig(
    name="console",
    title="Console",
    weight=0.3,  # 30% of bottom area
    min_size=100,
    detachable=True,
    builder=build_console,
    icon="💻"
)

# Create nested layout: horizontal main with vertical bottom section
bottom_container = FlexContainer(
    direction=LayoutDirection.HORIZONTAL,
    children=[editor_config, console_config],
    weight=0.7
)

main_layout = FlexContainer(
    direction=LayoutDirection.HORIZONTAL,
    children=[
        explorer_config,
        bottom_container,
        properties_config
    ]
)

# Create the flexible layout
layout = EnhancedFlexibleLayout(
    root,
    layout_config=main_layout,
    theme_name="dark"  # Use dark theme
)
layout.pack(fill="both", expand=True)

root.mainloop()
```

### Fixed Three-Pane Layout

```python
import tkinter as tk
from threepanewindows import FixedThreePaneLayout

root = tk.Tk()
root.title("Fixed Three-Pane Example")
root.geometry("800x500")

layout = FixedThreePaneLayout(root, side_width=180)
layout.pack(fill='both', expand=True)

# Customize panel labels
layout.set_label_texts(
    left="Navigation",
    center="Workspace",
    right="Properties"
)

# Add content to panels
layout.add_to_left(tk.Button(root, text="Menu Item 1"))
layout.add_to_center(tk.Text(root))
layout.add_to_right(tk.Label(root, text="Property 1"))

root.mainloop()
```

### Fixed Width Panes (NEW!)

All window types now support fixed width panes that don't resize with the
window:

```python
import tkinter as tk
from threepanewindows import DockableThreePaneWindow

def build_left(frame):
    tk.Label(frame, text="Fixed Width\n200px").pack(pady=10)

def build_center(frame):
    tk.Label(frame, text="Resizable Center").pack(pady=10)

def build_right(frame):
    tk.Label(frame, text="Fixed Width\n150px").pack(pady=10)

root = tk.Tk()

# Create menu bar
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="New", command=lambda: print("New"))
menubar.add_cascade(label="File", menu=file_menu)

# Create window with fixed width panes and menu
window = DockableThreePaneWindow(
    root,
    left_builder=build_left,
    center_builder=build_center,
    right_builder=build_right,
    left_fixed_width=200,   # Left pane fixed at 200px
    right_fixed_width=150,  # Right pane fixed at 150px
    menu_bar=menubar        # Integrated menu bar
)
window.pack(fill='both', expand=True)

# Dynamic width control
window.set_left_fixed_width(250)     # Change to 250px
window.clear_right_fixed_width()     # Make right pane resizable

root.mainloop()
```

> **See [FIXED_WIDTH_FEATURES.md](https://github.com/stntg/threepanewindows/blob/main/FIXED_WIDTH_FEATURES.md)
> for complete documentation of the fixed width and menu bar features.**

## Advanced Theming System (NEW!)

ThreePaneWindows now includes a powerful central theme manager that provides consistent theming across all components:

### Central Theme Manager

```python
import tkinter as tk
from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig
from threepanewindows.central_theme_manager import get_theme_manager, ThemeType

# Get the central theme manager
theme_manager = get_theme_manager()

# Set a global theme
theme_manager.set_theme(ThemeType.DARK)

# Create your application - theming is automatic
root = tk.Tk()
window = EnhancedDockableThreePaneWindow(root, theme_name="dark")

# All components will use the central theme automatically
```

### Available Themes

- **Light**: Clean, bright interface
- **Dark**: Modern dark theme with high contrast
- **Blue**: Professional blue theme
- **Green**: Nature-inspired green theme
- **Purple**: Creative purple theme
- **System**: Matches system theme preferences
- **Native**: Uses platform-native styling

### Custom Scrollbars and Menu Bars

```python
from threepanewindows.custom_scrollbar import ThemedScrollbar
from threepanewindows.custom_menubar import CustomMenubar, MenuItem

# Create themed scrollbar
scrollbar = ThemedScrollbar(parent, orient="vertical")

# Create custom themeable menubar
menubar = CustomMenubar(root)
menubar.add_menu("File", [
    MenuItem("New", command=new_file),
    MenuItem("Open", command=open_file),
    MenuItem("", separator=True),
    MenuItem("Exit", command=root.quit)
])
```

## Demo Application

Run the demo to see both layout types in action:

```bash
threepane-demo
```

Or run directly with Python:

```bash
python -m threepanewindows.examples
```

## Logging and Debugging

ThreePaneWindows includes a comprehensive logging system that is **silent by default**
but can be easily enabled for debugging and monitoring:

### Quick Start

```python
import threepanewindows

# Enable console logging
threepanewindows.enable_console_logging()

# Your application code - now with logging
window = threepanewindows.EnhancedDockableThreePaneWindow(root)
```

### Advanced Configuration

```python
import logging
import threepanewindows

# Enable file logging with debug level
threepanewindows.add_file_logging('debug.log', level=logging.DEBUG)

# Enable console logging with info level
threepanewindows.enable_console_logging(level=logging.INFO)

# Disable logging completely
threepanewindows.disable_logging()
```

### Custom Logger Configuration

```python
import logging

# Configure specific modules
logger = logging.getLogger('threepanewindows.themes')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('THEME: %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

> **See [docs/logging.md](docs/logging.md) for complete logging
> documentation and examples.**

## Development Logging

For developers working on the ThreePaneWindows library, comprehensive development logging tools are available:

### Quick Development Setup

```python
# Method 1: Automatic setup (easiest)
import setup_dev_logging  # Enables logging automatically

# Method 2: Development logger driver
# Run: python dev_logger.py --level DEBUG --file logs/dev.log
```

### Development Tools

- **`dev_logger.py`** - Full-featured development logger with examples and interactive mode
- **`setup_dev_logging.py`** - Quick import-and-go logging setup
- **`example_with_logging.py`** - Complete example showing logging in action
- **`start_dev_logging.bat`** - Windows batch file for easy access

### Interactive Development

```bash
# Interactive mode with logging enabled
python dev_logger.py --interactive

# Run examples with logging
python dev_logger.py --example basic --level DEBUG

# Test all logging levels
python dev_logger.py --test-levels
```

> **See [DEVELOPMENT_LOGGING.md](DEVELOPMENT_LOGGING.md) for complete development logging documentation.**

## System Requirements

- Python 3.9+
- tkinter (included with Python)

## License

This project is licensed under the MIT License.
