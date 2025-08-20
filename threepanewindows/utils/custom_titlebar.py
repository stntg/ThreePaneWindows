"""
Cross-platform custom titlebar implementation for ThreePaneWindows.

This module provides a unified interface for creating custom titlebars that work
across Windows, macOS, and Linux without requiring external dependencies like
CustomTkinter. It replicates the functionality of CustomTkinter's titlebar
system while integrating with the ThreePaneWindows architecture.
"""

import platform
import sys
import tkinter as tk
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional, Tuple, Union

from ..logging_config import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


class CustomTitleBarBase(ABC):
    """Abstract base class for custom titlebar implementations."""

    def __init__(self, window: tk.Tk, theme: Dict[str, Any], title: str = ""):
        self.window = window
        self.theme = theme
        self.title = title or window.title()
        self.titlebar_frame = None
        self.title_label = None
        self.buttons = []
        self.is_maximized = False
        self.normal_geometry = None
        self.drag_start_x = 0
        self.drag_start_y = 0

    @abstractmethod
    def create_titlebar(self) -> tk.Frame:
        """Create and return the custom titlebar frame."""
        pass

    @abstractmethod
    def apply_theme(self, theme: Dict[str, Any]) -> None:
        """Apply theme to the titlebar."""
        pass

    def set_title(self, title: str) -> None:
        """Set the window title."""
        self.title = title
        if self.title_label:
            self.title_label.config(text=title)

    def destroy(self) -> None:
        """Clean up titlebar resources."""
        if self.titlebar_frame:
            self.titlebar_frame.destroy()


