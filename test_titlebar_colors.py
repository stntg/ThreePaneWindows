#!/usr/bin/env python3
"""
Test script to demonstrate Windows titlebar color theming.

This script creates a simple window and cycles through different themes
to show how the titlebar colors change to match the selected theme.
"""

import os
import platform
import sys
import tkinter as tk
from tkinter import messagebox

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from threepanewindows.central_theme_manager import (
        get_theme_manager,
        set_global_theme,
    )
    from threepanewindows.utils.custom_titlebar import WindowsTitleBar
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


class TitlebarColorTest:
    """Test application for titlebar color theming."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Titlebar Color Test")
        self.root.geometry("600x400")

        # Initialize theme manager
        self.theme_manager = get_theme_manager()
        self.available_themes = self.theme_manager.get_theme_names()

        # Set initial theme
        set_global_theme("light")

        # Create titlebar
        self.setup_titlebar()

        # Create UI
        self.setup_ui()

        print(f"Windows version: {platform.version()}")
        print(f"Available themes: {', '.join(self.available_themes)}")

    def setup_titlebar(self):
        """Setup the Windows titlebar."""
        theme = self.theme_manager.get_current_theme()
        theme_dict = {
            "bg": theme.primary_bg,
            "fg": theme.primary_text,
            "btn_bg": theme.button_bg,
            "btn_fg": theme.button_text,
            "btn_active_bg": theme.button_hover,
            "font": ("Segoe UI", 10),
            "height": 32,
        }

        self.titlebar = WindowsTitleBar(self.root, theme_dict, "Titlebar Color Test")
        # The titlebar will use native Windows titlebar with custom colors

    def setup_ui(self):
        """Setup the user interface."""
        main_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Windows Titlebar Color Test",
            font=("Segoe UI", 16, "bold"),
            bg="white",
        )
        title_label.pack(pady=(0, 20))

        # Instructions
        instructions = tk.Label(
            main_frame,
            text="Click the buttons below to test different theme colors.\n"
            "On Windows 11, the titlebar should change to match the theme colors.\n"
            "On Windows 10, the titlebar will switch between light and dark modes.",
            font=("Segoe UI", 10),
            bg="white",
            justify="center",
        )
        instructions.pack(pady=(0, 20))

        # Theme buttons
        button_frame = tk.Frame(main_frame, bg="white")
        button_frame.pack(pady=10)

        themes_to_test = ["light", "dark", "blue", "green", "purple"]
        for theme in themes_to_test:
            if theme in self.available_themes:
                btn = tk.Button(
                    button_frame,
                    text=f"{theme.title()} Theme",
                    command=lambda t=theme: self.switch_theme(t),
                    font=("Segoe UI", 10),
                    padx=15,
                    pady=5,
                )
                btn.pack(side="left", padx=5)

        # Status label
        self.status_label = tk.Label(
            main_frame, text="Current theme: light", font=("Segoe UI", 10), bg="white"
        )
        self.status_label.pack(pady=(20, 0))

        # Info button
        info_btn = tk.Button(
            main_frame,
            text="Show Windows Version Info",
            command=self.show_version_info,
            font=("Segoe UI", 10),
            padx=15,
            pady=5,
        )
        info_btn.pack(pady=(10, 0))

    def switch_theme(self, theme_name):
        """Switch to a different theme."""
        try:
            print(f"Switching to theme: {theme_name}")
            set_global_theme(theme_name)

            # Update titlebar
            theme = self.theme_manager.get_current_theme()
            theme_dict = {
                "bg": theme.primary_bg,
                "fg": theme.primary_text,
                "btn_bg": theme.button_bg,
                "btn_fg": theme.button_text,
                "btn_active_bg": theme.button_hover,
                "font": ("Segoe UI", 10),
                "height": 32,
            }
            self.titlebar.apply_theme(theme_dict)

            # Update window background
            self.root.configure(bg=theme.primary_bg)

            # Update status
            self.status_label.config(text=f"Current theme: {theme_name}")

            print(f"✓ Theme switched to: {theme_name}")
            print(f"  Background color: {theme.primary_bg}")
            print(f"  Text color: {theme.primary_text}")

        except Exception as e:
            print(f"Error switching theme: {e}")
            messagebox.showerror("Error", f"Failed to switch theme: {e}")

    def show_version_info(self):
        """Show Windows version information."""
        version_info = f"""Windows Version Information:

Platform: {platform.system()}
Version: {platform.version()}
Release: {platform.release()}

Titlebar Color Support:
• Windows 11: Full custom colors (background + text)
• Windows 10: Light/Dark mode only

Current Theme: {getattr(self.theme_manager.current_theme, 'value', 'unknown')}
Available Themes: {', '.join(self.available_themes)}"""

        messagebox.showinfo("Windows Version Info", version_info)

    def run(self):
        """Run the test application."""
        print("Starting titlebar color test...")
        print(
            "Try switching between different themes to see the titlebar colors change!"
        )
        self.root.mainloop()


if __name__ == "__main__":
    app = TitlebarColorTest()
    app.run()
