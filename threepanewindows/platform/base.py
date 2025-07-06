"""
Base platform handler interface.

This module defines the abstract base class that all platform-specific
handlers must implement.
"""

import os
import tkinter as tk
from abc import ABC, abstractmethod
from typing import Any, List, Tuple


class PlatformHandler(ABC):
    """Abstract base class for platform-specific functionality."""

    @abstractmethod
    def get_recommended_icon_formats(self) -> List[str]:
        """
        Get the recommended icon formats for this platform.

        Returns:
            List of file extensions in order of preference (e.g., ['.ico', '.png'])
        """
        pass

    @abstractmethod
    def validate_icon_path(self, icon_path: str) -> Tuple[bool, str]:
        """
        Validate an icon path for this platform.

        Args:
            icon_path: Path to the icon file

        Returns:
            Tuple of (is_valid, message)
        """
        pass

    @abstractmethod
    def set_window_icon(self, window: tk.Tk, icon_path: str) -> bool:
        """
        Set the window icon using platform-specific methods.

        Args:
            window: The Tkinter window
            icon_path: Path to the icon file

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def apply_custom_titlebar(self, window: tk.Tk, theme_colors: Any) -> bool:
        """
        Apply custom titlebar styling for this platform.

        Args:
            window: The Tkinter window
            theme_colors: Theme color scheme object

        Returns:
            True if custom titlebar was applied, False otherwise
        """
        pass

    def is_dark_mode(self) -> bool:
        """
        Check if the system is in dark mode.

        Returns:
            True if dark mode is enabled, False otherwise
        """
        return False

    def get_system_accent_color(self) -> str:
        """
        Get the system accent color.

        Returns:
            Hex color string for the system accent color
        """
        return "#0078d4"  # Default blue

    def get_platform_native_colors(self, is_dark: bool = None) -> dict:
        """
        Get platform-specific native color scheme.

        Args:
            is_dark: Override dark mode detection

        Returns:
            Dictionary of native platform colors
        """
        return {}

    def get_platform_typography(self) -> dict:
        """
        Get platform-specific typography settings.

        Returns:
            Dictionary of typography settings
        """
        return {
            "font_family": "Segoe UI",
            "font_size_small": 9,
            "font_size_normal": 10,
            "font_size_large": 12,
            "font_size_title": 14,
        }

    def _is_icon_file(self, path: str) -> bool:
        """Check if a string is likely an icon file path."""
        if not isinstance(path, str) or len(path) < 4:
            return False

        if not os.path.exists(path):
            return False

        # Check for common icon file extensions (cross-platform)
        icon_extensions = (".ico", ".png", ".gif", ".bmp", ".xbm")
        path_lower = path.lower()

        return any(path_lower.endswith(ext) for ext in icon_extensions)

    def _load_icon_as_photo(self, icon_path: str) -> tk.PhotoImage:
        """
        Load an icon file as a PhotoImage.

        Args:
            icon_path: Path to the icon file

        Returns:
            PhotoImage object

        Raises:
            tk.TclError: If the image cannot be loaded
        """
        return tk.PhotoImage(file=icon_path)