class WindowsTitleBar(CustomTitleBarBase):
    """Windows-specific custom titlebar implementation."""

    def __init__(self, window: tk.Tk, theme: Dict[str, Any], title: str = ""):
        super().__init__(window, theme, title)
        self._setup_windows_titlebar()

    def _setup_windows_titlebar(self) -> None:
        """Set up Windows-specific titlebar features."""
        try:
            # Following CustomTkinter's approach: keep native titlebar, just theme it
            # This preserves all taskbar functionality and minimize behavior
            self._set_windows_titlebar_color()

            # Store original geometry for restore functionality
            self.normal_geometry = self.window.geometry()

        except Exception as e:
            logger.warning("Failed to setup Windows titlebar: %s", e)

    def _set_windows_titlebar_color(self) -> None:
        """Set Windows titlebar color using DWM API with Windows 11 custom colors."""
        try:
            import ctypes
            import platform

            # Wait for window to be created
            self.window.update_idletasks()

            # Get window handle (following CustomTkinter's approach)
            hwnd = ctypes.windll.user32.GetParent(self.window.winfo_id())

            # Check Windows version for advanced color support
            windows_version = platform.version()
            is_windows_11 = self._is_windows_11_or_later()

            if is_windows_11:
                # Windows 11 supports custom titlebar colors
                self._set_windows_11_titlebar_colors(hwnd)
            else:
                # Windows 10 - fallback to dark/light mode only
                self._set_windows_10_titlebar_mode(hwnd)

        except Exception as e:
            logger.warning("Failed to set Windows titlebar color: %s", e)

    def _is_windows_11_or_later(self) -> bool:
        """Check if running on Windows 11 or later."""
        try:
            import platform

            # Windows 11 is version 10.0.22000 and above
            version_parts = platform.version().split(".")
            if len(version_parts) >= 3:
                major = int(version_parts[0])
                minor = int(version_parts[1])
                build = int(version_parts[2])

                # Windows 11 starts at build 22000
                return major > 10 or (major == 10 and minor == 0 and build >= 22000)
            return False
        except Exception:
            return False

    def _set_windows_11_titlebar_colors(self, hwnd: int) -> None:
        """Set custom titlebar colors on Windows 11."""
        try:
            import ctypes

            # Windows 11 DWM attributes for custom colors
            DWMWA_CAPTION_COLOR = 35  # Background color of the caption
            DWMWA_TEXT_COLOR = 36  # Text color of the caption

            # Get theme colors
            bg_color = self.theme.get("bg", "#ffffff")
            text_color = self.theme.get("fg", "#000000")

            # Convert hex colors to COLORREF format (0x00BBGGRR)
            bg_colorref = self._hex_to_colorref(bg_color)
            text_colorref = self._hex_to_colorref(text_color)

            # Set caption background color
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_CAPTION_COLOR,
                ctypes.byref(ctypes.c_uint32(bg_colorref)),
                ctypes.sizeof(ctypes.c_uint32),
            )

            # Set caption text color
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_TEXT_COLOR,
                ctypes.byref(ctypes.c_uint32(text_colorref)),
                ctypes.sizeof(ctypes.c_uint32),
            )

            logger.info(
                f"Set Windows 11 titlebar colors: bg={bg_color}, text={text_color}"
            )

        except Exception as e:
            logger.warning(f"Failed to set Windows 11 titlebar colors: {e}")
            # Fallback to dark/light mode
            self._set_windows_10_titlebar_mode(hwnd)

    def _set_windows_10_titlebar_mode(self, hwnd: int) -> None:
        """Set titlebar dark/light mode on Windows 10."""
        try:
            import ctypes

            # Determine if theme is dark
            bg_color = self.theme.get("bg", "#ffffff")
            is_dark = self._is_dark_color(bg_color)
            value = 1 if is_dark else 0

            # Windows 10 version 2004 and later
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            # Windows 10 versions before 2004
            DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19

            # Try with the newer attribute first
            result = ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(ctypes.c_int(value)),
                ctypes.sizeof(ctypes.c_int(value)),
            )

            # If that fails, try with the older attribute
            if result != 0:
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1,
                    ctypes.byref(ctypes.c_int(value)),
                    ctypes.sizeof(ctypes.c_int(value)),
                )

            logger.info(
                f"Set Windows 10 titlebar mode: {'dark' if is_dark else 'light'}"
            )

        except Exception as e:
            logger.warning(f"Failed to set Windows 10 titlebar mode: {e}")

    def _hex_to_colorref(self, hex_color: str) -> int:
        """Convert hex color to Windows COLORREF format (0x00BBGGRR)."""
        try:
            # Remove # if present
            if hex_color.startswith("#"):
                hex_color = hex_color[1:]

            # Convert to RGB
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)

            # Convert to COLORREF format (BGR)
            return (b << 16) | (g << 8) | r

        except Exception:
            # Return white as fallback
            return 0x00FFFFFF

    def _is_dark_color(self, color: str) -> bool:
        """Determine if a color is dark (for titlebar theming)."""
        try:
            # Remove # if present
            if color.startswith("#"):
                color = color[1:]

            # Convert to RGB
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)

            # Calculate luminance
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return luminance < 0.5
        except Exception:
            return False  # Default to light

    def create_titlebar(self) -> tk.Frame:
        """Create Windows-style titlebar (uses native titlebar with theming)."""
        # For Windows, we use the native titlebar with custom theming
        # No custom titlebar frame is created - just return None
        # The native titlebar is themed in _setup_windows_titlebar()
        return None

    def apply_theme(self, theme: Dict[str, Any]) -> None:
        """Apply theme to Windows titlebar."""
        self.theme = theme

        # Update native titlebar color
        self._set_windows_titlebar_color()

    def _create_window_controls(self) -> None:
        """Create Windows-style window control buttons."""
        controls_frame = tk.Frame(
            self.titlebar_frame, bg=self.theme.get("bg", "#f0f0f0")
        )
        controls_frame.pack(side="right", padx=2, pady=2)

        # Close button
        close_btn = tk.Button(
            controls_frame,
            text="✕",
            bg=self.theme.get("btn_bg", "#e0e0e0"),
            fg=self.theme.get("btn_fg", "#000000"),
            activebackground="#e81123",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            width=4,
            height=1,
            font=("Segoe UI", 9),
            command=self._close_window,
        )
        close_btn.pack(side="right", padx=1)

        # Maximize button
        maximize_btn = tk.Button(
            controls_frame,
            text="🗖" if not self.is_maximized else "🗗",
            bg=self.theme.get("btn_bg", "#e0e0e0"),
            fg=self.theme.get("btn_fg", "#000000"),
            activebackground=self.theme.get("btn_active_bg", "#d0d0d0"),
            relief="flat",
            borderwidth=0,
            width=4,
            height=1,
            font=("Segoe UI", 9),
            command=self._toggle_maximize,
        )
        maximize_btn.pack(side="right", padx=1)

        # Minimize button
        minimize_btn = tk.Button(
            controls_frame,
            text="🗕",
            bg=self.theme.get("btn_bg", "#e0e0e0"),
            fg=self.theme.get("btn_fg", "#000000"),
            activebackground=self.theme.get("btn_active_bg", "#d0d0d0"),
            relief="flat",
            borderwidth=0,
            width=4,
            height=1,
            font=("Segoe UI", 9),
            command=self._minimize_window,
        )
        minimize_btn.pack(side="right", padx=1)

        self.buttons = [minimize_btn, maximize_btn, close_btn]

    def _setup_window_dragging(self) -> None:
        """Set up window dragging functionality."""
        pass  # Will be implemented in _enable_titlebar_dragging

    def _enable_titlebar_dragging(self) -> None:
        """Enable dragging the window by the titlebar."""

        def start_drag(event):
            self.drag_start_x = event.x_root
            self.drag_start_y = event.y_root

        def drag_window(event):
            if not self.is_maximized:
                x = self.window.winfo_x() + (event.x_root - self.drag_start_x)
                y = self.window.winfo_y() + (event.y_root - self.drag_start_y)
                self.window.geometry(f"+{x}+{y}")
                self.drag_start_x = event.x_root
                self.drag_start_y = event.y_root

        # Bind dragging to titlebar frame and title label
        self.titlebar_frame.bind("<Button-1>", start_drag)
        self.titlebar_frame.bind("<B1-Motion>", drag_window)
        if self.title_label:
            self.title_label.bind("<Button-1>", start_drag)
            self.title_label.bind("<B1-Motion>", drag_window)

    def _minimize_window(self) -> None:
        """Minimize the window."""
        try:
            # Use Windows API for proper minimize with taskbar support
            import ctypes

            hwnd = self.window.winfo_id()
            SW_MINIMIZE = 6
            ctypes.windll.user32.ShowWindow(hwnd, SW_MINIMIZE)
        except Exception:
            # Fallback to tkinter method
            self.window.iconify()

    def _toggle_maximize(self) -> None:
        """Toggle window maximize state."""
        if self.is_maximized:
            self._restore_window()
        else:
            self._maximize_window()

    def _maximize_window(self) -> None:
        """Maximize the window."""
        if not self.is_maximized:
            self.normal_geometry = self.window.geometry()
            try:
                # Use Windows API for proper maximize
                import ctypes

                hwnd = self.window.winfo_id()
                SW_MAXIMIZE = 3
                ctypes.windll.user32.ShowWindow(hwnd, SW_MAXIMIZE)
            except Exception:
                # Fallback to tkinter method
                self.window.state("zoomed")

            self.is_maximized = True
            # Update maximize button icon
            for btn in self.buttons:
                if btn.cget("text") == "🗖":
                    btn.config(text="🗗")

    def _restore_window(self) -> None:
        """Restore the window from maximized state."""
        if self.is_maximized:
            try:
                # Use Windows API for proper restore
                import ctypes

                hwnd = self.window.winfo_id()
                SW_RESTORE = 9
                ctypes.windll.user32.ShowWindow(hwnd, SW_RESTORE)
                if self.normal_geometry:
                    self.window.geometry(self.normal_geometry)
            except Exception:
                # Fallback to tkinter method
                self.window.state("normal")
                if self.normal_geometry:
                    self.window.geometry(self.normal_geometry)

            self.is_maximized = False
            # Update maximize button icon
            for btn in self.buttons:
                if btn.cget("text") == "🗗":
                    btn.config(text="🗖")

    def _close_window(self) -> None:
        """Close the window."""
        self.window.quit()
        self.window.destroy()

    def _is_dark_color(self, color: str) -> bool:
        """Determine if a color is dark."""
        try:
            if color.startswith("#"):
                color = color[1:]
            if len(color) == 6:
                r = int(color[0:2], 16)
                g = int(color[2:4], 16)
                b = int(color[4:6], 16)
                # Calculate luminance
                luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                return luminance < 0.5
        except ValueError:
            pass
        return False


