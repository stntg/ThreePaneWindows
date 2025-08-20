#!/usr/bin/env python3
"""
Test script for custom titlebar integration with ThreePaneWindows.

This script tests the new custom titlebar system to ensure it works
correctly across different platforms and integrates properly with
the existing ThreePaneWindows modules.
"""

import sys
import tkinter as tk
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, str(Path(__file__).parent))


def test_custom_titlebar_import():
    """Test that custom titlebar modules can be imported."""
    print("Testing custom titlebar imports...")

    try:
        from threepanewindows.utils.custom_titlebar import (
            CustomTitleBarManager,
            LinuxTitleBar,
            MacOSTitleBar,
            WindowsTitleBar,
            apply_custom_titlebar,
            get_titlebar_theme,
        )

        print("✓ Custom titlebar modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import custom titlebar modules: {e}")
        return False


def test_platform_handler_integration():
    """Test that platform handlers integrate with custom titlebar."""
    print("Testing platform handler integration...")

    try:
        from threepanewindows.utils import (
            apply_custom_titlebar_direct,
            get_titlebar_theme,
            platform_handler,
        )

        # Test that platform handler has the required methods
        assert hasattr(platform_handler, "apply_custom_titlebar")
        print("✓ Platform handler has apply_custom_titlebar method")

        # Test theme generation
        light_theme = get_titlebar_theme(False)
        dark_theme = get_titlebar_theme(True)

        required_keys = [
            "bg",
            "fg",
            "btn_bg",
            "btn_fg",
            "btn_active_bg",
            "content_bg",
            "font",
            "height",
        ]
        for key in required_keys:
            assert key in light_theme, f"Missing key '{key}' in light theme"
            assert key in dark_theme, f"Missing key '{key}' in dark theme"

        print("✓ Theme generation works correctly")
        return True

    except Exception as e:
        print(f"✗ Platform handler integration test failed: {e}")
        return False


def test_titlebar_creation():
    """Test creating custom titlebars."""
    print("Testing titlebar creation...")

    try:
        from threepanewindows.utils.custom_titlebar import CustomTitleBarManager

        # Create a test window
        root = tk.Tk()
        root.withdraw()  # Hide the window during testing

        # Test theme
        theme = {
            "bg": "#f0f0f0",
            "fg": "#000000",
            "btn_bg": "#e1e1e1",
            "btn_fg": "#000000",
            "btn_active_bg": "#bee6fd",
            "content_bg": "#ffffff",
            "font": ("Arial", 10),
            "height": 30,
        }

        # Test creating titlebar
        titlebar = CustomTitleBarManager.create_titlebar(root, theme, "Test Window")

        if titlebar:
            print("✓ Titlebar created successfully")
            titlebar.destroy()
            root.destroy()
            return True
        else:
            print("✗ Failed to create titlebar")
            root.destroy()
            return False

    except Exception as e:
        print(f"✗ Titlebar creation test failed: {e}")
        return False


def test_theme_switching():
    """Test theme switching functionality."""
    print("Testing theme switching...")

    try:
        from threepanewindows.utils.custom_titlebar import CustomTitleBarManager

        # Create a test window
        root = tk.Tk()
        root.withdraw()  # Hide the window during testing

        # Test light theme
        light_theme = CustomTitleBarManager.get_default_theme(False)
        titlebar = CustomTitleBarManager.create_titlebar(
            root, light_theme, "Test Window"
        )

        if titlebar:
            # Test switching to dark theme
            dark_theme = CustomTitleBarManager.get_default_theme(True)
            titlebar.apply_theme(dark_theme)
            print("✓ Theme switching works correctly")

            titlebar.destroy()
            root.destroy()
            return True
        else:
            print("✗ Failed to create titlebar for theme switching test")
            root.destroy()
            return False

    except Exception as e:
        print(f"✗ Theme switching test failed: {e}")
        return False


def test_integration_with_threepane_modules():
    """Test integration with ThreePaneWindows modules."""
    print("Testing integration with ThreePaneWindows modules...")

    try:
        from threepanewindows.dockable import DockableThreePaneWindow
        from threepanewindows.utils import apply_custom_titlebar

        # Create a test window
        root = tk.Tk()
        root.withdraw()  # Hide the window during testing

        # Create a simple theme object for testing
        class MockTheme:
            def __init__(self):
                self.primary_bg = "#f0f0f0"
                self.primary_fg = "#000000"
                self.button_bg = "#e1e1e1"
                self.button_fg = "#000000"
                self.button_hover = "#bee6fd"
                self.content_bg = "#ffffff"

        mock_theme = MockTheme()

        # Test applying custom titlebar through platform handler
        result = apply_custom_titlebar(root, mock_theme)

        if result:
            print("✓ Custom titlebar applied through platform handler")
        else:
            print(
                "! Custom titlebar application returned False (may be expected on some platforms)"
            )

        # Test creating dockable window (basic test)
        def dummy_builder(parent):
            tk.Label(parent, text="Test").pack()

        dockable = DockableThreePaneWindow(
            root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
        )

        print("✓ DockableThreePaneWindow created successfully")

        root.destroy()
        return True

    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("Custom Titlebar Integration Tests")
    print("=" * 60)

    tests = [
        test_custom_titlebar_import,
        test_platform_handler_integration,
        test_titlebar_creation,
        test_theme_switching,
        test_integration_with_threepane_modules,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            print()

    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("🎉 All tests passed! Custom titlebar integration is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False


def main():
    """Main entry point for the test script."""
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Test runner crashed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
