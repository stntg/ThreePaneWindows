#!/usr/bin/env python3
"""
Comprehensive test to verify:
1. Fixed panes use custom layout (no sash handles)
2. All resizable panes use TTK PanedWindow (with sash handles)
3. Detaching/reattaching works correctly
4. Center pane expands when other panes are detached
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
        text="Left Panel\n(Fixed Width: 200px)",
        bg="lightblue",
        justify="center",
        wraplength=180,
    )
    label.pack(fill="both", expand=True, padx=5, pady=5)


def build_center_panel(parent):
    """Build center panel content."""
    label = tk.Label(
        parent,
        text="Center Panel\n(Resizable)\nShould expand when others detach",
        bg="lightgreen",
        justify="center",
    )
    label.pack(fill="both", expand=True, padx=5, pady=5)


def build_right_panel(parent):
    """Build right panel content."""
    label = tk.Label(
        parent,
        text="Right Panel\n(Not Resizable: 150px)",
        bg="lightcoral",
        justify="center",
        wraplength=140,
    )
    label.pack(fill="both", expand=True, padx=5, pady=5)


def test_fixed_panes():
    """Test window with fixed panes (should use custom layout)."""
    root = tk.Tk()
    root.title("Test 1: Fixed Panes (Custom Layout)")
    root.geometry("800x600")

    left_config = PaneConfig(
        title="📁 Left Panel",
        fixed_width=200,  # Fixed width
        detachable=True,
        resizable=True,  # Ignored because fixed_width is set
    )

    center_config = PaneConfig(
        title="📝 Center Panel",
        detachable=True,
        resizable=True,  # Should expand to fill space
    )

    right_config = PaneConfig(
        title="🔧 Right Panel",
        resizable=False,  # Not resizable
        default_width=150,
        detachable=True,
    )

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

    instructions = tk.Label(
        root,
        text="FIXED PANES TEST:\n"
        "• No sash handles (custom layout)\n"
        "• Try detaching panes - center should expand\n"
        "• Try reattaching - should restore original layout",
        bg="lightyellow",
        justify="left",
        padx=10,
        pady=5,
    )
    instructions.pack(fill="x", side="bottom")

    print("Test 1: Fixed panes window created (should use custom layout)")
    root.mainloop()


def test_resizable_panes():
    """Test window with all resizable panes (should use TTK PanedWindow)."""
    root = tk.Tk()
    root.title("Test 2: All Resizable Panes (TTK PanedWindow)")
    root.geometry("800x600")

    left_config = PaneConfig(
        title="📁 Left Panel",
        resizable=True,  # Resizable
        default_width=200,
        detachable=True,
    )

    center_config = PaneConfig(
        title="📝 Center Panel",
        detachable=True,
        resizable=True,  # Resizable
    )

    right_config = PaneConfig(
        title="🔧 Right Panel",
        resizable=True,  # Resizable
        default_width=150,
        detachable=True,
    )

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

    instructions = tk.Label(
        root,
        text="ALL RESIZABLE TEST:\n"
        "• Should have sash handles (TTK PanedWindow)\n"
        "• All panes should be resizable via sashes\n"
        "• Detaching/reattaching should work normally",
        bg="lightcyan",
        justify="left",
        padx=10,
        pady=5,
    )
    instructions.pack(fill="x", side="bottom")

    print("Test 2: All resizable panes window created (should use TTK PanedWindow)")
    root.mainloop()


def main():
    """Main function to choose which test to run."""
    print("Choose test:")
    print("1. Fixed panes (custom layout)")
    print("2. All resizable panes (TTK PanedWindow)")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        test_fixed_panes()
    elif choice == "2":
        test_resizable_panes()
    else:
        print("Invalid choice. Running fixed panes test by default.")
        test_fixed_panes()


if __name__ == "__main__":
    main()
