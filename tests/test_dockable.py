"""
Tests for DockableThreePaneWindow functionality.
"""

import tkinter as tk
import pytest
from threepanewindows.dockable import DockableThreePaneWindow


class TestDockableThreePaneWindow:
    """Test cases for DockableThreePaneWindow."""

    def setup_method(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during testing

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

    def test_center_panel_expansion_no_placeholders(self):
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
        
        # Get initial number of panes
        initial_panes = len(window.paned.winfo_children())
        assert initial_panes == 3  # left, center, right
        
        # Detach left panel
        window._detach("left")
        
        # Should have one less pane (no placeholder created)
        after_left_detach = len(window.paned.winfo_children())
        assert after_left_detach == 2  # center, right
        assert window.left_placeholder is None
        
        # Detach right panel too
        window._detach("right")
        
        # Should have only center panel
        after_right_detach = len(window.paned.winfo_children())
        assert after_right_detach == 1  # only center
        assert window.right_placeholder is None
        
        # Clean up
        if window.left_window:
            window.left_window.destroy()
        if window.right_window:
            window.right_window.destroy()

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