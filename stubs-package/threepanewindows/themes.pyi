"""Type stubs for threepanewindows.themes module."""

import tkinter as tk
from dataclasses import dataclass
from enum import Enum
from tkinter import ttk
from typing import Any, Dict, List, Optional, Union

class ThemeType(Enum):
    LIGHT: str
    DARK: str
    BLUE: str
    GREEN: str
    PURPLE: str
    CUSTOM: str
    SYSTEM: str
    NATIVE: str
    NATIVE_LIGHT: str
    NATIVE_DARK: str

@dataclass
class ColorScheme:
    primary_bg: str
    secondary_bg: str
    accent_bg: str
    primary_text: str
    secondary_text: str
    accent_text: str
    border: str
    separator: str
    button_bg: str
    button_fg: str
    button_hover: str
    button_active: str
    success: str
    warning: str
    error: str
    info: str
    panel_header_bg: str
    panel_header_fg: str
    panel_content_bg: str
    drag_indicator: str
    drop_zone: str

@dataclass
class Typography:
    font_family: str
    font_family_fallback: str
    font_size_small: int
    font_size_normal: int
    font_size_large: int
    font_size_title: int
    font_weight_light: str
    font_weight_normal: str
    font_weight_medium: str
    font_weight_bold: str

@dataclass
class Spacing:
    padding_small: int
    padding_normal: int
    padding_large: int
    margin_small: int
    margin_normal: int
    margin_large: int
    border_width: int
    separator_width: int

@dataclass
class Theme:
    name: str
    colors: ColorScheme
    typography: Typography
    spacing: Spacing
    animation_duration: int
    enable_animations: bool
    enable_shadows: bool
    enable_gradients: bool
    corner_radius: int

class ThemeManager:
    """Professional theming system for three-pane windows."""

    def __init__(
        self,
        theme: Optional[Union[str, ThemeType]] = ...,
        custom_scheme: Optional[ColorScheme] = ...,
    ) -> None: ...
    def register_theme(self, theme: Theme) -> None: ...
    def set_theme(self, theme_name: Union[str, ThemeType]) -> None: ...
    def get_current_theme(self) -> Theme: ...
    def get_available_themes(self) -> Dict[str, str]: ...
    def get_theme(self, name: str) -> Optional[Theme]: ...
    def apply_theme_to_widget(
        self,
        widget: tk.Widget,
        widget_type: Optional[str] = ...,
        **style_overrides: Any,
    ) -> None: ...
    def create_themed_style(self) -> ttk.Style: ...
    def update_ttk_styles(self, style: ttk.Style) -> None: ...
    def add_theme_change_callback(self, callback: Any) -> None: ...
    def remove_theme_change_callback(self, callback: Any) -> None: ...
    def get_system_theme_preference(self) -> str: ...
    def is_dark_mode(self) -> bool: ...

def get_theme_manager() -> ThemeManager: ...
def set_global_theme(theme_name: Union[str, ThemeType]) -> None: ...
