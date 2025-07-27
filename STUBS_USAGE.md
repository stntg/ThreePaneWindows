# ThreePaneWindows Type Stubs Usage Guide

This document explains how to use the type stubs for the `threepanewindows` library.

## Overview

The type stubs provide complete type annotations for the threepanewindows library, enabling:
- Better IDE support with autocompletion and error detection
- Static type checking with tools like mypy
- Improved code documentation and maintainability

## Installation

### Option 1: Install from the stubs package directory
```bash
cd stubs-package
pip install -e .
```

### Option 2: Build and install the stub package
```bash
cd stubs-package
python setup.py sdist bdist_wheel
pip install dist/threepanewindows_stubs-1.0.4-py3-none-any.whl
```

## Usage Examples

### Basic Fixed Layout with Type Hints

```python
import tkinter as tk
from threepanewindows import FixedThreePaneWindow

def main() -> None:
    root = tk.Tk()
    root.title("Typed Three-Pane Window")

    # Type checker will know the exact type and available methods
    window: FixedThreePaneWindow = FixedThreePaneWindow(
        root,
        left_width=200,
        right_width=250,
        min_pane_size=100
    )
    window.pack(fill=tk.BOTH, expand=True)

    # IDE will provide autocompletion for these methods
    window.set_label_texts(
        left="File Explorer",
        center="Editor",
        right="Properties"
    )

    # Type-safe access to panes
    left_pane: tk.Frame = window.left_pane
    center_pane: tk.Frame = window.center_pane
    right_pane: tk.Frame = window.right_pane

    root.mainloop()

if __name__ == "__main__":
    main()
```

### Enhanced Layout with Configuration

```python
import tkinter as tk
from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig
from typing import Optional

def build_content(frame: tk.Widget) -> None:
    """Content builder with proper typing."""
    label = tk.Label(frame, text="Sample Content")
    label.pack(pady=10)

def main() -> None:
    root = tk.Tk()

    # Properly typed configuration
    left_config = PaneConfig(
        title="Explorer",
        detachable=True,
        default_width=280,
        min_width=200,
        custom_titlebar=True
    )

    # Type checker validates all parameters
    window: EnhancedDockableThreePaneWindow = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        left_builder=build_content,
        theme_name="dark",
        show_status_bar=True,
        enable_animations=True
    )
    window.pack(fill=tk.BOTH, expand=True)

    # Type-safe theme management
    current_theme = window.get_current_theme()
    window.set_theme("blue")

    root.mainloop()

if __name__ == "__main__":
    main()
```

### Theme Management with Types

```python
from threepanewindows import (
    get_theme_manager,
    ThemeManager,
    ThemeType,
)
from threepanewindows.themes import (
    ColorScheme,
    Typography,
    Spacing,
    Theme
)

def setup_custom_theme() -> None:
    """Example of type-safe theme customization."""
    theme_manager: ThemeManager = get_theme_manager()

    # Create custom color scheme with type checking
    custom_colors = ColorScheme(
        primary_bg="#2d3748",
        secondary_bg="#4a5568",
        primary_text="#ffffff",
        accent_text="#63b3ed"
    )

    # Create and register custom theme
    custom_theme = Theme(
        name="Custom Dark",
        colors=custom_colors,
        enable_animations=True,
        corner_radius=6
    )

    theme_manager.register_theme(custom_theme)
    theme_manager.set_theme("Custom Dark")
```

## Type Checking with mypy

Create a `mypy.ini` configuration file:

```ini
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True

[mypy-threepanewindows.*]
# Stubs are available, so require type annotations
disallow_untyped_defs = True
```

Run type checking:
```bash
mypy your_application.py
```

## IDE Configuration

### VS Code
Install the Python extension and ensure these settings in `settings.json`:
```json
{
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true
}
```

### PyCharm
The stubs will be automatically detected. Enable type checking in:
- Settings → Editor → Inspections → Python → Type checker

## Available Types

### Main Classes
- `FixedThreePaneWindow` / `FixedThreePaneLayout`
- `DockableThreePaneWindow`
- `EnhancedDockableThreePaneWindow`

### Configuration
- `PaneConfig` - Complete pane configuration
- `ColorScheme` - Theme color definitions
- `Typography` - Font and text styling
- `Spacing` - Layout spacing configuration
- `Theme` - Complete theme definition

### Enums
- `ThemeType` - Available theme types

### Utility Functions
- `get_recommended_icon_formats() -> List[str]`
- `validate_icon_path(icon_path: str) -> Tuple[bool, str]`
- `get_theme_manager() -> ThemeManager`
- `set_global_theme(theme_name: Union[str, ThemeType]) -> None`

## Benefits

1. **IDE Support**: Full autocompletion and parameter hints
2. **Error Detection**: Catch type-related errors before runtime
3. **Documentation**: Types serve as inline documentation
4. **Refactoring**: Safer code refactoring with type information
5. **Code Quality**: Enforces consistent API usage

## Troubleshooting

### Stubs Not Found
If your IDE doesn't recognize the stubs:
1. Ensure the stubs package is installed in the same environment
2. Restart your IDE
3. Check that `py.typed` file exists in the stubs directory

### Type Errors
If you encounter type errors:
1. Verify you're using the correct parameter types
2. Check the stub definitions for the expected signatures
3. Use `# type: ignore` comments for known false positives

### Missing Types
If some types are missing:
1. Check if you're using a newer version of the library
2. The stubs may need updating for new features
3. Consider contributing improvements to the stubs

## Contributing

To improve the stubs:
1. Identify missing or incorrect type annotations
2. Update the relevant `.pyi` files
3. Run `python verify_stubs.py` to validate changes
4. Test with your IDE and mypy

The stubs are designed to be comprehensive and accurate, covering all public APIs of the threepanewindows library.
