#!/usr/bin/env python3
"""
Central Theme Manager for ThreePaneWindows

This module provides a centralized theming system that can be used by all
ThreePaneWindows modules (fixed, dockable, enhanced_dockable, flexible, etc.).

Features:
- Single source of truth for all theming
- Comprehensive widget support (all Tkinter widgets)
- Menu theming (including dropdowns)
- TTK widget theming
- Consistent color schemes
- Easy theme switching
- No conflicts or multiple applications
"""

import os
import platform
import sys
import tkinter as tk
from dataclasses import dataclass
from enum import Enum
from tkinter import ttk
from typing import Any, Dict, Optional, Union

# Import platform handlers
try:
    from .utils.linux import LinuxPlatformHandler
    from .utils.macos import MacOSPlatformHandler
    from .utils.windows import WindowsPlatformHandler
except ImportError:
    # Fallback if utils not available
    WindowsPlatformHandler = None
    MacOSPlatformHandler = None
    LinuxPlatformHandler = None


class ThemeType(Enum):
    """Available theme types."""

    LIGHT = "light"
    DARK = "dark"
    BLUE = "blue"
    GREEN = "green"
    PURPLE = "purple"
    SYSTEM = "system"
    NATIVE = "native"


@dataclass
class ThemeColors:
    """Theme color definitions."""

    # Primary colors
    primary_bg: str
    primary_text: str
    secondary_bg: str
    secondary_text: str

    # Panel colors
    panel_bg: str
    panel_text: str
    panel_header_bg: str
    panel_header_text: str
    panel_content_bg: str

    # Accent colors
    accent_bg: str
    accent_text: str
    accent_hover: str

    # Button colors
    button_bg: str
    button_text: str
    button_hover: str
    button_active: str

    # Input colors
    input_bg: str
    input_text: str
    input_border: str
    input_focus: str

    # Menu colors
    menu_bg: str
    menu_text: str
    menu_hover: str
    menu_active: str

    # Border and selection colors
    border: str
    separator: str
    selection_bg: str
    selection_text: str

    # Status colors
    success: str
    warning: str
    error: str
    info: str


