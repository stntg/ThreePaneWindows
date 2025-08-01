"""
Linux-specific platform functionality.

This module provides Linux-specific implementations for icon handling,
titlebar customization, and other platform-specific features.
"""

import os
import shutil
import tkinter as tk
from typing import Any, List, Tuple

from ..logging_config import get_logger
from .base import PlatformHandler

# Initialize logger for this module
logger = get_logger(__name__)


class LinuxPlatformHandler(PlatformHandler):
    """Linux-specific platform handler."""

    def get_recommended_icon_formats(self) -> List[str]:
        """Get recommended icon formats for Linux."""
        return [".png", ".xbm", ".gif", ".bmp", ".ico"]

    def validate_icon_path(self, icon_path: str) -> Tuple[bool, str]:
        """Validate an icon path for Linux."""
        if not icon_path:
            return True, "No icon specified"

        if not os.path.exists(icon_path):
            return False, f"Icon file not found: {icon_path}"

        _, ext = os.path.splitext(icon_path.lower())
        recommended = self.get_recommended_icon_formats()

        if ext not in recommended:
            return (
                False,
                f"Icon format '{ext}' not recommended for Linux. "
                f"Recommended formats: {', '.join(recommended)}",
            )

        # Additional Linux-specific validation
        if ext == ".png":
            # PNG files are preferred on Linux
            return True, "PNG format is optimal for Linux"
        elif ext == ".xbm":
            return True, "XBM format is well-supported on Linux"
        elif ext in [".gif", ".bmp"]:
            return True, f"{ext.upper()} format is supported on Linux"
        elif ext == ".ico":
            return True, "ICO format is supported but PNG is preferred on Linux"

        return True, "Icon format is supported"

    def set_window_icon(self, window: tk.Tk, icon_path: str) -> bool:
        """Set window icon using Linux-optimized methods."""
        if not os.path.exists(icon_path):
            logger.warning("Icon file not found: %s", icon_path)
            return False

        try:
            # Get file extension
            _, ext = os.path.splitext(icon_path.lower())

            # On Linux, iconphoto generally works better than iconbitmap
            if ext in (".png", ".gif", ".bmp", ".xbm"):
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

            # For .ico files or as fallback, try iconbitmap
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
        """Apply Linux-specific titlebar customization."""
        # On Linux, we generally don't customize the titlebar as extensively
        # as on Windows or macOS, since window managers handle this
        # However, we can still apply some basic theming
        try:
            # Set window background to match theme
            window.configure(bg=theme_colors.primary_bg)

            # On some Linux desktop environments, we can set window properties
            # that might influence the titlebar appearance
            try:
                # Try to set window class for better integration with window managers
                window.wm_class("ThreePaneWindows", "ThreePaneWindows")
            except (tk.TclError, AttributeError):
                pass

            return True
        except Exception as e:
            logger.warning("Could not apply Linux titlebar customization: %s", e)
            return False

    def get_desktop_environment(self) -> str:
        """
        Detect the desktop environment on Linux.

        Returns:
            String identifying the desktop environment (e.g., 'gnome', 'kde', 'xfce')
        """
        try:
            # Try to detect desktop environment
            desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
            if desktop:
                return desktop

            # Fallback methods
            if os.environ.get("GNOME_DESKTOP_SESSION_ID"):
                return "gnome"
            elif os.environ.get("KDE_FULL_SESSION"):
                return "kde"
            elif os.environ.get("DESKTOP_SESSION"):
                return os.environ.get("DESKTOP_SESSION", "").lower()

            return "unknown"
        except (OSError, KeyError):
            return "unknown"

    def supports_transparency(self) -> bool:
        """
        Check if the current Linux environment supports window transparency.

        Returns:
            True if transparency is supported, False otherwise
        """
        try:
            # Check if compositor is running (basic check)
            desktop = self.get_desktop_environment()

            # Most modern desktop environments support transparency
            if desktop in ["gnome", "kde", "xfce", "cinnamon", "mate"]:
                return True

            # Check for common compositors
            try:
                import subprocess  # nosec B404

                # Use full path to pgrep for security
                pgrep_path = shutil.which("pgrep")
                if pgrep_path:
                    result = subprocess.run(  # nosec B603
                        [pgrep_path, "-x", "compton"],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        check=False,  # Don't raise exception on non-zero exit
                    )
                    if result.returncode == 0:
                        return True

                    result = subprocess.run(  # nosec B603
                        [pgrep_path, "-x", "picom"],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        check=False,  # Don't raise exception on non-zero exit
                    )
                    if result.returncode == 0:
                        return True
            except (
                ImportError,
                OSError,
                subprocess.SubprocessError,
                subprocess.TimeoutExpired,
            ):
                pass

            return False
        except (ImportError, OSError, Exception):
            return False

    def is_dark_mode(self) -> bool:
        """Check if Linux desktop is in dark mode."""
        try:
            # Try using darkdetect first (if available)
            import darkdetect  # type: ignore[import-untyped]

            return darkdetect.isDark() or False
        except ImportError:
            pass

        try:
            # Check GNOME settings
            import subprocess  # nosec B404

            # Use full path to gsettings for security
            gsettings_path = shutil.which("gsettings")
            if gsettings_path:
                result = subprocess.run(  # nosec B603
                    [gsettings_path, "get", "org.gnome.desktop.interface", "gtk-theme"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,  # Don't raise exception on non-zero exit
                )
                theme_name = result.stdout.strip().strip("'\"").lower()
                return "dark" in theme_name
        except (
            subprocess.SubprocessError,
            subprocess.TimeoutExpired,
            FileNotFoundError,
        ):
            pass

        try:
            # Check KDE settings
            import subprocess  # nosec B404

            # Use full path to kreadconfig5 for security
            kreadconfig_path = shutil.which("kreadconfig5")
            if kreadconfig_path:
                result = subprocess.run(  # nosec B603
                    [kreadconfig_path, "--group", "General", "--key", "ColorScheme"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,  # Don't raise exception on non-zero exit
                )
                color_scheme = result.stdout.strip().lower()
                return "dark" in color_scheme or "breeze dark" in color_scheme
        except (
            subprocess.SubprocessError,
            subprocess.TimeoutExpired,
            FileNotFoundError,
        ):
            pass

        # Check environment variables
        gtk_theme = os.environ.get("GTK_THEME", "").lower()
        if "dark" in gtk_theme:
            return True

        return False

    def get_system_accent_color(self) -> str:
        """Get Linux system accent color."""
        try:
            # Try to get GNOME accent color
            import subprocess  # nosec B404

            # Use full path to gsettings for security
            gsettings_path = shutil.which("gsettings")
            if gsettings_path:
                result = subprocess.run(  # nosec B603
                    [
                        gsettings_path,
                        "get",
                        "org.gnome.desktop.interface",
                        "accent-color",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,  # Don't raise exception on non-zero exit
                )
                if result.returncode == 0:
                    color = result.stdout.strip().strip("'\"")
                    if color and color != "blue":  # Default is blue
                        # Map GNOME accent color names to hex
                        gnome_colors = {
                            "red": "#e01b24",
                            "orange": "#ff7800",
                            "yellow": "#f5c211",
                            "green": "#33d17a",
                            "blue": "#3584e4",
                            "purple": "#9141ac",
                            "pink": "#f66151",
                            "slate": "#6f8396",
                        }
                        return gnome_colors.get(color, "#3584e4")
        except (
            subprocess.SubprocessError,
            subprocess.TimeoutExpired,
            FileNotFoundError,
        ):
            pass

        return "#3584e4"  # Default blue

    def get_platform_native_colors(self, is_dark: bool = None) -> dict:
        """Get Linux native color scheme."""
        if is_dark is None:
            is_dark = self.is_dark_mode()

        accent_color = self.get_system_accent_color()
        desktop = self.get_desktop_environment()

        if is_dark:
            if desktop == "gnome":
                return {
                    "window_bg": "#242424",
                    "content_bg": "#303030",
                    "sidebar_bg": "#2a2a2a",
                    "text_primary": "#ffffff",
                    "text_secondary": "#cccccc",
                    "text_tertiary": "#999999",
                    "separator": "#404040",
                    "accent": accent_color,
                    "accent_secondary": self._adjust_color_brightness(
                        accent_color, 0.8
                    ),
                    "button_bg": "#404040",
                    "button_hover": "#505050",
                    "selection_bg": self._lighten_color(accent_color, 0.8),
                    "border": "#404040",
                }
            elif desktop == "kde":
                return {
                    "window_bg": "#232629",
                    "content_bg": "#2a2e32",
                    "sidebar_bg": "#31363b",
                    "text_primary": "#fcfcfc",
                    "text_secondary": "#bdc3c7",
                    "text_tertiary": "#7f8c8d",
                    "separator": "#4d4d4d",
                    "accent": accent_color,
                    "accent_secondary": self._adjust_color_brightness(
                        accent_color, 0.8
                    ),
                    "button_bg": "#31363b",
                    "button_hover": "#3daee9",
                    "selection_bg": self._lighten_color(accent_color, 0.8),
                    "border": "#4d4d4d",
                }
            else:
                # Generic dark theme
                return {
                    "window_bg": "#2e2e2e",
                    "content_bg": "#3c3c3c",
                    "sidebar_bg": "#353535",
                    "text_primary": "#ffffff",
                    "text_secondary": "#cccccc",
                    "text_tertiary": "#999999",
                    "separator": "#555555",
                    "accent": accent_color,
                    "accent_secondary": self._adjust_color_brightness(
                        accent_color, 0.8
                    ),
                    "button_bg": "#555555",
                    "button_hover": "#666666",
                    "selection_bg": self._lighten_color(accent_color, 0.8),
                    "border": "#555555",
                }
        else:
            if desktop == "gnome":
                return {
                    "window_bg": "#ffffff",
                    "content_bg": "#ffffff",
                    "sidebar_bg": "#fafafa",
                    "text_primary": "#2e3436",
                    "text_secondary": "#555753",
                    "text_tertiary": "#888a85",
                    "separator": "#d3d7cf",
                    "accent": accent_color,
                    "accent_secondary": self._adjust_color_brightness(
                        accent_color, 1.2
                    ),
                    "button_bg": "#e9e9e7",
                    "button_hover": "#d3d7cf",
                    "selection_bg": self._lighten_color(accent_color, 0.8),
                    "border": "#babdb6",
                }
            elif desktop == "kde":
                return {
                    "window_bg": "#fcfcfc",
                    "content_bg": "#ffffff",
                    "sidebar_bg": "#eff0f1",
                    "text_primary": "#232629",
                    "text_secondary": "#31363b",
                    "text_tertiary": "#7f8c8d",
                    "separator": "#bdc3c7",
                    "accent": accent_color,
                    "accent_secondary": self._adjust_color_brightness(
                        accent_color, 1.2
                    ),
                    "button_bg": "#eff0f1",
                    "button_hover": "#3daee9",
                    "selection_bg": self._lighten_color(accent_color, 0.8),
                    "border": "#bdc3c7",
                }
            else:
                # Generic light theme
                return {
                    "window_bg": "#ffffff",
                    "content_bg": "#ffffff",
                    "sidebar_bg": "#f5f5f5",
                    "text_primary": "#000000",
                    "text_secondary": "#333333",
                    "text_tertiary": "#666666",
                    "separator": "#cccccc",
                    "accent": accent_color,
                    "accent_secondary": self._adjust_color_brightness(
                        accent_color, 1.2
                    ),
                    "button_bg": "#e6e6e6",
                    "button_hover": "#d9d9d9",
                    "selection_bg": self._lighten_color(accent_color, 0.8),
                    "border": "#cccccc",
                }

    def get_platform_typography(self) -> dict:
        """Get Linux native typography settings."""
        desktop = self.get_desktop_environment()

        if desktop == "gnome":
            return {
                "font_family": "Cantarell",
                "font_family_fallback": "Ubuntu",
                "font_size_small": 9,
                "font_size_normal": 11,
                "font_size_large": 13,
                "font_size_title": 15,
                "font_weight_light": "normal",
                "font_weight_normal": "normal",
                "font_weight_medium": "bold",
                "font_weight_bold": "bold",
            }
        elif desktop == "kde":
            return {
                "font_family": "Noto Sans",
                "font_family_fallback": "DejaVu Sans",
                "font_size_small": 8,
                "font_size_normal": 10,
                "font_size_large": 12,
                "font_size_title": 14,
                "font_weight_light": "normal",
                "font_weight_normal": "normal",
                "font_weight_medium": "bold",
                "font_weight_bold": "bold",
            }
        else:
            return {
                "font_family": "Ubuntu",
                "font_family_fallback": "DejaVu Sans",
                "font_size_small": 9,
                "font_size_normal": 11,
                "font_size_large": 13,
                "font_size_title": 15,
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
