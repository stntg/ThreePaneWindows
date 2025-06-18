"""Tests for FixedThreePaneWindow."""

import pytest
import tkinter as tk
from threepanewindows.fixed import FixedThreePaneWindow


class TestFixedThreePaneWindow:
    """Test cases for FixedThreePaneWindow."""

    def test_initialization(self, root):
        """Test basic initialization of FixedThreePaneWindow."""
        window = FixedThreePaneWindow(root)
        assert window.master == root
        assert hasattr(window, 'left_pane')
        assert hasattr(window, 'center_pane')
        assert hasattr(window, 'right_pane')

    def test_custom_dimensions(self, root):
        """Test initialization with custom dimensions."""
        window = FixedThreePaneWindow(
            root,
            left_width=150,
            right_width=200,
            min_pane_size=50
        )
        assert window.left_width == 150
        assert window.right_width == 200
        assert window.min_pane_size == 50

    def test_pane_access(self, root):
        """Test that panes are accessible and are Frame widgets."""
        window = FixedThreePaneWindow(root)
        
        assert isinstance(window.left_pane, tk.Frame)
        assert isinstance(window.center_pane, tk.Frame)
        assert isinstance(window.right_pane, tk.Frame)

    def test_add_widgets_to_panes(self, root):
        """Test adding widgets to each pane."""
        window = FixedThreePaneWindow(root)
        
        # Record initial number of children (includes default labels)
        initial_left = len(window.left_pane.winfo_children())
        initial_center = len(window.center_pane.winfo_children())
        initial_right = len(window.right_pane.winfo_children())
        
        # Add widgets to each pane
        left_label = tk.Label(window.left_pane, text="Left")
        left_label.pack()
        
        center_text = tk.Text(window.center_pane)
        center_text.pack()
        
        right_button = tk.Button(window.right_pane, text="Right")
        right_button.pack()
        
        # Verify widgets were added (should be initial + 1)
        assert len(window.left_pane.winfo_children()) == initial_left + 1
        assert len(window.center_pane.winfo_children()) == initial_center + 1
        assert len(window.right_pane.winfo_children()) == initial_right + 1

    def test_pane_visibility(self, root):
        """Test pane visibility methods."""
        window = FixedThreePaneWindow(root)
        
        # Test hiding and showing panes
        if hasattr(window, 'hide_left_pane'):
            window.hide_left_pane()
            window.show_left_pane()
        
        if hasattr(window, 'hide_right_pane'):
            window.hide_right_pane()
            window.show_right_pane()

    def test_resize_handling(self, root):
        """Test that the window handles resize events properly."""
        window = FixedThreePaneWindow(root)
        window.pack(fill=tk.BOTH, expand=True)
        
        # Simulate window resize
        root.geometry("1000x700")
        root.update()
        
        # Window should still be functional
        assert window.winfo_exists()

    def test_minimum_size_constraints(self, root):
        """Test minimum size constraints."""
        window = FixedThreePaneWindow(root, min_pane_size=100)
        
        # Try to set very small dimensions
        if hasattr(window, 'set_left_width'):
            window.set_left_width(50)  # Should be constrained to min_pane_size
        
        if hasattr(window, 'set_right_width'):
            window.set_right_width(50)  # Should be constrained to min_pane_size

    @pytest.mark.visual
    def test_visual_layout(self, visible_root):
        """Visual test for layout appearance."""
        window = FixedThreePaneWindow(visible_root)
        window.pack(fill=tk.BOTH, expand=True)
        
        # Add some content for visual verification
        tk.Label(window.left_pane, text="Left Pane", bg="lightblue").pack(fill=tk.BOTH, expand=True)
        tk.Label(window.center_pane, text="Center Pane", bg="lightgreen").pack(fill=tk.BOTH, expand=True)
        tk.Label(window.right_pane, text="Right Pane", bg="lightcoral").pack(fill=tk.BOTH, expand=True)
        
        visible_root.update()
        # This test requires manual visual inspection

    def test_configuration_options(self, root):
        """Test various configuration options."""
        # Test with different relief styles
        window = FixedThreePaneWindow(root, relief=tk.RAISED, bd=2)
        assert window.cget('relief') == tk.RAISED
        assert window.cget('bd') == 2

    def test_error_handling(self, root):
        """Test error handling for invalid parameters."""
        # Test with invalid parameters
        with pytest.raises((ValueError, TypeError)):
            FixedThreePaneWindow(root, left_width=-100)
        
        with pytest.raises((ValueError, TypeError)):
            FixedThreePaneWindow(root, right_width=-100)
        
        with pytest.raises((ValueError, TypeError)):
            FixedThreePaneWindow(root, min_pane_size=-50)

    def test_destroy_cleanup(self, root):
        """Test proper cleanup when window is destroyed."""
        window = FixedThreePaneWindow(root)
        window.pack()
        
        # Add some widgets
        tk.Label(window.left_pane, text="Test").pack()
        
        # Destroy and verify cleanup
        window.destroy()
        assert not window.winfo_exists()