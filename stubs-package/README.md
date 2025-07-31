# ThreePaneWindows Type Stubs

This package contains type stubs for the `threepanewindows` library, providing type
hints for better IDE support and static type checking.

## Requirements

- **Python**: 3.9 to 3.13
- **Compatible with**: threepanewindows >= 1.0.0

## Installation

```bash
pip install threepanewindows-stubs
```

## Usage

Once installed, your IDE and type checkers (like mypy) will automatically use these
stubs when working with the `threepanewindows` library.

## What's Included

The stubs cover all public APIs of the threepanewindows library:

- **Main Window Classes**:
  - `FixedThreePaneWindow` / `FixedThreePaneLayout`
  - `DockableThreePaneWindow`
  - `EnhancedDockableThreePaneWindow`

- **Configuration Classes**:
  - `PaneConfig`

- **Theming System**:
  - `ThemeManager`
  - `ThemeType`
  - `ColorScheme`
  - `Typography`
  - `Spacing`
  - `Theme`

- **Utility Functions**:
  - `get_recommended_icon_formats()`
  - `validate_icon_path()`
  - `get_theme_manager()`
  - `set_global_theme()`

- **Platform-Specific Utilities**:
  - Cross-platform icon support
  - System theme detection
  - Window appearance configuration

## System Requirements

- Python 3.9+
- threepanewindows library

## License

These stubs are provided under the same license as the original
threepanewindows library (MIT).
