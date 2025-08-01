"""
Type stubs for threepanewindows package.

This package provides professional three-pane window layouts for Tkinter applications.
"""

from typing import Tuple

from ._version import FULL_VERSION as FULL_VERSION
from ._version import __version__ as __version__
from ._version import __version_info__ as __version_info__
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
from .themes import ThemeManager as ThemeManager
from .themes import ThemeType as ThemeType
from .themes import get_theme_manager as get_theme_manager
from .themes import set_global_theme as set_global_theme
from .logging_config import add_file_logging as add_file_logging
from .logging_config import disable_logging as disable_logging
from .logging_config import enable_console_logging as enable_console_logging

__author__: str
__email__: str
__license__: str
__copyright__: str

__all__ = [
    "__version__",
    "__version_info__",
    "FULL_VERSION",
    "FixedThreePaneWindow",
    "FixedThreePaneLayout",
    "DockableThreePaneWindow",
    "EnhancedDockableThreePaneWindow",
    "PaneConfig",
    "get_recommended_icon_formats",
    "validate_icon_path",
    "ThemeManager",
    "get_theme_manager",
    "set_global_theme",
    "ThemeType",
    "enable_console_logging",
    "disable_logging",
    "add_file_logging",
]
