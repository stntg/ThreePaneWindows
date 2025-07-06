#!/usr/bin/env python3
"""
Debug demo to test the EnhancedDockableThreePaneWindow.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

# Add the threepanewindows package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "."))

from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig


def create_left_content(parent):
    """Create simple content for the left pane."""
    print("Creating left content...")
    label = tk.Label(parent, text="Left Pane Content", bg="lightblue")
    label.pack(fill="both", expand=True, padx=10, pady=10)
    return label


def create_center_content(parent):
    """Create simple content for the center pane."""
    print("Creating center content...")
    label = tk.Label(parent, text="Center Pane Content", bg="lightgreen")
    label.pack(fill="both", expand=True, padx=10, pady=10)
    return label


def create_right_content(parent):
    """Create simple content for the right pane."""
    print("Creating right content...")
    label = tk.Label(parent, text="Right Pane Content", bg="lightcoral")
    label.pack(fill="both", expand=True, padx=10, pady=10)
    return label


def main():
    """Run the debug demo."""
    print("Debug Demo - EnhancedDockableThreePaneWindow")
    print("=" * 50)

    # Create main window
    root = tk.Tk()
    root.title("Debug Demo")
    root.geometry("800x600")

    # Simple pane configs
    left_config = PaneConfig(title="Left", detachable=True)
    center_config = PaneConfig(title="Center", detachable=False)
    right_config = PaneConfig(title="Right", detachable=True)

    print("Creating EnhancedDockableThreePaneWindow...")

    # Create the three-pane window
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=create_left_content,
        center_builder=create_center_content,
        right_builder=create_right_content,
        theme_name="light",
    )
    window.pack(fill="both", expand=True)

    print("Window created, starting mainloop...")

    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()
