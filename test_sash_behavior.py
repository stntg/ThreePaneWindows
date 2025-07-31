#!/usr/bin/env python3
"""
Test script to verify that sash behavior is properly controlled for fixed-width
and non-resizable panes in EnhancedDockableThreePaneWindow.
"""

import tkinter as tk

from threepanewindows.enhanced_dockable import (
    EnhancedDockableThreePaneWindow,
    PaneConfig,
)


def build_left_panel(parent):
    """Build left panel content."""
    label = tk.Label(
        parent,
        text="Left Panel\n(Fixed Width: 200px)\nSash should NOT resize this",
        bg="lightblue",
        justify="center",
        wraplength=180,
    )
    label.pack(fill="both", expand=True, padx=5, pady=5)


def build_center_panel(parent):
    """Build center panel content."""
    label = tk.Label(
        parent,
        text="Center Panel\n(Resizable)\nSashes should resize this panel",
        bg="lightgreen",
        justify="center",
    )
    label.pack(fill="both", expand=True, padx=5, pady=5)


def build_right_panel(parent):
    """Build right panel content."""
    label = tk.Label(
        parent,
        text="Right Panel\n(Not Resizable: 150px)\nSash should NOT resize this",
        bg="lightcoral",
        justify="center",
        wraplength=140,
    )
    label.pack(fill="both", expand=True, padx=5, pady=5)


def main():
    """Main function to test sash behavior."""
    root = tk.Tk()
    root.title("Test Sash Behavior for Fixed Panes")
    root.geometry("800x600")

    # Configure panes with different settings
    left_config = PaneConfig(
        title="📁 Left Panel",
        fixed_width=200,  # Fixed width - sash should not resize this
        detachable=True,
        resizable=True,  # This should be ignored because fixed_width is set
    )

    center_config = PaneConfig(
        title="📝 Center Panel",
        detachable=False,
        resizable=True,  # Should be resizable via sashes
    )

    right_config = PaneConfig(
        title="🔧 Right Panel",
        resizable=False,  # Not resizable - sash should not resize this
        default_width=150,
        detachable=True,
    )

    # Create the window
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=build_left_panel,
        center_builder=build_center_panel,
        right_builder=build_right_panel,
        theme_name="light",
    )
    window.pack(fill="both", expand=True)

    # Add instructions
    instructions = tk.Label(
        root,
        text="SASH BEHAVIOR TEST:\n"
        "• Try dragging the LEFT sash (between left and center) - should NOT move\n"
        "• Try dragging the RIGHT sash (between center and right) - should NOT move\n"
        "• Only the CENTER panel should expand/contract when window is resized\n"
        "• Left panel should stay at 200px, right panel should stay at 150px\n"
        "• Drag handles in headers should still work for detaching",
        bg="lightyellow",
        justify="left",
        padx=10,
        pady=5,
    )
    instructions.pack(fill="x", side="bottom")

    print("Sash behavior test window created.")
    print("Expected behavior:")
    print("1. Left sash should be locked (left panel fixed at 200px)")
    print("2. Right sash should be locked (right panel fixed at 150px)")
    print("3. Only center panel should resize when window is resized")
    print("4. Dragging sashes should have no effect on fixed panes")

    root.mainloop()


if __name__ == "__main__":
    main()
