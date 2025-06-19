#!/usr/bin/env python3
"""Test script to verify version parsing works correctly."""

import sys
import os

# Add the threepanewindows directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'threepanewindows'))

def test_version_parsing():
    """Test version parsing with various formats."""
    
    # Import the parsing function
    from _version import _parse_version
    
    test_cases = [
        ("0.1.0", (0, 1, 0)),
        ("1.2.3", (1, 2, 3)),
        ("0.1.0-rc1", (0, 1, 0)),
        ("0.1.0-test1", (0, 1, 0)),
        ("1.0.0-alpha", (1, 0, 0)),
        ("2.5.10-beta.1", (2, 5, 10)),
        ("0.1.0-dev", (0, 1, 0)),
        ("1.0", (1, 0, 0)),  # Missing patch version
        ("2", (2, 0, 0)),    # Only major version
    ]
    
    print("Testing version parsing:")
    print("=" * 40)
    
    all_passed = True
    for version_str, expected in test_cases:
        try:
            result = _parse_version(version_str)
            if result == expected:
                print(f"✅ {version_str:15} -> {result}")
            else:
                print(f"❌ {version_str:15} -> {result} (expected {expected})")
                all_passed = False
        except Exception as e:
            print(f"❌ {version_str:15} -> ERROR: {e}")
            all_passed = False
    
    print("=" * 40)
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    return all_passed

def test_import():
    """Test that the module can be imported successfully."""
    print("\nTesting module import:")
    print("=" * 30)
    
    try:
        # Test importing the version module directly
        from _version import __version__, __version_info__, MAJOR, MINOR, PATCH, FULL_VERSION
        print(f"✅ Direct import successful")
        print(f"   __version__ = {__version__}")
        print(f"   __version_info__ = {__version_info__}")
        print(f"   MAJOR.MINOR.PATCH = {MAJOR}.{MINOR}.{PATCH}")
        print(f"   FULL_VERSION = {FULL_VERSION}")
        
        # Test importing through the main package
        import sys
        sys.path.insert(0, os.path.dirname(__file__))
        import threepanewindows
        print(f"✅ Package import successful")
        print(f"   threepanewindows.__version__ = {threepanewindows.__version__}")
        print(f"   threepanewindows.__version_info__ = {threepanewindows.__version_info__}")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    parsing_ok = test_version_parsing()
    import_ok = test_import()
    
    if parsing_ok and import_ok:
        print("\n🎉 All tests passed! The version parsing fix should work.")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)