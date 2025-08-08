"""
Type stubs for threepanewindows.central_theme_manager module.

Central Theme Manager for ThreePaneWindows - Single source of truth for all theming.
"""

import tkinter as tk
from dataclasses import dataclass
from enum import Enum
from tkinter import ttk
from typing import Any, Callable, Dict, List, Optional, Union

class ThemeType(Enum):
    """Available theme types."""

    LIGHT: str
    DARK: str
    BLUE: str
    GREEN: str
    PURPLE: str
    SYSTEM: str
    NATIVE: str

@dataclass
class ThemeColors:
    """Color scheme for a theme."""

    # Window and frame colors
    window_bg: str
    frame_bg: str
    panel_bg: str

    # Text colors
    text_fg: str
    text_bg: str
    text_select_bg: str
    text_select_fg: str

    # Button colors
    button_bg: str
    button_fg: str
    button_active_bg: str
    button_active_fg: str
    button_hover_bg: str
    button_hover_fg: str
    button_disabled_bg: str
    button_disabled_fg: str

    # Entry colors
    entry_bg: str
    entry_fg: str
    entry_select_bg: str
    entry_select_fg: str
    entry_disabled_bg: str
    entry_disabled_fg: str

    # Listbox colors
    listbox_bg: str
    listbox_fg: str
    listbox_select_bg: str
    listbox_select_fg: str

    # Menu colors
    menu_bg: str
    menu_fg: str
    menu_active_bg: str
    menu_active_fg: str
    menu_disabled_fg: str

    # Scrollbar colors
    scrollbar_bg: str
    scrollbar_fg: str
    scrollbar_active_bg: str
    scrollbar_trough_bg: str

    # Border and accent colors
    border_color: str
    accent_color: str
    highlight_color: str
    shadow_color: str

class CentralThemeManager:
    """
    Central theme manager for all ThreePaneWindows components.

    Provides a single source of truth for theming across all modules.
    """

    def __init__(self) -> None: ...
    @property
    def current_theme(self) -> ThemeType: ...
    @property
    def current_colors(self) -> ThemeColors: ...
    def set_theme(self, theme: ThemeType) -> None: ...
    def get_theme_colors(self, theme: ThemeType) -> ThemeColors: ...
    def register_custom_theme(self, name: str, colors: ThemeColors) -> None: ...
    def get_available_themes(self) -> List[ThemeType]: ...

    # Widget theming methods
    def apply_theme_to_widget(
        self, widget: tk.Widget, recursive: bool = ...
    ) -> None: ...
    def apply_window_theme(self, window: tk.Tk) -> None: ...
    def apply_frame_theme(self, frame: tk.Frame) -> None: ...
    def apply_button_theme(self, button: tk.Button) -> None: ...
    def apply_label_theme(self, label: tk.Label) -> None: ...
    def apply_entry_theme(self, entry: tk.Entry) -> None: ...
    def apply_text_theme(self, text: tk.Text) -> None: ...
    def apply_listbox_theme(self, listbox: tk.Listbox) -> None: ...
    def apply_menu_theme(self, menu: tk.Menu) -> None: ...
    def apply_scrollbar_theme(
        self, scrollbar: Union[tk.Scrollbar, ttk.Scrollbar]
    ) -> None: ...

    # TTK theming methods
    def apply_ttk_theme(self, widget: ttk.Widget) -> None: ...
    def configure_ttk_style(self) -> None: ...

    # Scrollbar creation methods
    def create_themed_scrollbar_auto(
        self,
        parent: tk.Widget,
        orient: str = ...,
        command: Optional[Callable] = ...,
        **kwargs: Any,
    ) -> Union[tk.Scrollbar, ttk.Scrollbar]: ...
    def create_themed_scrollbar_native(
        self,
        parent: tk.Widget,
        orient: str = ...,
        command: Optional[Callable] = ...,
        **kwargs: Any,
    ) -> tk.Scrollbar: ...
    def create_themed_scrollbar_ttk(
        self,
        parent: tk.Widget,
        orient: str = ...,
        command: Optional[Callable] = ...,
        **kwargs: Any,
    ) -> ttk.Scrollbar: ...

    # Utility methods
    def get_contrasting_color(self, color: str) -> str: ...
    def lighten_color(self, color: str, factor: float = ...) -> str: ...
    def darken_color(self, color: str, factor: float = ...) -> str: ...
    def is_dark_theme(self) -> bool: ...
    def get_platform_scrollbar_type(self) -> str: ...

# Global theme manager instance
def get_theme_manager() -> CentralThemeManager: ...

# Convenience functions
def set_global_theme(theme: ThemeType) -> None: ...
def get_current_theme() -> ThemeType: ...
def get_current_colors() -> ThemeColors: ...
