#!/usr/bin/env python3
"""
Test runner for new v1.3.0 features.

This script runs all the headless-compatible tests for the new functionality
introduced in ThreePaneWindows v1.3.0.

Features tested:
- Enhanced Flexible Layout System (7 tests)
- Central Theme Manager (23 tests)
- Custom UI Components (8 tests)
- Enhanced Logging System (30 tests)
- Integration and Summary (12 tests)

Total: 80 tests, all designed to pass in CI/CD environments.

Usage:
    python run_new_features_tests.py

Requirements:
    - pytest installed
    - ThreePaneWindows package installed
    - No GUI dependencies (runs in headless mode)
"""

import os
import subprocess
import sys


def run_tests():
    """Run all new feature tests in headless mode."""

    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Test files to run
    test_files = [
        "tests/test_flexible.py",
        "tests/test_custom_menubar.py",
        "tests/test_central_theme_manager_simple.py",
        "tests/test_logging_ci_safe.py",
        "tests/test_new_features_summary.py",
    ]

    # Convert to absolute paths
    test_paths = [os.path.join(script_dir, test_file) for test_file in test_files]

    # Build pytest command
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        *test_paths,
        "-v",  # Verbose output
        "-m",
        "not gui",  # Skip GUI tests
        "--tb=short",  # Short traceback format
        "--no-header",  # No pytest header
        "--no-summary",  # No summary section
    ]

    print("🧪 Running ThreePaneWindows v1.3.0 New Features Tests")
    print("=" * 60)
    print(f"Test files: {len(test_files)}")
    print(f"Mode: Headless (GUI tests skipped)")
    print("=" * 60)

    try:
        # Run the tests
        result = subprocess.run(cmd, cwd=script_dir, capture_output=False)

        print("=" * 60)
        if result.returncode == 0:
            print("✅ All tests passed!")
            print("🚀 New v1.3.0 features are working correctly.")
        else:
            print("❌ Some tests failed!")
            print("🔍 Check the output above for details.")

        return result.returncode

    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


def main():
    """Main entry point."""
    exit_code = run_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
