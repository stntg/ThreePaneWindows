"""
Tests for EnhancedDockableThreePaneWindow functionality.
"""

import tkinter as tk
from unittest.mock import Mock, patch

import pytest

from threepanewindows.enhanced_dockable import (
    DragHandle,
    EnhancedDockableThreePaneWindow,
    PaneConfig,
    get_recommended_icon_formats,
    validate_icon_path,
)
from threepanewindows.themes import ThemeManager, ThemeType


@pytest.mark.gui
class TestIconUtilities:
    """Test cases for icon utility functions."""

    def test_get_recommended_icon_formats(self):
        """Test get_recommended_icon_formats returns appropriate formats."""
        formats = get_recommended_icon_formats()

        # Should return a list of strings
        assert isinstance(formats, list)
        assert len(formats) > 0
        assert all(isinstance(fmt, str) for fmt in formats)
        assert all(fmt.startswith(".") for fmt in formats)

        # Should include common formats
        common_formats = {".png", ".ico", ".gif", ".bmp"}
        assert any(fmt in common_formats for fmt in formats)

    @patch("threepanewindows.enhanced_dockable.platform_handler")
    def test_get_recommended_icon_formats_windows(self, mock_handler):
        """Test Windows-specific icon format recommendations."""
        mock_handler.get_recommended_icon_formats.return_value = [
            ".ico",
            ".png",
            ".bmp",
            ".gif",
        ]
        formats = get_recommended_icon_formats()

        # Windows should prefer .ico first
        assert ".ico" in formats
        assert formats[0] == ".ico"
        assert ".png" in formats

    @patch("threepanewindows.enhanced_dockable.platform_handler")
    def test_get_recommended_icon_formats_macos(self, mock_handler):
        """Test macOS-specific icon format recommendations."""
        mock_handler.get_recommended_icon_formats.return_value = [
            ".png",
            ".gif",
            ".bmp",
            ".ico",
        ]
        formats = get_recommended_icon_formats()

        # macOS should prefer .png first
        assert ".png" in formats
        assert formats[0] == ".png"

    @patch("threepanewindows.enhanced_dockable.platform_handler")
    def test_get_recommended_icon_formats_linux(self, mock_handler):
        """Test Linux-specific icon format recommendations."""
        mock_handler.get_recommended_icon_formats.return_value = [
            ".png",
            ".xbm",
            ".gif",
            ".bmp",
            ".ico",
        ]
        formats = get_recommended_icon_formats()

        # Linux should prefer .png and .xbm
        assert ".png" in formats
        assert ".xbm" in formats

    @patch("threepanewindows.enhanced_dockable.platform_handler")
    def test_validate_icon_path_empty(self, mock_handler):
        """Test validate_icon_path with empty path."""
        mock_handler.validate_icon_path.return_value = (True, "No icon specified")

        is_valid, message = validate_icon_path("")
        assert is_valid is True
        assert "No icon specified" in message

    @patch("threepanewindows.enhanced_dockable.platform_handler")
    def test_validate_icon_path_missing_file(self, mock_handler):
        """Test validate_icon_path with missing file."""
        mock_handler.validate_icon_path.return_value = (
            False,
            "Icon file not found: missing.png",
        )

        is_valid, message = validate_icon_path("missing.png")
        assert is_valid is False
        assert "not found" in message

    @patch("threepanewindows.enhanced_dockable.platform_handler")
    def test_validate_icon_path_valid_format(self, mock_handler):
        """Test validate_icon_path with valid format."""
        mock_handler.validate_icon_path.return_value = (
            True,
            "ICO format is optimal for Windows",
        )

        is_valid, message = validate_icon_path("test.ico")
        assert is_valid is True
        assert "optimal" in message

    @patch("threepanewindows.enhanced_dockable.platform_handler")
    def test_validate_icon_path_invalid_format(self, mock_handler):
        """Test validate_icon_path with invalid format."""
        mock_handler.validate_icon_path.return_value = (
            False,
            "Icon format '.xyz' not recommended for Windows. Recommended formats: .ico, .png, .bmp, .gif",
        )

        is_valid, message = validate_icon_path("test.xyz")
        assert is_valid is False
        assert "not recommended" in message


