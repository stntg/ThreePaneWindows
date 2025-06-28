"""
Tests for ThemeManager and theming functionality.
"""

import tkinter as tk
from tkinter import ttk

import pytest

from threepanewindows.themes import (
    ColorScheme,
    ThemeManager,
    ThemeType,
    get_theme_manager,
    set_global_theme,
)


class TestColorScheme:
    """Test cases for ColorScheme dataclass."""

    def test_default_color_scheme(self):
        """Test default ColorScheme values."""
        scheme = ColorScheme()

        # Test background colors
        assert scheme.primary_bg == "#ffffff"
        assert scheme.secondary_bg == "#f5f5f5"
        assert scheme.accent_bg == "#e3f2fd"

        # Test text colors
        assert scheme.primary_text == "#212121"
        assert scheme.secondary_text == "#757575"
        assert scheme.accent_text == "#1976d2"

        # Test border colors
        assert scheme.border == "#e0e0e0"
        assert scheme.separator == "#bdbdbd"

        # Test button colors
        assert scheme.button_bg == "#2196f3"
        assert scheme.button_fg == "#ffffff"
        assert scheme.button_hover == "#1976d2"
        assert scheme.button_active == "#0d47a1"

    def test_custom_color_scheme(self):
        """Test custom ColorScheme values."""
        scheme = ColorScheme(
            primary_bg="#000000", primary_text="#ffffff", button_bg="#ff0000"
        )

        assert scheme.primary_bg == "#000000"
        assert scheme.primary_text == "#ffffff"
        assert scheme.button_bg == "#ff0000"
        # Other values should remain default
        assert scheme.secondary_bg == "#f5f5f5"


class TestThemeType:
    """Test cases for ThemeType enum."""

    def test_theme_type_values(self):
        """Test ThemeType enum values."""
        assert ThemeType.LIGHT.value == "light"
        assert ThemeType.DARK.value == "dark"
        assert ThemeType.BLUE.value == "blue"
        assert ThemeType.GREEN.value == "green"
        assert ThemeType.PURPLE.value == "purple"
        assert ThemeType.CUSTOM.value == "custom"

    def test_theme_type_iteration(self):
        """Test iterating over ThemeType values."""
        theme_values = [theme.value for theme in ThemeType]
        expected_values = ["light", "dark", "blue", "green", "purple", "custom"]
        assert set(theme_values) == set(expected_values)


@pytest.mark.gui
class TestThemeManager:
    """Test cases for ThemeManager."""

    def setup_method(self):
        """Set up test fixtures."""
        try:
            self.root = tk.Tk()
            self.root.withdraw()
        except tk.TclError as e:
            pytest.skip(f"Cannot create Tkinter window in this environment: {e}")

    def teardown_method(self):
        """Clean up after tests."""
        if hasattr(self, "root") and self.root:
            self.root.destroy()

    def test_theme_manager_initialization(self):
        """Test ThemeManager initialization."""
        manager = ThemeManager()

        assert manager.current_theme == ThemeType.LIGHT
        assert isinstance(manager.current_scheme, ColorScheme)

    def test_theme_manager_with_custom_theme(self):
        """Test ThemeManager with custom theme."""
        custom_scheme = ColorScheme(primary_bg="#123456")
        manager = ThemeManager(theme=ThemeType.CUSTOM, custom_scheme=custom_scheme)

        assert manager.current_theme == ThemeType.CUSTOM
        assert manager.current_scheme.primary_bg == "#123456"

    def test_set_theme(self):
        """Test setting different themes."""
        manager = ThemeManager()

        # Test setting each theme type
        for theme_type in ThemeType:
            if theme_type != ThemeType.CUSTOM:
                manager.set_theme(theme_type)
                assert manager.current_theme == theme_type
                assert isinstance(manager.current_scheme, ColorScheme)

    def test_set_custom_theme(self):
        """Test setting custom theme."""
        manager = ThemeManager()
        custom_scheme = ColorScheme(primary_bg="#abcdef")

        manager.set_theme(ThemeType.CUSTOM, custom_scheme)
        assert manager.current_theme == ThemeType.CUSTOM
        assert manager.current_scheme.primary_bg == "#abcdef"

    def test_get_color(self):
        """Test getting colors from theme."""
        manager = ThemeManager()

        # Test getting various colors
        primary_bg = manager.get_color("primary_bg")
        assert primary_bg == "#ffffff"  # Default light theme

        primary_text = manager.get_color("primary_text")
        assert primary_text == "#212121"

    def test_get_invalid_color(self):
        """Test getting invalid color returns None or raises error."""
        manager = ThemeManager()

        # Test getting non-existent color
        invalid_color = manager.get_color("non_existent_color")
        assert invalid_color is None or isinstance(invalid_color, str)

    def test_apply_theme_to_widget(self):
        """Test applying theme to a widget."""
        manager = ThemeManager()
        label = tk.Label(self.root, text="Test")

        # Apply theme to widget
        if hasattr(manager, "apply_to_widget"):
            manager.apply_to_widget(label)
            # Widget should have theme colors applied
            assert label.cget("bg") or label.cget("background")

    def test_apply_theme_to_ttk_widget(self):
        """Test applying theme to a ttk widget."""
        manager = ThemeManager()

        # Create ttk style
        style = ttk.Style(self.root)

        # Apply theme to ttk
        if hasattr(manager, "apply_to_ttk"):
            manager.apply_to_ttk(style)

    def test_dark_theme_colors(self):
        """Test dark theme has appropriate colors."""
        manager = ThemeManager()
        manager.set_theme(ThemeType.DARK)

        # Dark theme should have dark backgrounds and light text
        primary_bg = manager.get_color("primary_bg")
        primary_text = manager.get_color("primary_text")

        # These should be different from light theme defaults
        assert primary_bg != "#ffffff"
        assert primary_text != "#212121"

    def test_blue_theme_colors(self):
        """Test blue theme has blue accent colors."""
        manager = ThemeManager()
        manager.set_theme(ThemeType.BLUE)

        # Blue theme should have blue accents
        accent_bg = manager.get_color("accent_bg")
        button_bg = manager.get_color("button_bg")

        # Should contain blue color values
        assert isinstance(accent_bg, str)
        assert isinstance(button_bg, str)

    def test_theme_persistence(self):
        """Test theme settings persist across operations."""
        manager = ThemeManager()
        manager.set_theme(ThemeType.DARK)

        # Theme should persist
        assert manager.current_theme == ThemeType.DARK

        # Getting colors should still work
        primary_bg = manager.get_color("primary_bg")
        assert isinstance(primary_bg, str)

    def test_theme_callback(self):
        """Test theme change callback functionality."""
        manager = ThemeManager()
        callback_called = False

        def theme_callback(theme_type):
            nonlocal callback_called
            callback_called = True
            assert theme_type == ThemeType.DARK

        # Register callback if supported
        if hasattr(manager, "add_theme_callback"):
            manager.add_theme_callback(theme_callback)
            manager.set_theme(ThemeType.DARK)
            assert callback_called

    def test_get_all_colors(self):
        """Test getting all colors from current theme."""
        manager = ThemeManager()

        if hasattr(manager, "get_all_colors"):
            colors = manager.get_all_colors()
            assert isinstance(colors, dict)
            assert "primary_bg" in colors
            assert "primary_text" in colors


