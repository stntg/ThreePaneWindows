"""
Platform-specific functionality for ThreePaneWindows.

This module provides platform-specific implementations that are automatically
selected based on the current operating system.
"""

import platform
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import PlatformHandler as BasePlatformHandler

# Determine the current platform and import the appropriate handler
_system = platform.system().lower()
_platform_name = sys.platform

if _platform_name == "win32" or _system == "windows":
    from .windows import WindowsPlatformHandler as PlatformHandler
elif _platform_name == "darwin" or _system == "darwin":
    from .macos import MacOSPlatformHandler as PlatformHandler
else:
    # Linux and other Unix-like systems
    from .linux import LinuxPlatformHandler as PlatformHandler

# Create the global platform handler instance
platform_handler: "BasePlatformHandler" = PlatformHandler()

# Export the handler and common functions
__all__ = [
    "platform_handler",
    "get_recommended_icon_formats",
    "validate_icon_path",
    "set_window_icon",
    "apply_custom_titlebar",
    "is_dark_mode",
    "get_system_accent_color",
    "get_platform_native_colors",
    "get_platform_typography",
    "create_platform_scrollbar",
]


def get_recommended_icon_formats():
    """
    Get recommended icon formats for the current platform.

    Returns:
        List[str]: List of file extensions in order of preference for the current platform.
    """
    return platform_handler.get_recommended_icon_formats()


def validate_icon_path(icon_path: str):
    """
    Validate an icon path for the current platform.

    Args:
        icon_path (str): Path to the icon file to validate.

    Returns:
        Tuple[bool, str]: (is_valid, message) indicating validation result.
    """
    return platform_handler.validate_icon_path(icon_path)


def set_window_icon(window, icon_path: str):
    """
    Set window icon using platform-specific method.

    Args:
        window: The Tkinter window to set the icon for.
        icon_path (str): Path to the icon file.

    Returns:
        bool: True if successful, False otherwise.
    """
    return platform_handler.set_window_icon(window, icon_path)


def apply_custom_titlebar(window, theme_colors):
    """
    Apply custom titlebar styling for the current platform.

    Args:
        window: The Tkinter window to apply styling to.
        theme_colors: Theme color scheme object.

    Returns:
        bool: True if custom titlebar was applied, False otherwise.
    """
    return platform_handler.apply_custom_titlebar(window, theme_colors)


def is_dark_mode():
    """
    Check if the system is in dark mode.

    Returns:
        bool: True if dark mode is enabled, False otherwise.
    """
    return platform_handler.is_dark_mode()


def get_system_accent_color():
    """
    Get the system accent color.

    Returns:
        str: Hex color string for the system accent color.
    """
    return platform_handler.get_system_accent_color()


def get_platform_native_colors(is_dark=None):
    """
    Get platform-specific native color scheme.

    Args:
        is_dark (Optional[bool]): Override dark mode detection.

    Returns:
        dict: Dictionary of native platform colors.
    """
    return platform_handler.get_platform_native_colors(is_dark)


def get_platform_typography():
    """
    Get platform-specific typography settings.

    Returns:
        dict: Dictionary of typography settings including font family and sizes.
    """
    return platform_handler.get_platform_typography()


def create_platform_scrollbar(parent, orient="vertical", command=None, **kwargs):
    """
    Create a platform-appropriate scrollbar.

    On Windows: Uses custom ThemedScrollbar for better theming
    On macOS/Linux: Uses native TTK scrollbar for better system integration

    Args:
        parent: Parent widget
        orient: Orientation ("vertical" or "horizontal")
        command: Scroll command callback
        **kwargs: Additional arguments

    Returns:
        Scrollbar widget (native or custom based on platform)
    """
    return platform_handler.create_platform_scrollbar(parent, orient, command, **kwargs)