@pytest.mark.gui
class TestPaneConfig:
    """Test cases for PaneConfig dataclass."""

    def test_default_config(self):
        """Test default PaneConfig values."""
        config = PaneConfig()
        assert config.title == ""
        assert config.icon == ""
        assert config.min_width == 100
        assert config.max_width == 500
        assert config.default_width == 200
        assert config.resizable is True
        assert config.detachable is True
        assert config.closable is False
        assert config.fixed_width is None

    def test_custom_config(self):
        """Test custom PaneConfig values."""
        config = PaneConfig(
            title="Test Pane",
            icon="test.png",
            min_width=150,
            max_width=600,
            default_width=250,
            resizable=False,
            detachable=False,
            closable=True,
            fixed_width=300,
        )
        assert config.title == "Test Pane"
        assert config.icon == "test.png"
        assert config.min_width == 150
        assert config.max_width == 600
        assert config.default_width == 250
        assert config.resizable is False
        assert config.detachable is False
        assert config.closable is True
        assert config.fixed_width == 300


@pytest.mark.gui
class TestDragHandle:
    """Test cases for DragHandle widget."""

    def setup_method(self):
        """Set up test fixtures."""
        try:
            self.root = tk.Tk()
            self.root.withdraw()
            self.theme_manager = ThemeManager()
            self.on_detach_mock = Mock()
        except tk.TclError as e:
            pytest.skip(f"Cannot create Tkinter window in this environment: {e}")

    def teardown_method(self):
        """Clean up after tests."""
        if hasattr(self, "root") and self.root:
            self.root.destroy()

    def test_drag_handle_initialization(self):
        """Test DragHandle initialization."""
        handle = DragHandle(
            self.root,
            pane_side="left",
            on_detach=self.on_detach_mock,
            theme_manager=self.theme_manager,
        )

        assert handle.pane_side == "left"
        assert handle.on_detach == self.on_detach_mock
        assert handle.theme_manager == self.theme_manager
        assert handle.is_dragging is False
        assert handle.drag_start_x == 0
        assert handle.drag_start_y == 0

    def test_drag_handle_styling(self):
        """Test DragHandle applies theme styling."""
        handle = DragHandle(
            self.root,
            pane_side="right",
            on_detach=self.on_detach_mock,
            theme_manager=self.theme_manager,
        )

        # Should have applied theme styling
        assert handle.winfo_exists()


