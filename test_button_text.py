#!/usr/bin/env python3
"""
Test script specifically for button text theming issues.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

# Add the package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from threepanewindows.themes import ThemeManager, ThemeType


def main():
    """Test button text theming."""
    root = tk.Tk()
    root.title("Button Text Theming Test")
    root.geometry("600x400")

    # Create theme manager
    theme_manager = ThemeManager()

    # Title
    title_label = ttk.Label(
        root, text="Button Text Theming Test", font=("default", 16, "bold")
    )
    title_label.pack(pady=10)

    # Theme selection
    theme_frame = ttk.LabelFrame(root, text="Theme Selection")
    theme_frame.pack(fill="x", padx=10, pady=5)

    theme_var = tk.StringVar(value="light")

    def apply_theme():
        theme_name = theme_var.get()
        print(f"\nApplying theme: {theme_name}")

        try:
            # Get theme info before applying
            theme = theme_manager.get_theme(theme_name)
            if theme:
                print(
                    f"Button colors - bg: {theme.colors.button_bg}, fg: {theme.colors.button_fg}"
                )
                print(
                    f"Button hover: {theme.colors.button_hover}, active: {theme.colors.button_active}"
                )

            # Set the theme
            success = theme_manager.set_theme(theme_name, window=root)
            if success:
                print(f"✓ Successfully applied theme: {theme_name}")

                # Check TTK style after applying
                style = ttk.Style()
                button_config = style.configure("TButton")
                button_map = style.map("TButton")
                print(f"TTK Button config: {button_config}")
                print(f"TTK Button map: {button_map}")

            else:
                print(f"✗ Failed to set theme: {theme_name}")
        except Exception as e:
            print(f"✗ Error applying theme: {e}")
            import traceback

            traceback.print_exc()

    # Theme buttons
    button_frame = ttk.Frame(theme_frame)
    button_frame.pack(fill="x", padx=10, pady=5)

    themes = [
        "light",
        "dark",
        "blue",
        "green",
        "purple",
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
            btn.grid(row=i // 4, column=i % 4, sticky="w", padx=5, pady=2)

    # Test buttons section
    test_frame = ttk.LabelFrame(root, text="Test Buttons")
    test_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # TTK Buttons
    ttk_frame = ttk.LabelFrame(test_frame, text="TTK Buttons")
    ttk_frame.pack(fill="x", padx=5, pady=5)

    ttk_container = ttk.Frame(ttk_frame)
    ttk_container.pack(fill="x", padx=5, pady=5)

    ttk.Button(ttk_container, text="Normal TTK Button").pack(side="left", padx=5)
    ttk.Button(ttk_container, text="Another TTK Button").pack(side="left", padx=5)
    ttk.Button(ttk_container, text="Disabled TTK Button", state="disabled").pack(
        side="left", padx=5
    )

    # TK Buttons
    tk_frame = ttk.LabelFrame(test_frame, text="TK Buttons")
    tk_frame.pack(fill="x", padx=5, pady=5)

    tk_container = ttk.Frame(tk_frame)
    tk_container.pack(fill="x", padx=5, pady=5)

    tk.Button(tk_container, text="Normal TK Button").pack(side="left", padx=5)
    tk.Button(tk_container, text="Another TK Button").pack(side="left", padx=5)
    tk.Button(tk_container, text="Disabled TK Button", state="disabled").pack(
        side="left", padx=5
    )

    # Color info display
    info_frame = ttk.LabelFrame(root, text="Current Theme Colors")
    info_frame.pack(fill="x", padx=10, pady=5)

    info_text = tk.Text(info_frame, height=6, width=70)
    info_text.pack(fill="x", padx=5, pady=5)

    def update_color_info():
        """Update color information display."""
        try:
            current_theme = theme_manager.get_current_theme()
            colors = current_theme.colors

            info_content = []
            info_content.append(f"Theme: {current_theme.name}")
            info_content.append(f"Button BG: {colors.button_bg}")
            info_content.append(f"Button FG: {colors.button_fg}")
            info_content.append(f"Button Hover: {colors.button_hover}")
            info_content.append(f"Button Active: {colors.button_active}")
            info_content.append(f"Primary Text: {colors.primary_text}")

            info_text.delete("1.0", "end")
            info_text.insert("1.0", "\n".join(info_content))

        except Exception as e:
            info_text.delete("1.0", "end")
            info_text.insert("1.0", f"Error getting color info: {e}")

    # Update button to refresh color info
    update_btn = ttk.Button(
        info_frame, text="Update Color Info", command=update_color_info
    )
    update_btn.pack(pady=2)

    # Apply initial theme
    apply_theme()
    update_color_info()

    print("Button Text Theming Test")
    print("=" * 30)
    print("This test focuses specifically on button text theming.")
    print("Check if button text colors change when switching themes.")
    print("Both TTK and TK buttons should have proper text colors.")
    print("")

    root.mainloop()


if __name__ == "__main__":
    main()
