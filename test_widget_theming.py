#!/usr/bin/env python3
"""
Test script to verify that widget theming is working correctly.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

# Add the package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from threepanewindows.themes import ThemeManager, ThemeType


def create_test_widgets(parent):
    """Create a variety of widgets to test theming."""

    # TTK Widgets
    ttk_frame = ttk.LabelFrame(parent, text="TTK Widgets")
    ttk_frame.pack(fill="x", padx=10, pady=5)

    # Labels
    ttk.Label(ttk_frame, text="TTK Label").pack(anchor="w", padx=5, pady=2)

    # Buttons
    button_frame = ttk.Frame(ttk_frame)
    button_frame.pack(fill="x", padx=5, pady=2)

    ttk.Button(button_frame, text="TTK Button 1").pack(side="left", padx=2)
    ttk.Button(button_frame, text="TTK Button 2").pack(side="left", padx=2)

    # Entry and Combobox
    entry_frame = ttk.Frame(ttk_frame)
    entry_frame.pack(fill="x", padx=5, pady=2)

    ttk.Label(entry_frame, text="Entry:").pack(side="left")
    entry = ttk.Entry(entry_frame, width=20)
    entry.insert(0, "Sample text")
    entry.pack(side="left", padx=5)

    ttk.Label(entry_frame, text="Combobox:").pack(side="left", padx=(10, 0))
    combo = ttk.Combobox(
        entry_frame, values=["Option 1", "Option 2", "Option 3"], width=15
    )
    combo.set("Option 1")
    combo.pack(side="left", padx=5)

    # Checkbuttons and Radiobuttons
    check_frame = ttk.Frame(ttk_frame)
    check_frame.pack(fill="x", padx=5, pady=2)

    ttk.Checkbutton(check_frame, text="TTK Checkbox").pack(side="left")

    radio_var = tk.StringVar(value="1")
    ttk.Radiobutton(
        check_frame, text="TTK Radio 1", variable=radio_var, value="1"
    ).pack(side="left", padx=10)
    ttk.Radiobutton(
        check_frame, text="TTK Radio 2", variable=radio_var, value="2"
    ).pack(side="left", padx=5)

    # Progress bar
    progress_frame = ttk.Frame(ttk_frame)
    progress_frame.pack(fill="x", padx=5, pady=2)

    ttk.Label(progress_frame, text="Progress:").pack(side="left")
    progress = ttk.Progressbar(progress_frame, length=200, value=60)
    progress.pack(side="left", padx=5)

    # TK Widgets
    tk_frame = ttk.LabelFrame(parent, text="TK Widgets")
    tk_frame.pack(fill="x", padx=10, pady=5)

    # Text widget
    text_frame = ttk.Frame(tk_frame)
    text_frame.pack(fill="x", padx=5, pady=2)

    ttk.Label(text_frame, text="Text Widget:").pack(anchor="w")
    text_widget = tk.Text(text_frame, height=3, width=50)
    text_widget.insert(
        "1.0",
        "This is a TK Text widget.\nIt should be themed with the current theme colors.",
    )
    text_widget.pack(fill="x", pady=2)

    # Listbox
    list_frame = ttk.Frame(tk_frame)
    list_frame.pack(fill="x", padx=5, pady=2)

    ttk.Label(list_frame, text="Listbox:").pack(anchor="w")
    listbox = tk.Listbox(list_frame, height=4)
    for i in range(5):
        listbox.insert("end", f"TK List Item {i+1}")
    listbox.pack(fill="x", pady=2)

    # TK Labels and Buttons
    tk_controls_frame = ttk.Frame(tk_frame)
    tk_controls_frame.pack(fill="x", padx=5, pady=2)

    tk_label = tk.Label(tk_controls_frame, text="TK Label")
    tk_label.pack(side="left", padx=5)

    tk_button = tk.Button(tk_controls_frame, text="TK Button")
    tk_button.pack(side="left", padx=5)

    tk_entry = tk.Entry(tk_controls_frame, width=20)
    tk_entry.insert(0, "TK Entry")
    tk_entry.pack(side="left", padx=5)

    return {
        "text_widget": text_widget,
        "listbox": listbox,
        "tk_label": tk_label,
        "tk_button": tk_button,
        "tk_entry": tk_entry,
    }


def main():
    """Main test function."""
    root = tk.Tk()
    root.title("Widget Theming Test")
    root.geometry("800x600")

    # Create theme manager
    theme_manager = ThemeManager()

    # Title
    title_label = ttk.Label(
        root, text="Widget Theming Test", font=("default", 16, "bold")
    )
    title_label.pack(pady=10)

    # Theme selection
    theme_frame = ttk.LabelFrame(root, text="Theme Selection")
    theme_frame.pack(fill="x", padx=10, pady=5)

    theme_var = tk.StringVar(value="light")

    def apply_theme():
        theme_name = theme_var.get()
        print(f"Applying theme: {theme_name}")

        try:
            # Set the theme
            success = theme_manager.set_theme(theme_name, window=root)
            if success:
                # Apply theme to entire window
                theme_manager.apply_theme_to_window(root)
                print(f"✓ Successfully applied theme: {theme_name}")
            else:
                print(f"✗ Failed to set theme: {theme_name}")
        except Exception as e:
            print(f"✗ Error applying theme: {e}")

    # Theme buttons
    button_frame = ttk.Frame(theme_frame)
    button_frame.pack(fill="x", padx=10, pady=5)

    themes = [
        "light",
        "dark",
        "blue",
        "green",
        "purple",
        "system",
        "native",
        "native_light",
        "native_dark",
    ]
    available_themes = theme_manager.get_available_themes()

    for i, theme_name in enumerate(themes):
        if theme_name in available_themes:
            btn = ttk.Radiobutton(
                button_frame,
                text=theme_name.replace("_", " ").title(),
                variable=theme_var,
                value=theme_name,
                command=apply_theme,
            )
            btn.grid(row=i // 3, column=i % 3, sticky="w", padx=5, pady=2)

    # Create test widgets
    test_widgets = create_test_widgets(root)

    # Status
    status_var = tk.StringVar(value="Ready - Select a theme to test")
    status_label = ttk.Label(root, textvariable=status_var)
    status_label.pack(pady=5)

    # Apply initial theme
    apply_theme()

    print("Widget Theming Test")
    print("=" * 30)
    print("This test verifies that both TTK and TK widgets are properly themed.")
    print("Try switching between different themes to see the changes.")
    print("TTK widgets should change immediately, TK widgets should also update.")
    print("")

    root.mainloop()


if __name__ == "__main__":
    main()
