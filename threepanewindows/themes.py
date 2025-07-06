import platform
import tkinter as tk
from dataclasses import dataclass, field
from enum import Enum
from tkinter import ttk
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

if TYPE_CHECKING:
    from .custom_scrollbar import ThemedScrollbar

# Import platform-specific functionality
from .platform import platform_handler


class ThemeType(Enum):
    LIGHT = "light"
    DARK = "dark"
    BLUE = "blue"
    GREEN = "green"
    PURPLE = "purple"
    CUSTOM = "custom"
    SYSTEM = "system"
    NATIVE = "native"
    NATIVE_LIGHT = "native_light"
    NATIVE_DARK = "native_dark"


@dataclass
class ColorScheme:
    primary_bg: str = "#ffffff"
    secondary_bg: str = "#f5f5f5"
    accent_bg: str = "#e3f2fd"
    primary_text: str = "#212121"
    secondary_text: str = "#757575"
    accent_text: str = "#1976d2"
    border: str = "#e0e0e0"
    separator: str = "#bdbdbd"
    button_bg: str = "#2196f3"
    button_fg: str = "#ffffff"
    button_hover: str = "#1976d2"
    button_active: str = "#0d47a1"
    success: str = "#4caf50"
    warning: str = "#ff9800"
    error: str = "#f44336"
    info: str = "#2196f3"
    panel_header_bg: str = "#fafafa"
    panel_header_fg: str = "#424242"
    panel_content_bg: str = "#ffffff"
    drag_indicator: str = "#2196f3"
    drop_zone: str = "#e3f2fd"


@dataclass
class Typography:
    font_family: str = "Segoe UI"
    font_family_fallback: str = "Arial"
    font_size_small: int = 9
    font_size_normal: int = 10
    font_size_large: int = 12
    font_size_title: int = 14
    font_weight_light: str = "normal"
    font_weight_normal: str = "normal"
    font_weight_medium: str = "bold"
    font_weight_bold: str = "bold"


@dataclass
class Spacing:
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
    name: str
    colors: ColorScheme = field(default_factory=ColorScheme)
    typography: Typography = field(default_factory=Typography)
    spacing: Spacing = field(default_factory=Spacing)
    animation_duration: int = 200
    enable_animations: bool = True
    enable_shadows: bool = True
    enable_gradients: bool = False
    corner_radius: int = 4


