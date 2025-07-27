# ThreePaneWindows

[![PyPI version](https://img.shields.io/pypi/v/threepanewindows.svg)](https://pypi.org/project/threepanewindows/)
[![Python versions](https://img.shields.io/pypi/pyversions/threepanewindows.svg)](https://pypi.org/project/threepanewindows/)
[![CI Status](https://github.com/stntg/threepanewindows/workflows/CI/badge.svg)](https://github.com/stntg/threepanewindows/actions)
[![CodeFactor](https://www.codefactor.io/repository/github/stntg/threepanewindows/badge)](https://www.codefactor.io/repository/github/stntg/threepanewindows)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Professional three-pane window layouts for Tkinter applications with docking, theming, and advanced UI components.**

## Features

- **DockableThreePaneWindow**: A sophisticated three-pane layout with detachable side panels and automatic center panel expansion
- **FixedThreePaneLayout**: A simple fixed three-pane layout with customizable panels
- **✨ NEW: EnhancedDockableThreePaneWindow**: Professional-grade interface with advanced features
- **🔒 NEW: Fixed Width Panes**: Optional fixed-width panes that don't resize with the window
- **📋 NEW: Menu Bar Integration**: Built-in support for menu bars across all window types
- Easy-to-use builder pattern for content creation
- Fully customizable panel sizes and colors
- Dynamic width control and constraint management
- Cross-platform compatibility (Windows, macOS, Linux)

### 🎨 Enhanced Professional Features (NEW!)

- **Professional Theming System**: Light, Dark, and Blue Professional themes
- **Cross-Platform Icon Support**: Multiple icon formats (.ico, .png, .gif, .bmp, .xbm) with automatic platform optimization
- **Drag & Drop Interface**: Intuitive panel detaching by dragging headers
- **Advanced Customization**: Configurable panel properties, icons, and constraints
- **Fixed Width Control**: Panes can be set to fixed widths or remain resizable
- **Menu Bar Integration**: Seamless menu bar support across all window types
- **Beautiful UI**: Modern, professional appearance with smooth interactions
- **Smart Positioning**: Intelligent window placement and sizing
- **Visual Feedback**: Professional hover effects and drag indicators

> 📖 **See [ENHANCED_FEATURES.md](https://github.com/stntg/threepanewindows/blob/main/ENHANCED_FEATURES.md) for complete documentation of the new professional features.**
>
> 🖼️ **See [CROSS_PLATFORM_ICONS.md](https://github.com/stntg/threepanewindows/blob/main/CROSS_PLATFORM_ICONS.md) for detailed cross-platform icon support documentation.**

## Installation

### From Source
```bash
git clone <repository-url>
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

### ✨ Enhanced Professional Three-Pane Window (NEW!)

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

### 🔒 Fixed Width Panes (NEW!)

All window types now support fixed width panes that don't resize with the window:

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

> 📖 **See [FIXED_WIDTH_FEATURES.md](https://github.com/stntg/threepanewindows/blob/main/FIXED_WIDTH_FEATURES.md) for complete documentation of the fixed width and menu bar features.**

## Demo Application

Run the demo to see both layout types in action:

```bash
threepane-demo
```

Or run directly with Python:

```bash
python -m threepanewindows.examples
```

## Requirements

- Python 3.9+
- tkinter (included with Python)

## License

This project is licensed under the MIT License.
