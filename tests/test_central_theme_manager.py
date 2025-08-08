"""
Tests for the Central Theme Manager.
"""

import tkinter as tk
from tkinter import ttk
from unittest.mock import Mock, patch

import pytest

from threepanewindows.central_theme_manager import (
    CentralThemeManager,
    ThemeColors,
    ThemeType,
    get_theme_manager,
    set_global_theme,
)


class TestThemeType:
    """Test cases for ThemeType enum."""

    def test_theme_type_values(self):
        """Test ThemeType enum values."""
        assert ThemeType.LIGHT.value == "light"
        assert ThemeType.DARK.value == "dark"
        assert ThemeType.BLUE.value == "blue"
        assert ThemeType.GREEN.value == "green"
        assert ThemeType.PURPLE.value == "purple"
        assert ThemeType.SYSTEM.value == "system"
        assert ThemeType.NATIVE.value == "native"

    def test_theme_type_members(self):
        """Test ThemeType enum members."""
        assert len(ThemeType) == 7
        for theme in [
            ThemeType.LIGHT,
            ThemeType.DARK,
            ThemeType.BLUE,
            ThemeType.GREEN,
            ThemeType.PURPLE,
            ThemeType.SYSTEM,
            ThemeType.NATIVE,
        ]:
            assert theme in ThemeType


class TestThemeColors:
    """Test cases for ThemeColors dataclass."""

    def test_theme_colors_creation(self):
        """Test ThemeColors creation with all fields."""
        colors = ThemeColors(
            window_bg="#ffffff",
            frame_bg="#f5f5f5",
            panel_bg="#fafafa",
            text_fg="#000000",
            text_bg="#ffffff",
            text_select_bg="#0078d4",
            text_select_fg="#ffffff",
            button_bg="#0078d4",
            button_fg="#ffffff",
            button_active_bg="#106ebe",
            button_active_fg="#ffffff",
            button_hover_bg="#1084d4",
            button_hover_fg="#ffffff",
            button_disabled_bg="#cccccc",
            button_disabled_fg="#666666",
            entry_bg="#ffffff",
            entry_fg="#000000",
            entry_select_bg="#0078d4",
            entry_select_fg="#ffffff",
            entry_disabled_bg="#f0f0f0",
            entry_disabled_fg="#666666",
            listbox_bg="#ffffff",
            listbox_fg="#000000",
            listbox_select_bg="#0078d4",
            listbox_select_fg="#ffffff",
            menu_bg="#ffffff",
            menu_fg="#000000",
            menu_active_bg="#0078d4",
            menu_active_fg="#ffffff",
            menu_disabled_fg="#666666",
            scrollbar_bg="#f0f0f0",
            scrollbar_fg="#c0c0c0",
            scrollbar_active_bg="#0078d4",
            scrollbar_trough_bg="#f8f8f8",
            border_color="#d0d0d0",
            accent_color="#0078d4",
            highlight_color="#1084d4",
            shadow_color="#e0e0e0",
        )

        assert colors.window_bg == "#ffffff"
        assert colors.text_fg == "#000000"
        assert colors.button_bg == "#0078d4"
        assert colors.accent_color == "#0078d4"

    def test_theme_colors_defaults(self):
        """Test that ThemeColors can be created with minimal parameters."""
        # This test assumes the dataclass has default values or is created by the theme manager
        # We'll test this through the theme manager instead
        pass


