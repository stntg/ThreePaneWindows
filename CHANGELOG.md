# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

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