#!/usr/bin/env python3
"""
Debug script to compare theme objects passed to scrollbars in both approaches.
"""

import os
import sys
import tkinter as tk

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from threepanewindows.central_theme_manager import ThemeType, get_theme_manager
    from threepanewindows.custom_scrollbar import ThemedScrollbar
    from threepanewindows.themes import ThemeManager

    print("✅ Successfully imported all modules")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def debug_theme_objects():
    """Debug the theme objects passed to scrollbars."""

    print("🔍 Debugging theme objects...")

    # Get central theme manager
    central_manager = get_theme_manager()
    central_manager.set_theme(ThemeType.LIGHT)

    # Get original theme manager
    original_manager = ThemeManager("light")

    print("\n📋 Central Theme Manager:")
    print(f"   get_current_theme() type: {type(central_manager.get_current_theme())}")
    print(f"   colors property type: {type(central_manager.colors)}")

    # Check the wrapper approach
    wrapper = central_manager._get_theme_for_scrollbar()
    print(f"   _get_theme_for_scrollbar() type: {type(wrapper)}")
    print(f"   wrapper.colors type: {type(wrapper.colors)}")

    print("\n📋 Original Theme Manager:")
    print(f"   get_current_theme() type: {type(original_manager.get_current_theme())}")
    print(
        f"   get_current_theme().colors type: {type(original_manager.get_current_theme().colors)}"
    )

    # Compare specific properties
    print("\n🎨 Comparing theme properties:")

    central_theme = central_manager.colors
    original_theme = original_manager.get_current_theme().colors
    wrapper_theme = wrapper.colors

    properties_to_check = [
        "panel_content_bg",
        "secondary_bg",
        "separator",
        "border",
        "secondary_text",
        "accent_text",
        "button_hover",
    ]

    for prop in properties_to_check:
        central_val = getattr(central_theme, prop, "MISSING")
        original_val = getattr(original_theme, prop, "MISSING")
        wrapper_val = getattr(wrapper_theme, prop, "MISSING")

        print(f"   {prop}:")
        print(f"      Central: {central_val}")
        print(f"      Original: {original_val}")
        print(f"      Wrapper: {wrapper_val}")

        if central_val != original_val:
            print(f"      ❌ MISMATCH between central and original!")
        if central_val != wrapper_val:
            print(f"      ❌ MISMATCH between central and wrapper!")

    # Test actual scrollbar creation
    print("\n🧪 Testing scrollbar creation:")

    root = tk.Tk()
    root.withdraw()  # Hide the window

    # Create scrollbars using both methods
    test_frame = tk.Frame(root)

    # Method 1: Direct creation like in professional_enhanced_demo
    print("   Creating scrollbar via central_manager.create_themed_scrollbar_auto...")
    scrollbar1 = central_manager.create_themed_scrollbar_auto(
        test_frame, orient="vertical"
    )

    # Method 2: Direct creation like in test_scrollbar_theming_comparison
    print("   Creating scrollbar via original_manager.create_themed_scrollbar_auto...")
    scrollbar2 = original_manager.create_themed_scrollbar_auto(
        test_frame, orient="vertical"
    )

    print(f"   Scrollbar 1 type: {type(scrollbar1)}")
    print(f"   Scrollbar 2 type: {type(scrollbar2)}")

    # Check if they have the same theming
    if hasattr(scrollbar1, "trough") and hasattr(scrollbar2, "trough"):
        try:
            color1 = scrollbar1.trough.cget("bg")
            color2 = scrollbar2.trough.cget("bg")
            print(f"   Scrollbar 1 trough color: {color1}")
            print(f"   Scrollbar 2 trough color: {color2}")

            if color1 != color2:
                print("   ❌ SCROLLBAR COLORS ARE DIFFERENT!")
            else:
                print("   ✅ Scrollbar colors match")
        except Exception as e:
            print(f"   ⚠️ Could not compare colors: {e}")

    root.destroy()


def main():
    """Main function."""
    print("🚀 Starting Scrollbar Theme Debug...")

    try:
        debug_theme_objects()
        print("\n✅ Debug completed")
    except Exception as e:
        print(f"❌ Error during debug: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