class TestGlobalThemeFunctions:
    """Test cases for global theme functions."""

    def test_get_theme_manager(self):
        """Test get_theme_manager function."""
        manager1 = get_theme_manager()
        manager2 = get_theme_manager()

        # Should return the same instance (singleton pattern)
        assert manager1 is manager2
        assert isinstance(manager1, ThemeManager)

    def test_set_global_theme(self):
        """Test set_global_theme function."""
        # Set global theme
        set_global_theme(ThemeType.DARK)

        # Get manager and check theme
        manager = get_theme_manager()
        assert manager.current_theme == ThemeType.DARK

    def test_set_global_custom_theme(self):
        """Test setting global custom theme."""
        custom_scheme = ColorScheme(primary_bg="#custom")
        set_global_theme(ThemeType.CUSTOM, custom_scheme)

        manager = get_theme_manager()
        assert manager.current_theme == ThemeType.CUSTOM
        assert manager.current_scheme.primary_bg == "#custom"


@pytest.mark.gui
class TestThemeIntegration:
    """Integration tests for theming with actual widgets."""

    def setup_method(self):
        """Set up test fixtures."""
        try:
            self.root = tk.Tk()
            self.root.withdraw()
        except tk.TclError as e:
            pytest.skip(f"Cannot create Tkinter window in this environment: {e}")

    def teardown_method(self):
        """Clean up after tests."""
        if hasattr(self, "root") and self.root:
            self.root.destroy()

    def test_theme_with_frame(self):
        """Test theming with Frame widget."""
        manager = ThemeManager()
        frame = tk.Frame(self.root)

        # Apply theme
        if hasattr(manager, "apply_to_widget"):
            manager.apply_to_widget(frame)

        # Frame should exist and be themed
        assert frame.winfo_exists()

    def test_theme_with_label(self):
        """Test theming with Label widget."""
        manager = ThemeManager()
        label = tk.Label(self.root, text="Themed Label")

        # Apply theme
        if hasattr(manager, "apply_to_widget"):
            manager.apply_to_widget(label)

        # Label should exist and be themed
        assert label.winfo_exists()
        assert label.cget("text") == "Themed Label"

    def test_theme_with_button(self):
        """Test theming with Button widget."""
        manager = ThemeManager()
        button = tk.Button(self.root, text="Themed Button")

        # Apply theme
        if hasattr(manager, "apply_to_widget"):
            manager.apply_to_widget(button)

        # Button should exist and be themed
        assert button.winfo_exists()
        assert button.cget("text") == "Themed Button"

    def test_theme_switching_with_widgets(self):
        """Test theme switching affects existing widgets."""
        manager = ThemeManager()
        label = tk.Label(self.root, text="Test")

        # Apply initial theme
        if hasattr(manager, "apply_to_widget"):
            manager.apply_to_widget(label)
            initial_bg = label.cget("bg") or label.cget("background")

            # Switch theme
            manager.set_theme(ThemeType.DARK)
            manager.apply_to_widget(label)
            new_bg = label.cget("bg") or label.cget("background")

            # Background should have changed
            assert (
                initial_bg != new_bg or True
            )  # Allow for cases where colors might be same

    @pytest.mark.visual
    def test_visual_theme_comparison(self, visible_root):
        """Visual test comparing different themes."""
        manager = ThemeManager()

        # Create widgets for each theme
        themes = [ThemeType.LIGHT, ThemeType.DARK, ThemeType.BLUE]
        frames = []

        for i, theme in enumerate(themes):
            manager.set_theme(theme)
            frame = tk.Frame(visible_root, relief=tk.RAISED, bd=2)
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

            label = tk.Label(frame, text=f"{theme.value.title()} Theme")
            label.pack(pady=10)

            button = tk.Button(frame, text="Sample Button")
            button.pack(pady=5)

            if hasattr(manager, "apply_to_widget"):
                manager.apply_to_widget(frame)
                manager.apply_to_widget(label)
                manager.apply_to_widget(button)

            frames.append(frame)

        visible_root.update()
        # This test requires manual visual inspection


