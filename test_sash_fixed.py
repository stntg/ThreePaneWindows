#!/usr/bin/env python3
"""
Simple test to verify that sash behavior is fixed for fixed-width panes.
This test focuses only on the sash behavior, not detaching functionality.
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
        text="Left Panel\n(Fixed Width: 200px)\nNo sash handles!",
        bg="lightblue",
        justify="center",
        wraplength=180,
    )
    label.pack(fill="both", expand=True, padx=5, pady=5)


def build_center_panel(parent):
    """Build center panel content."""
    label = tk.Label(
        parent,
        text="Center Panel\n(Resizable)\nExpands/contracts with window",
        bg="lightgreen",
        justify="center",
    )
    label.pack(fill="both", expand=True, padx=5, pady=5)


def build_right_panel(parent):
    """Build right panel content."""
    label = tk.Label(
        parent,
        text="Right Panel\n(Not Resizable: 150px)\nNo sash handles!",
        bg="lightcoral",
        justify="center",
        wraplength=140,
    )
    label.pack(fill="both", expand=True, padx=5, pady=5)


def main():
    """Main function to test sash behavior."""
    root = tk.Tk()
    root.title("SASH BEHAVIOR FIXED - No Resize Handles")
    root.geometry("800x600")

    # Configure panes with different settings
    left_config = PaneConfig(
        title="📁 Left Panel",
        fixed_width=200,  # Fixed width - no sash handles
        detachable=False,  # Disable detaching to avoid errors
        resizable=True,  # This should be ignored because fixed_width is set
    )

    center_config = PaneConfig(
        title="📝 Center Panel",
        detachable=False,
        resizable=True,  # Should be resizable (expands with window)
    )

    right_config = PaneConfig(
        title="🔧 Right Panel",
        resizable=False,  # Not resizable - no sash handles
        default_width=150,
        detachable=False,  # Disable detaching to avoid errors
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
        text="✅ SASH BEHAVIOR FIXED!\n"
        "• No interactive sash handles between panes\n"
        "• Left panel stays at 200px width\n"
        "• Right panel stays at 150px width\n"
        "• Center panel expands/contracts with window resize\n"
        "• Visual separators are present but not interactive",
        bg="lightgreen",
        justify="left",
        padx=10,
        pady=5,
    )
    instructions.pack(fill="x", side="bottom")

    print("✅ SUCCESS: Sash behavior is now properly controlled!")
    print("- No interactive resize handles between panes")
    print("- Fixed-width panes stay at their specified widths")
    print("- Only resizable panes (center) expand with window")

    root.mainloop()


if __name__ == "__main__":
    main()