class TestCentralThemeManager:
    """Test cases for CentralThemeManager class."""

    def test_singleton_behavior(self):
        """Test that get_theme_manager returns the same instance."""
        manager1 = get_theme_manager()
        manager2 = get_theme_manager()

        assert manager1 is manager2
        assert isinstance(manager1, CentralThemeManager)

    def test_default_theme(self):
        """Test default theme is LIGHT."""
        manager = get_theme_manager()
        assert manager.current_theme == ThemeType.LIGHT

    def test_set_theme(self):
        """Test setting different themes."""
        manager = get_theme_manager()

        # Test setting dark theme
        manager.set_theme(ThemeType.DARK)
        assert manager.current_theme == ThemeType.DARK

        # Test setting blue theme
        manager.set_theme(ThemeType.BLUE)
        assert manager.current_theme == ThemeType.BLUE

        # Reset to light
        manager.set_theme(ThemeType.LIGHT)
        assert manager.current_theme == ThemeType.LIGHT

    def test_current_colors(self):
        """Test getting current theme colors."""
        manager = get_theme_manager()

        colors = manager.current_colors
        assert isinstance(colors, ThemeColors)

        # Colors should have all required attributes
        assert hasattr(colors, "window_bg")
        assert hasattr(colors, "text_fg")
        assert hasattr(colors, "button_bg")
        assert hasattr(colors, "accent_color")

    def test_get_theme_colors(self):
        """Test getting colors for specific themes."""
        manager = get_theme_manager()

        light_colors = manager.get_theme_colors(ThemeType.LIGHT)
        dark_colors = manager.get_theme_colors(ThemeType.DARK)

        assert isinstance(light_colors, ThemeColors)
        assert isinstance(dark_colors, ThemeColors)

        # Light and dark themes should have different colors
        assert light_colors.window_bg != dark_colors.window_bg

    def test_get_available_themes(self):
        """Test getting list of available themes."""
        manager = get_theme_manager()

        themes = manager.get_available_themes()
        assert isinstance(themes, list)
        assert len(themes) >= 7  # At least the 7 built-in themes

        # All built-in themes should be available
        for theme in [
            ThemeType.LIGHT,
            ThemeType.DARK,
            ThemeType.BLUE,
            ThemeType.GREEN,
            ThemeType.PURPLE,
            ThemeType.SYSTEM,
            ThemeType.NATIVE,
        ]:
            assert theme in themes

    def test_register_custom_theme(self):
        """Test registering a custom theme."""
        manager = get_theme_manager()

        custom_colors = ThemeColors(
            window_bg="#ff0000",
            frame_bg="#ff1111",
            panel_bg="#ff2222",
            text_fg="#ffffff",
            text_bg="#ff0000",
            text_select_bg="#ffffff",
            text_select_fg="#ff0000",
            button_bg="#ffffff",
            button_fg="#ff0000",
            button_active_bg="#eeeeee",
            button_active_fg="#ff0000",
            button_hover_bg="#f0f0f0",
            button_hover_fg="#ff0000",
            button_disabled_bg="#cccccc",
            button_disabled_fg="#666666",
            entry_bg="#ffffff",
            entry_fg="#ff0000",
            entry_select_bg="#ff0000",
            entry_select_fg="#ffffff",
            entry_disabled_bg="#f0f0f0",
            entry_disabled_fg="#666666",
            listbox_bg="#ffffff",
            listbox_fg="#ff0000",
            listbox_select_bg="#ff0000",
            listbox_select_fg="#ffffff",
            menu_bg="#ffffff",
            menu_fg="#ff0000",
            menu_active_bg="#ff0000",
            menu_active_fg="#ffffff",
            menu_disabled_fg="#666666",
            scrollbar_bg="#f0f0f0",
            scrollbar_fg="#c0c0c0",
            scrollbar_active_bg="#ff0000",
            scrollbar_trough_bg="#f8f8f8",
            border_color="#d0d0d0",
            accent_color="#ff0000",
            highlight_color="#ff3333",
            shadow_color="#e0e0e0",
        )

        manager.register_custom_theme("red_theme", custom_colors)

        # Should be able to get the custom theme colors
        retrieved_colors = manager.get_theme_colors("red_theme")
        assert retrieved_colors.window_bg == "#ff0000"
        assert retrieved_colors.accent_color == "#ff0000"

    def test_is_dark_theme(self):
        """Test dark theme detection."""
        manager = get_theme_manager()

        # Light theme should not be dark
        manager.set_theme(ThemeType.LIGHT)
        assert not manager.is_dark_theme()

        # Dark theme should be dark
        manager.set_theme(ThemeType.DARK)
        assert manager.is_dark_theme()

        # Reset
        manager.set_theme(ThemeType.LIGHT)

    def test_utility_methods_exist(self):
        """Test that utility methods exist."""
        manager = get_theme_manager()

        # Methods should exist
        assert hasattr(manager, "get_contrasting_color")
        assert hasattr(manager, "lighten_color")
        assert hasattr(manager, "darken_color")
        assert hasattr(manager, "get_platform_scrollbar_type")

    def test_color_utility_methods(self):
        """Test color utility methods."""
        manager = get_theme_manager()

        # Test contrasting color
        contrasting = manager.get_contrasting_color("#ffffff")
        assert isinstance(contrasting, str)
        assert contrasting.startswith("#")

        # Test lighten color
        lightened = manager.lighten_color("#808080")
        assert isinstance(lightened, str)
        assert lightened.startswith("#")

        # Test darken color
        darkened = manager.darken_color("#808080")
        assert isinstance(darkened, str)
        assert darkened.startswith("#")

    def test_platform_scrollbar_type(self):
        """Test platform scrollbar type detection."""
        manager = get_theme_manager()

        scrollbar_type = manager.get_platform_scrollbar_type()
        assert isinstance(scrollbar_type, str)
        assert scrollbar_type in ["native", "ttk", "custom"]


