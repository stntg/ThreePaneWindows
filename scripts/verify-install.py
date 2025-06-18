#!/usr/bin/env python3
"""
Verification script for ThreePaneWindows installation.

This script verifies that the package is properly installed and working.
"""

import sys
import tkinter as tk
from pathlib import Path

def test_import():
    """Test importing the package."""
    try:
        import threepanewindows
        print(f"✅ Successfully imported threepanewindows v{threepanewindows.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import threepanewindows: {e}")
        return False

def test_classes():
    """Test importing main classes."""
    try:
        from threepanewindows import (
            FixedThreePaneWindow,
            DockableThreePaneWindow,
            EnhancedDockableThreePaneWindow,
            ThemeManager
        )
        print("✅ Successfully imported main classes")
        return True
    except ImportError as e:
        print(f"❌ Failed to import main classes: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality."""
    try:
        from threepanewindows import FixedThreePaneWindow
        
        # Create a hidden root window for testing
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Test creating a window
        window = FixedThreePaneWindow(root)
        
        # Test accessing panes
        assert hasattr(window, 'left_pane')
        assert hasattr(window, 'center_pane')
        assert hasattr(window, 'right_pane')
        
        # Test adding widgets
        label = tk.Label(window.left_pane, text="Test")
        label.pack()
        
        # Cleanup
        window.destroy()
        root.destroy()
        
        print("✅ Basic functionality test passed")
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_theming():
    """Test theming system."""
    try:
        from threepanewindows import ThemeManager, get_theme_manager
        
        theme_manager = get_theme_manager()
        themes = theme_manager.get_available_themes()
        
        if themes:
            print(f"✅ Theming system working - Available themes: {', '.join(themes)}")
            return True
        else:
            print("⚠️  Theming system loaded but no themes available")
            return False
    except Exception as e:
        print(f"❌ Theming system test failed: {e}")
        return False

def main():
    """Run all verification tests."""
    print("🔍 Verifying ThreePaneWindows installation")
    print("=" * 50)
    
    tests = [
        ("Package Import", test_import),
        ("Class Import", test_classes),
        ("Basic Functionality", test_basic_functionality),
        ("Theming System", test_theming),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! ThreePaneWindows is ready to use.")
        print("\n🚀 Try running an example:")
        print("   python -m threepanewindows.examples")
        return True
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please check your installation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)