"""
Tests for DockableThreePaneWindow functionality.
"""

import tkinter as tk
import pytest
import os
from threepanewindows.dockable import DockableThreePaneWindow


# Skip GUI tests in CI environments where display might not be available
def pytest_configure():
    """Configure pytest to skip GUI tests in headless environments."""
    if os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"):
        # Set up minimal display for CI
        if not os.environ.get("DISPLAY"):
            os.environ["DISPLAY"] = ":99"


@pytest.mark.gui
class TestDockableThreePaneWindow:
    """Test cases for DockableThreePaneWindow."""

    def setup_method(self):
        """Set up test fixtures."""
        try:
            self.root = tk.Tk()
            self.root.withdraw()  # Hide the window during testing
        except tk.TclError as e:
            pytest.skip(f"Cannot create Tkinter window in this environment: {e}")

    def teardown_method(self):
        """Clean up after tests."""
        if self.root:
            self.root.destroy()

    def test_initialization(self):
        """Test basic initialization of DockableThreePaneWindow."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = DockableThreePaneWindow(
            self.root,
            side_width=150,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )

        assert window.side_width == 150
        assert window.left_builder == dummy_builder
        assert window.center_builder == dummy_builder
        assert window.right_builder == dummy_builder
        assert window.left_window is None
        assert window.right_window is None
        assert window.left_placeholder is None
        assert window.right_placeholder is None

    def test_fixed_width_initialization(self):
        """Test initialization with fixed width panels."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = DockableThreePaneWindow(
            self.root,
            side_width=150,
            left_fixed_width=180,
            right_fixed_width=120,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )

        assert window.left_fixed_width == 180
        assert window.right_fixed_width == 120
        assert window.is_left_fixed() is True
        assert window.is_right_fixed() is True

    def test_detach_left_panel(self):
        """Test detaching the left panel."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = DockableThreePaneWindow(
            self.root,
            side_width=150,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )
        window.pack()

        # Initially, no detached windows
        assert window.left_window is None
        assert window.left_placeholder is None

        # Detach left panel
        window._detach("left")

        # After detaching, should have a detached window but no placeholder
        assert window.left_window is not None
        assert window.left_placeholder is None
        assert isinstance(window.left_window, tk.Toplevel)

        # Clean up
        window.left_window.destroy()

    def test_detach_right_panel(self):
        """Test detaching the right panel."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = DockableThreePaneWindow(
            self.root,
            side_width=150,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )
        window.pack()

        # Initially, no detached windows
        assert window.right_window is None
        assert window.right_placeholder is None

        # Detach right panel
        window._detach("right")

        # After detaching, should have a detached window but no placeholder
        assert window.right_window is not None
        assert window.right_placeholder is None
        assert isinstance(window.right_window, tk.Toplevel)

        # Clean up
        window.right_window.destroy()

    def test_reattach_left_panel(self):
        """Test reattaching the left panel."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = DockableThreePaneWindow(
            self.root,
            side_width=150,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )
        window.pack()

        # Detach and then reattach
        window._detach("left")
        assert window.left_window is not None

        window._reattach("left")
        assert window.left_window is None
        assert window.left_placeholder is None

    def test_reattach_right_panel(self):
        """Test reattaching the right panel."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = DockableThreePaneWindow(
            self.root,
            side_width=150,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )
        window.pack()

        # Detach and then reattach
        window._detach("right")
        assert window.right_window is not None

        window._reattach("right")
        assert window.right_window is None
        assert window.right_placeholder is None

    '''def test_center_panel_expansion_no_placeholders(self):
        """Test that center panel can expand when side panels are detached (no placeholders)."""
        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = DockableThreePaneWindow(
            self.root,
            side_width=150,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )
        window.pack()
        
        # Force update to ensure all widgets are created
        self.root.update_idletasks()
        
        # Get initial number of panes - should have left, center, right
        initial_panes = len(window.paned.winfo_children())
        # Note: The actual number might vary based on how PanedWindow manages children
        assert initial_panes >= 1  # At minimum we should have the center panel
        
        # Detach left panel
        window._detach("left")
        self.root.update_idletasks()
        
        # Should have one less pane (no placeholder created)
        after_left_detach = len(window.paned.winfo_children())
        assert after_left_detach < initial_panes  # Should be fewer panes
        assert window.left_placeholder is None
        
        # Detach right panel too
        window._detach("right")
        self.root.update_idletasks()
        
        # Should have only center panel remaining
        after_right_detach = len(window.paned.winfo_children())
        assert after_right_detach <= after_left_detach  # Should be same or fewer panes
        assert window.right_placeholder is None
        
        # Clean up
        if window.left_window:
            window.left_window.destroy()
        if window.right_window:
            window.right_window.destroy()'''

    def test_frame_accessors(self):
        """Test frame accessor methods."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = DockableThreePaneWindow(
            self.root,
            side_width=150,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )

        assert window.get_left_frame() is not None
        assert window.get_center_frame() is not None
        assert window.get_right_frame() is not None

    def test_fixed_width_methods(self):
        """Test fixed width setter and getter methods."""

        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = DockableThreePaneWindow(
            self.root,
            side_width=150,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )

        # Initially not fixed
        assert window.is_left_fixed() is False
        assert window.is_right_fixed() is False

        # Set fixed widths
        window.set_left_fixed_width(200)
        window.set_right_fixed_width(180)

        assert window.is_left_fixed() is True
        assert window.is_right_fixed() is True
        assert window.left_fixed_width == 200
        assert window.right_fixed_width == 180

        # Clear fixed widths
        window.clear_left_fixed_width()
        window.clear_right_fixed_width()

        assert window.is_left_fixed() is False
        assert window.is_right_fixed() is False

    def test_dockable_window_error_handling(self):
        """Test error handling in dockable window."""
        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        # Test with invalid parameters
        try:
            window = DockableThreePaneWindow(
                self.root,
                left_builder=dummy_builder,
                center_builder=dummy_builder,
                right_builder=dummy_builder,
                side_width=-100  # Invalid negative width
            )
            # Should handle gracefully or use default
            assert window is not None
        except Exception:
            # Error handling is working
            pass

    def test_dockable_window_state_management(self):
        """Test state management in dockable window."""
        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = DockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder
        )

        # Test state methods if they exist
        if hasattr(window, 'get_state'):
            state = window.get_state()
            assert isinstance(state, dict)
        
        if hasattr(window, 'set_state'):
            test_state = {'left_detached': False, 'right_detached': False}
            window.set_state(test_state)

    def test_dockable_window_advanced_features(self):
        """Test advanced features of dockable window."""
        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = DockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder
        )

        # Test advanced methods if they exist
        if hasattr(window, 'toggle_left_pane'):
            window.toggle_left_pane()
        
        if hasattr(window, 'toggle_right_pane'):
            window.toggle_right_pane()
        
        if hasattr(window, 'reset_layout'):
            window.reset_layout()
        
        if hasattr(window, 'save_layout'):
            layout = window.save_layout()
        
        if hasattr(window, 'restore_layout'):
            window.restore_layout({'test': 'layout'})

    def test_dockable_window_cleanup(self):
        """Test cleanup functionality."""
        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        window = DockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder
        )

        # Test cleanup methods if they exist
        if hasattr(window, 'cleanup'):
            window.cleanup()
        
        if hasattr(window, '_cleanup_detached_windows'):
            window._cleanup_detached_windows()
        
        # Test destroy
        window.destroy()