class CentralThemeManager:
    """
    Central theme manager for all ThreePaneWindows modules.

    This class provides a single, consistent theming system that can be used
    by all modules without conflicts or multiple applications.
    """

    def __init__(self):
        """Initialize the central theme manager."""
        self.current_theme = ThemeType.LIGHT
        self.themes = self._create_theme_definitions()
        self._ttk_style = None
        self._system_theme_cache = None

        # Initialize platform handler
        self._platform_handler = self._get_platform_handler()

    def _get_platform_handler(self):
        """Get the appropriate platform handler."""
        system = platform.system()

        if system == "Windows" and WindowsPlatformHandler:
            return WindowsPlatformHandler()
        elif system == "Darwin" and MacOSPlatformHandler:
            return MacOSPlatformHandler()
        elif system == "Linux" and LinuxPlatformHandler:
            return LinuxPlatformHandler()
        else:
            # Return None if no platform handler available
            return None

    def _create_theme_definitions(self) -> Dict[ThemeType, ThemeColors]:
        """Create comprehensive theme definitions."""
        return {
            ThemeType.LIGHT: ThemeColors(
                # Primary colors - matching themes.py
                primary_bg="#ffffff",
                primary_text="#212121",
                secondary_bg="#f8f9fa",
                secondary_text="#6c757d",
                # Panel colors - matching themes.py
                panel_bg="#ffffff",
                panel_text="#212121",
                panel_header_bg="#f8f9fa",
                panel_header_text="#495057",
                panel_content_bg="#ffffff",
                # Accent colors - matching themes.py
                accent_bg="#e3f2fd",
                accent_text="#0d6efd",
                accent_hover="#e3f2fd",
                # Button colors - matching themes.py
                button_bg="#6c757d",
                button_text="#ffffff",
                button_hover="#0b5ed7",
                button_active="#0a58ca",
                # Input colors
                input_bg="#ffffff",
                input_text="#212121",
                input_border="#dee2e6",
                input_focus="#0d6efd",
                # Menu colors
                menu_bg="#ffffff",
                menu_text="#212121",
                menu_hover="#f8f9fa",
                menu_active="#e9ecef",
                # Border and selection colors - matching themes.py
                border="#dee2e6",
                separator="#e9ecef",
                selection_bg="#e9ecef",
                selection_text="#212121",
                # Status colors
                success="#28a745",
                warning="#ffc107",
                error="#dc3545",
                info="#17a2b8",
            ),
            ThemeType.DARK: ThemeColors(
                # Primary colors - matching themes.py
                primary_bg="#1e1e1e",
                primary_text="#ffffff",
                secondary_bg="#2d2d30",
                secondary_text="#cccccc",
                # Panel colors - matching themes.py
                panel_bg="#1e1e1e",
                panel_text="#ffffff",
                panel_header_bg="#2d2d30",
                panel_header_text="#cccccc",
                panel_content_bg="#1e1e1e",
                # Accent colors - matching themes.py
                accent_bg="#094771",
                accent_text="#4fc3f7",
                accent_hover="#094771",
                # Button colors - matching themes.py
                button_bg="#0e639c",
                button_text="#ffffff",
                button_hover="#1177bb",
                button_active="#143d66",
                # Input colors
                input_bg="#2d2d30",
                input_text="#ffffff",
                input_border="#3e3e42",
                input_focus="#4fc3f7",
                # Menu colors
                menu_bg="#1e1e1e",
                menu_text="#ffffff",
                menu_hover="#2d2d30",
                menu_active="#094771",
                # Border and selection colors - matching themes.py
                border="#3e3e42",
                separator="#3e3e42",
                selection_bg="#094771",
                selection_text="#ffffff",
                # Status colors
                success="#4caf50",
                warning="#ff9800",
                error="#f44336",
                info="#2196f3",
            ),
            ThemeType.BLUE: ThemeColors(
                # Primary colors - matching themes.py
                primary_bg="#fafbfc",
                primary_text="#202124",
                secondary_bg="#f1f3f4",
                secondary_text="#5f6368",
                # Panel colors - matching themes.py
                panel_bg="#ffffff",
                panel_text="#202124",
                panel_header_bg="#f1f3f4",
                panel_header_text="#3c4043",
                panel_content_bg="#ffffff",
                # Accent colors - matching themes.py
                accent_bg="#e8f0fe",
                accent_text="#1a73e8",
                accent_hover="#d2e3fc",
                # Button colors - matching themes.py
                button_bg="#1a73e8",
                button_text="#ffffff",
                button_hover="#1557b0",
                button_active="#1246a0",
                # Input colors
                input_bg="#ffffff",
                input_text="#202124",
                input_border="#dadce0",
                input_focus="#1a73e8",
                # Menu colors
                menu_bg="#ffffff",
                menu_text="#202124",
                menu_hover="#e8f0fe",
                menu_active="#d2e3fc",
                # Border and selection colors - matching themes.py
                border="#dadce0",
                separator="#dadce0",
                selection_bg="#e8f0fe",
                selection_text="#202124",
                # Status colors
                success="#34a853",
                warning="#fbbc04",
                error="#ea4335",
                info="#4285f4",
            ),
            ThemeType.GREEN: ThemeColors(
                # Primary colors - matching themes.py
                primary_bg="#ffffff",
                primary_text="#1b5e20",
                secondary_bg="#f8f9fa",
                secondary_text="#388e3c",
                # Panel colors - matching themes.py
                panel_bg="#ffffff",
                panel_text="#1b5e20",
                panel_header_bg="#e8f5e8",
                panel_header_text="#1b5e20",
                panel_content_bg="#ffffff",
                # Accent colors - matching themes.py
                accent_bg="#e8f5e8",
                accent_text="#2e7d32",
                accent_hover="#e8f5e8",
                # Button colors - matching themes.py
                button_bg="#4caf50",
                button_text="#ffffff",
                button_hover="#388e3c",
                button_active="#2e7d32",
                # Input colors
                input_bg="#ffffff",
                input_text="#1b5e20",
                input_border="#c8e6c9",
                input_focus="#4caf50",
                # Menu colors
                menu_bg="#ffffff",
                menu_text="#1b5e20",
                menu_hover="#c8e6c9",
                menu_active="#a5d6a7",
                # Border and selection colors
                border="#c8e6c9",
                separator="#c8e6c9",
                selection_bg="#c8e6c9",
                selection_text="#1b5e20",
                # Status colors
                success="#4caf50",
                warning="#ff9800",
                error="#f44336",
                info="#2196f3",
            ),
            ThemeType.PURPLE: ThemeColors(
                # Primary colors - matching themes.py
                primary_bg="#ffffff",
                primary_text="#4a148c",
                secondary_bg="#f8f9fa",
                secondary_text="#7b1fa2",
                # Panel colors - matching themes.py
                panel_bg="#ffffff",
                panel_text="#4a148c",
                panel_header_bg="#f3e5f5",
                panel_header_text="#4a148c",
                panel_content_bg="#ffffff",
                # Accent colors - matching themes.py
                accent_bg="#f3e5f5",
                accent_text="#8e24aa",
                accent_hover="#f3e5f5",
                # Button colors - matching themes.py
                button_bg="#9c27b0",
                button_text="#ffffff",
                button_hover="#7b1fa2",
                button_active="#6a1b9a",
                # Input colors
                input_bg="#ffffff",
                input_text="#4a148c",
                input_border="#ce93d8",
                input_focus="#9c27b0",
                # Menu colors
                menu_bg="#ffffff",
                menu_text="#4a148c",
                menu_hover="#f3e5f5",
                menu_active="#f3e5f5",
                # Border and selection colors - matching themes.py
                border="#ce93d8",
                separator="#ce93d8",
                selection_bg="#f3e5f5",
                selection_text="#4a148c",
                # Status colors
                success="#4caf50",
                warning="#ff9800",
                error="#f44336",
                info="#2196f3",
            ),
        }

    def _detect_system_theme(self) -> ThemeColors:
        """Detect the current system theme and return appropriate colors."""
        if self._system_theme_cache is not None:
            return self._system_theme_cache

        # Try to detect system theme
        is_dark = self._is_system_dark_theme()

        if is_dark:
            # Use dark theme colors for dark system theme
            base_theme = self.themes[ThemeType.DARK]
        else:
            # Use light theme colors for light system theme
            base_theme = self.themes[ThemeType.LIGHT]

        # Create system theme based on detected theme but with system colors where appropriate
        system_theme = ThemeColors(
            # Use detected theme colors but with some system integration
            primary_bg=base_theme.primary_bg,
            primary_text=base_theme.primary_text,
            secondary_bg=base_theme.secondary_bg,
            secondary_text=base_theme.secondary_text,
            panel_bg=base_theme.panel_bg,
            panel_text=base_theme.panel_text,
            panel_header_bg=base_theme.panel_header_bg,
            panel_header_text=base_theme.panel_header_text,
            panel_content_bg=base_theme.panel_content_bg,
            accent_bg=base_theme.accent_bg,
            accent_text=base_theme.accent_text,
            accent_hover=base_theme.accent_hover,
            button_bg=base_theme.button_bg,
            button_text=base_theme.button_text,
            button_hover=base_theme.button_hover,
            button_active=base_theme.button_active,
            input_bg=base_theme.input_bg,
            input_text=base_theme.input_text,
            input_border=base_theme.input_border,
            input_focus=base_theme.input_focus,
            menu_bg=base_theme.menu_bg,
            menu_text=base_theme.menu_text,
            menu_hover=base_theme.menu_hover,
            menu_active=base_theme.menu_active,
            border=base_theme.border,
            separator=base_theme.separator,
            selection_bg=base_theme.selection_bg,
            selection_text=base_theme.selection_text,
            success=base_theme.success,
            warning=base_theme.warning,
            error=base_theme.error,
            info=base_theme.info,
        )

        self._system_theme_cache = system_theme
        return system_theme

    def _is_system_dark_theme(self) -> bool:
        """Detect if the system is using a dark theme."""
        if self._platform_handler:
            try:
                return self._platform_handler.is_dark_mode()
            except Exception:
                pass

        # Fallback detection if no platform handler
        try:
            # Windows detection
            if platform.system() == "Windows":
                try:
                    import winreg

                    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                    key = winreg.OpenKey(
                        registry,
                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                    )
                    value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                    winreg.CloseKey(key)
                    return value == 0  # 0 = dark theme, 1 = light theme
                except:
                    pass

            # macOS detection
            elif platform.system() == "Darwin":
                try:
                    import subprocess

                    result = subprocess.run(
                        ["defaults", "read", "-g", "AppleInterfaceStyle"],
                        capture_output=True,
                        text=True,
                    )
                    return "Dark" in result.stdout
                except:
                    pass

            # Linux detection (basic)
            elif platform.system() == "Linux":
                try:
                    import subprocess

                    # Try to detect GNOME theme
                    result = subprocess.run(
                        [
                            "gsettings",
                            "get",
                            "org.gnome.desktop.interface",
                            "gtk-theme",
                        ],
                        capture_output=True,
                        text=True,
                    )
                    theme_name = result.stdout.strip().lower()
                    return "dark" in theme_name
                except:
                    pass

        except Exception:
            pass

        # Default to light theme if detection fails
        return False

    def _invalidate_system_theme_cache(self):
        """Invalidate the system theme cache to force re-detection."""
        self._system_theme_cache = None

    def set_theme(self, theme: Union[str, ThemeType]) -> None:
        """Set the current theme."""
        if isinstance(theme, str):
            theme = ThemeType(theme.lower())

        # Special handling for system and native themes
        if theme == ThemeType.SYSTEM:
            self._invalidate_system_theme_cache()  # Force re-detection
            self.current_theme = theme
            detected = "dark" if self._is_system_dark_theme() else "light"
            print(f"🎨 Theme set to: {theme.value} (detected: {detected})")
        elif theme == ThemeType.NATIVE:
            self.current_theme = theme
            print(f"🎨 Theme set to: {theme.value} (using system colors)")
        else:
            if theme not in self.themes:
                raise ValueError(f"Unknown theme: {theme}")
            self.current_theme = theme
            print(f"🎨 Theme set to: {theme.value}")

    def get_current_theme(self) -> ThemeColors:
        """Get the current theme colors."""
        if self.current_theme == ThemeType.SYSTEM:
            return self._detect_system_theme()
        elif self.current_theme == ThemeType.NATIVE:
            return self._get_native_theme()
        return self.themes[self.current_theme]

    def _get_theme_for_scrollbar(self):
        """Get theme in format compatible with create_themed_scrollbar function."""
        theme_colors = self.get_current_theme()

        # Return a wrapper object that has a .colors property for compatibility
        # with the create_themed_scrollbar function
        class ThemeWrapper:
            def __init__(self, colors):
                self.colors = colors

        return ThemeWrapper(theme_colors)

    @property
    def colors(self) -> ThemeColors:
        """Get current theme colors - compatibility property for themes.py interface."""
        return self.get_current_theme()

    def _get_native_theme(self) -> ThemeColors:
        """Get native system colors theme."""
        return ThemeColors(
            # Native system appearance (minimal theming)
            primary_bg="SystemButtonFace",
            primary_text="SystemButtonText",
            secondary_bg="SystemButtonFace",
            secondary_text="SystemButtonText",
            panel_bg="SystemButtonFace",
            panel_text="SystemButtonText",
            panel_header_bg="SystemButtonFace",
            panel_header_text="SystemButtonText",
            panel_content_bg="SystemWindow",
            accent_bg="SystemHighlight",
            accent_text="SystemHighlightText",
            accent_hover="SystemHighlight",
            button_bg="SystemButtonFace",
            button_text="SystemButtonText",
            button_hover="SystemButtonFace",
            button_active="SystemButtonFace",
            input_bg="SystemWindow",
            input_text="SystemWindowText",
            input_border="SystemButtonShadow",
            input_focus="SystemHighlight",
            menu_bg="SystemMenu",
            menu_text="SystemMenuText",
            menu_hover="SystemHighlight",
            menu_active="SystemHighlight",
            border="SystemButtonShadow",
            separator="SystemButtonShadow",
            selection_bg="SystemHighlight",
            selection_text="SystemHighlightText",
            success="#008000",
            warning="#ff8000",
            error="#ff0000",
            info="#0000ff",
        )

    def get_theme_names(self) -> list[str]:
        """Get list of available theme names."""
        return [theme.value for theme in ThemeType]

    def apply_theme_to_widget(self, widget: tk.Widget, recursive: bool = True) -> None:
        """
        Apply the current theme to a widget and optionally its children.

        This is the main theming method that should be used by all modules.
        """
        theme = self.get_current_theme()

        # Special handling for root window
        if isinstance(widget, tk.Tk):
            self.apply_window_theme(widget)

        # Apply theme based on widget type
        self._theme_widget_by_type(widget, theme)

        # Recursively theme children if requested
        if recursive:
            try:
                for child in widget.winfo_children():
                    self.apply_theme_to_widget(child, recursive=True)
            except tk.TclError:
                # Widget might be destroyed, ignore
                pass

    def _theme_widget_by_type(self, widget: tk.Widget, theme: ThemeColors) -> None:
        """Apply theme to a specific widget based on its type."""
        # Check for custom scrollbars first (before getting widget_class)
        if self._is_custom_scrollbar(widget):
            self._theme_custom_scrollbar(widget, theme)
            return

        widget_class = widget.winfo_class()

        # Check if this is a scrollbar component - don't theme them
        if hasattr(widget, "master") and self._is_custom_scrollbar(widget.master):
            return  # Don't theme scrollbar components

        # Debug: Track which widget types we're theming
        if not hasattr(self, "_themed_widget_types"):
            self._themed_widget_types = set()
        self._themed_widget_types.add(widget_class)

        try:
            if widget_class == "Frame":
                widget.configure(bg=theme.panel_bg)

            elif widget_class == "Label":
                widget.configure(bg=theme.panel_bg, fg=theme.panel_text)

            elif widget_class == "Button":
                # Skip control buttons (detach/reattach) that have custom styling
                if not hasattr(widget, "_is_control_button"):
                    widget.configure(
                        bg=theme.button_bg,
                        fg=theme.button_text,
                        activebackground=theme.button_hover,
                        activeforeground=theme.button_text,
                        relief="flat",
                        borderwidth=1,
                        highlightthickness=0,
                    )

            elif widget_class == "Entry":
                widget.configure(
                    bg=theme.input_bg,
                    fg=theme.input_text,
                    insertbackground=theme.input_text,
                    selectbackground=theme.selection_bg,
                    selectforeground=theme.selection_text,
                    relief="solid",
                    borderwidth=1,
                    highlightthickness=1,
                    highlightcolor=theme.input_focus,
                )

            elif widget_class == "Text":
                widget.configure(
                    bg=theme.input_bg,
                    fg=theme.input_text,
                    insertbackground=theme.input_text,
                    selectbackground=theme.selection_bg,
                    selectforeground=theme.selection_text,
                    relief="solid",
                    borderwidth=1,
                    highlightthickness=1,
                    highlightcolor=theme.input_focus,
                )

            elif widget_class == "Listbox":
                widget.configure(
                    bg=theme.input_bg,
                    fg=theme.input_text,
                    selectbackground=theme.selection_bg,
                    selectforeground=theme.selection_text,
                    relief="solid",
                    borderwidth=1,
                    highlightthickness=1,
                    highlightcolor=theme.input_focus,
                )

            elif widget_class == "LabelFrame":
                widget.configure(
                    bg=theme.panel_bg,
                    fg=theme.panel_text,
                    relief="flat",
                    borderwidth=1,
                    highlightbackground=theme.border,
                )

            elif widget_class in ["Checkbutton", "Radiobutton"]:
                widget.configure(
                    bg=theme.panel_bg,
                    fg=theme.panel_text,
                    activebackground=theme.panel_bg,
                    activeforeground=theme.panel_text,
                    selectcolor=theme.accent_bg,
                    relief="flat",
                    borderwidth=0,
                    highlightthickness=0,
                )

            elif widget_class == "Scale":
                widget.configure(
                    bg=theme.panel_bg,
                    fg=theme.panel_text,
                    activebackground=theme.accent_bg,
                    troughcolor=theme.input_bg,
                    relief="flat",
                    borderwidth=0,
                    highlightthickness=0,
                )

            elif widget_class == "Spinbox":
                widget.configure(
                    bg=theme.input_bg,
                    fg=theme.input_text,
                    buttonbackground=theme.button_bg,
                    relief="solid",
                    borderwidth=1,
                    highlightthickness=1,
                    highlightcolor=theme.input_focus,
                )

            elif widget_class == "Canvas":
                widget.configure(bg=theme.panel_content_bg)

            elif widget_class == "Message":
                widget.configure(bg=theme.panel_bg, fg=theme.panel_text)

            elif widget_class == "Menubutton":
                widget.configure(
                    bg=theme.button_bg,
                    fg=theme.button_text,
                    activebackground=theme.button_hover,
                    activeforeground=theme.button_text,
                    relief="flat",
                    borderwidth=1,
                )

            elif widget_class == "PanedWindow":
                widget.configure(bg=theme.panel_bg)

            elif widget_class == "Toplevel":
                widget.configure(bg=theme.primary_bg)

            elif widget_class == "Tk":
                widget.configure(bg=theme.primary_bg)

            elif widget_class == "Scrollbar":
                widget.configure(
                    bg=theme.panel_bg,
                    troughcolor=theme.secondary_bg,
                    activebackground=theme.accent_bg,
                    relief="flat",
                    borderwidth=0,
                    highlightthickness=0,
                )

            # Additional Tkinter widgets for complete coverage
            elif widget_class == "OptionMenu":
                widget.configure(
                    bg=theme.button_bg,
                    fg=theme.button_text,
                    activebackground=theme.button_hover,
                    activeforeground=theme.button_text,
                    relief="flat",
                    borderwidth=1,
                    highlightthickness=0,
                )
                # Theme the dropdown menu
                if hasattr(widget, "nametowidget"):
                    try:
                        menu = widget.nametowidget(widget.menuname)
                        self.apply_menu_theme(menu)
                    except (tk.TclError, AttributeError):
                        pass

            elif widget_class == "Bitmap":
                widget.configure(bg=theme.panel_bg)

            elif widget_class == "PhotoImage":
                # PhotoImage doesn't have configurable colors
                pass

            elif widget_class == "BitmapImage":
                # BitmapImage doesn't have configurable colors
                pass

            elif widget_class == "Wm":
                # Window manager class - configure as window
                widget.configure(bg=theme.primary_bg)

            # Handle any other Frame-like widgets
            elif "Frame" in widget_class:
                widget.configure(bg=theme.panel_bg)

            # Handle any other Label-like widgets
            elif "Label" in widget_class:
                widget.configure(bg=theme.panel_bg, fg=theme.panel_text)

            # Handle any other Button-like widgets
            elif "Button" in widget_class and not hasattr(widget, "_is_control_button"):
                widget.configure(
                    bg=theme.button_bg,
                    fg=theme.button_text,
                    activebackground=theme.button_hover,
                    activeforeground=theme.button_text,
                    relief="flat",
                    borderwidth=1,
                    highlightthickness=0,
                )

            # Handle any other Entry-like widgets
            elif "Entry" in widget_class:
                widget.configure(
                    bg=theme.input_bg,
                    fg=theme.input_text,
                    insertbackground=theme.input_text,
                    selectbackground=theme.selection_bg,
                    selectforeground=theme.selection_text,
                    relief="solid",
                    borderwidth=1,
                    highlightthickness=1,
                    highlightcolor=theme.input_focus,
                )

            # Handle any other Text-like widgets
            elif "Text" in widget_class:
                widget.configure(
                    bg=theme.input_bg,
                    fg=theme.input_text,
                    insertbackground=theme.input_text,
                    selectbackground=theme.selection_bg,
                    selectforeground=theme.selection_text,
                    relief="solid",
                    borderwidth=1,
                    highlightthickness=1,
                    highlightcolor=theme.input_focus,
                )

            # Handle TTK widgets
            elif widget_class.startswith("T"):
                self._theme_ttk_widget(widget, theme)

            # Handle custom widgets
            elif self._is_custom_scrollbar(widget):
                self._theme_custom_scrollbar(widget, theme)
            elif self._is_scrollbar_component(widget):
                # Skip theming scrollbar components - they're handled by the scrollbar itself
                pass

        except tk.TclError:
            # Some widgets might not support certain options, ignore
            pass

    def _theme_ttk_widget(self, widget: tk.Widget, theme: ThemeColors) -> None:
        """Apply theme to TTK widgets using TTK styling."""
        if not self._ttk_style:
            self._ttk_style = ttk.Style()

        widget_class = widget.winfo_class()

        try:
            if widget_class == "TFrame":
                self._ttk_style.configure("TFrame", background=theme.panel_bg)

            elif widget_class == "TLabel":
                self._ttk_style.configure(
                    "TLabel", background=theme.panel_bg, foreground=theme.panel_text
                )

            elif widget_class == "TButton":
                self._ttk_style.configure(
                    "TButton",
                    background=theme.button_bg,
                    foreground=theme.button_text,
                    borderwidth=1,
                    relief="flat",
                )
                self._ttk_style.map(
                    "TButton",
                    background=[("active", theme.button_hover)],
                    foreground=[("active", theme.button_text)],
                )

            elif widget_class == "TEntry":
                self._ttk_style.configure(
                    "TEntry",
                    fieldbackground=theme.input_bg,
                    foreground=theme.input_text,
                    borderwidth=1,
                    relief="solid",
                )
                self._ttk_style.map("TEntry", focuscolor=[("focus", theme.input_focus)])

            elif widget_class == "TCombobox":
                self._ttk_style.configure(
                    "TCombobox",
                    fieldbackground=theme.input_bg,
                    foreground=theme.input_text,
                    borderwidth=1,
                    relief="solid",
                )

            elif widget_class == "TCheckbutton":
                self._ttk_style.configure(
                    "TCheckbutton",
                    background=theme.panel_bg,
                    foreground=theme.panel_text,
                )

            elif widget_class == "TRadiobutton":
                self._ttk_style.configure(
                    "TRadiobutton",
                    background=theme.panel_bg,
                    foreground=theme.panel_text,
                )

            elif widget_class == "TScale":
                self._ttk_style.configure(
                    "TScale", background=theme.panel_bg, troughcolor=theme.input_bg
                )

            elif widget_class == "TProgressbar":
                self._ttk_style.configure(
                    "TProgressbar",
                    background=theme.accent_bg,
                    troughcolor=theme.input_bg,
                    borderwidth=1,
                    relief="solid",
                )

            elif widget_class == "TScrollbar":
                self._ttk_style.configure(
                    "TScrollbar",
                    background=theme.panel_bg,
                    troughcolor=theme.secondary_bg,
                    borderwidth=0,
                    relief="flat",
                )
                self._ttk_style.map(
                    "TScrollbar", background=[("active", theme.accent_bg)]
                )

            elif widget_class == "TNotebook":
                self._ttk_style.configure(
                    "TNotebook",
                    background=theme.panel_bg,
                    borderwidth=1,
                    relief="solid",
                )
                self._ttk_style.configure(
                    "TNotebook.Tab",
                    background=theme.secondary_bg,
                    foreground=theme.secondary_text,
                    padding=[10, 5],
                )
                self._ttk_style.map(
                    "TNotebook.Tab",
                    background=[("selected", theme.panel_bg)],
                    foreground=[("selected", theme.panel_text)],
                )

            elif widget_class == "TLabelFrame":
                self._ttk_style.configure(
                    "TLabelFrame",
                    background=theme.panel_bg,
                    foreground=theme.panel_text,
                    borderwidth=1,
                    relief="solid",
                )

            elif widget_class == "TPanedwindow":
                self._ttk_style.configure("TPanedwindow", background=theme.panel_bg)

        except tk.TclError:
            # Some TTK widgets might not support certain options, ignore
            pass

    def _theme_custom_scrollbar(self, scrollbar, theme: ThemeColors) -> None:
        """Apply theme to custom ThemedScrollbar widgets using their built-in theming."""
        try:
            # Debug: Track custom scrollbar theming
            if not hasattr(self, "_themed_widget_types"):
                self._themed_widget_types = set()
            self._themed_widget_types.add("ThemedScrollbar")

            # Use the scrollbar's own apply_theme method, just like themes.py does
            # The theme parameter is already a ThemeColors object, which is what apply_theme expects
            scrollbar.apply_theme(theme)
        except (tk.TclError, AttributeError):
            # Some custom scrollbar attributes might not exist, ignore
            pass

    def _is_custom_scrollbar(self, widget) -> bool:
        """Check if a widget is a custom scrollbar."""
        return (
            hasattr(widget, "apply_theme") and "scrollbar" in str(type(widget)).lower()
        )

    def _is_scrollbar_component(self, widget) -> bool:
        """Check if a widget is a component of a scrollbar."""
        parent = widget.master

        # Check if parent is a scrollbar
        if (
            parent
            and hasattr(parent, "apply_theme")
            and "scrollbar" in str(type(parent)).lower()
        ):
            return True

        # Check if grandparent is a scrollbar
        if (
            parent
            and parent.master
            and hasattr(parent.master, "apply_theme")
            and "scrollbar" in str(type(parent.master)).lower()
        ):
            return True

        return False

    def get_themed_widget_types(self) -> set:
        """Get the set of widget types that have been themed."""
        return getattr(self, "_themed_widget_types", set())

    def print_themed_widget_report(self) -> None:
        """Print a report of all widget types that have been themed."""
        themed_types = self.get_themed_widget_types()
        print(f"🎨 Themed Widget Types Report ({len(themed_types)} types):")
        for widget_type in sorted(themed_types):
            print(f"   ✅ {widget_type}")

    def should_use_custom_scrollbars(self) -> bool:
        """
        Determine whether to use custom scrollbars based on platform.

        Returns:
            bool: True if custom scrollbars should be used, False for native scrollbars

        Platform-specific behavior:
        - Windows: Custom scrollbars (better theming support)
        - macOS/Linux: Native scrollbars (better system integration)
        """
        import platform

        return platform.system() == "Windows"

    def create_themed_scrollbar_auto(
        self,
        parent: tk.Widget,
        orient: str = "vertical",
        command=None,
        **kwargs,
    ):
        """
        Create a scrollbar with automatic platform-specific type selection.

        Args:
            parent: Parent widget
            orient: Scrollbar orientation ("vertical" or "horizontal")
            command: Scroll command callback
            **kwargs: Additional arguments passed to scrollbar creation

        Returns:
            Scrollbar widget (custom or native based on platform)
        """
        # Import here to avoid circular imports
        from .custom_scrollbar import create_themed_scrollbar

        use_custom = self.should_use_custom_scrollbars()

        # Use the same create_themed_scrollbar function as the original themes.py
        # This ensures proper theme manager integration and consistent behavior

        # Create a temporary theme manager wrapper that provides the expected interface
        class ThemeManagerWrapper:
            def __init__(self, central_manager):
                self.central_manager = central_manager

            def get_current_theme(self):
                # Return a Theme-like object with a .colors property
                # to match the interface expected by create_themed_scrollbar
                theme_colors = self.central_manager.get_current_theme()

                class ThemeLikeObject:
                    def __init__(self, colors):
                        self.colors = colors

                return ThemeLikeObject(theme_colors)

        wrapper = ThemeManagerWrapper(self)
        scrollbar = create_themed_scrollbar(
            parent=parent,
            orient=orient,
            command=command,
            use_custom=use_custom,
            theme_manager=wrapper,
            **kwargs,
        )
        return scrollbar

    def apply_menu_theme(self, menu: tk.Menu) -> None:
        """Apply theme specifically to a menu widget."""
        theme = self.get_current_theme()

        try:
            # Enhanced menu configuration for better theming
            menu.configure(
                bg=theme.menu_bg,
                fg=theme.menu_text,
                activebackground=theme.menu_hover,
                activeforeground=theme.menu_text,
                selectcolor=theme.accent_bg,
                relief="flat",
                borderwidth=0,
                tearoff=0,
                disabledforeground=theme.secondary_text,
                font=("Segoe UI", 9) if platform.system() == "Windows" else None,
            )

            # Force menu to update its appearance
            try:
                menu.update_idletasks()
            except:
                pass

            print(f"✓ Menu themed: {menu}")
        except tk.TclError as e:
            print(f"✗ Failed to theme menu {menu}: {e}")

    def apply_menubar_theme(self, menubar: tk.Menu, root_window: tk.Tk) -> None:
        """Apply theme specifically to the main menubar."""
        theme = self.get_current_theme()

        try:
            # Configure the menubar itself
            menubar.configure(
                bg=theme.menu_bg,
                fg=theme.menu_text,
                activebackground=theme.menu_hover,
                activeforeground=theme.menu_text,
                relief="flat",
                borderwidth=0,
                font=("Segoe UI", 9) if platform.system() == "Windows" else None,
            )

            # Platform-specific menubar theming
            if platform.system() == "Windows":
                self._apply_windows_menubar_theme(menubar, root_window, theme)
            elif platform.system() == "Darwin":
                self._apply_macos_menubar_theme(menubar, root_window, theme)
            elif platform.system() == "Linux":
                self._apply_linux_menubar_theme(menubar, root_window, theme)

            # Force update
            menubar.update_idletasks()
            root_window.update_idletasks()

            print(f"✓ Menubar themed with platform-specific handling")
        except tk.TclError as e:
            print(f"✗ Failed to theme menubar: {e}")

    def _apply_windows_menubar_theme(
        self, menubar: tk.Menu, root_window: tk.Tk, theme: ThemeColors
    ) -> None:
        """Apply Windows-specific menubar theming."""
        try:
            # Try to use Windows API to theme the menubar
            import ctypes
            from ctypes import wintypes

            hwnd = root_window.winfo_id()

            # Set window theme
            if self._is_dark_color(theme.menu_bg):
                # Dark theme
                try:
                    # Enable dark mode for the entire window
                    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                    value = ctypes.c_int(1)
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        hwnd,
                        DWMWA_USE_IMMERSIVE_DARK_MODE,
                        ctypes.byref(value),
                        ctypes.sizeof(value),
                    )

                    # Try to set dark menu colors
                    user32 = ctypes.windll.user32
                    gdi32 = ctypes.windll.gdi32

                    # Get menu handle
                    hmenu = user32.GetMenu(hwnd)
                    if hmenu:
                        # Set menu colors (this is a hack but might work)
                        menuinfo = wintypes.MENUINFO()
                        menuinfo.cbSize = ctypes.sizeof(menuinfo)
                        menuinfo.fMask = 0x00000010  # MIM_BACKGROUND

                        # Create dark brush
                        dark_color = int(theme.menu_bg.lstrip("#"), 16)
                        r = (dark_color >> 16) & 0xFF
                        g = (dark_color >> 8) & 0xFF
                        b = dark_color & 0xFF
                        brush = gdi32.CreateSolidBrush((b << 16) | (g << 8) | r)

                        menuinfo.hbrBack = brush
                        user32.SetMenuInfo(hmenu, ctypes.byref(menuinfo))

                    print("✓ Windows dark menubar applied")
                except Exception as e:
                    print(f"✗ Windows dark menubar failed: {e}")
            else:
                # Light theme
                try:
                    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                    value = ctypes.c_int(0)
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        hwnd,
                        DWMWA_USE_IMMERSIVE_DARK_MODE,
                        ctypes.byref(value),
                        ctypes.sizeof(value),
                    )
                    print("✓ Windows light menubar applied")
                except Exception as e:
                    print(f"✗ Windows light menubar failed: {e}")

        except Exception as e:
            print(f"✗ Windows menubar theming failed: {e}")

    def _apply_macos_menubar_theme(
        self, menubar: tk.Menu, root_window: tk.Tk, theme: ThemeColors
    ) -> None:
        """Apply macOS-specific menubar theming."""
        try:
            # macOS uses system menubar, so we focus on window appearance
            if self._is_dark_color(theme.menu_bg):
                root_window.tk.call(
                    "::tk::unsupported::MacWindowStyle",
                    "style",
                    root_window._w,
                    "document",
                    "closeBox collapseBox resizable",
                )
                print("✓ macOS dark menubar style applied")
            else:
                root_window.tk.call(
                    "::tk::unsupported::MacWindowStyle",
                    "style",
                    root_window._w,
                    "document",
                    "closeBox collapseBox resizable",
                )
                print("✓ macOS light menubar style applied")
        except Exception as e:
            print(f"✗ macOS menubar theming failed: {e}")

    def _apply_linux_menubar_theme(
        self, menubar: tk.Menu, root_window: tk.Tk, theme: ThemeColors
    ) -> None:
        """Apply Linux-specific menubar theming."""
        try:
            # Linux menubar theming through window manager
            if self._is_dark_color(theme.menu_bg):
                root_window.wm_attributes("-type", "normal")
                print("✓ Linux dark menubar applied")
            else:
                root_window.wm_attributes("-type", "normal")
                print("✓ Linux light menubar applied")
        except Exception as e:
            print(f"✗ Linux menubar theming failed: {e}")

    def apply_window_theme(self, window: tk.Tk) -> None:
        """Apply theme to window including titlebar and frame."""
        theme = self.get_current_theme()

        try:
            # Set window background
            window.configure(bg=theme.primary_bg)

            # Use platform handler for titlebar theming if available
            if self._platform_handler:
                try:
                    success = self._platform_handler.apply_custom_titlebar(
                        window, theme
                    )
                    if success:
                        print(f"✓ Platform-specific titlebar applied")
                    else:
                        print(f"✗ Platform-specific titlebar failed")
                except Exception as e:
                    print(f"✗ Platform titlebar error: {e}")

            # Apply additional comprehensive window theming
            self._apply_comprehensive_window_theme(window, theme)

            print(f"✓ Window themed: {window}")
        except tk.TclError as e:
            print(f"✗ Failed to theme window {window}: {e}")

    def _apply_comprehensive_window_theme(
        self, window: tk.Tk, theme: ThemeColors
    ) -> None:
        """Apply comprehensive window theming including titlebar and frame."""
        try:
            if platform.system() == "Windows":
                self._apply_windows_comprehensive_theme(window, theme)
            elif platform.system() == "Darwin":
                self._apply_macos_comprehensive_theme(window, theme)
            elif platform.system() == "Linux":
                self._apply_linux_comprehensive_theme(window, theme)
        except Exception as e:
            print(f"✗ Comprehensive window theming failed: {e}")

    def _apply_windows_comprehensive_theme(
        self, window: tk.Tk, theme: ThemeColors
    ) -> None:
        """Apply comprehensive Windows theming."""
        try:
            import ctypes
            from ctypes import wintypes

            hwnd = window.winfo_id()

            # Determine if we should use dark theme
            is_dark = self._is_dark_color(theme.primary_bg)

            # Apply dark/light mode to the entire window
            try:
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                value = ctypes.c_int(1 if is_dark else 0)
                result = ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_USE_IMMERSIVE_DARK_MODE,
                    ctypes.byref(value),
                    ctypes.sizeof(value),
                )

                if result == 0:  # S_OK
                    print(
                        f"✓ Windows {'dark' if is_dark else 'light'} mode applied to window"
                    )
                else:
                    print(f"✗ Windows theme application failed with code: {result}")

            except Exception as e:
                print(f"✗ Windows DWM theming failed: {e}")

            # Try to apply window frame colors
            try:
                # Set window border color (Windows 11)
                DWMWA_BORDER_COLOR = 34
                if is_dark:
                    border_color = 0x2D2D2D  # Dark border
                else:
                    border_color = 0xE0E0E0  # Light border

                border_value = ctypes.c_int(border_color)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_BORDER_COLOR,
                    ctypes.byref(border_value),
                    ctypes.sizeof(border_value),
                )
                print(f"✓ Windows border color set")

            except Exception as e:
                print(f"✗ Windows border color failed: {e}")

            # Try to set caption color (Windows 11)
            try:
                DWMWA_CAPTION_COLOR = 35
                if is_dark:
                    caption_color = 0x1E1E1E  # Dark caption
                else:
                    caption_color = 0xFFFFFF  # Light caption

                caption_value = ctypes.c_int(caption_color)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_CAPTION_COLOR,
                    ctypes.byref(caption_value),
                    ctypes.sizeof(caption_value),
                )
                print(f"✓ Windows caption color set")

            except Exception as e:
                print(f"✗ Windows caption color failed: {e}")

            # Force window to redraw
            try:
                user32 = ctypes.windll.user32
                user32.RedrawWindow(
                    hwnd, None, None, 0x0001 | 0x0004
                )  # RDW_INVALIDATE | RDW_UPDATENOW
                print("✓ Windows forced redraw")
            except Exception as e:
                print(f"✗ Windows redraw failed: {e}")

        except Exception as e:
            print(f"✗ Windows comprehensive theming failed: {e}")

    def _apply_macos_comprehensive_theme(
        self, window: tk.Tk, theme: ThemeColors
    ) -> None:
        """Apply comprehensive macOS theming."""
        try:
            is_dark = self._is_dark_color(theme.primary_bg)

            # Set window appearance
            if is_dark:
                window.tk.call(
                    "::tk::unsupported::MacWindowStyle",
                    "style",
                    window._w,
                    "document",
                    "closeBox collapseBox resizable",
                )
                # Try to set dark appearance
                try:
                    window.tk.call(
                        "::tk::unsupported::MacWindowStyle",
                        "appearance",
                        window._w,
                        "darkAqua",
                    )
                    print("✓ macOS dark appearance set")
                except:
                    print("✗ macOS dark appearance failed")
            else:
                window.tk.call(
                    "::tk::unsupported::MacWindowStyle",
                    "style",
                    window._w,
                    "document",
                    "closeBox collapseBox resizable",
                )
                try:
                    window.tk.call(
                        "::tk::unsupported::MacWindowStyle",
                        "appearance",
                        window._w,
                        "aqua",
                    )
                    print("✓ macOS light appearance set")
                except:
                    print("✗ macOS light appearance failed")

        except Exception as e:
            print(f"✗ macOS comprehensive theming failed: {e}")

    def _apply_linux_comprehensive_theme(
        self, window: tk.Tk, theme: ThemeColors
    ) -> None:
        """Apply comprehensive Linux theming."""
        try:
            is_dark = self._is_dark_color(theme.primary_bg)

            # Set window manager hints
            if is_dark:
                window.wm_attributes("-type", "normal")
                # Try to set dark theme hint
                try:
                    window.tk.call("wm", "attributes", window._w, "-class", "dark")
                    print("✓ Linux dark theme hint set")
                except:
                    print("✗ Linux dark theme hint failed")
            else:
                window.wm_attributes("-type", "normal")
                try:
                    window.tk.call("wm", "attributes", window._w, "-class", "light")
                    print("✓ Linux light theme hint set")
                except:
                    print("✗ Linux light theme hint failed")

        except Exception as e:
            print(f"✗ Linux comprehensive theming failed: {e}")

    def _apply_titlebar_theme(self, window: tk.Tk, theme: ThemeColors) -> None:
        """Apply titlebar theming based on platform."""
        try:
            if platform.system() == "Windows":
                self._apply_windows_titlebar_theme(window, theme)
            elif platform.system() == "Darwin":
                self._apply_macos_titlebar_theme(window, theme)
            elif platform.system() == "Linux":
                self._apply_linux_titlebar_theme(window, theme)
        except Exception as e:
            print(f"✗ Titlebar theming failed: {e}")

    def _apply_windows_titlebar_theme(self, window: tk.Tk, theme: ThemeColors) -> None:
        """Apply Windows-specific titlebar theming."""
        try:
            # Try to use Windows DWM API for titlebar theming
            if hasattr(window, "wm_attributes"):
                # For dark themes, try to enable dark titlebar
                if theme.primary_bg.startswith("#") and self._is_dark_color(
                    theme.primary_bg
                ):
                    try:
                        # Windows 10/11 dark titlebar
                        window.wm_attributes("-transparentcolor", "")
                        # Try to set dark mode titlebar (Windows 10 1903+)
                        import ctypes
                        from ctypes import wintypes

                        hwnd = window.winfo_id()
                        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                        value = ctypes.c_int(1)  # Enable dark mode
                        ctypes.windll.dwmapi.DwmSetWindowAttribute(
                            hwnd,
                            DWMWA_USE_IMMERSIVE_DARK_MODE,
                            ctypes.byref(value),
                            ctypes.sizeof(value),
                        )
                        print("✓ Windows dark titlebar enabled")
                    except:
                        # Fallback: just set window background
                        pass
                else:
                    try:
                        # Light titlebar
                        import ctypes
                        from ctypes import wintypes

                        hwnd = window.winfo_id()
                        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                        value = ctypes.c_int(0)  # Disable dark mode
                        ctypes.windll.dwmapi.DwmSetWindowAttribute(
                            hwnd,
                            DWMWA_USE_IMMERSIVE_DARK_MODE,
                            ctypes.byref(value),
                            ctypes.sizeof(value),
                        )
                        print("✓ Windows light titlebar enabled")
                    except:
                        pass
        except Exception as e:
            print(f"✗ Windows titlebar theming failed: {e}")

    def _apply_macos_titlebar_theme(self, window: tk.Tk, theme: ThemeColors) -> None:
        """Apply macOS-specific titlebar theming."""
        try:
            # macOS titlebar appearance
            if self._is_dark_color(theme.primary_bg):
                # Dark appearance
                window.tk.call(
                    "::tk::unsupported::MacWindowStyle",
                    "style",
                    window._w,
                    "document",
                    "closeBox collapseBox resizable",
                )
                print("✓ macOS dark titlebar style applied")
            else:
                # Light appearance
                window.tk.call(
                    "::tk::unsupported::MacWindowStyle",
                    "style",
                    window._w,
                    "document",
                    "closeBox collapseBox resizable",
                )
                print("✓ macOS light titlebar style applied")
        except Exception as e:
            print(f"✗ macOS titlebar theming failed: {e}")

    def _apply_linux_titlebar_theme(self, window: tk.Tk, theme: ThemeColors) -> None:
        """Apply Linux-specific titlebar theming."""
        try:
            # Linux window manager hints
            if self._is_dark_color(theme.primary_bg):
                window.wm_attributes("-type", "normal")
                print("✓ Linux dark window hints applied")
            else:
                window.wm_attributes("-type", "normal")
                print("✓ Linux light window hints applied")
        except Exception as e:
            print(f"✗ Linux titlebar theming failed: {e}")

    def _is_dark_color(self, color: str) -> bool:
        """Check if a color is dark."""
        try:
            if color.startswith("#"):
                # Convert hex to RGB
                hex_color = color.lstrip("#")
                if len(hex_color) == 6:
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    # Calculate luminance
                    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                    return luminance < 0.5
        except:
            pass
        return False

    def apply_ttk_theme(self, style: Optional[ttk.Style] = None) -> None:
        """Apply theme to TTK widgets."""
        if style is None:
            style = ttk.Style()

        self._ttk_style = style
        theme = self.get_current_theme()

        # Configure TTK styles
        style.theme_use("clam")  # Use clam as base theme

        # Configure TTK Button
        style.configure(
            "TButton",
            background=theme.button_bg,
            foreground=theme.button_text,
            borderwidth=1,
            focuscolor="none",
        )
        style.map(
            "TButton",
            background=[
                ("active", theme.button_hover),
                ("pressed", theme.button_active),
            ],
            foreground=[("active", theme.button_text), ("pressed", theme.button_text)],
        )

        # Configure TTK Entry
        style.configure(
            "TEntry",
            fieldbackground=theme.input_bg,
            foreground=theme.input_text,
            borderwidth=1,
            insertcolor=theme.input_text,
        )
        style.map("TEntry", focuscolor=[("focus", theme.input_focus)])

        # Configure TTK Combobox
        style.configure(
            "TCombobox",
            fieldbackground=theme.input_bg,
            foreground=theme.input_text,
            borderwidth=1,
        )

        # Configure TTK Notebook
        style.configure("TNotebook", background=theme.panel_bg, borderwidth=1)
        style.configure(
            "TNotebook.Tab",
            background=theme.secondary_bg,
            foreground=theme.secondary_text,
            padding=[8, 4],
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", theme.accent_bg), ("active", theme.accent_hover)],
            foreground=[("selected", theme.accent_text), ("active", theme.accent_text)],
        )

        # Configure TTK Treeview
        style.configure(
            "Treeview",
            background=theme.input_bg,
            foreground=theme.input_text,
            fieldbackground=theme.input_bg,
            borderwidth=1,
        )
        style.configure(
            "Treeview.Heading",
            background=theme.panel_header_bg,
            foreground=theme.panel_header_text,
            borderwidth=1,
        )
        style.map(
            "Treeview",
            background=[("selected", theme.selection_bg)],
            foreground=[("selected", theme.selection_text)],
        )

        # Configure TTK Progressbar
        style.configure(
            "TProgressbar",
            background=theme.accent_bg,
            troughcolor=theme.secondary_bg,
            borderwidth=1,
        )

        # Configure TTK Scale
        style.configure(
            "TScale",
            background=theme.panel_bg,
            troughcolor=theme.input_bg,
            borderwidth=1,
        )

        print("✓ TTK theme applied")

    def create_themed_menu(self, parent: tk.Widget, **kwargs) -> tk.Menu:
        """Create a new menu with theme applied and proper border handling."""
        # Set default values for clean appearance
        defaults = {"tearoff": 0, "relief": "flat", "borderwidth": 0}

        # Merge with user-provided kwargs (user values take precedence)
        for key, value in defaults.items():
            if key not in kwargs:
                kwargs[key] = value

        menu = tk.Menu(parent, **kwargs)
        self.apply_menu_theme(menu)
        return menu

    def apply_comprehensive_theme(
        self,
        root_window: tk.Tk,
        menubar: Optional[tk.Menu] = None,
        menus: Optional[list] = None,
    ) -> None:
        """
        Apply comprehensive theming to a complete application.

        This method handles:
        - Window and titlebar theming (platform-specific)
        - Menubar theming (platform-specific)
        - All widget theming (recursive)
        - Individual menu theming
        - TTK theming

        Args:
            root_window: The main Tk window
            menubar: The main menubar (optional)
            menus: List of individual menus to theme (optional)
        """
        print(f"🎨 Applying comprehensive {self.current_theme.value} theme...")

        # 1. Apply TTK theme first
        self.apply_ttk_theme()

        # 2. Apply window theme (including titlebar and frame)
        self.apply_window_theme(root_window)

        # 3. Apply menubar theme with platform-specific handling
        if menubar:
            self.apply_menubar_theme(menubar, root_window)
            print(f"✓ Menubar themed with platform-specific handling")

        # 4. Apply theme to all widgets recursively
        self.apply_theme_to_widget(root_window, recursive=True)

        # 5. Apply individual menu themes
        if menus:
            for menu in menus:
                if menu:
                    self.apply_menu_theme(menu)
            print(f"✓ {len([m for m in menus if m])} individual menus themed")

        # 6. Force multiple display updates for proper rendering
        root_window.update_idletasks()
        root_window.update()

        # 7. Additional platform-specific updates
        if platform.system() == "Windows":
            try:
                # Force Windows to refresh the window
                import ctypes

                hwnd = root_window.winfo_id()
                ctypes.windll.user32.InvalidateRect(hwnd, None, True)
                ctypes.windll.user32.UpdateWindow(hwnd)
                print("✓ Windows display refresh forced")
            except:
                pass

        print(
            f"✅ Comprehensive {self.current_theme.value} theme applied successfully!"
        )

    def get_widget_style(self, widget_type: str) -> Dict[str, Any]:
        """Get style dictionary for a specific widget type."""
        theme = self.get_current_theme()

        styles = {
            "button": {
                "bg": theme.button_bg,
                "fg": theme.button_text,
                "activebackground": theme.button_hover,
                "activeforeground": theme.button_text,
                "relief": "flat",
                "borderwidth": 1,
                "highlightthickness": 0,
            },
            "entry": {
                "bg": theme.input_bg,
                "fg": theme.input_text,
                "insertbackground": theme.input_text,
                "selectbackground": theme.selection_bg,
                "selectforeground": theme.selection_text,
                "relief": "solid",
                "borderwidth": 1,
                "highlightthickness": 1,
                "highlightcolor": theme.input_focus,
            },
            "text": {
                "bg": theme.input_bg,
                "fg": theme.input_text,
                "insertbackground": theme.input_text,
                "selectbackground": theme.selection_bg,
                "selectforeground": theme.selection_text,
                "relief": "solid",
                "borderwidth": 1,
                "highlightthickness": 1,
                "highlightcolor": theme.input_focus,
            },
            "label": {"bg": theme.panel_bg, "fg": theme.panel_text},
            "frame": {"bg": theme.panel_bg},
            "menu": {
                "bg": theme.menu_bg,
                "fg": theme.menu_text,
                "activebackground": theme.menu_hover,
                "activeforeground": theme.menu_text,
                "selectcolor": theme.accent_bg,
                "relief": "flat",
                "borderwidth": 1,
                "tearoff": 0,
            },
        }

        return styles.get(widget_type.lower(), {})


