"""
ThreePaneWindows - Professional three-pane window layouts for Tkinter applications.

This package provides sophisticated three-pane window layouts with advanced features:
- Enhanced flexible layout system with weight-based distribution (NEW v1.3.0)
- Central theme manager with unified theming (NEW v1.3.0)
- Custom UI components: scrollbars and menu bars (NEW v1.3.0)
- Comprehensive logging system (NEW v1.3.0)
- Fixed and dockable layouts
- Professional theming system
- Cross-platform icon support (.ico, .png, .gif, .bmp, .xbm)
- Drag-and-drop pane management
- Resizable panes with constraints
- Cross-platform compatibility

Main Components:
    - EnhancedFlexibleLayout: Modern flexible layout with weight-based distribution (NEW v1.3.0)
    - CentralThemeManager: Unified theming system across all components (NEW v1.3.0)
    - ThemedScrollbar: Fully themeable custom scrollbar (NEW v1.3.0)
    - CustomMenubar: Cross-platform themeable menu bar (NEW v1.3.0)
    - FixedThreePaneWindow: Simple fixed three-pane layout
    - DockableThreePaneWindow: Advanced layout with docking capabilities
    - EnhancedDockableThreePaneWindow: Full-featured layout with all bells and whistles
    - ThemeManager: Legacy theming system

Quick Start:
    >>> import tkinter as tk
    >>> from threepanewindows import FixedThreePaneWindow
    >>>
    >>> root = tk.Tk()
    >>> window = FixedThreePaneWindow(root)
    >>> window.pack(fill=tk.BOTH, expand=True)
    >>>
    >>> # Add content to panes
    >>> tk.Label(window.left_pane, text="Left").pack()
    >>> tk.Label(window.center_pane, text="Center").pack()
    >>> tk.Label(window.right_pane, text="Right").pack()
"""

from ._version import FULL_VERSION, __version__, __version_info__
from .dockable import DockableThreePaneWindow
from .enhanced_dockable import (
    EnhancedDockableThreePaneWindow,
    PaneConfig,
    get_recommended_icon_formats,
    validate_icon_path,
)
from .fixed import FixedThreePaneLayout, FixedThreePaneWindow
from .flexible import (
    EnhancedFlexibleLayout,
    FlexContainer,
    FlexPaneConfig,
    LayoutDirection,
)
from .logging_config import add_file_logging, disable_logging, enable_console_logging
from .themes import ThemeManager, ThemeType, get_theme_manager, set_global_theme

# Metadata
__author__ = "Stan Griffiths"
__email__ = "stantgriffiths@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2025 Stan Griffiths"

# Public API
__all__ = [
    # Version info
    "__version__",
    "__version_info__",
    "FULL_VERSION",
    # Main window classes
    "FixedThreePaneWindow",
    "FixedThreePaneLayout",  # Legacy alias
    "DockableThreePaneWindow",
    "EnhancedDockableThreePaneWindow",
    "EnhancedFlexibleLayout",
    # Configuration classes
    "PaneConfig",
    "FlexPaneConfig",
    "FlexContainer",
    "LayoutDirection",
    # Icon utilities
    "get_recommended_icon_formats",
    "validate_icon_path",
    # Theming system
    "ThemeManager",
    "get_theme_manager",
    "set_global_theme",
    "ThemeType",
    # Logging system
    "enable_console_logging",
    "disable_logging",
    "add_file_logging",
]

# Note: FixedThreePaneWindow is the modern name, FixedThreePaneLayout is legacy
# Trigger workflow
