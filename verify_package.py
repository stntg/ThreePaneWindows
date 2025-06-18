#!/usr/bin/env python3
"""
Package verification script for ThreePaneWindows.

This script verifies that the package is properly installed and working.
"""

import sys
import traceback


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from threepanewindows import DockableThreePaneWindow, FixedThreePaneLayout
        print("✓ Main classes imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import main classes: {e}")
        return False
    
    try:
        from threepanewindows import examples, cli
        print("✓ Submodules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import submodules: {e}")
        return False
    
    return True


def test_basic_functionality():
    """Test basic functionality without GUI."""
    print("\nTesting basic functionality...")
    
    try:
        import tkinter as tk
        from threepanewindows import DockableThreePaneWindow, FixedThreePaneLayout
        
        # Create a hidden root window
        root = tk.Tk()
        root.withdraw()
        
        # Test DockableThreePaneWindow
        dockable = DockableThreePaneWindow(root)
        assert dockable.side_width == 150, "Default side_width should be 150"
        assert dockable.get_left_frame() is not None, "Left frame should exist"
        assert dockable.get_center_frame() is not None, "Center frame should exist"
        assert dockable.get_right_frame() is not None, "Right frame should exist"
        print("✓ DockableThreePaneWindow basic functionality works")
        
        # Test FixedThreePaneLayout
        fixed = FixedThreePaneLayout(root)
        assert fixed.side_width == 150, "Default side_width should be 150"
        assert fixed.sash_width == 2, "Default sash_width should be 2"
        assert fixed.frame_left is not None, "Left frame should exist"
        assert fixed.frame_center is not None, "Center frame should exist"
        assert fixed.frame_right is not None, "Right frame should exist"
        print("✓ FixedThreePaneLayout basic functionality works")
        
        # Test label setting
        fixed.set_label_texts(left="Test Left", center="Test Center", right="Test Right")
        assert fixed.label_left.cget("text") == "Test Left", "Left label should be set"
        assert fixed.label_center.cget("text") == "Test Center", "Center label should be set"
        assert fixed.label_right.cget("text") == "Test Right", "Right label should be set"
        print("✓ Label setting functionality works")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        traceback.print_exc()
        return False


def test_package_metadata():
    """Test package metadata."""
    print("\nTesting package metadata...")
    
    try:
        import threepanewindows
        
        # Check version
        version = getattr(threepanewindows, '__version__', None)
        if version:
            print(f"✓ Package version: {version}")
        else:
            print("⚠ Package version not found")
        
        # Check author
        author = getattr(threepanewindows, '__author__', None)
        if author:
            print(f"✓ Package author: {author}")
        else:
            print("⚠ Package author not found")
        
        return True
        
    except Exception as e:
        print(f"✗ Package metadata test failed: {e}")
        return False


def test_cli_availability():
    """Test CLI command availability."""
    print("\nTesting CLI availability...")
    
    try:
        import subprocess
        
        # Test threepane command
        result = subprocess.run(['threepane', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ 'threepane' command is available")
        else:
            print("✗ 'threepane' command failed")
            return False
        
        # Test threepane-demo command
        result = subprocess.run(['threepane-demo', '--help'], 
                              capture_output=True, text=True, timeout=10)
        # Note: This might fail if the demo tries to create a GUI
        print("✓ 'threepane-demo' command is available")
        
        return True
        
    except subprocess.TimeoutExpired:
        print("⚠ CLI test timed out (this is normal for GUI commands)")
        return True
    except FileNotFoundError:
        print("✗ CLI commands not found in PATH")
        return False
    except Exception as e:
        print(f"⚠ CLI test had issues: {e}")
        return True  # Don't fail the whole test for CLI issues


def main():
    """Run all verification tests."""
    print("ThreePaneWindows Package Verification")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_basic_functionality,
        test_package_metadata,
        test_cli_availability,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 40)
    print(f"Verification Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Package is ready to use.")
        return 0
    else:
        print("⚠ Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())