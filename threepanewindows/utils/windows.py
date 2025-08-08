"""
Windows-specific platform functionality.

This module provides Windows-specific implementations for icon handling,
titlebar customization, and other platform-specific features.
"""

import ctypes
import os
import tkinter as tk
from typing import Any, List, Tuple

from ..logging_config import get_logger
from .base import PlatformHandler

# Initialize logger for this module
logger = get_logger(__name__)


def set_windows_titlebar_color(hwnd: int, color_hex: str) -> None:
    """
    Set the Windows titlebar color using DWM API.

    Args:
        hwnd: Window handle
        color_hex: Color in hex format (e.g., '#ff0000')
    """
    color_hex = color_hex.lstrip("#")
    r, g, b = [int(color_hex[i : i + 2], 16) for i in (0, 2, 4)]
    colorref = r | (g << 8) | (b << 16)
    DWMWA_CAPTION_COLOR = 35

    try:
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_CAPTION_COLOR,
            ctypes.byref(ctypes.c_int(colorref)),
            ctypes.sizeof(ctypes.c_int),
        )
    except Exception as e:
        logger.warning("Failed to set Windows titlebar color: %s", e)


class WindowsPlatformHandler(PlatformHandler):
    """Windows-specific platform handler."""

    def get_recommended_icon_formats(self) -> List[str]:
        """Get recommended icon formats for Windows."""
        return [".ico", ".png", ".bmp", ".gif"]

    def validate_icon_path(self, icon_path: str) -> Tuple[bool, str]:
        """Validate an icon path for Windows."""
        if not icon_path:
            return True, "No icon specified"

        if not os.path.exists(icon_path):
            return False, f"Icon file not found: {icon_path}"

        _, ext = os.path.splitext(icon_path.lower())
        recommended = self.get_recommended_icon_formats()

        if ext not in recommended:
            return (
                False,
                f"Icon format '{ext}' not recommended for Windows. "
                f"Recommended formats: {', '.join(recommended)}",
            )

        # Additional Windows-specific validation
        if ext == ".ico":
            # .ico files are preferred on Windows
            return True, "ICO format is optimal for Windows"
        elif ext in [".png", ".bmp", ".gif"]:
            return True, f"{ext.upper()} format is supported on Windows"

        return True, "Icon format is supported"

    def set_window_icon(self, window: tk.Tk, icon_path: str) -> bool:
        """Set window icon using Windows-optimized methods."""
        if not os.path.exists(icon_path):
            logger.warning("Icon file not found: %s", icon_path)
            return False

        try:
            # Get file extension
            _, ext = os.path.splitext(icon_path.lower())

            # For .ico files, use iconbitmap (works best on Windows)
            if ext == ".ico":
                try:
                    window.iconbitmap(icon_path)
                    return True
                except tk.TclError:
                    # iconbitmap failed, fall through to iconphoto
                    pass

            # For other formats, use iconphoto
            if ext in (".png", ".gif", ".bmp"):
                try:
                    # Load image using PhotoImage
                    photo = self._load_icon_as_photo(icon_path)
                    window.iconphoto(True, photo)
                    # Keep a reference to prevent garbage collection
                    if not hasattr(window, "_icon_photos"):
                        window._icon_photos = []
                    window._icon_photos.append(photo)
                    return True
                except tk.TclError as e:
                    logger.warning(
                        "Could not load icon as PhotoImage '%s': %s", icon_path, e
                    )

            # If we get here, try iconbitmap as last resort
            try:
                window.iconbitmap(icon_path)
                return True
            except tk.TclError as e:
                logger.warning("Could not set icon '%s': %s", icon_path, e)
                return False

        except Exception as e:
            logger.error("Error setting window icon: %s", e)
            return False

    def apply_custom_titlebar(self, window: tk.Tk, theme_colors: Any) -> bool:
        """Apply Windows-specific titlebar customization."""
        try:
            # Try to get the window handle
            hwnd = window.winfo_id()
            # If it's a child window, get the parent
            parent_hwnd = ctypes.windll.user32.GetParent(hwnd)
            if parent_hwnd:
                hwnd = parent_hwnd

            # Set the titlebar color using Windows DWM API
            set_windows_titlebar_color(hwnd, theme_colors.primary_bg)
            return True
        except Exception as e:
            logger.warning("Could not set Windows titlebar color: %s", e)
            return False

    def is_dark_mode(self) -> bool:
        """Check if Windows is in dark mode."""
        try:
            # Try using darkdetect first (if available)
            import darkdetect  # type: ignore[import-untyped]

            return darkdetect.isDark() or False
        except ImportError:
            pass

        try:
            # Fallback: Check Windows registry for dark mode
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return value == 0  # 0 = dark mode, 1 = light mode
        except (ImportError, OSError, FileNotFoundError):
            pass

        return False

    def get_system_accent_color(self) -> str:
        """Get Windows system accent color."""
        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\DWM"
            )
            value, _ = winreg.QueryValueEx(key, "AccentColor")
            winreg.CloseKey(key)

            # Convert DWORD to hex color
            r = (value >> 0) & 0xFF
            g = (value >> 8) & 0xFF
            b = (value >> 16) & 0xFF
            return f"#{r:02x}{g:02x}{b:02x}"
        except (ImportError, OSError, FileNotFoundError):
            pass

        return "#0078d4"  # Default Windows blue

    def get_platform_native_colors(self, is_dark: bool = None) -> dict:
        """Get Windows native color scheme."""
        if is_dark is None:
            is_dark = self.is_dark_mode()

        accent_color = self.get_system_accent_color()

        if is_dark:
            return {
                "window_bg": "#202020",
                "content_bg": "#2d2d2d",
                "sidebar_bg": "#252525",
                "text_primary": "#ffffff",
                "text_secondary": "#cccccc",
                "text_tertiary": "#999999",
                "separator": "#404040",
                "accent": accent_color,
                "accent_secondary": self._adjust_color_brightness(accent_color, 0.8),
                "button_bg": "#404040",
                "button_hover": "#505050",
                "selection_bg": self._lighten_color(accent_color, 0.8),
                "border": "#404040",
            }
        else:
            return {
                "window_bg": "#ffffff",
                "content_bg": "#ffffff",
                "sidebar_bg": "#f3f3f3",
                "text_primary": "#000000",
                "text_secondary": "#323130",
                "text_tertiary": "#605e5c",
                "separator": "#edebe9",
                "accent": accent_color,
                "accent_secondary": self._adjust_color_brightness(accent_color, 1.2),
                "button_bg": "#f3f2f1",
                "button_hover": "#e1dfdd",
                "selection_bg": self._lighten_color(accent_color, 0.8),
                "border": "#d2d0ce",
            }

    def get_platform_typography(self) -> dict:
        """Get Windows native typography settings."""
        return {
            "font_family": "Segoe UI",
            "font_family_fallback": "Tahoma",
            "font_size_small": 9,
            "font_size_normal": 10,
            "font_size_large": 12,
            "font_size_title": 14,
            "font_weight_light": "normal",
            "font_weight_normal": "normal",
            "font_weight_medium": "bold",
            "font_weight_bold": "bold",
        }

    def _adjust_color_brightness(self, hex_color: str, factor: float) -> str:
        """Adjust the brightness of a hex color."""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            return hex_color

        try:
            r, g, b = [int(hex_color[i : i + 2], 16) for i in (0, 2, 4)]
            r = min(int(r * factor), 255)
            g = min(int(g * factor), 255)
            b = min(int(b * factor), 255)
            return f"#{r:02x}{g:02x}{b:02x}"
        except ValueError:
            return hex_color

    def _lighten_color(self, hex_color: str, factor: float) -> str:
        """Lighten a hex color by mixing it with white."""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            return hex_color

        try:
            r, g, b = [int(hex_color[i : i + 2], 16) for i in (0, 2, 4)]
            # Mix with white
            r = int(r + (255 - r) * factor)
            g = int(g + (255 - g) * factor)
            b = int(b + (255 - b) * factor)
            return f"#{r:02x}{g:02x}{b:02x}"
        except ValueError:
            return hex_color

    def create_platform_scrollbar(
        self, parent: tk.Widget, orient: str = "vertical", command=None, **kwargs
    ):
        """
        Create a Windows-optimized scrollbar using custom ThemedScrollbar.

        Args:
            parent: Parent widget
            orient: Orientation ("vertical" or "horizontal")
            command: Scroll command callback
            **kwargs: Additional arguments

        Returns:
            ThemedScrollbar widget for better Windows theming
        """
        try:
            from ..custom_scrollbar import ThemedScrollbar

            return ThemedScrollbar(parent, orient=orient, command=command, **kwargs)
        except ImportError:
            # Fallback to TTK scrollbar if custom scrollbar is not available
            logger.warning(
                "ThemedScrollbar not available, falling back to TTK scrollbar"
            )
            from tkinter import ttk

            return ttk.Scrollbar(parent, orient=orient, command=command, **kwargs)