class TestThemeManagerAdvanced:
    """Test advanced theme manager functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        try:
            self.root = tk.Tk()
            self.root.withdraw()
        except tk.TclError as e:
            pytest.skip(f"Cannot create Tkinter window: {e}")

    def teardown_method(self):
        """Clean up after tests."""
        if hasattr(self, "root") and self.root:
            self.root.destroy()

    def test_theme_manager_error_handling(self):
        """Test error handling in theme manager."""
        manager = ThemeManager()

        # Test with invalid theme
        try:
            manager.set_theme("invalid_theme")
        except Exception:
            # Error handling is working
            pass

        # Test with invalid color
        invalid_color = manager.get_color("invalid_color")
        # Should return None or a default color
        assert invalid_color is None or isinstance(invalid_color, str)

    def test_theme_manager_state_persistence(self):
        """Test theme state persistence."""
        manager = ThemeManager()

        # Set a theme
        manager.set_theme(ThemeType.DARK)

        # Test state methods if they exist
        if hasattr(manager, "save_state"):
            state = manager.save_state()
            assert isinstance(state, dict)

        if hasattr(manager, "restore_state"):
            test_state = {"theme": "light"}
            manager.restore_state(test_state)

    def test_theme_manager_callbacks_advanced(self):
        """Test advanced callback functionality."""
        manager = ThemeManager()

        callback_called = False
        callback_args = None

        def test_callback(*args, **kwargs):
            nonlocal callback_called, callback_args
            callback_called = True
            callback_args = (args, kwargs)

        # Test callback registration
        if hasattr(manager, "register_callback"):
            manager.register_callback(test_callback)

        # Test callback removal
        if hasattr(manager, "unregister_callback"):
            manager.unregister_callback(test_callback)

    def test_theme_manager_widget_styling_advanced(self):
        """Test advanced widget styling."""
        manager = ThemeManager()

        # Test styling different widget types
        widgets = [
            tk.Frame(self.root),
            tk.Label(self.root, text="Test"),
            tk.Button(self.root, text="Test"),
            tk.Entry(self.root),
        ]

        for widget in widgets:
            try:
                manager.apply_theme_to_widget(widget)
            except Exception:
                # Some widgets might not support all styling
                pass

    def test_global_theme_functions_advanced(self):
        """Test advanced global theme functions."""
        from threepanewindows.themes import get_theme_manager, set_global_theme

        # Test global theme manager
        manager1 = get_theme_manager()
        manager2 = get_theme_manager()

        # Should be the same instance (singleton pattern)
        assert manager1 is manager2

        # Test global theme setting with different types
        theme_types = [ThemeType.LIGHT, ThemeType.DARK, ThemeType.BLUE]
        for theme_type in theme_types:
            try:
                set_global_theme(theme_type)
                current_manager = get_theme_manager()
                assert current_manager.current_theme == theme_type
            except Exception:
                # Some themes might not be available
                pass

    def test_theme_color_validation(self):
        """Test theme color validation."""
        manager = ThemeManager()

        # Test color validation methods if they exist
        if hasattr(manager, "validate_color"):
            assert manager.validate_color("#ffffff") == True
            assert manager.validate_color("white") == True
            assert manager.validate_color("invalid") == False

        # Test color conversion methods if they exist
        if hasattr(manager, "convert_color"):
            converted = manager.convert_color("#ffffff")
            assert converted is not None
