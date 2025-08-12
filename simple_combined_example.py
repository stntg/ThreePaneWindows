#!/usr/bin/env python3
"""
Simple Example: Typography + Spacing + Central Theme Manager

This example demonstrates the key concept: all three modules work independently
but complement each other perfectly when used together.
"""

import tkinter as tk

from threepanewindows.central_theme_manager import CentralThemeManager
from threepanewindows.spacing import Spacing, SpacingManager
from threepanewindows.typography import Typography, TypographyManager


def create_simple_demo():
    """Create a simple demo showing all three modules working together."""

    # Create main window
    root = tk.Tk()
    root.title("Simple Combined Modules Example")
    root.geometry("600x400")

    print("🎨 Initializing all three modules independently...")

    # 1. Typography Module - Independent font management
    typography = Typography(
        font_family="Arial", font_size_normal=12, font_size_large=16, font_size_title=20
    )
    typo_manager = TypographyManager(typography)
    print("✓ Typography module initialized")

    # 2. Spacing Module - Independent spacing management
    spacing = Spacing(
        padding_normal=15, margin_normal=10, button_padding_x=20, button_padding_y=8
    )
    spacing_manager = SpacingManager(spacing)
    print("✓ Spacing module initialized")

    # 3. Central Theme Manager - Independent color theming
    theme_manager = CentralThemeManager()
    theme_manager.set_theme("dark")  # Set to dark theme
    print("✓ Central Theme Manager initialized")

    # Create UI using all three modules together
    main_frame = tk.Frame(root)
    main_frame.pack(
        fill=tk.BOTH,
        expand=True,
        padx=spacing.get_padding("normal"),
        pady=spacing.get_padding("normal"),
    )

    # Title using typography
    title = tk.Label(main_frame, text="Three Modules Working Together")
    typo_manager.typography.apply_to_widget(title, size="title", weight="bold")
    title.pack(pady=spacing.get_margin("normal"))

    # Description using typography and spacing
    desc = tk.Label(
        main_frame,
        text="Typography handles fonts, Spacing handles layout, Theme Manager handles colors",
    )
    typo_manager.typography.apply_to_widget(desc, size="normal")
    desc.pack(pady=spacing.get_margin("normal"))

    # Button with custom spacing
    button = tk.Button(main_frame, text="Example Button")
    button.configure(padx=spacing.button_padding_x, pady=spacing.button_padding_y)
    button.pack(pady=spacing.get_margin("large"))

    # Entry with spacing
    entry = tk.Entry(main_frame)
    spacing_manager.apply_padding_to_widget(entry, size="normal")
    entry.pack(pady=spacing.get_margin("normal"))

    # Apply theme to everything (colors)
    theme_manager.apply_comprehensive_theme(root)

    print("\n" + "=" * 50)
    print("✅ SUCCESS: All three modules working together!")
    print("=" * 50)
    print("Key Points:")
    print("• Typography module manages fonts independently")
    print("• Spacing module manages layout independently")
    print("• Central Theme Manager manages colors independently")
    print("• No module imports or depends on the others")
    print("• They work together through composition, not inheritance")
    print("=" * 50)

    # Add theme switching buttons to demonstrate independence
    controls_frame = tk.Frame(main_frame)
    controls_frame.pack(pady=spacing.get_margin("large"))

    themes = ["light", "dark", "blue"]
    for theme in themes:
        btn = tk.Button(
            controls_frame,
            text=f"{theme.title()} Theme",
            command=lambda t=theme: switch_theme(theme_manager, root, t),
        )
        btn.configure(
            padx=spacing.button_padding_x // 2, pady=spacing.button_padding_y // 2
        )
        btn.pack(side=tk.LEFT, padx=spacing.get_margin("small"))

    return root, theme_manager


def switch_theme(theme_manager, root, theme_name):
    """Switch theme to demonstrate central theme manager independence."""
    try:
        theme_manager.set_theme(theme_name)
        theme_manager.apply_comprehensive_theme(root)
        print(
            f"✓ Switched to {theme_name} theme - Theme Manager working independently!"
        )
    except Exception as e:
        print(f"❌ Error switching theme: {e}")


def main():
    """Run the simple combined example."""
    try:
        root, theme_manager = create_simple_demo()
        root.mainloop()
    except Exception as e:
        print(f"❌ Example failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
