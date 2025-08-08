"""
Type stubs for threepanewindows package.

This package provides professional three-pane window layouts for Tkinter applications
with advanced features including flexible layouts, central theme management, custom
scrollbars, and comprehensive logging.
"""

from typing import Tuple

# Version information
from ._version import FULL_VERSION as FULL_VERSION
from ._version import __version__ as __version__
from ._version import __version_info__ as __version_info__

# NEW: Central theme manager
from .central_theme_manager import CentralThemeManager as CentralThemeManager
from .central_theme_manager import ThemeColors as ThemeColors
from .central_theme_manager import get_theme_manager as get_central_theme_manager
from .central_theme_manager import set_global_theme as set_central_theme

# NEW: Custom UI components
from .custom_menubar import CustomMenubar as CustomMenubar
from .custom_menubar import MenuItem as MenuItem
from .custom_scrollbar import ThemedScrollbar as ThemedScrollbar

# Main window classes
from .dockable import DockableThreePaneWindow as DockableThreePaneWindow
from .enhanced_dockable import (
    EnhancedDockableThreePaneWindow as EnhancedDockableThreePaneWindow,
)
from .enhanced_dockable import PaneConfig as PaneConfig
from .enhanced_dockable import (
    get_recommended_icon_formats as get_recommended_icon_formats,
)
from .enhanced_dockable import validate_icon_path as validate_icon_path
from .fixed import FixedThreePaneLayout as FixedThreePaneLayout
from .fixed import FixedThreePaneWindow as FixedThreePaneWindow

# NEW: Flexible layout system
from .flexible import EnhancedFlexibleLayout as EnhancedFlexibleLayout
from .flexible import FlexContainer as FlexContainer
from .flexible import FlexPaneConfig as FlexPaneConfig
from .flexible import LayoutDirection as LayoutDirection

# Logging system
from .logging_config import add_file_logging as add_file_logging
from .logging_config import disable_logging as disable_logging
from .logging_config import enable_console_logging as enable_console_logging

# Theme management systems
from .themes import ThemeManager as ThemeManager
from .themes import ThemeType as ThemeType
from .themes import get_theme_manager as get_theme_manager
from .themes import set_global_theme as set_global_theme

__author__: str
__email__: str
__license__: str
__copyright__: str

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
    # Theming systems
    "ThemeManager",
    "get_theme_manager",
    "set_global_theme",
    "ThemeType",
    "CentralThemeManager",
    "ThemeColors",
    "get_central_theme_manager",
    "set_central_theme",
    # Custom UI components
    "CustomMenubar",
    "MenuItem",
    "ThemedScrollbar",
    # Logging system
    "enable_console_logging",
    "disable_logging",
    "add_file_logging",
]
