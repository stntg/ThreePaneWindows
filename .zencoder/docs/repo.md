# ThreePaneWindows Information

## Summary

ThreePaneWindows is a Python library that provides professional three-pane window layouts for Tkinter applications. It offers sophisticated UI components with features like docking, theming, and cross-platform icon support. The library includes multiple window types: fixed layouts, dockable layouts, and enhanced professional layouts with advanced features.

## Structure

- **threepanewindows/**: Core package containing the main implementation
  - **dockable.py**: Implementation of DockableThreePaneWindow
  - **enhanced_dockable.py**: Implementation of EnhancedDockableThreePaneWindow
  - **fixed.py**: Implementation of FixedThreePaneWindow/Layout
  - **themes.py**: Theming system implementation
  - **cli.py**: Command-line interface
  - **examples.py**: Example applications and demo
- **tests/**: Test suite for the package
- **docs/**: Documentation source files
- **scripts/**: Utility scripts for development and release
- **dev_files/**: Development resources and examples

## Language & Runtime

**Language**: Python
**Version**: Python 3.8+ (supports 3.8, 3.9, 3.10, 3.11, 3.12)
**Build System**: setuptools
**Package Manager**: pip

## Dependencies

**Main Dependencies**:

- tkinter (included in Python standard library)
- typing-extensions (for Python < 3.10)

**Development Dependencies**:

- pytest (>=7.0)
- pytest-cov (>=4.0)
- pytest-xvfb (>=2.0, Linux only)
- black (>=22.0)
- flake8 (>=5.0)
- mypy (>=1.0)
- isort (>=5.0)
- pre-commit (>=2.20)
- sphinx (>=5.0, for documentation)

## Build & Installation

```bash
# Basic installation
pip install threepanewindows

# From source
git clone https://github.com/stntg/threepanewindows.git
cd threepanewindows
pip install -e .

# Development installation
pip install -e ".[dev]"

# Documentation installation
pip install -e ".[docs]"
```

## Main Entry Points

**Package Entry Points**:

- `threepane`: CLI tool for running demos and displaying information
- `threepane-demo`: Direct access to run the interactive demo

**Main Classes**:

- `FixedThreePaneWindow`: Simple fixed three-pane layout
- `DockableThreePaneWindow`: Advanced layout with docking capabilities
- `EnhancedDockableThreePaneWindow`: Full-featured layout with professional features
- `ThemeManager`: Professional theming system

## Testing

**Framework**: pytest
**Test Location**: tests/ directory
**Naming Convention**: test_*.py files with test_* functions
**Configuration**: pytest.ini, pytest_ci.ini, pytest_py38.ini
**Run Command**:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=threepanewindows

# Run CI workflow tests (Python 3.9+)
pytest -c pytest_ci.ini tests/ -m "not gui"

# Run CI workflow tests (Python 3.8)
pytest -c pytest_py38.ini tests/ -m "not gui" -k "not test_demo_integration_with_mainloop and not test_run_demo_creates_window and not test_examples_no_longer_hang"

# Run specific test categories
pytest -m "not slow"
pytest -m "not gui"
```

## Features

- Multiple window layout types (fixed, dockable, enhanced)
- Professional theming system with light, dark, and blue themes
- Cross-platform icon support (.ico, .png, .gif, .bmp, .xbm)
- Drag & drop interface for panel detaching
- Fixed width panes that don't resize with the window
- Menu bar integration across all window types
- Fully customizable panel sizes, colors, and constraints
- Cross-platform compatibility (Windows, macOS, Linux)