# Global instance for easy access
_global_theme_manager = None


def get_theme_manager() -> CentralThemeManager:
    """Get the global theme manager instance."""
    global _global_theme_manager
    if _global_theme_manager is None:
        _global_theme_manager = CentralThemeManager()
    return _global_theme_manager


def set_global_theme(theme: Union[str, ThemeType]) -> None:
    """Set the global theme."""
    manager = get_theme_manager()
    manager.set_theme(theme)


def apply_theme_to_widget(widget: tk.Widget, recursive: bool = True) -> None:
    """Apply the current global theme to a widget."""
    manager = get_theme_manager()
    manager.apply_theme_to_widget(widget, recursive)


def apply_menu_theme(menu: tk.Menu) -> None:
    """Apply the current global theme to a menu."""
    manager = get_theme_manager()
    manager.apply_menu_theme(menu)


def apply_menubar_theme(menubar: tk.Menu, root_window: tk.Tk) -> None:
    """Apply the current global theme to a menubar with platform-specific handling."""
    manager = get_theme_manager()
    manager.apply_menubar_theme(menubar, root_window)


def apply_ttk_theme(style: Optional[ttk.Style] = None) -> None:
    """Apply the current global theme to TTK widgets."""
    manager = get_theme_manager()
    manager.apply_ttk_theme(style)


def create_themed_menu(parent: tk.Widget, **kwargs) -> tk.Menu:
    """Create a themed menu."""
    manager = get_theme_manager()
    return manager.create_themed_menu(parent, **kwargs)


def apply_window_theme(window: tk.Tk) -> None:
    """Apply the current global theme to a window including titlebar."""
    manager = get_theme_manager()
    manager.apply_window_theme(window)


def apply_comprehensive_theme(
    root_window: tk.Tk, menubar: Optional[tk.Menu] = None, menus: Optional[list] = None
) -> None:
    """Apply comprehensive theming to a complete application."""
    manager = get_theme_manager()
    manager.apply_comprehensive_theme(root_window, menubar, menus)