class MacOSTitleBar(CustomTitleBarBase):
    """macOS-specific custom titlebar implementation."""

    def __init__(self, window: tk.Tk, theme: Dict[str, Any], title: str = ""):
        super().__init__(window, theme, title)
        self._setup_macos_titlebar()

    def _setup_macos_titlebar(self) -> None:
        """Set up macOS-specific titlebar features."""
        try:
            # Enable dark titlebar support globally (like CustomTkinter does)
            self._enable_macos_dark_titlebar()
        except Exception as e:
            logger.warning("Failed to setup macOS titlebar: %s", e)

    def _enable_macos_dark_titlebar(self) -> None:
        """Enable macOS dark titlebar support."""
        try:
            import os
            import subprocess

            from packaging import version

            # Check Python and Tcl/Tk versions (like CustomTkinter)
            if version.parse(platform.python_version()) < version.parse("3.10"):
                tcl_version = tk.Tcl().call("info", "patchlevel")
                if version.parse(tcl_version) >= version.parse("8.6.9"):
                    # Enable dark mode for all applications
                    os.system(
                        "defaults write -g NSRequiresAquaSystemAppearance -bool No"
                    )
        except Exception as e:
            logger.warning("Failed to enable macOS dark titlebar: %s", e)

    def create_titlebar(self) -> tk.Frame:
        """Create macOS-style custom titlebar."""
        # For macOS, we primarily rely on native titlebar theming
        # But we can create a minimal custom frame for consistency
        self.titlebar_frame = tk.Frame(
            self.window,
            bg=self.theme.get("bg", "#f0f0f0"),
            height=self.theme.get("height", 28),
        )

        # Add title label (optional, since macOS has native title)
        self.title_label = tk.Label(
            self.titlebar_frame,
            text=self.title,
            bg=self.theme.get("bg", "#f0f0f0"),
            fg=self.theme.get("fg", "#000000"),
            font=self.theme.get("font", ("SF Pro Display", 13)),
        )
        self.title_label.pack(side="left", padx=8, pady=2)

        return self.titlebar_frame

    def apply_theme(self, theme: Dict[str, Any]) -> None:
        """Apply theme to macOS titlebar."""
        self.theme = theme

        # Update custom elements if they exist
        if self.titlebar_frame:
            self.titlebar_frame.config(bg=theme.get("bg", "#f0f0f0"))
        if self.title_label:
            self.title_label.config(
                bg=theme.get("bg", "#f0f0f0"),
                fg=theme.get("fg", "#000000"),
                font=theme.get("font", ("SF Pro Display", 13)),
            )

    def destroy(self) -> None:
        """Clean up macOS titlebar resources."""
        try:
            # Restore default macOS titlebar behavior
            import os

            os.system("defaults delete -g NSRequiresAquaSystemAppearance")
        except Exception as e:
            logger.warning("Failed to restore macOS titlebar: %s", e)
        super().destroy()


