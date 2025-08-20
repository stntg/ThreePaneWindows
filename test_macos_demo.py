#!/usr/bin/env python3
"""
Quick test script for the macOS Flexible Titlebar Demo

This script performs a quick validation of the demo functionality
without requiring user interaction.
"""

import os
import sys
import tkinter as tk

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def test_demo_import():
    """Test that the demo can be imported successfully."""
    try:
        from macos_flexible_titlebar_demo import MacOSFlexibleTitlebarDemo

        print("✓ Demo import successful")
        return True
    except ImportError as e:
        print(f"✗ Demo import failed: {e}")
        return False


def test_demo_initialization():
    """Test that the demo can be initialized."""
    try:
        from macos_flexible_titlebar_demo import MacOSFlexibleTitlebarDemo

        # Create demo instance
        demo = MacOSFlexibleTitlebarDemo()

        # Test basic properties
        assert demo.root is not None, "Root window not created"
        assert demo.theme_manager is not None, "Theme manager not initialized"
        assert demo.available_themes is not None, "Available themes not loaded"
        assert len(demo.available_themes) > 0, "No themes available"
        assert demo.custom_titlebar is not None, "Custom titlebar not created"

        # Test theme switching
        original_theme = demo.theme_manager.current_theme
        for theme_name in demo.available_themes[:3]:  # Test first 3 themes
            demo._switch_theme(theme_name)
            print(f"✓ Theme switch to '{theme_name}' successful")

        # Test titlebar functionality
        if (
            hasattr(demo.custom_titlebar, "titlebar_frame")
            and demo.custom_titlebar.titlebar_frame
        ):
            print("✓ Custom titlebar frame created")
        else:
            print("⚠ Custom titlebar frame not found")

        # Cleanup
        demo.root.destroy()

        print("✓ Demo initialization and theme switching successful")
        return True

    except Exception as e:
        print(f"✗ Demo initialization failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run the test suite."""
    print("macOS Flexible Titlebar Demo - Test Suite")
    print("=" * 50)

    tests = [
        ("Import Test", test_demo_import),
        ("Initialization Test", test_demo_initialization),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"✗ {test_name} failed")

    print(f"\nTest Results: {passed}/{total} tests passed")

    if passed == total:
        print("✓ All tests passed! Demo is ready to use.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
