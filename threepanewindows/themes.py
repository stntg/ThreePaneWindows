"""
Professional themes and styling for ThreePaneWindows.

This module provides a comprehensive theming system with predefined themes
and customization options for creating beautiful, professional-looking interfaces.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ThemeType(Enum):
    """Available theme types."""
    LIGHT = "light"
    DARK = "dark"
    BLUE = "blue"
    GREEN = "green"
    PURPLE = "purple"
    CUSTOM = "custom"


@dataclass
class ColorScheme:
    """Color scheme for theming."""
    # Background colors
    primary_bg: str = "#ffffff"
    secondary_bg: str = "#f5f5f5"
    accent_bg: str = "#e3f2fd"
    
    # Text colors
    primary_text: str = "#212121"
    secondary_text: str = "#757575"
    accent_text: str = "#1976d2"
    
    # Border and separator colors
    border: str = "#e0e0e0"
    separator: str = "#bdbdbd"
    
    # Interactive elements
    button_bg: str = "#2196f3"
    button_fg: str = "#ffffff"
    button_hover: str = "#1976d2"
    button_active: str = "#0d47a1"
    
    # Status colors
    success: str = "#4caf50"
    warning: str = "#ff9800"
    error: str = "#f44336"
    info: str = "#2196f3"
    
    # Panel specific
    panel_header_bg: str = "#fafafa"
    panel_header_fg: str = "#424242"
    panel_content_bg: str = "#ffffff"
    
    # Drag and drop
    drag_indicator: str = "#2196f3"
    drop_zone: str = "#e3f2fd"


@dataclass
class Typography:
    """Typography settings."""
    font_family: str = "Segoe UI"
    font_size_small: int = 9
    font_size_normal: int = 10
    font_size_large: int = 12
    font_size_title: int = 14
    font_weight_normal: str = "normal"
    font_weight_bold: str = "bold"


@dataclass
class Spacing:
    """Spacing and sizing settings."""
    padding_small: int = 4
    padding_normal: int = 8
    padding_large: int = 16
    margin_small: int = 2
    margin_normal: int = 4
    margin_large: int = 8
    border_width: int = 1
    separator_width: int = 1


@dataclass
class Theme:
    """Complete theme configuration."""
    name: str
    colors: ColorScheme = field(default_factory=ColorScheme)
    typography: Typography = field(default_factory=Typography)
    spacing: Spacing = field(default_factory=Spacing)
    
    # Animation settings
    animation_duration: int = 200  # milliseconds
    enable_animations: bool = True
    
    # Visual effects
    enable_shadows: bool = True
    enable_gradients: bool = False
    corner_radius: int = 4


class ThemeManager:
    """Manages themes and provides styling utilities."""
    
    def __init__(self):
        self._themes: Dict[str, Theme] = {}
        self._current_theme: Optional[Theme] = None
        self._style_cache: Dict[str, Dict[str, Any]] = {}
        self._initialize_default_themes()
    
    def _initialize_default_themes(self):
        """Initialize default themes."""
        
        # Light Theme
        light_colors = ColorScheme(
            primary_bg="#ffffff",
            secondary_bg="#f8f9fa",
            accent_bg="#e3f2fd",
            primary_text="#212529",
            secondary_text="#6c757d",
            accent_text="#0d6efd",
            border="#dee2e6",
            separator="#e9ecef",
            button_bg="#0d6efd",
            button_fg="#ffffff",
            button_hover="#0b5ed7",
            button_active="#0a58ca",
            panel_header_bg="#f8f9fa",
            panel_header_fg="#495057",
            panel_content_bg="#ffffff",
            drag_indicator="#0d6efd",
            drop_zone="#e7f3ff"
        )
        
        self._themes["light"] = Theme(
            name="Light",
            colors=light_colors,
            typography=Typography(font_family="Segoe UI"),
            spacing=Spacing()
        )
        
        # Dark Theme
        dark_colors = ColorScheme(
            primary_bg="#1e1e1e",
            secondary_bg="#2d2d30",
            accent_bg="#094771",
            primary_text="#ffffff",
            secondary_text="#cccccc",
            accent_text="#4fc3f7",
            border="#3e3e42",
            separator="#464647",
            button_bg="#0e639c",
            button_fg="#ffffff",
            button_hover="#1177bb",
            button_active="#143d66",
            panel_header_bg="#2d2d30",
            panel_header_fg="#cccccc",
            panel_content_bg="#1e1e1e",
            drag_indicator="#4fc3f7",
            drop_zone="#094771"
        )
        
        self._themes["dark"] = Theme(
            name="Dark",
            colors=dark_colors,
            typography=Typography(font_family="Segoe UI"),
            spacing=Spacing()
        )
        
        # Blue Professional Theme
        blue_colors = ColorScheme(
            primary_bg="#fafbfc",
            secondary_bg="#f1f3f4",
            accent_bg="#e8f0fe",
            primary_text="#202124",
            secondary_text="#5f6368",
            accent_text="#1a73e8",
            border="#dadce0",
            separator="#e8eaed",
            button_bg="#1a73e8",
            button_fg="#ffffff",
            button_hover="#1557b0",
            button_active="#1246a0",
            panel_header_bg="#f1f3f4",
            panel_header_fg="#3c4043",
            panel_content_bg="#ffffff",
            drag_indicator="#1a73e8",
            drop_zone="#e8f0fe"
        )
        
        self._themes["blue"] = Theme(
            name="Blue Professional",
            colors=blue_colors,
            typography=Typography(font_family="Segoe UI"),
            spacing=Spacing()
        )
        
        # Set default theme
        self._current_theme = self._themes["light"]
    
    def get_theme(self, name: str) -> Optional[Theme]:
        """Get a theme by name."""
        return self._themes.get(name.lower())
    
    def set_theme(self, name: str) -> bool:
        """Set the current theme."""
        theme = self.get_theme(name)
        if theme:
            self._current_theme = theme
            self._style_cache.clear()  # Clear cache when theme changes
            return True
        return False
    
    def get_current_theme(self) -> Theme:
        """Get the current theme."""
        return self._current_theme or self._themes["light"]
    
    def register_theme(self, theme: Theme):
        """Register a custom theme."""
        self._themes[theme.name.lower()] = theme
    
    def get_style(self, component: str, state: str = "normal") -> Dict[str, Any]:
        """Get styling for a component in a specific state."""
        cache_key = f"{component}_{state}"
        if cache_key in self._style_cache:
            return self._style_cache[cache_key]
        
        theme = self.get_current_theme()
        style = self._generate_style(component, state, theme)
        self._style_cache[cache_key] = style
        return style
    
    def _generate_style(self, component: str, state: str, theme: Theme) -> Dict[str, Any]:
        """Generate style dictionary for a component."""
        colors = theme.colors
        typography = theme.typography
        spacing = theme.spacing
        
        base_style = {
            "font": (typography.font_family, typography.font_size_normal),
            "relief": "flat",
            "borderwidth": 0,
        }
        
        if component == "panel_header":
            return {
                **base_style,
                "bg": colors.panel_header_bg,
                "fg": colors.panel_header_fg,
                "font": (typography.font_family, typography.font_size_normal, typography.font_weight_bold),
                "padx": spacing.padding_normal,
                "pady": spacing.padding_small,
            }
        
        elif component == "panel_content":
            return {
                **base_style,
                "bg": colors.panel_content_bg,
                "fg": colors.primary_text,
            }
        
        elif component == "button":
            if state == "hover":
                bg = colors.button_hover
            elif state == "active":
                bg = colors.button_active
            else:
                bg = colors.button_bg
            
            return {
                **base_style,
                "bg": bg,
                "fg": colors.button_fg,
                "activebackground": colors.button_active,
                "activeforeground": colors.button_fg,
                "padx": spacing.padding_normal,
                "pady": spacing.padding_small,
                "cursor": "hand2",
            }
        
        elif component == "drag_handle":
            return {
                **base_style,
                "bg": colors.secondary_bg,
                "fg": colors.secondary_text,
                "cursor": "fleur",
                "relief": "raised",
                "borderwidth": 1,
            }
        
        elif component == "separator":
            return {
                "bg": colors.separator,
                "width": spacing.separator_width,
                "relief": "flat",
                "borderwidth": 0,
            }
        
        return base_style
    
    def apply_ttk_theme(self, style: ttk.Style):
        """Apply current theme to ttk widgets."""
        theme = self.get_current_theme()
        colors = theme.colors
        typography = theme.typography
        
        # Configure ttk styles
        style.theme_use('clam')  # Use clam as base theme
        
        # PanedWindow
        style.configure("Themed.TPanedwindow", 
                       background=colors.secondary_bg,
                       borderwidth=0,
                       relief="flat")
        
        style.configure("Themed.TPanedwindow.Sash",
                       sashthickness=4,
                       gripcount=0,
                       background=colors.separator)
        
        # Frame
        style.configure("Themed.TFrame",
                       background=colors.panel_content_bg,
                       borderwidth=0,
                       relief="flat")
        
        style.configure("Header.TFrame",
                       background=colors.panel_header_bg,
                       borderwidth=theme.spacing.border_width,
                       relief="solid")
        
        # Label
        style.configure("Themed.TLabel",
                       background=colors.panel_content_bg,
                       foreground=colors.primary_text,
                       font=(typography.font_family, typography.font_size_normal))
        
        style.configure("Header.TLabel",
                       background=colors.panel_header_bg,
                       foreground=colors.panel_header_fg,
                       font=(typography.font_family, typography.font_size_normal, typography.font_weight_bold))
        
        # Button
        style.configure("Themed.TButton",
                       background=colors.button_bg,
                       foreground=colors.button_fg,
                       borderwidth=0,
                       focuscolor="none",
                       font=(typography.font_family, typography.font_size_normal))
        
        style.map("Themed.TButton",
                 background=[("active", colors.button_hover),
                           ("pressed", colors.button_active)])


# Global theme manager instance
theme_manager = ThemeManager()


def get_theme_manager() -> ThemeManager:
    """Get the global theme manager instance."""
    return theme_manager


def set_global_theme(theme_name: str) -> bool:
    """Set the global theme."""
    return theme_manager.set_theme(theme_name)


def get_current_theme() -> Theme:
    """Get the current global theme."""
    return theme_manager.get_current_theme()