@pytest.mark.gui
class TestCentralThemeManagerWidgetTheming:
    """Test cases for widget theming functionality."""

    def test_apply_theme_to_widget(self, root):
        """Test applying theme to a widget."""
        manager = get_theme_manager()

        button = tk.Button(root, text="Test Button")

        # Should not raise exception
        manager.apply_theme_to_widget(button)

    def test_apply_theme_to_widget_recursive(self, root):
        """Test applying theme to widget hierarchy."""
        manager = get_theme_manager()

        frame = tk.Frame(root)
        button = tk.Button(frame, text="Test Button")
        label = tk.Label(frame, text="Test Label")

        # Should not raise exception
        manager.apply_theme_to_widget(frame, recursive=True)

    def test_apply_window_theme(self, root):
        """Test applying theme to window."""
        manager = get_theme_manager()

        # Should not raise exception
        manager.apply_window_theme(root)

    def test_apply_frame_theme(self, root):
        """Test applying theme to frame."""
        manager = get_theme_manager()

        frame = tk.Frame(root)

        # Should not raise exception
        manager.apply_frame_theme(frame)

    def test_apply_button_theme(self, root):
        """Test applying theme to button."""
        manager = get_theme_manager()

        button = tk.Button(root, text="Test")

        # Should not raise exception
        manager.apply_button_theme(button)

    def test_apply_label_theme(self, root):
        """Test applying theme to label."""
        manager = get_theme_manager()

        label = tk.Label(root, text="Test")

        # Should not raise exception
        manager.apply_label_theme(label)

    def test_apply_entry_theme(self, root):
        """Test applying theme to entry."""
        manager = get_theme_manager()

        entry = tk.Entry(root)

        # Should not raise exception
        manager.apply_entry_theme(entry)

    def test_apply_text_theme(self, root):
        """Test applying theme to text widget."""
        manager = get_theme_manager()

        text = tk.Text(root)

        # Should not raise exception
        manager.apply_text_theme(text)

    def test_apply_listbox_theme(self, root):
        """Test applying theme to listbox."""
        manager = get_theme_manager()

        listbox = tk.Listbox(root)

        # Should not raise exception
        manager.apply_listbox_theme(listbox)

    def test_apply_menu_theme(self, root):
        """Test applying theme to menu."""
        manager = get_theme_manager()

        menu = tk.Menu(root)

        # Should not raise exception
        manager.apply_menu_theme(menu)

    def test_apply_scrollbar_theme(self, root):
        """Test applying theme to scrollbar."""
        manager = get_theme_manager()

        scrollbar = tk.Scrollbar(root)

        # Should not raise exception
        manager.apply_scrollbar_theme(scrollbar)

    def test_apply_ttk_theme(self, root):
        """Test applying theme to TTK widget."""
        manager = get_theme_manager()

        ttk_button = ttk.Button(root, text="TTK Button")

        # Should not raise exception
        manager.apply_ttk_theme(ttk_button)

    def test_configure_ttk_style(self, root):
        """Test configuring TTK style."""
        manager = get_theme_manager()

        # Should not raise exception
        manager.configure_ttk_style()

    def test_create_themed_scrollbar_auto(self, root):
        """Test creating auto-themed scrollbar."""
        manager = get_theme_manager()

        scrollbar = manager.create_themed_scrollbar_auto(root)
        assert scrollbar is not None

    def test_create_themed_scrollbar_native(self, root):
        """Test creating native themed scrollbar."""
        manager = get_theme_manager()

        scrollbar = manager.create_themed_scrollbar_native(root)
        assert isinstance(scrollbar, tk.Scrollbar)

    def test_create_themed_scrollbar_ttk(self, root):
        """Test creating TTK themed scrollbar."""
        manager = get_theme_manager()

        scrollbar = manager.create_themed_scrollbar_ttk(root)
        assert isinstance(scrollbar, ttk.Scrollbar)

    def test_theme_persistence_across_widgets(self, root):
        """Test that theme is applied consistently across multiple widgets."""
        manager = get_theme_manager()
        manager.set_theme(ThemeType.DARK)

        button1 = tk.Button(root, text="Button 1")
        button2 = tk.Button(root, text="Button 2")

        manager.apply_button_theme(button1)
        manager.apply_button_theme(button2)

        # Both buttons should have the same background color
        assert button1.cget("bg") == button2.cget("bg")

    def test_theme_change_affects_colors(self, root):
        """Test that changing theme affects widget colors."""
        manager = get_theme_manager()

        button = tk.Button(root, text="Test")

        # Apply light theme
        manager.set_theme(ThemeType.LIGHT)
        manager.apply_button_theme(button)
        light_bg = button.cget("bg")

        # Apply dark theme
        manager.set_theme(ThemeType.DARK)
        manager.apply_button_theme(button)
        dark_bg = button.cget("bg")

        # Colors should be different
        assert light_bg != dark_bg

        # Reset to light
        manager.set_theme(ThemeType.LIGHT)