@pytest.mark.gui
class TestEnhancedDockableThreePaneWindow:
    """Test cases for EnhancedDockableThreePaneWindow."""

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

    def test_basic_initialization(self):
        """Test basic initialization of EnhancedDockableThreePaneWindow."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )

        assert window.master == self.root
        assert window.left_builder == dummy_builder
        assert window.center_builder == dummy_builder
        assert window.right_builder == dummy_builder

    def test_initialization_with_configs(self):
        """Test initialization with pane configurations."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        left_config = PaneConfig(title="Left", min_width=150)
        center_config = PaneConfig(title="Center", resizable=False)
        right_config = PaneConfig(title="Right", detachable=False)

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            left_config=left_config,
            center_config=center_config,
            right_config=right_config,
        )

        assert window.left_config == left_config
        assert window.center_config == center_config
        assert window.right_config == right_config

    def test_theme_initialization(self):
        """Test initialization with different themes."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        # Test with different theme types
        for theme_type in [ThemeType.LIGHT, ThemeType.DARK, ThemeType.BLUE]:
            window = EnhancedDockableThreePaneWindow(
                self.root,
                left_builder=dummy_builder,
                center_builder=dummy_builder,
                right_builder=dummy_builder,
                theme=theme_type,
            )
            assert window.theme_manager.current_theme == theme_type

    def test_pane_access_methods(self):
        """Test pane access methods."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )

        # Test frame access methods
        left_frame = window.get_left_frame()
        center_frame = window.get_center_frame()
        right_frame = window.get_right_frame()

        assert isinstance(left_frame, tk.Widget)
        assert isinstance(center_frame, tk.Widget)
        assert isinstance(right_frame, tk.Widget)

    def test_detach_functionality(self):
        """Test pane detaching functionality."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        left_config = PaneConfig(detachable=True)
        right_config = PaneConfig(detachable=True)

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            left_config=left_config,
            right_config=right_config,
        )
        window.pack()

        # Test detaching left pane
        if hasattr(window, "detach_left"):
            window.detach_left()
            # Should create a detached window
            assert hasattr(window, "left_detached_window")

        # Test detaching right pane
        if hasattr(window, "detach_right"):
            window.detach_right()
            # Should create a detached window
            assert hasattr(window, "right_detached_window")

    def test_reattach_functionality(self):
        """Test pane reattaching functionality."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )
        window.pack()

        # Test reattaching after detaching
        if hasattr(window, "detach_left") and hasattr(window, "reattach_left"):
            window.detach_left()
            window.reattach_left()

    def test_icon_configuration(self):
        """Test icon configuration in PaneConfig."""
        config = PaneConfig(title="Test Panel", icon="🔧", window_icon="test_icon.png")

        assert config.title == "Test Panel"
        assert config.icon == "🔧"
        assert config.window_icon == "test_icon.png"

    @patch("os.path.exists")
    def test_detached_window_icon_handling(self, mock_exists):
        """Test that detached windows handle icons properly."""
        mock_exists.return_value = False  # Simulate missing icon file

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        config = PaneConfig(
            title="Test Panel", icon="🔧", window_icon="missing_icon.png"
        )

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            left_config=config,
        )
        window.pack()

        # Should handle missing icon gracefully
        # The window should still be created successfully

    def test_fixed_width_panes(self):
        """Test fixed width pane functionality."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        left_config = PaneConfig(fixed_width=200)
        right_config = PaneConfig(fixed_width=150)

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            left_config=left_config,
            right_config=right_config,
        )

        assert window.left_config.fixed_width == 200
        assert window.right_config.fixed_width == 150

    def test_pane_visibility_methods(self):
        """Test pane visibility control methods."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )

        # Test visibility methods if they exist
        if hasattr(window, "hide_left_pane"):
            window.hide_left_pane()
        if hasattr(window, "show_left_pane"):
            window.show_left_pane()
        if hasattr(window, "hide_right_pane"):
            window.hide_right_pane()
        if hasattr(window, "show_right_pane"):
            window.show_right_pane()

    def test_resize_constraints(self):
        """Test pane resize constraints."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        left_config = PaneConfig(min_width=100, max_width=300)
        right_config = PaneConfig(min_width=80, max_width=250)

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            left_config=left_config,
            right_config=right_config,
        )

        assert window.left_config.min_width == 100
        assert window.left_config.max_width == 300
        assert window.right_config.min_width == 80
        assert window.right_config.max_width == 250

    def test_theme_switching(self):
        """Test dynamic theme switching."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            theme=ThemeType.LIGHT,
        )

        # Test switching themes
        if hasattr(window, "set_theme"):
            window.set_theme(ThemeType.DARK)
            assert window.theme_manager.current_theme == ThemeType.DARK

    def test_status_bar_integration(self):
        """Test status bar integration if available."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            show_status_bar=True,
        )

        # Check if status bar was created
        if hasattr(window, "status_bar"):
            assert window.status_bar is not None

    def test_toolbar_integration(self):
        """Test toolbar integration if available."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            show_toolbar=True,
        )

        # Check if toolbar was created
        if hasattr(window, "toolbar"):
            assert window.toolbar is not None

    @pytest.mark.visual
    def test_visual_appearance(self, visible_root):
        """Visual test for enhanced window appearance."""

        def dummy_builder(frame):
            tk.Label(frame, text="Enhanced Test", bg="lightblue").pack(
                fill=tk.BOTH, expand=True
            )

        window = EnhancedDockableThreePaneWindow(
            visible_root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            theme=ThemeType.BLUE,
        )
        window.pack(fill=tk.BOTH, expand=True)

        visible_root.update()
        # This test requires manual visual inspection

    def test_error_handling(self):
        """Test error handling for invalid parameters."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        # Test with invalid theme
        with pytest.raises((ValueError, TypeError)):
            EnhancedDockableThreePaneWindow(
                self.root,
                left_builder=dummy_builder,
                center_builder=dummy_builder,
                right_builder=dummy_builder,
                theme="invalid_theme",
            )

    def test_cleanup_on_destroy(self):
        """Test proper cleanup when window is destroyed."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )
        window.pack()

        # Destroy and verify cleanup
        window.destroy()
        assert not window.winfo_exists()

    def test_drag_handle_with_title(self):
        """Test drag handle with title configuration."""
        from threepanewindows.enhanced_dockable import DragHandle
        from threepanewindows.themes import get_theme_manager

        # Create drag handle with required parameters
        def dummy_detach():
            pass

        handle = DragHandle(
            self.root,
            pane_side="left",
            on_detach=dummy_detach,
            theme_manager=get_theme_manager(),
        )
        handle.pack()

        # Force update to trigger styling
        self.root.update_idletasks()

        # Verify handle was created
        assert handle is not None
        assert hasattr(handle, "pane_side")
        assert handle.pane_side == "left"

    def test_drag_handle_events(self):
        """Test drag handle mouse events."""
        from threepanewindows.enhanced_dockable import DragHandle
        from threepanewindows.themes import get_theme_manager

        # Create drag handle with required parameters
        def dummy_detach():
            pass

        handle = DragHandle(
            self.root,
            pane_side="right",
            on_detach=dummy_detach,
            theme_manager=get_theme_manager(),
        )
        handle.pack()

        # Test event binding
        handle._bind_events()

        # Simulate mouse events
        event = type("Event", (), {"x": 10, "y": 10, "x_root": 100, "y_root": 100})()

        # Test drag start
        handle._on_drag_start(event)

        # Test drag motion
        handle._on_drag_motion(event)

        # Test drag end
        handle._on_drag_end(event)

        # Test enter/leave events
        handle._on_enter(event)
        handle._on_leave(event)

    def test_enhanced_window_with_all_configs(self):
        """Test enhanced window with comprehensive configurations."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        left_config = PaneConfig(
            title="Left Panel",
            min_width=150,
            max_width=300,
            detachable=True,
            resizable=True,
        )

        right_config = PaneConfig(
            title="Right Panel", fixed_width=200, detachable=False, resizable=False
        )

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            left_config=left_config,
            right_config=right_config,
            show_status_bar=True,
            show_toolbar=True,
        )

        # Test all configurations are applied
        assert window.left_config == left_config
        assert window.right_config == right_config
        assert hasattr(window, "status_bar")
        assert hasattr(window, "toolbar")

    def test_window_state_management(self):
        """Test window state save/restore functionality."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )

        # Test state methods exist and are callable
        if hasattr(window, "save_state"):
            state = window.save_state()
            assert isinstance(state, dict)

        if hasattr(window, "restore_state"):
            test_state = {"left_width": 200, "right_width": 150}
            window.restore_state(test_state)

    def test_enhanced_window_advanced_features(self):
        """Test advanced features of enhanced window."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )

        # Test keyboard shortcut binding
        if hasattr(window, "_bind_keyboard_shortcuts"):
            window._bind_keyboard_shortcuts()

        # Test shortcut methods exist
        if hasattr(window, "_toggle_left_pane"):
            window._toggle_left_pane()

        if hasattr(window, "_toggle_right_pane"):
            window._toggle_right_pane()

        # Test menu creation
        if hasattr(window, "create_menu"):
            menu = window.create_menu()
            assert menu is not None

        # Test context menu
        if hasattr(window, "_create_context_menu"):
            menu = window._create_context_menu()
            assert menu is not None
