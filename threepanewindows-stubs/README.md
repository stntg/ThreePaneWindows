# ThreePaneWindows Type Stubs

This package contains type stubs for the `threepanewindows` library,
providing type hints for better IDE support and static type checking.

## Requirements

- **Python**: 3.9 to 3.13
- **Compatible with**: threepanewindows >= 1.3.0

## Installation

```bash
pip install threepanewindows-stubs
```

## Usage

Once installed, your IDE and type checkers (like mypy) will automatically
use these stubs when working with the `threepanewindows` library.

## What's Included

The stubs cover all public APIs of the threepanewindows library:

- **Core Layout Systems**:
  - `EnhancedFlexibleLayout` *(NEW v1.3.0)*
  - `FixedThreePaneWindow` / `FixedThreePaneLayout`
  - `DockableThreePaneWindow`
  - `EnhancedDockableThreePaneWindow`

- **Configuration Classes**:
  - `FlexPaneConfig` *(NEW v1.3.0)*
  - `FlexContainer` *(NEW v1.3.0)*
  - `LayoutDirection` *(NEW v1.3.0)*
  - `PaneConfig`

- **Advanced Theming & UI Components** *(NEW v1.3.0)*:
  - `CentralThemeManager`
  - `ThemedScrollbar`
  - `CustomMenubar`
  - `MenuItem`
  - `ThemeType` (extended)
  - `ThemeColors`

- **Legacy Theming System**:
  - `ThemeManager`
  - `ColorScheme`
  - `Typography`
  - `Spacing`
  - `Theme`

- **Logging System** *(NEW v1.3.0)*:
  - `ThreePaneWindowsLogger`
  - `get_logger()`

- **Utility Functions**:
  - `get_recommended_icon_formats()`
  - `validate_icon_path()`
  - `get_theme_manager()`
  - `set_global_theme()`

- **Platform-Specific Utilities**:
  - Cross-platform icon support
  - System theme detection
  - Window appearance configuration

## License

These stubs are provided under the same license as the original
threepanewindows library (MIT).
