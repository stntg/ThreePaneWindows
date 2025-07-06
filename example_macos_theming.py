#!/usr/bin/env python3
"""
Example demonstrating macOS-specific theming features.

This example shows how the enhanced theming system provides:
- Native macOS appearance integration
- System accent color detection
- macOS-specific typography (SF Pro Display)
- Dark mode detection and adaptation
- Platform-specific color schemes
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

# Add the package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from threepanewindows.dockable import DockableThreePaneWindow
from threepanewindows.platform import platform_handler
from threepanewindows.themes import ThemeManager, ThemeType


class MacOSThemingDemo:
    """Demo application showcasing macOS theming features."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("macOS Theming Demo - ThreePaneWindows")
        self.root.geometry("1000x700")

        # Initialize theme manager with native theme
        self.theme_manager = ThemeManager(theme=ThemeType.NATIVE)

        # Create the UI
        self.create_ui()

        # Apply initial theming
        self.apply_current_theme()

    def create_ui(self):
        """Create the user interface."""
        # Create main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="macOS Native Theming Demo",
            font=(
                ("SF Pro Display", 18, "bold")
                if sys.platform == "darwin"
                else ("Segoe UI", 18, "bold")
            ),
        )
        title_label.pack(pady=(0, 20))

        # Platform info section
        self.create_platform_info_section(main_frame)

        # Theme controls section
        self.create_theme_controls_section(main_frame)

        # Three-pane window demo
        self.create_three_pane_demo(main_frame)

    def create_platform_info_section(self, parent):
        """Create platform information section."""
        info_frame = ttk.LabelFrame(parent, text="Platform & System Information")
        info_frame.pack(fill="x", pady=(0, 10))

        # Get platform information
        platform_info = self.theme_manager.get_platform_info()

        # Display platform info in a grid
        row = 0
        for key, value in platform_info.items():
            label = ttk.Label(info_frame, text=f"{key.replace('_', ' ').title()}:")
            label.grid(row=row, column=0, sticky="w", padx=5, pady=2)

            value_label = ttk.Label(info_frame, text=str(value))
            value_label.grid(row=row, column=1, sticky="w", padx=20, pady=2)

            row += 1

        # Add macOS-specific information if on macOS
        if sys.platform == "darwin":
            try:
                # Try to get macOS-specific info
                if hasattr(platform_handler, "get_system_accent_color"):
                    accent_color = platform_handler.get_system_accent_color()
                    accent_label = ttk.Label(info_frame, text="System Accent Color:")
                    accent_label.grid(row=row, column=0, sticky="w", padx=5, pady=2)

                    # Create a colored square to show the accent color
                    accent_frame = tk.Frame(
                        info_frame, bg=accent_color, width=20, height=20
                    )
                    accent_frame.grid(row=row, column=1, sticky="w", padx=20, pady=2)

                    accent_text = ttk.Label(info_frame, text=accent_color)
                    accent_text.grid(row=row, column=2, sticky="w", padx=5, pady=2)

                    row += 1
            except Exception as e:
                print(f"Could not get macOS-specific info: {e}")

    def create_theme_controls_section(self, parent):
        """Create theme control section."""
        controls_frame = ttk.LabelFrame(parent, text="Theme Controls")
        controls_frame.pack(fill="x", pady=(0, 10))

        # Theme selection
        theme_label = ttk.Label(controls_frame, text="Select Theme:")
        theme_label.pack(anchor="w", padx=5, pady=2)

        # Create theme buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(fill="x", padx=5, pady=5)

        themes_to_show = [
            "light",
            "dark",
            "blue",
            "native",
            "native_light",
            "native_dark",
            "system",
        ]
        available_themes = self.theme_manager.get_available_themes()

        for i, theme_name in enumerate(themes_to_show):
            if theme_name in available_themes:
                btn = ttk.Button(
                    button_frame,
                    text=theme_name.replace("_", " ").title(),
                    command=lambda t=theme_name: self.switch_theme(t),
                )
                btn.grid(row=i // 4, column=i % 4, padx=2, pady=2, sticky="ew")

        # Configure grid weights
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)

        # Refresh button
        refresh_btn = ttk.Button(
            controls_frame,
            text="Refresh System Theme",
            command=self.refresh_system_theme,
        )
        refresh_btn.pack(pady=5)

        # Current theme display
        self.current_theme_var = tk.StringVar()
        current_theme_label = ttk.Label(
            controls_frame, textvariable=self.current_theme_var
        )
        current_theme_label.pack(pady=2)

        self.update_current_theme_display()

    def create_three_pane_demo(self, parent):
        """Create a three-pane window demo."""
        demo_frame = ttk.LabelFrame(parent, text="Three-Pane Window Demo")
        demo_frame.pack(fill="both", expand=True)

        # Create a simple three-pane layout
        paned_window = ttk.PanedWindow(demo_frame, orient="horizontal")
        paned_window.pack(fill="both", expand=True, padx=5, pady=5)

        # Left pane
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)

        left_label = ttk.Label(left_frame, text="Left Panel")
        left_label.pack(pady=10)

        left_text = tk.Text(left_frame, height=10, width=20)
        left_text.insert(
            "1.0",
            "This is the left panel.\n\nIt demonstrates how themes affect text widgets.",
        )
        left_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Center pane
        center_frame = ttk.Frame(paned_window)
        paned_window.add(center_frame, weight=2)

        center_label = ttk.Label(center_frame, text="Center Panel")
        center_label.pack(pady=10)

        # Add various widgets to demonstrate theming
        sample_entry = ttk.Entry(center_frame)
        sample_entry.insert(0, "Sample Entry")
        sample_entry.pack(pady=5)

        sample_button = ttk.Button(center_frame, text="Sample Button")
        sample_button.pack(pady=5)

        sample_check = ttk.Checkbutton(center_frame, text="Sample Checkbox")
        sample_check.pack(pady=5)

        sample_radio1 = ttk.Radiobutton(center_frame, text="Option 1", value=1)
        sample_radio1.pack(pady=2)

        sample_radio2 = ttk.Radiobutton(center_frame, text="Option 2", value=2)
        sample_radio2.pack(pady=2)

        # Right pane
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=1)

        right_label = ttk.Label(right_frame, text="Right Panel")
        right_label.pack(pady=10)

        # Listbox with scrollbar
        listbox_frame = ttk.Frame(right_frame)
        listbox_frame.pack(fill="both", expand=True, padx=5, pady=5)

        listbox = tk.Listbox(listbox_frame)
        scrollbar = ttk.Scrollbar(
            listbox_frame, orient="vertical", command=listbox.yview
        )
        listbox.configure(yscrollcommand=scrollbar.set)

        for i in range(20):
            listbox.insert("end", f"Item {i+1}")

        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Store references for theming
        self.sample_widgets = {
            "left_text": left_text,
            "listbox": listbox,
            "entry": sample_entry,
        }

    def switch_theme(self, theme_name):
        """Switch to a different theme."""
        try:
            success = self.theme_manager.set_theme(theme_name, window=self.root)
            if success:
                self.apply_current_theme()
                self.update_current_theme_display()
                print(f"Switched to theme: {theme_name}")
            else:
                print(f"Failed to switch to theme: {theme_name}")
        except Exception as e:
            print(f"Error switching theme: {e}")

    def refresh_system_theme(self):
        """Refresh system theme to match current OS settings."""
        try:
            success = self.theme_manager.refresh_system_theme()
            if success:
                self.apply_current_theme()
                self.update_current_theme_display()
                print("System theme refreshed")
            else:
                print("Failed to refresh system theme")
        except Exception as e:
            print(f"Error refreshing system theme: {e}")

    def apply_current_theme(self):
        """Apply the current theme to all widgets."""
        try:
            # Apply ttk theme
            style = ttk.Style()
            self.theme_manager.apply_ttk_theme(style)

            # Apply theme to custom widgets
            current_theme = self.theme_manager.get_current_theme()

            # Update root window background
            self.root.configure(bg=current_theme.colors.primary_bg)

            # Apply theme to text widgets
            if hasattr(self, "sample_widgets"):
                text_style = self.theme_manager.get_tk_widget_style("text")
                self.sample_widgets["left_text"].configure(**text_style)

                listbox_style = self.theme_manager.get_tk_widget_style("listbox")
                self.sample_widgets["listbox"].configure(**listbox_style)

        except Exception as e:
            print(f"Error applying theme: {e}")

    def update_current_theme_display(self):
        """Update the current theme display."""
        current_theme = self.theme_manager.get_current_theme()
        self.current_theme_var.set(f"Current Theme: {current_theme.name}")

    def run(self):
        """Run the demo application."""
        print("macOS Theming Demo")
        print("=" * 30)
        print(
            "This demo showcases the enhanced theming system with macOS-specific features."
        )
        print("Try switching between different themes to see the native integration.")
        print("")

        self.root.mainloop()


if __name__ == "__main__":
    try:
        demo = MacOSThemingDemo()
        demo.run()
    except Exception as e:
        print(f"Error running demo: {e}")
        import traceback

        traceback.print_exc()
