#!/usr/bin/env python3
"""
Test script for enhanced cross-platform theming functionality.

This script demonstrates the new theming capabilities including:
- Platform-native themes
- System appearance detection
- Cross-platform font handling
- Enhanced theme management
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

# Add the package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from threepanewindows.platform import platform_handler
from threepanewindows.themes import ThemeManager, ThemeType


def create_test_window():
    """Create a test window to demonstrate theming capabilities."""
    root = tk.Tk()
    root.title("Enhanced Theming Test")
    root.geometry("800x600")

    # Create theme manager
    theme_manager = ThemeManager()

    # Create main frame
    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Platform info section
    info_frame = ttk.LabelFrame(main_frame, text="Platform Information")
    info_frame.pack(fill="x", pady=(0, 10))

    platform_info = theme_manager.get_platform_info()
    for key, value in platform_info.items():
        info_label = ttk.Label(info_frame, text=f"{key}: {value}")
        info_label.pack(anchor="w", padx=5, pady=2)

    # Theme selection section
    theme_frame = ttk.LabelFrame(main_frame, text="Theme Selection")
    theme_frame.pack(fill="x", pady=(0, 10))

    # Available themes
    available_themes = theme_manager.get_available_themes()
    theme_var = tk.StringVar(value=theme_manager.get_current_theme().name.lower())

    themes_label = ttk.Label(theme_frame, text="Available Themes:")
    themes_label.pack(anchor="w", padx=5, pady=2)

    for theme_name in available_themes:
        theme_radio = ttk.Radiobutton(
            theme_frame,
            text=theme_name.title(),
            variable=theme_var,
            value=theme_name,
            command=lambda t=theme_name: apply_theme(theme_manager, t, root),
        )
        theme_radio.pack(anchor="w", padx=20, pady=1)

    # Sample widgets section
    sample_frame = ttk.LabelFrame(main_frame, text="Sample Widgets")
    sample_frame.pack(fill="both", expand=True)

    # Create sample widgets
    sample_label = ttk.Label(sample_frame, text="Sample Label")
    sample_label.pack(pady=5)

    sample_button = ttk.Button(sample_frame, text="Sample Button")
    sample_button.pack(pady=5)

    sample_entry = ttk.Entry(sample_frame)
    sample_entry.insert(0, "Sample Entry")
    sample_entry.pack(pady=5)

    sample_text = tk.Text(sample_frame, height=5, width=50)
    sample_text.insert("1.0", "Sample Text Widget\nThis demonstrates theming.")
    sample_text.pack(pady=5)

    # Apply initial theme
    apply_theme(theme_manager, theme_var.get(), root)

    return root, theme_manager


def apply_theme(theme_manager, theme_name, window):
    """Apply a theme to the window."""
    try:
        # Set the theme
        success = theme_manager.set_theme(theme_name, window=window)
        if success:
            print(f"Applied theme: {theme_name}")

            # Apply ttk styling
            style = ttk.Style()
            theme_manager.apply_ttk_theme(style)

            # Update window background
            current_theme = theme_manager.get_current_theme()
            window.configure(bg=current_theme.colors.primary_bg)

        else:
            print(f"Failed to apply theme: {theme_name}")
    except Exception as e:
        print(f"Error applying theme {theme_name}: {e}")


def test_theme_functionality():
    """Test various theme functionality."""
    print("Testing Enhanced Theming System")
    print("=" * 40)

    # Create theme manager
    theme_manager = ThemeManager()

    # Test platform detection
    print("\nPlatform Information:")
    platform_info = theme_manager.get_platform_info()
    for key, value in platform_info.items():
        print(f"  {key}: {value}")

    # Test available themes
    print(f"\nAvailable Themes: {theme_manager.get_available_themes()}")
    print(f"Native Theme Available: {theme_manager.is_native_theme_available()}")

    # Test theme switching
    print("\nTesting Theme Switching:")
    for theme_name in ["light", "dark", "blue"]:
        success = theme_manager.set_theme(theme_name)
        current = theme_manager.get_current_theme()
        print(f"  {theme_name}: {'✓' if success else '✗'} (Current: {current.name})")

    # Test native themes if available
    if theme_manager.is_native_theme_available():
        print("\nTesting Native Themes:")
        for theme_name in ["native", "native_light", "native_dark"]:
            if theme_name in theme_manager.get_available_themes():
                success = theme_manager.set_theme(theme_name)
                current = theme_manager.get_current_theme()
                print(
                    f"  {theme_name}: {'✓' if success else '✗'} (Current: {current.name})"
                )

    # Test system theme refresh
    print(
        f"\nSystem Theme Refresh: {'✓' if theme_manager.refresh_system_theme() else '✗'}"
    )

    print("\nTest completed!")


if __name__ == "__main__":
    # Run functionality tests
    test_theme_functionality()

    # Create and show test window
    print("\nCreating test window...")
    try:
        root, theme_manager = create_test_window()
        print("Test window created. Close the window to exit.")
        root.mainloop()
    except Exception as e:
        print(f"Error creating test window: {e}")
        import traceback

        traceback.print_exc()
