"""
macOS-specific platform functionality.

This module provides macOS-specific implementations for icon handling,
titlebar customization, theming, and other platform-specific features.
"""

import os
import subprocess  # nosec B404
import tkinter as tk
from tkinter import ttk
from typing import Any, List, Optional, Tuple

from .base import PlatformHandler


def detect_macos_dark_mode() -> bool:
    """
    Detect if macOS is in dark mode.

    Returns:
        True if dark mode is enabled, False otherwise
    """
    try:
        # Try using darkdetect first (if available)
        import darkdetect  # type: ignore[import-untyped]

        return darkdetect.isDark() or False
    except ImportError:
        pass

    try:
        # Fallback: Use AppleScript to check system appearance
        # Using hardcoded path to osascript for security
        result = subprocess.run(  # nosec B603
            [
                "/usr/bin/osascript",
                "-e",
                (
                    'tell application "System Events" to tell appearance '
                    "preferences to get dark mode"
                ),
            ],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,  # Don't raise exception on non-zero exit
        )
        return result.stdout.strip().lower() == "true"
    except (subprocess.SubprocessError, subprocess.TimeoutExpired, FileNotFoundError):
        pass

    try:
        # Another fallback: Check system defaults
        # Using hardcoded path to defaults command for security
        result = subprocess.run(  # nosec B603
            ["/usr/bin/defaults", "read", "-g", "AppleInterfaceStyle"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,  # Don't raise exception on non-zero exit
        )
        return result.stdout.strip().lower() == "dark"
    except (subprocess.SubprocessError, subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Final fallback
    return False


def get_macos_accent_color() -> Optional[str]:
    """
    Get the macOS system accent color.

    Returns:
        Hex color string or None if unable to detect
    """
    try:
        # Try to get the accent color from system preferences
        # Using hardcoded path to defaults command for security
        result = subprocess.run(  # nosec B603
            ["/usr/bin/defaults", "read", "-g", "AppleAccentColor"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,  # Don't raise exception on non-zero exit
        )

        accent_id = result.stdout.strip()
        if accent_id.isdigit():
            # Map macOS accent color IDs to hex colors
            accent_colors = {
                "-1": "#007AFF",  # Blue (default)
                "0": "#FF3B30",  # Red
                "1": "#FF9500",  # Orange
                "2": "#FFCC00",  # Yellow
                "3": "#34C759",  # Green
                "4": "#007AFF",  # Blue
                "5": "#5856D6",  # Purple
                "6": "#FF2D92",  # Pink
            }
            return accent_colors.get(accent_id, "#007AFF")
    except (subprocess.SubprocessError, subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return "#007AFF"  # Default blue


class MacOSPlatformHandler(PlatformHandler):
    """macOS-specific platform handler."""

    def __init__(self):
        """Initialize macOS platform handler."""
        self._system_dark_mode = detect_macos_dark_mode()
        self._system_accent_color = get_macos_accent_color()

    def get_recommended_icon_formats(self) -> List[str]:
        """Get recommended icon formats for macOS."""
        return [".png", ".gif", ".bmp", ".ico"]

    def validate_icon_path(self, icon_path: str) -> Tuple[bool, str]:
        """Validate an icon path for macOS."""
        if not icon_path:
            return True, "No icon specified"

        if not os.path.exists(icon_path):
            return False, f"Icon file not found: {icon_path}"

        _, ext = os.path.splitext(icon_path.lower())
        recommended = self.get_recommended_icon_formats()

        if ext not in recommended:
            return (
                False,
                f"Icon format '{ext}' not recommended for macOS. "
                f"Recommended formats: {', '.join(recommended)}",
            )

        # Additional macOS-specific validation
        if ext == ".png":
            # PNG files are preferred on macOS
            return True, "PNG format is optimal for macOS"
        elif ext in [".gif", ".bmp"]:
            return True, f"{ext.upper()} format is supported on macOS"
        elif ext == ".ico":
            return True, "ICO format is supported but PNG is preferred on macOS"

        return True, "Icon format is supported"

    def set_window_icon(self, window: tk.Tk, icon_path: str) -> bool:
        """Set window icon using macOS-optimized methods."""
        if not os.path.exists(icon_path):
            print(f"Warning: Icon file not found: {icon_path}")
            return False

        try:
            # Get file extension
            _, ext = os.path.splitext(icon_path.lower())

            # On macOS, iconphoto works better than iconbitmap
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
                    print(
                        f"Warning: Could not load icon as PhotoImage '{icon_path}': {e}"
                    )

            # For .ico files or as fallback, try iconbitmap
            try:
                window.iconbitmap(icon_path)
                return True
            except tk.TclError as e:
                print(f"Warning: Could not set icon '{icon_path}': {e}")
                return False

        except Exception as e:
            print(f"Error setting window icon: {e}")
            return False

    def apply_custom_titlebar(self, window: tk.Tk, theme_colors: Any) -> bool:
        """Apply macOS-specific custom titlebar."""
        try:
            self._apply_macos_custom_titlebar(window, theme_colors)
            return True
        except Exception as e:
            print(f"Could not apply macOS custom titlebar: {e}")
            return False

    def _apply_macos_custom_titlebar(self, window: tk.Tk, colors: Any) -> None:
        """Apply custom titlebar for macOS."""
        window.overrideredirect(True)
        style = ttk.Style()
        style.configure("CustomTitle.TFrame", background=colors.panel_header_bg)

        titlebar = ttk.Frame(window, style="CustomTitle.TFrame")
        titlebar.pack(side="top", fill="x")

        def brighten(color_hex: str, factor: float = 1.2) -> str:
            """Brighten a hex color by a given factor."""
            color_hex = color_hex.lstrip("#")
            r, g, b = [
                min(int(int(color_hex[i : i + 2], 16) * factor), 255) for i in (0, 2, 4)
            ]
            return f"#{r:02x}{g:02x}{b:02x}"

        # Add window controls (close, minimize, maximize buttons)
        controls_frame = ttk.Frame(titlebar)
        controls_frame.pack(side="left", padx=10, pady=5)

        # Close button (red)
        close_btn = tk.Button(
            controls_frame,
            text="●",
            font=("Arial", 12),
            fg="white",
            bg="#ff5f57",
            bd=0,
            width=2,
            height=1,
            command=window.quit,
        )
        close_btn.pack(side="left", padx=2)

        # Minimize button (yellow)
        minimize_btn = tk.Button(
            controls_frame,
            text="●",
            font=("Arial", 12),
            fg="white",
            bg="#ffbd2e",
            bd=0,
            width=2,
            height=1,
            command=window.iconify,
        )
        minimize_btn.pack(side="left", padx=2)

        # Maximize button (green)
        def toggle_fullscreen():
            if window.attributes("-fullscreen"):
                window.attributes("-fullscreen", False)
            else:
                window.attributes("-fullscreen", True)

        maximize_btn = tk.Button(
            controls_frame,
            text="●",
            font=("Arial", 12),
            fg="white",
            bg="#28ca42",
            bd=0,
            width=2,
            height=1,
            command=toggle_fullscreen,
        )
        maximize_btn.pack(side="left", padx=2)

        # Title label
        title_label = ttk.Label(
            titlebar,
            text=window.title() or "ThreePaneWindows",
            style="CustomTitle.TLabel",
        )
        title_label.pack(expand=True)

        # Configure title label style
        style.configure(
            "CustomTitle.TLabel",
            background=colors.panel_header_bg,
            foreground=colors.primary_text,
        )

        # Make titlebar draggable
        def start_move(event):
            window.x = event.x
            window.y = event.y

        def stop_move(event):
            window.x = None
            window.y = None

        def do_move(event):
            if hasattr(window, "x") and window.x is not None:
                deltax = event.x - window.x
                deltay = event.y - window.y
                x = window.winfo_x() + deltax
                y = window.winfo_y() + deltay
                window.geometry(f"+{x}+{y}")

        titlebar.bind("<Button-1>", start_move)
        titlebar.bind("<ButtonRelease-1>", stop_move)
        titlebar.bind("<B1-Motion>", do_move)
        title_label.bind("<Button-1>", start_move)
        title_label.bind("<ButtonRelease-1>", stop_move)
        title_label.bind("<B1-Motion>", do_move)

    def is_dark_mode(self) -> bool:
        """Check if macOS is currently in dark mode."""
        return detect_macos_dark_mode()

    def get_system_accent_color(self) -> str:
        """Get the current macOS system accent color."""
        return get_macos_accent_color() or "#007AFF"

    def get_macos_native_colors(self, is_dark: bool = None) -> dict:
        """
        Get macOS native color scheme.

        Args:
            is_dark: Override dark mode detection

        Returns:
            Dictionary of native macOS colors
        """
        if is_dark is None:
            is_dark = self.is_dark_mode()

        accent_color = self.get_system_accent_color()

        if is_dark:
            return {
                "window_bg": "#1e1e1e",
                "content_bg": "#2d2d2d",
                "sidebar_bg": "#252525",
                "text_primary": "#ffffff",
                "text_secondary": "#a0a0a0",
                "text_tertiary": "#6e6e6e",
                "separator": "#404040",
                "accent": accent_color,
                "accent_secondary": self._adjust_color_brightness(accent_color, 0.8),
                "button_bg": "#3a3a3a",
                "button_hover": "#4a4a4a",
                "selection_bg": self._lighten_color(accent_color, 0.8),
                "border": "#404040",
            }
        else:
            return {
                "window_bg": "#ffffff",
                "content_bg": "#ffffff",
                "sidebar_bg": "#f5f5f5",
                "text_primary": "#000000",
                "text_secondary": "#3c3c43",
                "text_tertiary": "#8e8e93",
                "separator": "#d1d1d6",
                "accent": accent_color,
                "accent_secondary": self._adjust_color_brightness(accent_color, 1.2),
                "button_bg": "#f2f2f7",
                "button_hover": "#e5e5ea",
                "selection_bg": self._lighten_color(accent_color, 0.8),
                "border": "#d1d1d6",
            }

    def get_macos_typography(self) -> dict:
        """Get macOS native typography settings."""
        return {
            "font_family": "SF Pro Display",  # macOS system font
            "font_family_fallback": "Helvetica Neue",
            "font_size_small": 11,
            "font_size_normal": 13,
            "font_size_large": 15,
            "font_size_title": 17,
            "font_weight_light": "normal",
            "font_weight_normal": "normal",
            "font_weight_medium": "bold",
            "font_weight_bold": "bold",
        }

    def _adjust_color_brightness(self, hex_color: str, factor: float) -> str:
        """
        Adjust the brightness of a hex color.

        Args:
            hex_color: Hex color string (e.g., '#ff0000')
            factor: Brightness factor (>1 = brighter, <1 = darker)

        Returns:
            Adjusted hex color string
        """
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

    def apply_macos_native_styling(self, window: tk.Tk, theme_colors: Any) -> bool:
        """
        Apply macOS native styling to the window.

        Args:
            window: The Tkinter window
            theme_colors: Theme color scheme object

        Returns:
            True if styling was applied successfully
        """
        try:
            # Set macOS-specific window attributes
            window.tk.call(
                "::tk::unsupported::MacWindowStyle",
                "style",
                window._w,
                "document",
                "closeBox collapseBox resizable",
            )

            # Configure for dark mode if needed
            if self.is_dark_mode():
                # This requires macOS 10.14+ and appropriate Tk version
                try:
                    window.tk.call(
                        "::tk::unsupported::MacWindowStyle",
                        "appearance",
                        window._w,
                        "darkAqua",
                    )
                except tk.TclError:
                    pass

            return True
        except (tk.TclError, AttributeError):
            return False
