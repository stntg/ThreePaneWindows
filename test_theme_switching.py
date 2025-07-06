#!/usr/bin/env python3
"""
Test theme switching functionality.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

# Add the threepanewindows package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "."))

from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig


def create_test_content(parent):
    """Create test content with various widgets."""
    frame = ttk.Frame(parent, style="Themed.TFrame")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Add various widgets to test theming
    ttk.Label(frame, text="Test Label", style="Themed.TLabel").pack(pady=5)

    entry = ttk.Entry(frame)
    entry.pack(pady=5, fill="x")
    entry.insert(0, "Test Entry")

    button = ttk.Button(frame, text="Test Button")
    button.pack(pady=5)

    # Text widget with scrollbar
    text_frame = tk.Frame(frame)
    text_frame.pack(fill="both", expand=True, pady=5)

    text = tk.Text(text_frame, height=5)
    text.pack(side="left", fill="both", expand=True)
    text.insert("1.0", "Test text content\nLine 2\nLine 3")

    scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text.yview)
    scrollbar.pack(side="right", fill="y")
    text.configure(yscrollcommand=scrollbar.set)

    return frame


def main():
    """Test theme switching."""
    print("Testing Theme Switching")
    print("=" * 30)

    root = tk.Tk()
    root.title("Theme Switching Test")
    root.geometry("800x600")

    # Create simple configs
    left_config = PaneConfig(title="Left Test", detachable=True)
    center_config = PaneConfig(title="Center Test", detachable=False)
    right_config = PaneConfig(title="Right Test", detachable=True)

    # Create window
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=create_test_content,
        center_builder=create_test_content,
        right_builder=create_test_content,
        theme_name="light",
    )
    window.pack(fill="both", expand=True)

    # Add theme switching controls
    control_frame = tk.Frame(root, bg="lightgray")
    control_frame.pack(fill="x", padx=5, pady=5)

    tk.Label(control_frame, text="Theme:", bg="lightgray").pack(side="left", padx=5)

    themes = ["light", "dark", "blue", "green", "purple"]
    current_theme = tk.StringVar(value="light")

    def change_theme():
        theme_name = current_theme.get()
        print(f"Switching to theme: {theme_name}")

        # Get current theme colors before switch
        old_theme = window.theme_manager.get_current_theme()
        print(
            f"  Old theme colors - bg: {old_theme.colors.primary_bg}, text: {old_theme.colors.primary_text}"
        )

        # Switch theme
        success = window.switch_theme(theme_name, update_status=False)
        print(f"  Switch result: {success}")

        # Get new theme colors after switch
        new_theme = window.theme_manager.get_current_theme()
        print(
            f"  New theme colors - bg: {new_theme.colors.primary_bg}, text: {new_theme.colors.primary_text}"
        )

        # Force update
        window.update_idletasks()
        root.update_idletasks()

        print(f"  Theme switch to {theme_name} completed\n")

    for theme in themes:
        tk.Radiobutton(
            control_frame,
            text=theme.title(),
            variable=current_theme,
            value=theme,
            command=change_theme,
            bg="lightgray",
        ).pack(side="left", padx=2)

    print("Window created. Try switching themes using the radio buttons.")
    print("Watch the console for theme change details.")

    root.mainloop()


if __name__ == "__main__":
    main()
