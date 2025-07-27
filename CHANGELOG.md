# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-01-20

### Added

- **Enhanced Cross-Platform Theming System**: Complete theme management with multiple theme types (light, dark, blue, green, purple, system, native)
- **Platform Utilities Framework**: New `utils` package with Windows, macOS, and Linux platform handlers
- **Professional Type Stubs Package**: Complete type annotations with separate stubs distribution for enhanced IDE support
- **Comprehensive Documentation**: Professional docstring coverage across all modules, classes, and methods
- **Cross-Platform Icon Support**: Enhanced detached windows now support multiple icon formats (.ico, .png, .gif, .bmp, .xbm) with automatic platform optimization
- **Icon Utility Functions**: Added `get_recommended_icon_formats()` and `validate_icon_path()` for better icon management
- **Platform-Specific Optimizations**: Automatic icon format selection and fallback mechanisms for Windows, macOS, and Linux
- **Native Theme Detection**: Automatic system theme detection and integration across platforms
- **Professional Color Schemes**: Multiple professionally designed color schemes with proper contrast ratios

### Changed

- **Development Status**: Promoted from Beta to Production/Stable release
- **Python Support**: Updated minimum Python version from 3.7 to 3.9, added Python 3.13 support (now supports 3.9-3.13)
- **Theme Management**: Completely redesigned theming system with platform-specific theme detection
- **Code Quality**: Enhanced code quality with comprehensive docstrings following imperative mood conventions
- **Enhanced Icon Handling**: Improved icon loading with better error handling and cross-platform compatibility
- **PaneConfig Documentation**: Updated window_icon field to reflect multi-format support
- **Platform Behavior**: Added platform-specific window behavior optimizations for detached windows
- **Developer Experience**: Improved IDE support with complete type annotations and stubs

### Fixed

- **Docstring Compliance**: Fixed all docstring formatting issues and missing documentation
- **Icon Display Issues**: Fixed icon display problems on Linux and macOS platforms
- **Format Compatibility**: Resolved .ico file compatibility issues on non-Windows platforms
- **Theme Application**: Fixed theme application consistency across different UI components

### Security

## [1.0.4] - 2025-01-20

### Fixed

- **Critical Fix**: Center panel now properly expands when side panels are detached
- Removed placeholder frames that were preventing center panel expansion in DockableThreePaneWindow
- Fixed layout issue where detached panels left empty spaces instead of allowing center panel to fill available area

### Added

- Comprehensive test suite for DockableThreePaneWindow functionality
- New test cases covering detach/reattach behavior and center panel expansion

### Changed

- Improved DockableThreePaneWindow detach mechanism for better space utilization
- Enhanced layout behavior when panels are detached/reattached

## [1.0.3] - 2025-01-20

### Added

- Added comprehensive CHANGELOG.md with complete version history
- CHANGELOG.md now included in package distribution

### Changed

- Updated package documentation to include changelog
- Improved package metadata completeness

## [1.0.2] - 2025-01-20

### Fixed

- Fixed broken documentation links in PyPI package description
- Documentation files now included in package distribution via MANIFEST.in
- README links now use absolute GitHub URLs instead of relative paths

### Changed

- Updated package manifest to include ENHANCED_FEATURES.md and FIXED_WIDTH_FEATURES.md
- Improved PyPI package metadata and description

## [1.0.1] - 2025-01-20

### Fixed

- Fixed detach button bug where detached windows incorrectly showed "Detach" buttons instead of "Reattach" buttons
- Improved panel sizing consistency for fixed-width panels

### Added

- Added Fixed Width Dockable Demo to examples
- Enhanced demo selector with new demonstration option

### Changed

- Updated version management across all configuration files
- Improved build process compatibility

## [1.0.0] - 2025-01-20

### Added

- **✨ NEW: EnhancedDockableThreePaneWindow**: Professional-grade interface with advanced features
- **🔒 NEW: Fixed Width Panes**: Optional fixed-width panes that don't resize with the window
- **📋 NEW: Menu Bar Integration**: Built-in support for menu bars across all window types
- **Professional Theming System**: Light, Dark, and Blue Professional themes
- **Drag & Drop Interface**: Intuitive panel detaching by dragging headers
- **Advanced Customization**: Configurable panel properties, icons, and constraints
- **PaneConfig class**: Professional configuration system for panel settings
- **Smart Positioning**: Intelligent window placement and sizing
- **Visual Feedback**: Professional hover effects and drag indicators

### Enhanced Features

- **Professional UI**: Modern, professional appearance with smooth interactions
- **Theme Support**: Multiple built-in themes (light, dark, blue professional)
- **Fixed Width Control**: Panes can be set to fixed widths or remain resizable
- **Menu Integration**: Seamless menu bar support across all window types
- **Enhanced Examples**: Comprehensive demonstration applications
- **Improved Documentation**: Complete feature documentation and guides

### Technical Improvements

- Enhanced type hints and code documentation
- Improved error handling and validation
- Better separation of concerns in codebase
- Comprehensive testing for new features

## [0.1.0] - 2024-12-18

### Added

- Initial release of ThreePaneWindows library
- `DockableThreePaneWindow` class with detachable side panels
- `FixedThreePaneLayout` class with fixed three-pane layout
- Builder pattern support for content creation
- Comprehensive test suite
- Example applications and demos
- Full documentation and README

### Features

- **DockableThreePaneWindow**:
  - Detachable left and right panels
  - Customizable panel widths
  - Builder functions for dynamic content creation
  - Automatic reattachment on window close
  - Resizable panels with PanedWindow

- **FixedThreePaneLayout**:
  - Fixed-width side panels
  - Customizable panel colors and labels
  - Widget management methods (add_to_*, clear_*)
  - Property accessors for frame references
  - Automatic layout management

### Technical Details

- Python 3.7+ compatibility
- Pure Tkinter implementation (no external dependencies)
- Cross-platform support (Windows, macOS, Linux)
- Comprehensive unit tests with 100% coverage
- Installable via pip with proper package structure
