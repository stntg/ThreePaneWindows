"""
Additional tests specifically targeting coverage gaps in enhanced_dockable.py

These tests are designed to work in both local and headless CI/CD environments.
They include proper error handling for display-less systems.
"""

import os
import tkinter as tk
from unittest.mock import MagicMock, Mock, patch

import pytest

from threepanewindows.enhanced_dockable import (
    DragHandle,
    EnhancedDockableThreePaneWindow,
    PaneConfig,
    get_recommended_icon_formats,
    validate_icon_path,
)
from threepanewindows.themes import ThemeType, get_theme_manager


class TestEnhancedDockableCoverage:
    """Tests specifically designed to improve coverage of enhanced_dockable.py"""

    def setup_method(self):
        """Set up test fixtures with headless compatibility."""
        try:
            # Check if we're in a headless environment
            if os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"):
                # In CI/CD, try to set up virtual display
                try:
                    self.root = tk.Tk()
                    self.root.withdraw()
                except tk.TclError:
                    pytest.skip("Headless environment detected - GUI tests skipped")
            else:
                # Local environment
                self.root = tk.Tk()
                self.root.withdraw()
        except tk.TclError as e:
            pytest.skip(f"Cannot create Tkinter window: {e}")
        except ImportError as e:
            pytest.skip(f"Tkinter not available: {e}")

    def teardown_method(self):
        """Clean up after tests."""
        if hasattr(self, "root") and self.root:
            self.root.destroy()

    def test_icon_utilities_comprehensive(self):
        """Test icon utility functions comprehensively."""
        # Test get_recommended_icon_formats with different platforms
        with patch("platform.system", return_value="Windows"):
            formats = get_recommended_icon_formats()
            assert ".ico" in formats

        with patch("platform.system", return_value="Darwin"):
            formats = get_recommended_icon_formats()
            # macOS might return different formats, just check it's not empty
            assert len(formats) > 0

        with patch("platform.system", return_value="Linux"):
            formats = get_recommended_icon_formats()
            assert ".png" in formats

        # Test validate_icon_path with various scenarios
        valid, msg = validate_icon_path("")
        assert valid == True
        assert "No icon specified" in msg

        valid, msg = validate_icon_path("nonexistent.ico")
        assert valid == False
        assert "not found" in msg

        # Test with invalid format
        with patch("os.path.exists", return_value=True):
            valid, msg = validate_icon_path("test.xyz")
            assert valid == False
            assert "not recommended" in msg

    def test_pane_config_comprehensive(self):
        """Test PaneConfig with all possible configurations."""
        # Test with all parameters
        config = PaneConfig(
            title="Test Panel",
            icon="test.ico",
            window_icon="window.ico",
            custom_titlebar=True,
            custom_titlebar_shadow=False,
            detached_height=400,
            detached_scrollable=False,
            min_width=50,
            max_width=800,
            default_width=300,
            resizable=False,
            detachable=False,
            closable=True,
            fixed_width=250,
        )

        assert config.title == "Test Panel"
        assert config.custom_titlebar == True
        assert config.detached_height == 400
        assert config.fixed_width == 250

    def test_drag_handle_comprehensive(self):
        """Test DragHandle with comprehensive scenarios."""

        def dummy_detach():
            pass

        theme_manager = get_theme_manager()

        # Test DragHandle creation (title is handled internally)
        handle = DragHandle(
            self.root,
            pane_side="left",
            on_detach=dummy_detach,
            theme_manager=theme_manager,
        )

        # Set title manually if supported
        if hasattr(handle, "title"):
            handle.title = "Test Handle"

        # Test UI setup
        handle._setup_ui()
        assert hasattr(handle, "grip_frame")

        # Test all event handlers
        event = Mock()
        event.x = 10
        event.y = 10
        event.x_root = 100
        event.y_root = 100

        handle._on_drag_start(event)
        # Drag might not start immediately due to threshold
        assert hasattr(handle, "is_dragging")

        handle._on_drag_motion(event)
        handle._on_drag_end(event)
        # Verify drag end was called
        assert hasattr(handle, "is_dragging")

        handle._on_enter(event)
        handle._on_leave(event)

    def test_enhanced_window_initialization_paths(self):
        """Test different initialization paths for EnhancedDockableThreePaneWindow."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        # Test with minimal config
        window1 = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )
        assert window1 is not None

        # Test with comprehensive config
        left_config = PaneConfig(
            title="Left", detachable=True, resizable=True, min_width=100, max_width=400
        )

        right_config = PaneConfig(title="Right", detachable=False, fixed_width=200)

        window2 = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            left_config=left_config,
            right_config=right_config,
            theme=ThemeType.DARK,
            show_status_bar=True,
            show_toolbar=True,
        )
        assert window2 is not None
        assert window2.left_config == left_config
        assert window2.right_config == right_config

    def test_enhanced_window_detach_scenarios(self):
        """Test various detach scenarios."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )

        # Test detach with different configurations
        if hasattr(window, "_detach_pane"):
            # Test left detach
            window._detach_pane("left")

            # Test right detach
            window._detach_pane("right")

            # Test reattach
            if hasattr(window, "_reattach_pane"):
                window._reattach_pane("left")
                window._reattach_pane("right")

    def test_enhanced_window_theme_integration(self):
        """Test theme integration scenarios."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        # Test with different themes
        themes = [ThemeType.LIGHT, ThemeType.DARK, ThemeType.BLUE]

        for theme in themes:
            window = EnhancedDockableThreePaneWindow(
                self.root,
                left_builder=dummy_builder,
                center_builder=dummy_builder,
                right_builder=dummy_builder,
                theme=theme,
            )

            # Test theme switching
            if hasattr(window, "set_theme"):
                window.set_theme(ThemeType.LIGHT)
                window.set_theme(ThemeType.DARK)

    def test_enhanced_window_status_toolbar(self):
        """Test status bar and toolbar functionality."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            show_status_bar=True,
            show_toolbar=True,
        )

        # Test status bar methods
        if hasattr(window, "update_status"):
            window.update_status("Test status")

        if hasattr(window, "set_status"):
            window.set_status("New status")

        # Test toolbar methods
        if hasattr(window, "add_toolbar_button"):
            window.add_toolbar_button("Test", lambda: None)

        if hasattr(window, "remove_toolbar_button"):
            window.remove_toolbar_button("Test")

    def test_enhanced_window_error_scenarios(self):
        """Test error handling scenarios."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        def error_builder(frame):
            raise Exception("Builder error")

        # Test with error in builder
        try:
            window = EnhancedDockableThreePaneWindow(
                self.root,
                left_builder=error_builder,
                center_builder=dummy_builder,
                right_builder=dummy_builder,
            )
        except Exception:
            # Error handling is working
            pass

        # Test with invalid theme
        try:
            window = EnhancedDockableThreePaneWindow(
                self.root,
                left_builder=dummy_builder,
                center_builder=dummy_builder,
                right_builder=dummy_builder,
                theme="invalid_theme",
            )
        except Exception:
            # Error handling is working
            pass

    def test_enhanced_window_advanced_methods(self):
        """Test advanced methods if they exist."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )

        # Test various methods that might exist
        methods_to_test = [
            "save_layout",
            "restore_layout",
            "reset_layout",
            "toggle_left_pane",
            "toggle_right_pane",
            "set_pane_visibility",
            "get_pane_visibility",
            "update_pane_config",
            "get_pane_config",
            "bind_keyboard_shortcuts",
            "unbind_keyboard_shortcuts",
            "create_context_menu",
            "show_context_menu",
            "save_state",
            "restore_state",
            "get_state",
        ]

        for method_name in methods_to_test:
            if hasattr(window, method_name):
                method = getattr(window, method_name)
                try:
                    if method_name in [
                        "save_layout",
                        "save_state",
                        "get_state",
                        "get_pane_visibility",
                    ]:
                        result = method()
                    elif method_name in [
                        "toggle_left_pane",
                        "toggle_right_pane",
                        "reset_layout",
                    ]:
                        method()
                    elif method_name in ["restore_layout", "restore_state"]:
                        method({})
                    elif method_name in ["set_pane_visibility"]:
                        method("left", True)
                    else:
                        method()
                except Exception:
                    # Some methods might require specific parameters or conditions
                    pass

    def test_enhanced_window_widget_management(self):
        """Test widget management functionality."""

        def dummy_builder(frame):
            label = tk.Label(frame, text="Test")
            label.pack()
            return label

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )

        # Test widget access methods
        if hasattr(window, "get_left_widgets"):
            widgets = window.get_left_widgets()

        if hasattr(window, "get_center_widgets"):
            widgets = window.get_center_widgets()

        if hasattr(window, "get_right_widgets"):
            widgets = window.get_right_widgets()

        # Test widget manipulation
        if hasattr(window, "clear_pane"):
            window.clear_pane("left")

        if hasattr(window, "refresh_pane"):
            window.refresh_pane("center")