class ThemeManager:
    def __init__(
        self,
        theme: Optional[Union[str, ThemeType]] = None,
        custom_scheme: Optional[ColorScheme] = None,
    ) -> None:
        self._themes: Dict[str, Theme] = {}
        self._current_theme: Optional[Theme] = None
        self._style_cache: Dict[str, Dict[str, Any]] = {}
        self._initialize_default_themes()
        if theme == ThemeType.CUSTOM and custom_scheme:
            custom_theme = Theme(name="custom", colors=custom_scheme)
            self.register_theme(custom_theme)
            self.set_theme("custom")
        elif theme:
            self.set_theme(theme)

    # original
    def _initialize_default_themes(self) -> None:
        """Initialize default themes."""

        # Light Theme
        light_colors = ColorScheme(
            primary_bg="#ffffff",
            secondary_bg="#f8f9fa",
            accent_bg="#e3f2fd",
            primary_text="#212121",
            secondary_text="#6c757d",
            accent_text="#0d6efd",
            border="#dee2e6",
            separator="#e9ecef",
            button_bg="#6c757d",  # "#0d6efd",
            button_fg="#ffffff",
            button_hover="#0b5ed7",
            button_active="#0a58ca",
            panel_header_bg="#f8f9fa",
            panel_header_fg="#495057",
            panel_content_bg="#ffffff",
            drag_indicator="#0d6efd",
            drop_zone="#e7f3ff",
        )

        self._themes["light"] = Theme(
            name="Light",
            colors=light_colors,
            typography=Typography(font_family="Segoe UI"),
            spacing=Spacing(),
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
            drop_zone="#094771",
        )

        self._themes["dark"] = Theme(
            name="Dark",
            colors=dark_colors,
            typography=Typography(font_family="Segoe UI"),
            spacing=Spacing(),
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
            drop_zone="#e8f0fe",
        )

        self._themes["blue"] = Theme(
            name="Blue Professional",
            colors=blue_colors,
            typography=Typography(font_family="Segoe UI"),
            spacing=Spacing(),
        )

        # Green Theme
        green_colors = ColorScheme(
            primary_bg="#ffffff",
            secondary_bg="#f8f9fa",
            accent_bg="#e8f5e8",
            primary_text="#1b5e20",
            secondary_text="#388e3c",
            accent_text="#2e7d32",
            border="#c8e6c9",
            separator="#a5d6a7",
            button_bg="#4caf50",
            button_fg="#ffffff",
            button_hover="#388e3c",
            button_active="#2e7d32",
            panel_header_bg="#e8f5e8",
            panel_header_fg="#1b5e20",
            panel_content_bg="#ffffff",
            drag_indicator="#4caf50",
            drop_zone="#e8f5e8",
        )

        self._themes["green"] = Theme(
            name="Green Nature",
            colors=green_colors,
            typography=Typography(font_family="Segoe UI"),
            spacing=Spacing(),
        )

        # Purple Theme
        purple_colors = ColorScheme(
            primary_bg="#ffffff",
            secondary_bg="#f8f9fa",
            accent_bg="#f3e5f5",
            primary_text="#4a148c",
            secondary_text="#7b1fa2",
            accent_text="#8e24aa",
            border="#ce93d8",
            separator="#ba68c8",
            button_bg="#9c27b0",
            button_fg="#ffffff",
            button_hover="#7b1fa2",
            button_active="#6a1b9a",
            panel_header_bg="#f3e5f5",
            panel_header_fg="#4a148c",
            panel_content_bg="#ffffff",
            drag_indicator="#9c27b0",
            drop_zone="#f3e5f5",
        )

        self._themes["purple"] = Theme(
            name="Purple Elegance",
            colors=purple_colors,
            typography=Typography(font_family="Segoe UI"),
            spacing=Spacing(),
        )

        # System Theme - dynamically follows OS theme
        self._initialize_system_theme()

        # Platform Native Themes - use platform-specific styling
        self._initialize_native_themes()

        # Set default theme
        self._current_theme = self._themes["light"]

    def _initialize_system_theme(self) -> None:
        """Initialize system theme that follows OS theme."""
        try:
            import darkdetect  # type: ignore[import-untyped]

            is_dark = darkdetect.isDark()
        except ImportError:
            # Fallback if darkdetect is not available
            is_dark = False

        # Use existing dark or light theme as base for system theme
        base_theme = self._themes["dark"] if is_dark else self._themes["light"]

        # Create system theme as a copy of the appropriate base theme
        self._themes["system"] = Theme(
            name="System",
            colors=base_theme.colors,
            typography=base_theme.typography,
            spacing=base_theme.spacing,
            animation_duration=base_theme.animation_duration,
            enable_animations=base_theme.enable_animations,
            enable_shadows=base_theme.enable_shadows,
            enable_gradients=base_theme.enable_gradients,
            corner_radius=base_theme.corner_radius,
        )

    def _update_system_theme(self) -> bool:
        """Update system theme to match current OS theme."""
        try:
            import darkdetect

            is_dark = darkdetect.isDark()
        except ImportError:
            is_dark = False

        # Update system theme to match OS
        base_theme = self._themes["dark"] if is_dark else self._themes["light"]
        self._themes["system"] = Theme(
            name="System",
            colors=base_theme.colors,
            typography=base_theme.typography,
            spacing=base_theme.spacing,
            animation_duration=base_theme.animation_duration,
            enable_animations=base_theme.enable_animations,
            enable_shadows=base_theme.enable_shadows,
            enable_gradients=base_theme.enable_gradients,
            corner_radius=base_theme.corner_radius,
        )

        return bool(is_dark)

    def _initialize_native_themes(self) -> None:
        """Initialize platform-native themes."""
        try:
            # Get platform-specific colors and typography
            platform_colors = platform_handler.get_platform_native_colors()
            platform_typography = platform_handler.get_platform_typography()

            if platform_colors and platform_typography:
                # Create native light theme
                native_light_colors = self._create_native_color_scheme(
                    platform_handler.get_platform_native_colors(is_dark=False)
                )
                native_light_typography = self._create_native_typography(
                    platform_typography
                )

                self._themes["native_light"] = Theme(
                    name="Native Light",
                    colors=native_light_colors,
                    typography=native_light_typography,
                    spacing=Spacing(),
                )

                # Create native dark theme
                native_dark_colors = self._create_native_color_scheme(
                    platform_handler.get_platform_native_colors(is_dark=True)
                )

                self._themes["native_dark"] = Theme(
                    name="Native Dark",
                    colors=native_dark_colors,
                    typography=native_light_typography,  # Same typography for both
                    spacing=Spacing(),
                )

                # Create adaptive native theme that follows system
                is_system_dark = platform_handler.is_dark_mode()
                base_native_theme = (
                    self._themes["native_dark"]
                    if is_system_dark
                    else self._themes["native_light"]
                )

                self._themes["native"] = Theme(
                    name="Native",
                    colors=base_native_theme.colors,
                    typography=base_native_theme.typography,
                    spacing=base_native_theme.spacing,
                    animation_duration=base_native_theme.animation_duration,
                    enable_animations=base_native_theme.enable_animations,
                    enable_shadows=base_native_theme.enable_shadows,
                    enable_gradients=base_native_theme.enable_gradients,
                    corner_radius=base_native_theme.corner_radius,
                )

        except Exception as e:
            print(f"Warning: Could not initialize native themes: {e}")
            # Create fallback native themes based on existing themes
            self._create_fallback_native_themes()

    def _create_native_color_scheme(self, platform_colors: dict) -> ColorScheme:
        """Create a ColorScheme from platform-specific colors."""
        # Clean up selection_bg to remove alpha channel if present
        selection_bg = platform_colors.get("selection_bg", "#e3f2fd")
        if selection_bg and len(selection_bg) > 7:  # Has alpha channel
            selection_bg = selection_bg[:7]  # Remove alpha part

        # If selection_bg is still invalid, create a lighter version of accent color
        accent_color = platform_colors.get("accent", "#0078d4")
        if not selection_bg or selection_bg == accent_color + "40":
            selection_bg = self._lighten_color(accent_color, 0.8)

        return ColorScheme(
            primary_bg=platform_colors.get("window_bg", "#ffffff"),
            secondary_bg=platform_colors.get("sidebar_bg", "#f5f5f5"),
            accent_bg=selection_bg,
            primary_text=platform_colors.get("text_primary", "#000000"),
            secondary_text=platform_colors.get("text_secondary", "#666666"),
            accent_text=accent_color,
            border=platform_colors.get("border", "#cccccc"),
            separator=platform_colors.get("separator", "#cccccc"),
            button_bg=platform_colors.get("button_bg", "#e6e6e6"),
            button_fg=platform_colors.get("text_primary", "#000000"),
            button_hover=platform_colors.get("button_hover", "#d9d9d9"),
            button_active=accent_color,
            success="#4caf50",
            warning="#ff9800",
            error="#f44336",
            info=accent_color,
            panel_header_bg=platform_colors.get("sidebar_bg", "#f5f5f5"),
            panel_header_fg=platform_colors.get("text_primary", "#000000"),
            panel_content_bg=platform_colors.get("content_bg", "#ffffff"),
            drag_indicator=accent_color,
            drop_zone=selection_bg,
        )

    def _create_native_typography(self, platform_typography: dict) -> Typography:
        """Create a Typography from platform-specific typography."""
        return Typography(
            font_family=platform_typography.get("font_family", "Segoe UI"),
            font_family_fallback=platform_typography.get(
                "font_family_fallback", "Arial"
            ),
            font_size_small=platform_typography.get("font_size_small", 9),
            font_size_normal=platform_typography.get("font_size_normal", 10),
            font_size_large=platform_typography.get("font_size_large", 12),
            font_size_title=platform_typography.get("font_size_title", 14),
            font_weight_light=platform_typography.get("font_weight_light", "normal"),
            font_weight_normal=platform_typography.get("font_weight_normal", "normal"),
            font_weight_medium=platform_typography.get("font_weight_medium", "bold"),
            font_weight_bold=platform_typography.get("font_weight_bold", "bold"),
        )

    def _create_fallback_native_themes(self) -> None:
        """Create fallback native themes when platform detection fails."""
        # Use existing themes as base for native themes
        self._themes["native_light"] = Theme(
            name="Native Light",
            colors=self._themes["light"].colors,
            typography=self._themes["light"].typography,
            spacing=self._themes["light"].spacing,
        )

        self._themes["native_dark"] = Theme(
            name="Native Dark",
            colors=self._themes["dark"].colors,
            typography=self._themes["dark"].typography,
            spacing=self._themes["dark"].spacing,
        )

        # Adaptive native theme
        try:
            is_system_dark = platform_handler.is_dark_mode()
            base_theme = (
                self._themes["native_dark"]
                if is_system_dark
                else self._themes["native_light"]
            )
        except (ImportError, AttributeError, KeyError):
            base_theme = self._themes["native_light"]

        self._themes["native"] = Theme(
            name="Native",
            colors=base_theme.colors,
            typography=base_theme.typography,
            spacing=base_theme.spacing,
        )

    def set_theme(
        self,
        name: Union[str, ThemeType],
        custom_scheme: Optional[ColorScheme] = None,
        window: Optional[tk.Tk] = None,
    ) -> bool:
        if custom_scheme and (
            name == ThemeType.CUSTOM
            or (hasattr(name, "value") and name.value == "custom")
        ):
            custom_theme = Theme(name="custom", colors=custom_scheme)
            self.register_theme(custom_theme)
            name = "custom"

        # Handle native theme updates
        theme_name = name.value if hasattr(name, "value") else str(name).lower()
        if theme_name in ["native", "native_light", "native_dark"]:
            self._update_native_themes()

        theme = self.get_theme(name)
        if theme:
            self._current_theme = theme
            self._style_cache.clear()

            if window:
                # Use platform-specific titlebar customization
                platform_handler.apply_custom_titlebar(window, theme.colors)

                # Apply platform-specific styling for native themes
                if theme_name.startswith("native"):
                    self._apply_platform_specific_styling(window, theme)

                # Apply the theme to the entire window
                self.apply_theme_to_window(window)

            return True
        return False

    def _update_native_themes(self) -> None:
        """Update native themes to reflect current system settings."""
        try:
            # Re-initialize native themes with current system settings
            self._initialize_native_themes()
        except Exception as e:
            print(f"Warning: Could not update native themes: {e}")

    def _apply_platform_specific_styling(self, window: tk.Tk, theme: Theme) -> None:
        """Apply platform-specific styling enhancements."""
        try:
            # Apply macOS-specific styling if available
            if hasattr(platform_handler, "apply_macos_native_styling"):
                platform_handler.apply_macos_native_styling(window, theme.colors)
        except Exception as e:
            print(f"Warning: Could not apply platform-specific styling: {e}")

    def refresh_system_theme(self) -> bool:
        """
        Refresh system and native themes to match current OS settings.

        Returns:
            True if themes were updated successfully
        """
        try:
            # Update system theme
            self._update_system_theme()

            # Update native themes
            self._update_native_themes()

            # If current theme is system or native, refresh it
            current_name = (
                self._current_theme.name.lower() if self._current_theme else ""
            )
            if current_name in ["system", "native", "native_light", "native_dark"]:
                # Re-apply the current theme to pick up changes
                theme_type = None
                for theme_enum in ThemeType:
                    if theme_enum.value == current_name:
                        theme_type = theme_enum
                        break

                if theme_type:
                    return self.set_theme(theme_type)

            return True
        except Exception as e:
            print(f"Warning: Could not refresh system theme: {e}")
            return False

    def get_theme(self, name: Union[str, ThemeType]) -> Optional[Theme]:
        if hasattr(name, "value"):
            name = name.value
        return self._themes.get(str(name).lower())

    def get_current_theme(self) -> Theme:
        return self._current_theme or self._themes["light"]

    @property
    def current_theme(self) -> ThemeType:
        """Get the current theme as a ThemeType enum."""
        current = self.get_current_theme()
        # Find the theme name by comparing the theme object
        for name, theme in self._themes.items():
            if theme is current:
                # Convert string name to ThemeType enum
                try:
                    return ThemeType(name)
                except ValueError:
                    # If it's a custom theme not in ThemeType enum
                    return ThemeType.CUSTOM
        return ThemeType.LIGHT  # fallback

    @property
    def current_scheme(self) -> ColorScheme:
        """Get the current color scheme (alias for current theme colors)."""
        return self.get_current_theme().colors

    def get_color(self, color_name: str) -> Optional[str]:
        """Get a color value from the current theme."""
        try:
            color_value = getattr(self.get_current_theme().colors, color_name)
            return str(color_value) if color_value is not None else None
        except AttributeError:
            return None

    def register_theme(self, theme: Theme) -> None:
        self._themes[theme.name.lower()] = theme

    def get_available_themes(self) -> List[str]:
        """Get list of all available theme names."""
        return list(self._themes.keys())

    def get_available_theme_types(self) -> List[ThemeType]:
        """Get list of available theme types as enums."""
        available_types = []
        for name in self._themes.keys():
            try:
                theme_type = ThemeType(name)
                available_types.append(theme_type)
            except ValueError:
                # Custom themes that don't have enum values
                if name == "custom":
                    available_types.append(ThemeType.CUSTOM)
        return available_types

    def is_native_theme_available(self) -> bool:
        """Check if native themes are available on this platform."""
        return "native" in self._themes

    def get_platform_info(self) -> dict:
        """Get information about the current platform and theming capabilities."""
        return {
            "platform": platform.system(),
            "supports_dark_mode_detection": hasattr(platform_handler, "is_dark_mode"),
            "supports_accent_color_detection": hasattr(
                platform_handler, "get_system_accent_color"
            ),
            "supports_native_theming": self.is_native_theme_available(),
            "current_dark_mode": (
                platform_handler.is_dark_mode()
                if hasattr(platform_handler, "is_dark_mode")
                else False
            ),
            "system_accent_color": (
                platform_handler.get_system_accent_color()
                if hasattr(platform_handler, "get_system_accent_color")
                else None
            ),
        }

    def get_style(self, component: str, state: str = "normal") -> Dict[str, Any]:
        """Get styling for a component in a specific state."""
        cache_key = f"{component}_{state}"
        if cache_key in self._style_cache:
            return self._style_cache[cache_key]

        theme = self.get_current_theme()
        style = self._generate_style(component, state, theme)
        self._style_cache[cache_key] = style
        return style

    def _generate_style(
        self, component: str, state: str, theme: Theme
    ) -> Dict[str, Any]:
        """Generate style dictionary for a component."""
        colors = theme.colors
        typography = theme.typography
        spacing = theme.spacing

        # Create font tuple with fallback
        font_family = self._get_available_font(
            typography.font_family, typography.font_family_fallback
        )

        base_style = {
            "font": (font_family, typography.font_size_normal),
            "relief": "flat",
            "borderwidth": 0,
        }

        if component == "panel_header":
            return {
                **base_style,
                "bg": colors.panel_header_bg,
                "fg": colors.panel_header_fg,
                "font": (
                    font_family,
                    typography.font_size_normal,
                    typography.font_weight_bold,
                ),
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

    def _get_available_font(
        self, primary_font: str, fallback_font: str = "Arial"
    ) -> str:
        """
        Get an available font from the system, with fallback.

        Args:
            primary_font: Preferred font family
            fallback_font: Fallback font family

        Returns:
            Available font family name
        """
        try:
            import tkinter.font as tkfont

            available_fonts = tkfont.families()

            # Check if primary font is available
            if primary_font in available_fonts:
                return primary_font

            # Check if fallback font is available
            if fallback_font in available_fonts:
                return fallback_font

            # Platform-specific fallbacks
            system = platform.system().lower()
            if system == "darwin":  # macOS
                macos_fonts = ["SF Pro Display", "Helvetica Neue", "Helvetica", "Arial"]
                for font in macos_fonts:
                    if font in available_fonts:
                        return font
            elif system == "windows":
                windows_fonts = ["Segoe UI", "Tahoma", "Arial"]
                for font in windows_fonts:
                    if font in available_fonts:
                        return font
            else:  # Linux and others
                linux_fonts = [
                    "Ubuntu",
                    "Cantarell",
                    "DejaVu Sans",
                    "Liberation Sans",
                    "Arial",
                ]
                for font in linux_fonts:
                    if font in available_fonts:
                        return font

            # Final fallback
            return "TkDefaultFont"
        except Exception:
            return fallback_font

    def _lighten_color(self, hex_color: str, factor: float) -> str:
        """
        Lighten a hex color by mixing it with white.

        Args:
            hex_color: Hex color string (e.g., '#ff0000')
            factor: Lightening factor (0.0 = original, 1.0 = white)

        Returns:
            Lightened hex color string
        """
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

    def apply_theme_to_widget(self, widget, recursive: bool = True) -> None:
        """
        Apply current theme to a widget and optionally its children.

        Args:
            widget: The widget to theme
            recursive: Whether to theme child widgets as well
        """
        try:
            widget_class = widget.winfo_class()

            # Apply TTK widget theming (these are handled by apply_ttk_theme)
            if widget_class.startswith("T"):
                # TTK widgets are themed via style configuration
                pass
            else:
                # Apply TK widget theming
                if widget_class == "Text":
                    style = self.get_tk_widget_style("text")
                    widget.configure(**style)
                elif widget_class == "Listbox":
                    style = self.get_tk_widget_style("listbox")
                    widget.configure(**style)
                elif widget_class == "Canvas":
                    style = self.get_tk_widget_style("canvas")
                    widget.configure(**style)
                elif widget_class == "Entry":
                    style = self.get_tk_widget_style("entry")
                    widget.configure(**style)
                elif widget_class == "Label":
                    style = self.get_tk_widget_style("label")
                    widget.configure(**style)
                elif widget_class == "Button":
                    style = self.get_tk_widget_style("button")
                    widget.configure(**style)
                elif widget_class == "Frame":
                    style = self.get_tk_widget_style("frame")
                    widget.configure(**style)
                elif widget_class == "Toplevel":
                    theme = self.get_current_theme()
                    widget.configure(bg=theme.colors.primary_bg)
                elif widget_class == "Tk":
                    theme = self.get_current_theme()
                    widget.configure(bg=theme.colors.primary_bg)

            # Recursively apply to children if requested
            if recursive:
                try:
                    for child in widget.winfo_children():
                        self.apply_theme_to_widget(child, recursive=True)
                except Exception:
                    pass  # Some widgets don't support winfo_children()

        except Exception:
            # Silently ignore theming errors for individual widgets
            pass

    def apply_theme_to_window(self, window) -> None:
        """
        Apply current theme to an entire window and all its widgets.

        Args:
            window: The root window or toplevel to theme
        """
        try:
            # Apply TTK theme first
            style = ttk.Style(window)
            self.apply_ttk_theme(style)

            # Apply theme to the window and all its widgets
            self.apply_theme_to_widget(window, recursive=True)

        except Exception as e:
            print(f"Warning: Could not fully apply theme to window: {e}")

    def _is_dark_theme(self, colors: ColorScheme) -> bool:
        """Determine if a theme is dark based on its background color."""
        # Convert hex to RGB and check brightness
        bg_color = colors.panel_content_bg.lstrip("#")
        r, g, b = [int(bg_color[i : i + 2], 16) for i in (0, 2, 4)]
        # Calculate luminance (perceived brightness)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return luminance < 0.5  # Dark if luminance is less than 50%

    def get_tk_widget_style(
        self, widget_type: str, state: str = "normal"
    ) -> Dict[str, Any]:
        """Get styling for custom Tkinter widgets."""
        theme = self.get_current_theme()
        colors = theme.colors
        typography = theme.typography
        spacing = theme.spacing

        # Create font tuple with fallback
        font_family = self._get_available_font(
            typography.font_family, typography.font_family_fallback
        )

        base_style = {
            "font": (font_family, typography.font_size_normal),
            "relief": "flat",
            "borderwidth": 0,
        }

        if widget_type == "text":
            return {
                **base_style,
                "bg": colors.panel_content_bg,
                "fg": colors.primary_text,
                "insertbackground": colors.primary_text,
                "selectbackground": colors.accent_bg,
                "selectforeground": colors.primary_text,
                "highlightcolor": colors.accent_text,
                "highlightbackground": colors.border,
                "highlightthickness": 1,
                "borderwidth": 1,
                "relief": "solid",
            }

        elif widget_type == "listbox":
            return {
                **base_style,
                "bg": colors.panel_content_bg,
                "fg": colors.primary_text,
                "selectbackground": colors.accent_bg,
                "selectforeground": colors.primary_text,
                "highlightcolor": colors.accent_text,
                "highlightbackground": colors.border,
                "highlightthickness": 1,
                "borderwidth": 1,
                "relief": "solid",
                "activestyle": "dotbox",
            }

        elif widget_type == "scrollbar":
            # For dark themes, use specific dark colors
            is_dark_theme = self._is_dark_theme(colors)
            if is_dark_theme:
                scrollbar_bg = colors.secondary_bg  # #2d2d30 for dark theme
                trough_color = colors.panel_content_bg  # #1e1e1e for dark theme
                border_color = colors.panel_content_bg  # #1e1e1e for dark theme
                _ = colors.secondary_text  # Arrow color (not used in current config)
            else:
                # For colored themes, use white bg and theme color for trough/border
                scrollbar_bg = "#ffffff"  # White background
                trough_color = colors.accent_bg  # Theme color for trough
                border_color = colors.accent_bg  # Theme color for border
                _ = colors.primary_text  # Arrow color (not used in current config)

            return {
                "bg": scrollbar_bg,
                "troughcolor": trough_color,
                "activebackground": colors.button_hover,
                "highlightbackground": border_color,
                "highlightcolor": colors.accent_text,
                "relief": "flat",
                "borderwidth": 1,
                "highlightthickness": 0,
                "elementborderwidth": 1,
                "width": 16,
                # Additional options that work on most platforms
                "jump": 1,
                "repeatdelay": 300,
                "repeatinterval": 100,
            }

        elif widget_type == "canvas":
            return {
                "bg": colors.panel_content_bg,
                "highlightcolor": colors.accent_text,
                "highlightbackground": colors.border,
                "highlightthickness": 1,
                "relief": "flat",
                "borderwidth": 0,
            }

        elif widget_type == "frame":
            return {
                "bg": colors.panel_content_bg,
                "relief": "flat",
                "borderwidth": 0,
            }

        elif widget_type == "toplevel":
            return {
                "bg": colors.panel_content_bg,
                "relief": "flat",
                "borderwidth": 0,
            }

        elif widget_type == "label":
            return {
                **base_style,
                "bg": colors.panel_content_bg,
                "fg": colors.primary_text,
            }

        elif widget_type == "button":
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
                "cursor": "hand2",
                "padx": spacing.padding_normal,
                "pady": spacing.padding_small,
            }

        elif widget_type == "entry":
            return {
                **base_style,
                "bg": colors.panel_content_bg,
                "fg": colors.primary_text,
                "insertbackground": colors.primary_text,
                "selectbackground": colors.accent_bg,
                "selectforeground": colors.primary_text,
                "highlightcolor": colors.accent_text,
                "highlightbackground": colors.border,
                "highlightthickness": 1,
                "borderwidth": 1,
                "relief": "solid",
            }

        elif widget_type == "checkbutton":
            return {
                **base_style,
                "bg": colors.panel_content_bg,
                "fg": colors.primary_text,
                "activebackground": colors.panel_content_bg,
                "activeforeground": colors.primary_text,
                "selectcolor": colors.panel_content_bg,
                "cursor": "hand2",
            }

        elif widget_type == "radiobutton":
            return {
                **base_style,
                "bg": colors.panel_content_bg,
                "fg": colors.primary_text,
                "activebackground": colors.panel_content_bg,
                "activeforeground": colors.primary_text,
                "selectcolor": colors.panel_content_bg,
                "cursor": "hand2",
            }

        elif widget_type == "scale":
            return {
                **base_style,
                "bg": colors.panel_content_bg,
                "fg": colors.primary_text,
                "troughcolor": colors.secondary_bg,
                "activebackground": colors.button_hover,
                "highlightcolor": colors.accent_text,
                "highlightbackground": colors.border,
            }

        elif widget_type == "spinbox":
            return {
                **base_style,
                "bg": colors.panel_content_bg,
                "fg": colors.primary_text,
                "insertbackground": colors.primary_text,
                "selectbackground": colors.accent_bg,
                "selectforeground": colors.primary_text,
                "highlightcolor": colors.accent_text,
                "highlightbackground": colors.border,
                "highlightthickness": 1,
                "borderwidth": 1,
                "relief": "solid",
                "buttonbackground": colors.button_bg,
            }

        elif widget_type == "menu":
            return {
                **base_style,
                "bg": colors.panel_content_bg,
                "fg": colors.primary_text,
                "activebackground": colors.accent_bg,
                "activeforeground": colors.primary_text,
                "selectcolor": colors.accent_bg,
                "borderwidth": 1,
                "relief": "solid",
            }

        elif widget_type == "menubutton":
            return {
                **base_style,
                "bg": colors.button_bg,
                "fg": colors.button_fg,
                "activebackground": colors.button_hover,
                "activeforeground": colors.button_fg,
                "cursor": "hand2",
                "padx": spacing.padding_normal,
                "pady": spacing.padding_small,
            }

        elif widget_type == "message":
            return {
                **base_style,
                "bg": colors.panel_content_bg,
                "fg": colors.primary_text,
            }

        return base_style

    def apply_ttk_theme(self, style: ttk.Style) -> None:
        """Apply current theme to ttk widgets."""
        theme = self.get_current_theme()
        colors = theme.colors
        typography = theme.typography

        # Get available font with fallback
        font_family = self._get_available_font(
            typography.font_family, typography.font_family_fallback
        )

        # Configure ttk styles - choose base theme based on current theme
        base_theme = "clam"  # Default base theme

        # Choose better base theme based on platform and theme
        # Use clam for better theming control across all platforms
        try:
            available_themes = style.theme_names()

            # Always use clam for consistent theming
            if "clam" in available_themes:
                base_theme = "clam"
            else:
                # Fallback to default if clam is not available
                base_theme = available_themes[0] if available_themes else "default"

        except Exception:
            base_theme = "clam"

        style.theme_use(base_theme)

        # Configure default TTK widget styles
        # These will apply to all TTK widgets unless overridden

        # Default Label
        style.configure(
            "TLabel",
            background=colors.panel_content_bg,
            foreground=colors.primary_text,
            font=(font_family, typography.font_size_normal),
        )

        # Default Button
        style.configure(
            "TButton",
            background=colors.button_bg,
            foreground=colors.button_fg,
            font=(font_family, typography.font_size_normal),
            borderwidth=1,
            focuscolor="none",
            relief="raised",
            padding=(8, 4),
        )

        style.map(
            "TButton",
            background=[
                ("active", colors.button_hover),
                ("pressed", colors.button_active),
                ("disabled", colors.secondary_bg),
            ],
            foreground=[
                ("active", colors.button_fg),
                ("pressed", colors.button_fg),
                ("disabled", colors.secondary_text),
            ],
            relief=[
                ("pressed", "sunken"),
                ("active", "raised"),
            ],
        )

        # Default Entry
        style.configure(
            "TEntry",
            fieldbackground=colors.panel_content_bg,
            foreground=colors.primary_text,
            bordercolor=colors.border,
            lightcolor=colors.border,
            darkcolor=colors.border,
            font=(font_family, typography.font_size_normal),
            borderwidth=1,
        )

        style.map(
            "TEntry",
            focuscolor=[("focus", colors.accent_text)],
            bordercolor=[("focus", colors.accent_text)],
        )

        # Default Combobox
        style.configure(
            "TCombobox",
            fieldbackground=colors.panel_content_bg,
            foreground=colors.primary_text,
            background=colors.button_bg,
            bordercolor=colors.border,
            arrowcolor=colors.primary_text,
            font=(font_family, typography.font_size_normal),
            borderwidth=1,
        )

        style.map(
            "TCombobox",
            focuscolor=[("focus", colors.accent_text)],
            bordercolor=[("focus", colors.accent_text)],
            fieldbackground=[("readonly", colors.secondary_bg)],
        )

        # Default Checkbutton
        style.configure(
            "TCheckbutton",
            background=colors.panel_content_bg,
            foreground=colors.primary_text,
            focuscolor="none",
            font=(font_family, typography.font_size_normal),
        )

        style.map(
            "TCheckbutton",
            background=[("active", colors.panel_content_bg)],
            indicatorcolor=[
                ("selected", colors.accent_text),
                ("pressed", colors.button_active),
            ],
        )

        # Default Radiobutton
        style.configure(
            "TRadiobutton",
            background=colors.panel_content_bg,
            foreground=colors.primary_text,
            focuscolor="none",
            font=(font_family, typography.font_size_normal),
        )

        style.map(
            "TRadiobutton",
            background=[("active", colors.panel_content_bg)],
            indicatorcolor=[
                ("selected", colors.accent_text),
                ("pressed", colors.button_active),
            ],
        )

        # Default Frame
        style.configure(
            "TFrame",
            background=colors.panel_content_bg,
            borderwidth=0,
        )

        # Default LabelFrame
        style.configure(
            "TLabelframe",
            background=colors.panel_content_bg,
            foreground=colors.primary_text,
            bordercolor=colors.border,
            lightcolor=colors.border,
            darkcolor=colors.border,
            font=(font_family, typography.font_size_normal),
            borderwidth=1,
        )

        style.configure(
            "TLabelframe.Label",
            background=colors.panel_content_bg,
            foreground=colors.primary_text,
            font=(font_family, typography.font_size_normal),
        )

        # Default Notebook
        style.configure(
            "TNotebook",
            background=colors.secondary_bg,
            borderwidth=1,
            tabmargins=[2, 5, 2, 0],
        )

        style.configure(
            "TNotebook.Tab",
            background=colors.secondary_bg,
            foreground=colors.primary_text,
            padding=[12, 8, 12, 8],
            font=(font_family, typography.font_size_normal),
        )

        style.map(
            "TNotebook.Tab",
            background=[
                ("selected", colors.panel_content_bg),
                ("active", colors.accent_bg),
            ],
            foreground=[
                ("selected", colors.primary_text),
                ("active", colors.primary_text),
            ],
        )

        # Default Progressbar
        style.configure(
            "TProgressbar",
            background=colors.accent_text,
            troughcolor=colors.secondary_bg,
            borderwidth=1,
            lightcolor=colors.border,
            darkcolor=colors.border,
        )

        # Default Scale
        style.configure(
            "TScale",
            background=colors.panel_content_bg,
            troughcolor=colors.secondary_bg,
            borderwidth=1,
            lightcolor=colors.border,
            darkcolor=colors.border,
        )

        # Default Scrollbar
        style.configure(
            "TScrollbar",
            background=colors.secondary_bg,
            troughcolor=colors.panel_content_bg,
            bordercolor=colors.border,
            arrowcolor=colors.primary_text,
            darkcolor=colors.border,
            lightcolor=colors.border,
        )

        style.map(
            "TScrollbar",
            background=[
                ("active", colors.accent_bg),
                ("pressed", colors.accent_text),
            ],
        )

        # Default Treeview
        style.configure(
            "Treeview",
            background=colors.panel_content_bg,
            foreground=colors.primary_text,
            fieldbackground=colors.panel_content_bg,
            bordercolor=colors.border,
            lightcolor=colors.border,
            darkcolor=colors.border,
            font=(font_family, typography.font_size_normal),
        )

        style.configure(
            "Treeview.Heading",
            background=colors.panel_header_bg,
            foreground=colors.panel_header_fg,
            font=(
                font_family,
                typography.font_size_normal,
                typography.font_weight_bold,
            ),
        )

        style.map(
            "Treeview",
            background=[("selected", colors.accent_bg)],
            foreground=[("selected", colors.primary_text)],
        )

        style.map(
            "Treeview.Heading",
            background=[("active", colors.accent_bg)],
        )

        # Custom themed styles (for explicit theming)
        # PanedWindow
        style.configure(
            "Themed.TPanedwindow",
            background=colors.secondary_bg,
            borderwidth=0,
            relief="flat",
        )

        style.configure(
            "Themed.TPanedwindow.Sash",
            sashthickness=4,
            gripcount=0,
            background=colors.separator,
        )

        # Frame
        style.configure(
            "Themed.TFrame",
            background=colors.panel_content_bg,
            borderwidth=0,
            relief="flat",
        )

        style.configure(
            "Header.TFrame",
            background=colors.panel_header_bg,
            borderwidth=theme.spacing.border_width,
            relief="solid",
        )

        # Label
        style.configure(
            "Themed.TLabel",
            background=colors.panel_content_bg,
            foreground=colors.primary_text,
            font=(font_family, typography.font_size_normal),
        )

        style.configure(
            "Header.TLabel",
            background=colors.panel_header_bg,
            foreground=colors.panel_header_fg,
            font=(
                font_family,
                typography.font_size_normal,
                typography.font_weight_bold,
            ),
        )

        # Button
        style.configure(
            "Themed.TButton",
            background=colors.button_bg,
            foreground=colors.button_fg,
            borderwidth=0,
            focuscolor="none",
            font=(typography.font_family, typography.font_size_normal),
        )

        style.map(
            "Themed.TButton",
            background=[
                ("active", colors.button_hover),
                ("pressed", colors.button_active),
            ],
        )

        # Checkbutton
        style.configure(
            "Themed.TCheckbutton",
            background=colors.panel_content_bg,
            foreground=colors.primary_text,
            focuscolor="none",
            font=(typography.font_family, typography.font_size_normal),
        )

        style.map(
            "Themed.TCheckbutton",
            background=[
                ("active", colors.panel_content_bg),
                ("pressed", colors.panel_content_bg),
            ],
            foreground=[
                ("active", colors.primary_text),
                ("pressed", colors.primary_text),
            ],
        )

        # Radiobutton
        style.configure(
            "Themed.TRadiobutton",
            background=colors.panel_content_bg,
            foreground=colors.primary_text,
            focuscolor="none",
            font=(typography.font_family, typography.font_size_normal),
        )

        style.map(
            "Themed.TRadiobutton",
            background=[
                ("active", colors.panel_content_bg),
                ("pressed", colors.panel_content_bg),
            ],
            foreground=[
                ("active", colors.primary_text),
                ("pressed", colors.primary_text),
            ],
        )

        # Entry
        style.configure(
            "Themed.TEntry",
            fieldbackground=colors.panel_content_bg,
            background=colors.panel_content_bg,
            foreground=colors.primary_text,
            bordercolor=colors.border,
            lightcolor=colors.border,
            darkcolor=colors.border,
            insertcolor=colors.primary_text,
            selectbackground=colors.accent_bg,
            selectforeground=colors.primary_text,
            font=(typography.font_family, typography.font_size_normal),
        )

        style.map(
            "Themed.TEntry",
            fieldbackground=[
                ("focus", colors.panel_content_bg),
                ("!focus", colors.panel_content_bg),
            ],
            bordercolor=[
                ("focus", colors.accent_text),
                ("!focus", colors.border),
            ],
        )

        # Combobox
        style.configure(
            "Themed.TCombobox",
            fieldbackground=colors.panel_content_bg,
            background=colors.panel_content_bg,
            foreground=colors.primary_text,
            bordercolor=colors.border,
            lightcolor=colors.border,
            darkcolor=colors.border,
            insertcolor=colors.primary_text,
            selectbackground=colors.accent_bg,
            selectforeground=colors.primary_text,
            font=(typography.font_family, typography.font_size_normal),
        )

        style.map(
            "Themed.TCombobox",
            fieldbackground=[
                ("focus", colors.panel_content_bg),
                ("!focus", colors.panel_content_bg),
            ],
            bordercolor=[
                ("focus", colors.accent_text),
                ("!focus", colors.border),
            ],
        )

        # Spinbox
        style.configure(
            "Themed.TSpinbox",
            fieldbackground=colors.panel_content_bg,
            background=colors.panel_content_bg,
            foreground=colors.primary_text,
            bordercolor=colors.border,
            lightcolor=colors.border,
            darkcolor=colors.border,
            insertcolor=colors.primary_text,
            selectbackground=colors.accent_bg,
            selectforeground=colors.primary_text,
            font=(typography.font_family, typography.font_size_normal),
        )

        style.map(
            "Themed.TSpinbox",
            fieldbackground=[
                ("focus", colors.panel_content_bg),
                ("!focus", colors.panel_content_bg),
            ],
            bordercolor=[
                ("focus", colors.accent_text),
                ("!focus", colors.border),
            ],
        )

        # Scale - configure both orientations
        style.configure(
            "Themed.Horizontal.TScale",
            background=colors.panel_content_bg,
            troughcolor=colors.secondary_bg,
            bordercolor=colors.border,
            lightcolor=colors.border,
            darkcolor=colors.border,
        )

        style.configure(
            "Themed.Vertical.TScale",
            background=colors.panel_content_bg,
            troughcolor=colors.secondary_bg,
            bordercolor=colors.border,
            lightcolor=colors.border,
            darkcolor=colors.border,
        )

        # Progressbar - configure both orientations
        style.configure(
            "Themed.Horizontal.TProgressbar",
            background=colors.accent_bg,
            troughcolor=colors.secondary_bg,
            bordercolor=colors.border,
            lightcolor=colors.border,
            darkcolor=colors.border,
        )

        style.configure(
            "Themed.Vertical.TProgressbar",
            background=colors.accent_bg,
            troughcolor=colors.secondary_bg,
            bordercolor=colors.border,
            lightcolor=colors.border,
            darkcolor=colors.border,
        )

        # Scrollbar - Enhanced theming for better visibility
        is_dark_theme = self._is_dark_theme(colors)
        if is_dark_theme:
            scrollbar_bg = colors.secondary_bg
            scrollbar_trough = colors.panel_content_bg
            scrollbar_arrow = colors.secondary_text
        else:
            scrollbar_bg = colors.panel_content_bg
            scrollbar_trough = colors.accent_bg
            scrollbar_arrow = colors.primary_text

        style.configure(
            "Themed.Vertical.TScrollbar",
            background=scrollbar_bg,
            troughcolor=scrollbar_trough,
            bordercolor=colors.border,
            arrowcolor=scrollbar_arrow,
            darkcolor=colors.border,
            lightcolor=colors.panel_content_bg,
            relief="flat",
            borderwidth=1,
        )

        style.configure(
            "Themed.Horizontal.TScrollbar",
            background=scrollbar_bg,
            troughcolor=scrollbar_trough,
            bordercolor=colors.border,
            arrowcolor=scrollbar_arrow,
            darkcolor=colors.border,
            lightcolor=colors.panel_content_bg,
            relief="flat",
            borderwidth=1,
        )

        style.map(
            "Themed.Vertical.TScrollbar",
            background=[
                ("active", colors.button_hover),
                ("pressed", colors.button_active),
            ],
            troughcolor=[
                ("active", scrollbar_trough),
                ("pressed", scrollbar_trough),
            ],
            arrowcolor=[
                ("active", colors.accent_text),
                ("pressed", colors.accent_text),
            ],
        )

        style.map(
            "Themed.Horizontal.TScrollbar",
            background=[
                ("active", colors.button_hover),
                ("pressed", colors.button_active),
            ],
            troughcolor=[
                ("active", scrollbar_trough),
                ("pressed", scrollbar_trough),
            ],
            arrowcolor=[
                ("active", colors.accent_text),
                ("pressed", colors.accent_text),
            ],
        )

        # Listbox (via Treeview styling)
        style.configure(
            "Themed.Treeview",
            background=colors.panel_content_bg,
            foreground=colors.primary_text,
            fieldbackground=colors.panel_content_bg,
            bordercolor=colors.border,
            lightcolor=colors.border,
            darkcolor=colors.border,
            font=(typography.font_family, typography.font_size_normal),
        )

        style.configure(
            "Themed.Treeview.Heading",
            background=colors.panel_header_bg,
            foreground=colors.panel_header_fg,
            font=(
                typography.font_family,
                typography.font_size_normal,
                typography.font_weight_bold,
            ),
        )

        style.map(
            "Themed.Treeview",
            background=[
                ("selected", colors.accent_bg),
                ("focus", colors.accent_bg),
            ],
            foreground=[
                ("selected", colors.primary_text),
                ("focus", colors.primary_text),
            ],
        )

        # Notebook
        style.configure(
            "Themed.TNotebook",
            background=colors.secondary_bg,
            bordercolor=colors.border,
            lightcolor=colors.border,
            darkcolor=colors.border,
        )

        style.configure(
            "Themed.TNotebook.Tab",
            background=colors.secondary_bg,
            foreground=colors.secondary_text,
            bordercolor=colors.border,
            lightcolor=colors.border,
            darkcolor=colors.border,
            font=(typography.font_family, typography.font_size_normal),
            padding=[12, 8, 12, 8],
        )

        style.map(
            "Themed.TNotebook.Tab",
            background=[
                ("selected", colors.panel_content_bg),
                ("active", colors.accent_bg),
            ],
            foreground=[
                ("selected", colors.primary_text),
                ("active", colors.primary_text),
            ],
        )