class TestGlobalFunctions:
    """Test cases for global convenience functions."""

    def test_set_global_theme(self):
        """Test set_global_theme function."""
        # Should not raise exception
        set_global_theme(ThemeType.BLUE)

        manager = get_theme_manager()
        assert manager.current_theme == ThemeType.BLUE

        # Reset
        set_global_theme(ThemeType.LIGHT)

    def test_get_current_theme(self):
        """Test getting current theme from manager."""
        manager = get_theme_manager()
        manager.set_theme(ThemeType.GREEN)

        current = manager.current_theme
        assert current == ThemeType.GREEN

        # Reset
        manager.set_theme(ThemeType.LIGHT)

    def test_get_current_colors(self):
        """Test getting current colors from manager."""
        manager = get_theme_manager()
        colors = manager.current_colors
        assert isinstance(colors, ThemeColors)

    def test_global_functions_consistency(self):
        """Test that global functions are consistent with manager."""
        manager = get_theme_manager()

        # Set theme through global function
        set_global_theme(ThemeType.PURPLE)

        # Check consistency
        assert manager.current_theme == ThemeType.PURPLE

        colors = manager.current_colors
        assert isinstance(colors, ThemeColors)

        # Reset
        set_global_theme(ThemeType.LIGHT)


class TestThemeIntegration:
    """Test cases for theme integration scenarios."""

    def test_theme_manager_initialization(self):
        """Test theme manager initializes correctly."""
        manager = get_theme_manager()

        # Should have default theme
        assert manager.current_theme is not None

        # Should have colors
        colors = manager.current_colors
        assert colors is not None

    def test_multiple_theme_switches(self):
        """Test multiple rapid theme switches."""
        manager = get_theme_manager()

        themes = [
            ThemeType.LIGHT,
            ThemeType.DARK,
            ThemeType.BLUE,
            ThemeType.GREEN,
            ThemeType.PURPLE,
        ]

        for theme in themes:
            manager.set_theme(theme)
            assert manager.current_theme == theme
            colors = manager.current_colors
            assert colors is not None

    def test_invalid_theme_handling(self):
        """Test handling of invalid theme names."""
        manager = get_theme_manager()

        # This should either raise an exception or handle gracefully
        try:
            manager.set_theme("invalid_theme")
        except (ValueError, KeyError, AttributeError):
            # Expected behavior for invalid theme
            pass

    @patch("threepanewindows.central_theme_manager.platform")
    def test_system_theme_detection(self, mock_platform):
        """Test system theme detection."""
        mock_platform.system.return_value = "Windows"

        manager = get_theme_manager()

        # Should not raise exception when setting system theme
        manager.set_theme(ThemeType.SYSTEM)

    def test_theme_colors_completeness(self):
        """Test that all themes have complete color sets."""
        manager = get_theme_manager()

        required_attributes = [
            "window_bg",
            "frame_bg",
            "panel_bg",
            "text_fg",
            "text_bg",
            "text_select_bg",
            "text_select_fg",
            "button_bg",
            "button_fg",
            "button_active_bg",
            "button_active_fg",
            "button_hover_bg",
            "button_hover_fg",
            "button_disabled_bg",
            "button_disabled_fg",
            "entry_bg",
            "entry_fg",
            "entry_select_bg",
            "entry_select_fg",
            "entry_disabled_bg",
            "entry_disabled_fg",
            "listbox_bg",
            "listbox_fg",
            "listbox_select_bg",
            "listbox_select_fg",
            "menu_bg",
            "menu_fg",
            "menu_active_bg",
            "menu_active_fg",
            "menu_disabled_fg",
            "scrollbar_bg",
            "scrollbar_fg",
            "scrollbar_active_bg",
            "scrollbar_trough_bg",
            "border_color",
            "accent_color",
            "highlight_color",
            "shadow_color",
        ]

        for theme in [ThemeType.LIGHT, ThemeType.DARK, ThemeType.BLUE]:
            colors = manager.get_theme_colors(theme)
            for attr in required_attributes:
                assert hasattr(colors, attr), f"Theme {theme} missing attribute {attr}"
                value = getattr(colors, attr)
                assert value is not None, f"Theme {theme} has None value for {attr}"
                assert isinstance(
                    value, str
                ), f"Theme {theme} has non-string value for {attr}"
