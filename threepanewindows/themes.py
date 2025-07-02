import platform
import sys
from dataclasses import dataclass, field
from enum import Enum
import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, List, Optional, Union, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .custom_scrollbar import ThemedScrollbar

if sys.platform == "win32":
    import ctypes

    def set_windows_titlebar_color(hwnd: int, color_hex: str) -> None:
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
            print(f"Failed to set title bar color: {e}")


class ThemeType(Enum):
    LIGHT = "light"
    DARK = "dark"
    BLUE = "blue"
    GREEN = "green"
    PURPLE = "purple"
    CUSTOM = "custom"


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
    font_size_small: int = 9
    font_size_normal: int = 10
    font_size_large: int = 12
    font_size_title: int = 14
    font_weight_normal: str = "normal"
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

        theme = self.get_theme(name)
        if theme:
            self._current_theme = theme
            self._style_cache.clear()

            if window:
                if sys.platform == "win32":
                    try:
                        # Try to get the window handle
                        hwnd = window.winfo_id()
                        # If it's a child window, get the parent
                        parent_hwnd = ctypes.windll.user32.GetParent(hwnd)
                        if parent_hwnd:
                            hwnd = parent_hwnd
                        set_windows_titlebar_color(hwnd, theme.colors.primary_bg)
                    except Exception as e:
                        print(f"Could not set Windows titlebar color: {e}")
                elif sys.platform == "darwin":
                    self._apply_macos_custom_titlebar(window, theme.colors)

            return True
        return False

    def _apply_macos_custom_titlebar(self, window: tk.Tk, colors: ColorScheme) -> None:
        window.overrideredirect(True)
        style = ttk.Style()
        style.configure("CustomTitle.TFrame", background=colors.panel_header_bg)

        titlebar = ttk.Frame(window, style="CustomTitle.TFrame")
        titlebar.pack(side="top", fill="x")

        def brighten(color_hex: str, factor: float = 1.2) -> str:
            color_hex = color_hex.lstrip("#")
            r, g, b = [
                min(int(int(color_hex[i : i + 2], 16) * factor), 255) for i in (0, 2, 4)
            ]
            return f"#{r:02x}{g:02x}{b:02x}"

        def create_circle_button(
            base_color: str, command: Callable[[], None]
        ) -> ttk.Label:
            btn = ttk.Label(
                titlebar,
                text="",
                background=base_color,
                width=2,
                anchor="center",
                relief="flat",
            )
            btn.pack(side="left", padx=(6, 4), pady=4)

            def on_enter(e: tk.Event) -> None:
                btn.configure(background=brighten(base_color))

            def on_leave(e: tk.Event) -> None:
                btn.configure(background=base_color)

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            btn.bind("<Button-1>", lambda e: command())
            return btn

        create_circle_button("#ff5f57", window.destroy)
        create_circle_button("#ffbd2e", lambda: window.iconify())

        def toggle_fullscreen() -> None:
            is_fullscreen = window.attributes("-fullscreen")
            window.attributes("-fullscreen", not is_fullscreen)

        create_circle_button("#28c840", toggle_fullscreen)

        title_label = ttk.Label(
            titlebar,
            text=window.title(),
            background=colors.panel_header_bg,
            foreground=colors.panel_header_fg,
            anchor="center",
            font=("Segoe UI", 12, "bold"),
        )
        title_label.pack(side="left", padx=10)

        def start_move(event: tk.Event) -> None:
            window._drag_start_x = event.x  # type: ignore[attr-defined]
            window._drag_start_y = event.y  # type: ignore[attr-defined]

        def do_move(event: tk.Event) -> None:
            x = window.winfo_pointerx() - window._drag_start_x  # type: ignore[attr-defined]
            y = window.winfo_pointery() - window._drag_start_y  # type: ignore[attr-defined]
            window.geometry(f"+{x}+{y}")

        titlebar.bind("<ButtonPress-1>", start_move)
        titlebar.bind("<B1-Motion>", do_move)

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
                "font": (
                    typography.font_family,
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

        base_style = {
            "font": (typography.font_family, typography.font_size_normal),
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

        # Configure ttk styles - choose base theme based on current theme
        base_theme = "clam"  # Default base theme

        # On Windows, use vista or winnative for better integration
        # import platform
        # if platform.system() == "Windows":
        #    try:
        #        # Try vista first (better looking), fall back to winnative
        #        available_themes = style.theme_names()
        #        if "vista" in available_themes:
        #            base_theme = "vista"
        #        elif "winnative" in available_themes:
        #            base_theme = "winnative"
        #    except:
        #        pass

        style.theme_use(base_theme)

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
            font=(typography.font_family, typography.font_size_normal),
        )

        style.configure(
            "Header.TLabel",
            background=colors.panel_header_bg,
            foreground=colors.panel_header_fg,
            font=(
                typography.font_family,
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

        # LabelFrame
        style.configure(
            "Themed.TLabelframe",
            background=colors.panel_content_bg,
            bordercolor=colors.border,
            lightcolor=colors.border,
            darkcolor=colors.border,
        )

        style.configure(
            "Themed.TLabelframe.Label",
            background=colors.panel_content_bg,
            foreground=colors.primary_text,
            font=(
                typography.font_family,
                typography.font_size_normal,
                typography.font_weight_bold,
            ),
        )

        # Menubutton
        style.configure(
            "Themed.TMenubutton",
            background=colors.button_bg,
            foreground=colors.button_fg,
            bordercolor=colors.border,
            lightcolor=colors.border,
            darkcolor=colors.border,
            font=(typography.font_family, typography.font_size_normal),
        )

        style.map(
            "Themed.TMenubutton",
            background=[
                ("active", colors.button_hover),
                ("pressed", colors.button_active),
            ],
            foreground=[
                ("active", colors.button_fg),
                ("pressed", colors.button_fg),
            ],
        )

        # Separator
        style.configure(
            "Themed.TSeparator",
            background=colors.separator,
        )

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


# Global instance
theme_manager = ThemeManager()


def get_theme_manager() -> ThemeManager:
    return theme_manager


def set_global_theme(
    theme_name: Union[str, ThemeType],
    custom_scheme: Optional[ColorScheme] = None,
    window: Optional[tk.Tk] = None,
) -> bool:
    return theme_manager.set_theme(theme_name, custom_scheme, window)


def get_current_theme() -> Theme:
    return theme_manager.get_current_theme()