# Global theme manager instance
_global_theme_manager: Optional[ThemeManager] = None


def get_theme_manager() -> ThemeManager:
    """Get the global theme manager instance."""
    global _global_theme_manager
    if _global_theme_manager is None:
        _global_theme_manager = ThemeManager()
    return _global_theme_manager


def set_global_theme(
    theme: Union[str, ThemeType],
    custom_scheme: Optional[ColorScheme] = None,
    window: Optional[tk.Tk] = None,
) -> bool:
    """Set the global theme for all ThreePaneWindows components."""
    return get_theme_manager().set_theme(theme, custom_scheme, window)


# Add missing methods to ThemeManager class
def _add_missing_methods():
    """Add missing methods to ThemeManager class."""
    from typing import Any, Callable, Dict, List, Union

    def get_available_themes(self) -> List[str]:
        """Get list of available theme names."""
        return list(self._themes.keys())

    def list_themes(self) -> Dict[str, str]:
        """Get dictionary of theme names and their display names."""
        return {name: theme.name for name, theme in self._themes.items()}

    def should_use_custom_scrollbars(self) -> bool:
        """
        Determine whether to use custom scrollbars based on platform.

        Returns:
            bool: True if custom scrollbars should be used, False for native scrollbars

        Platform-specific behavior:
        - Windows: Custom scrollbars (better theming support)
        - macOS/Linux: Native scrollbars (better system integration)
        """
        return platform.system() == "Windows"

    def get_platform_info(self) -> Dict[str, str]:
        """
        Get platform information for display purposes.

        Returns:
            Dict containing platform name and recommended scrollbar type
        """
        system = platform.system()
        scrollbar_type = "custom" if self.should_use_custom_scrollbars() else "native"

        return {
            "platform": system,
            "scrollbar_type": scrollbar_type,
            "scrollbar_description": (
                "Custom scrollbars (better theming)"
                if scrollbar_type == "custom"
                else "Native scrollbars (better integration)"
            ),
        }

    def create_themed_scrollbar_auto(
        self,
        parent: tk.Widget,
        orient: str = "vertical",
        command: Optional[Callable] = None,
        **kwargs: Any,
    ) -> Union["ThemedScrollbar", ttk.Scrollbar]:
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
        scrollbar = create_themed_scrollbar(
            parent=parent,
            orient=orient,
            command=command,
            use_custom=use_custom,
            theme_manager=self,
            **kwargs,
        )
        return scrollbar  # type: ignore[no-any-return]

    # Add methods to ThemeManager class
    ThemeManager.get_available_themes = get_available_themes
    ThemeManager.list_themes = list_themes
    ThemeManager.should_use_custom_scrollbars = should_use_custom_scrollbars
    ThemeManager.get_platform_info = get_platform_info
    ThemeManager.create_themed_scrollbar_auto = create_themed_scrollbar_auto


# Call the function to add missing methods
_add_missing_methods()