class LinuxTitleBar(CustomTitleBarBase):
    """Linux-specific custom titlebar implementation with full window controls."""

    def __init__(
        self,
        window: tk.Tk,
        theme: Dict[str, Any],
        title: str = "",
        prefer_theme_matching: bool = True,
    ):
        super().__init__(window, theme, title)
        self.prefer_theme_matching = prefer_theme_matching
        self._setup_linux_titlebar()

    def _setup_linux_titlebar(self) -> None:
        """Set up Linux-specific titlebar features."""
        try:
            if self.prefer_theme_matching:
                # User prefers theme-matching titlebar
                # Try X11 Motif hints first (best approach)
                if self._try_motif_hints():
                    logger.info(
                        "Using custom Linux titlebar with Motif hints (perfect integration)"
                    )
                    self._use_custom_titlebar = True
                else:
                    # Fallback to overrideredirect (may have taskbar issues)
                    logger.info(
                        "Using custom Linux titlebar with overrideredirect (may have taskbar issues)"
                    )
                    self.window.overrideredirect(True)
                    self._use_custom_titlebar = True
                    self._attempt_taskbar_integration()
            else:
                # User prefers perfect integration (native titlebar)
                logger.info("Using native Linux titlebar for perfect integration")
                self._use_custom_titlebar = False

            # Set window class for better desktop integration
            try:
                self.window.wm_class("ThreePaneWindows", "ThreePaneWindows")
            except (tk.TclError, AttributeError):
                pass  # Not all systems support wm_class

        except Exception as e:
            logger.warning("Failed to setup Linux titlebar: %s", e)
            self._use_custom_titlebar = False

    def _try_motif_hints(self) -> bool:
        """Try to use X11 Motif Window Manager Hints to remove decorations."""
        try:
            from .offscreen_motif import (
                apply_offscreen_hints_to_existing_window,
                is_x11_available,
            )

            if not is_x11_available():
                logger.debug("X11 not available for Motif hints")
                return False

            # Use off-screen approach to eliminate flashing
            return apply_offscreen_hints_to_existing_window(self.window)

        except ImportError:
            logger.debug("Off-screen Motif hints module not available")
            # Fallback to original approach
            try:
                from .x11_motif_hints import remove_window_decorations

                self.window.after(50, lambda: remove_window_decorations(self.window))
                return True
            except ImportError:
                return False
        except Exception as e:
            logger.debug(f"Motif hints failed: {e}")
            return False

    def _attempt_taskbar_integration(self) -> None:
        """Attempt to maintain taskbar integration with overrideredirect."""
        try:
            # These hints may help with taskbar integration on some window managers
            try:
                self.window.wm_attributes("-type", "normal")
            except tk.TclError:
                pass

            try:
                self.window.wm_attributes("-toolwindow", False)
            except tk.TclError:
                pass

            # Force window to appear initially
            self.window.lift()
            self.window.focus_force()

        except Exception as e:
            logger.debug(f"Taskbar integration attempts failed: {e}")

    def create_titlebar(self) -> tk.Frame:
        """Create Linux-style titlebar (custom if window manager hints work, native otherwise)."""
        if getattr(self, "_use_custom_titlebar", False):
            # Create custom titlebar with theme support
            return self._create_custom_titlebar()
        else:
            # Use native titlebar with menu bar for theme switching
            logger.info("Using native Linux titlebar - no custom titlebar created")
            return None

    def _create_custom_titlebar(self) -> tk.Frame:
        """Create custom Linux titlebar with full theme support."""
        self.titlebar_frame = tk.Frame(
            self.window,
            bg=self.theme.get("bg", "#f0f0f0"),
            height=self.theme.get("height", 30),
        )
        self.titlebar_frame.pack(fill="x")

        # Title label
        self.title_label = tk.Label(
            self.titlebar_frame,
            text=self.title,
            bg=self.theme.get("bg", "#f0f0f0"),
            fg=self.theme.get("fg", "#000000"),
            font=self.theme.get("font", ("Ubuntu", 10)),
        )
        self.title_label.pack(side="left", padx=8, pady=4)

        # Button container
        btn_frame = tk.Frame(self.titlebar_frame, bg=self.theme.get("bg", "#f0f0f0"))
        btn_frame.pack(side="right")

        # Window control buttons
        button_configs = [
            ("—", self._minimize_window, "Minimize"),
            ("□", self._toggle_maximize, "Maximize/Restore"),
            ("✕", self._close_window, "Close"),
        ]

        for symbol, command, tooltip in button_configs:
            btn = self._create_control_button(btn_frame, symbol, command, tooltip)
            self.buttons.append(btn)

        # Enable window dragging
        self._setup_window_dragging()

        logger.info("Created custom Linux titlebar with theme support")
        return self.titlebar_frame

    def _create_control_button(
        self, parent: tk.Widget, symbol: str, command: Callable, tooltip: str
    ) -> tk.Label:
        """Create a window control button."""
        btn = tk.Label(
            parent,
            text=symbol,
            bg=self.theme.get("btn_bg", "#e0e0e0"),
            fg=self.theme.get("btn_fg", "#000000"),
            font=self.theme.get("font", ("Ubuntu", 10)),
            width=4,
            cursor="hand2",
        )
        btn.pack(side="right", padx=2, pady=2)

        # Bind click event
        btn.bind("<Button-1>", lambda e: command())

        # Bind hover effects
        btn.bind(
            "<Enter>",
            lambda e: btn.config(bg=self.theme.get("btn_active_bg", "#c0c0c0")),
        )
        btn.bind(
            "<Leave>", lambda e: btn.config(bg=self.theme.get("btn_bg", "#e0e0e0"))
        )

        return btn

    def _setup_window_dragging(self) -> None:
        """Set up window dragging functionality."""
        # Bind dragging to titlebar frame and title label
        for widget in (self.titlebar_frame, self.title_label):
            widget.bind("<ButtonPress-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._on_drag)

    def _start_drag(self, event) -> None:
        """Start window dragging."""
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def _on_drag(self, event) -> None:
        """Handle window dragging."""
        x = event.x_root - self.drag_start_x
        y = event.y_root - self.drag_start_y
        self.window.geometry(f"+{x}+{y}")

    def _minimize_window(self) -> None:
        """Minimize the window."""
        self.window.iconify()

    def _toggle_maximize(self) -> None:
        """Toggle window maximize/restore."""
        if not self.is_maximized:
            # Store current geometry
            self.normal_geometry = self.window.geometry()
            # Maximize window
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            self.window.geometry(f"{screen_width}x{screen_height}+0+0")
            self.is_maximized = True
        else:
            # Restore window
            if self.normal_geometry:
                self.window.geometry(self.normal_geometry)
            self.is_maximized = False

    def _close_window(self) -> None:
        """Close the window."""
        self.window.destroy()

    def apply_theme(self, theme: Dict[str, Any]) -> None:
        """Apply theme to Linux titlebar."""
        self.theme = theme

        # Update titlebar frame
        if self.titlebar_frame:
            self.titlebar_frame.config(bg=theme.get("bg", "#f0f0f0"))

        # Update title label
        if self.title_label:
            self.title_label.config(
                bg=theme.get("bg", "#f0f0f0"),
                fg=theme.get("fg", "#000000"),
                font=theme.get("font", ("Ubuntu", 10)),
            )

        # Update control buttons
        for btn in self.buttons:
            btn.config(
                bg=theme.get("btn_bg", "#e0e0e0"),
                fg=theme.get("btn_fg", "#000000"),
                font=theme.get("font", ("Ubuntu", 10)),
            )

            # Rebind hover effects with new colors
            btn.unbind("<Enter>")
            btn.unbind("<Leave>")
            btn.bind(
                "<Enter>",
                lambda e, b=btn: b.config(bg=theme.get("btn_active_bg", "#c0c0c0")),
            )
            btn.bind(
                "<Leave>", lambda e, b=btn: b.config(bg=theme.get("btn_bg", "#e0e0e0"))
            )


class CustomTitleBarManager:
    """Manager class for creating platform-appropriate custom titlebars."""

    @staticmethod
    def create_titlebar(
        window: tk.Tk,
        theme: Dict[str, Any],
        title: str = "",
        force_custom: bool = False,
    ) -> Optional[CustomTitleBarBase]:
        """
        Create a platform-appropriate custom titlebar.

        Args:
            window: The Tkinter window
            theme: Theme dictionary with colors and fonts
            title: Window title (optional)
            force_custom: Force custom titlebar on all platforms

        Returns:
            CustomTitleBarBase instance or None if not supported
        """
        try:
            system = platform.system().lower()

            if system == "windows" and not force_custom:
                return WindowsTitleBar(window, theme, title)
            elif system == "darwin" and not force_custom:
                return MacOSTitleBar(window, theme, title)
            else:
                # Linux or forced custom titlebar
                return LinuxTitleBar(window, theme, title)

        except Exception as e:
            logger.error("Failed to create custom titlebar: %s", e)
            return None

    @staticmethod
    def get_default_theme(is_dark: bool = False) -> Dict[str, Any]:
        """
        Get a default theme for custom titlebars.

        Args:
            is_dark: Whether to use dark theme

        Returns:
            Dictionary with theme settings
        """
        if is_dark:
            return {
                "bg": "#2d2d30",
                "fg": "#ffffff",
                "btn_bg": "#3e3e42",
                "btn_fg": "#ffffff",
                "btn_active_bg": "#007acc",
                "content_bg": "#1e1e1e",
                "font": ("Segoe UI", 10),
                "height": 30,
            }
        else:
            return {
                "bg": "#f0f0f0",
                "fg": "#000000",
                "btn_bg": "#e1e1e1",
                "btn_fg": "#000000",
                "btn_active_bg": "#bee6fd",
                "content_bg": "#ffffff",
                "font": ("Segoe UI", 10),
                "height": 30,
            }


# Convenience functions for easy integration
def apply_custom_titlebar(
    window: tk.Tk, theme: Dict[str, Any], title: str = "", force_custom: bool = False
) -> Optional[CustomTitleBarBase]:
    """
    Apply custom titlebar to a window.

    Args:
        window: The Tkinter window
        theme: Theme dictionary
        title: Window title
        force_custom: Force custom titlebar on all platforms

    Returns:
        CustomTitleBarBase instance or None
    """
    return CustomTitleBarManager.create_titlebar(window, theme, title, force_custom)


def get_titlebar_theme(is_dark: bool = False) -> Dict[str, Any]:
    """
    Get a default titlebar theme.

    Args:
        is_dark: Whether to use dark theme

    Returns:
        Theme dictionary
    """
    return CustomTitleBarManager.get_default_theme(is_dark)
