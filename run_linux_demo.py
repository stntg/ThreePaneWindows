#!/usr/bin/env python3
"""
Linux Demo Launcher

Simple launcher script for the Linux Comprehensive Demo.
This script ensures proper path setup and provides helpful information.
"""

import os
import platform
import sys


def main():
    """Launch the Linux comprehensive demo."""
    print("ThreePaneWindows - Linux Comprehensive Demo")
    print("=" * 50)

    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        print(f"Current version: {platform.python_version()}")
        return 1

    # Check if running on Linux
    current_os = platform.system()
    if current_os != "Linux":
        print(f"Warning: This demo is optimized for Linux systems.")
        print(f"Current system: {current_os}")
        print("Some features may not work as expected.")
        print()

    # Add project root to path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    try:
        # Import and run the demo
        from examples.linux_comprehensive_demo import LinuxComprehensiveDemo

        print("Initializing Linux demo...")
        print("Features included:")
        print("• Flexible layout system")
        print("• Linux-native theming")
        print("• Ubuntu/DejaVu Sans typography")
        print("• PNG icon support")
        print("• Desktop environment detection")
        print("• Dark mode integration")
        print("• Professional Linux styling")
        print()

        demo = LinuxComprehensiveDemo()
        demo.run()

    except ImportError as e:
        print(f"Error importing demo modules: {e}")
        print("Make sure you're running this from the project root directory")
        return 1
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
        return 0
    except Exception as e:
        print(f"Error running Linux demo: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
