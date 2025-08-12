#!/usr/bin/env python3
"""
Test script to demonstrate that typography and spacing modules can be used
independently from the central_theme_manager.
"""

import tkinter as tk

from threepanewindows.spacing import Spacing, SpacingManager, get_spacing_manager
from threepanewindows.typography import (
    Typography,
    TypographyManager,
    get_typography_manager,
)


def test_typography_independence():
    """Test that typography module works independently."""
    print("Testing Typography module independence...")

    # Create a root window for font operations
    root = tk.Tk()
    root.withdraw()  # Hide the window

    try:
        # Create a custom typography configuration
        custom_typography = Typography(
            font_size_normal=12, font_size_large=16, font_family="Arial"
        )

        # Create a typography manager
        typo_manager = TypographyManager(custom_typography)

        # Test font tuple generation (doesn't need root window)
        font_tuple = custom_typography.get_font_tuple(size="normal", weight="normal")
        print(f"Font tuple: {font_tuple}")

        # Test font creation (needs root window)
        font = typo_manager.get_font(size="large", weight="bold")
        print(f"Created font: {font}")

        print("✓ Typography module works independently!")
        return True
    finally:
        root.destroy()


def test_spacing_independence():
    """Test that spacing module works independently."""
    print("\nTesting Spacing module independence...")

    # Create a custom spacing configuration
    custom_spacing = Spacing(padding_normal=10, margin_normal=5, border_normal=2)

    # Create a spacing manager
    spacing_manager = SpacingManager(custom_spacing)

    # Test spacing values
    padding = custom_spacing.get_padding("normal")
    margin = custom_spacing.get_margin("normal")
    border = custom_spacing.get_border_width("normal")

    print(f"Padding: {padding}, Margin: {margin}, Border: {border}")

    # Test button padding
    button_padding = spacing_manager.get_button_padding()
    print(f"Button padding: {button_padding}")

    print("✓ Spacing module works independently!")
    return True


def test_combined_usage():
    """Test using both modules together without central_theme_manager."""
    print("\nTesting combined usage without central_theme_manager...")

    # Create root window
    root = tk.Tk()
    root.title("Independent Typography & Spacing Test")
    root.geometry("400x300")

    # Get global managers
    typo_manager = get_typography_manager()
    spacing_manager = get_spacing_manager()

    # Create a label with custom typography
    label = tk.Label(root, text="This is a test label")
    typo_manager.typography.apply_to_widget(label, size="large", weight="bold")
    label.pack(pady=spacing_manager.spacing.get_padding("medium"))

    # Create a button with custom spacing
    button = tk.Button(root, text="Test Button")
    button_padx, button_pady = spacing_manager.get_button_padding()
    button.configure(padx=button_padx, pady=button_pady)
    button.pack(pady=spacing_manager.spacing.get_margin("large"))

    # Create an entry with custom styling
    entry = tk.Entry(root)
    typo_manager.typography.apply_to_widget(entry, size="normal")
    spacing_manager.apply_padding_to_widget(entry, size="small")
    entry.pack(pady=spacing_manager.spacing.get_margin("normal"))

    print("✓ Combined usage works without central_theme_manager!")

    # Don't start mainloop in test, just destroy
    root.destroy()
    return True


def main():
    """Run all independence tests."""
    print("=" * 60)
    print("Testing Typography and Spacing Module Independence")
    print("=" * 60)

    try:
        # Test individual modules
        test_typography_independence()
        test_spacing_independence()
        test_combined_usage()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("Typography and Spacing modules can be used independently")
        print("from the central_theme_manager!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
