#!/usr/bin/env python3
"""
Launcher for macOS Flexible Layout + Custom Titlebar Demo

This script provides an easy way to launch the comprehensive demo that showcases:
- Flexible layout system with complex nested layouts
- Custom titlebar for both main window and detached panes
- Complete theme switching through all available themes
- macOS-optimized styling and behavior
- Professional detached window management

Usage:
    python3 run_macos_flexible_titlebar_demo.py

Or make it executable and run directly:
    chmod +x run_macos_flexible_titlebar_demo.py
    ./run_macos_flexible_titlebar_demo.py
"""

import os
import platform
import sys


def main():
    """Launch the macOS Flexible Titlebar Demo."""
    print("🍎 macOS Flexible Layout + Custom Titlebar Demo Launcher")
    print("=" * 60)

    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Error: Python 3.8 or higher is required")
        print(f"Current version: {platform.python_version()}")
        return 1

    # Check platform and provide appropriate guidance
    current_os = platform.system()
    print(f"Platform detected: {current_os}")

    if current_os == "Darwin":
        print("✓ Running on macOS - all features will be available")
        # Check macOS version
        try:
            macos_version = platform.mac_ver()[0]
            print(f"macOS version: {macos_version}")
            if macos_version and float(macos_version.split(".")[0]) >= 10:
                print("✓ macOS version supported")
            else:
                print("⚠️ macOS 10.14+ recommended for best experience")
        except:
            print("⚠️ Could not detect macOS version")
    elif current_os == "Linux":
        print("⚠️ Running on Linux - demo will work but with Linux-specific adaptations")
    elif current_os == "Windows":
        print(
            "⚠️ Running on Windows - demo will work but with Windows-specific adaptations"
        )
    else:
        print(f"⚠️ Running on {current_os} - some features may not work as expected")

    print()

    # Add project root to path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    try:
        # Import and run the demo
        print("🔄 Loading demo modules...")
        from macos_flexible_titlebar_demo import MacOSFlexibleTitlebarDemo

        print("✓ Modules loaded successfully")
        print()
        print("🚀 Launching demo...")
        print()
        print("Demo Features:")
        print("• 📐 Flexible layout with 6 detachable panes")
        print("• 🎨 macOS-style custom titlebar with theme switching menu")
        print("• 🌈 All available themes (Light, Dark, Blue, Green, Purple, etc.)")
        print("• 🍎 macOS-optimized styling and fonts (SF Pro, Menlo)")
        print("• 🪟 Professional detached window management")
        print("• ⚡ Real-time theme switching")
        print("• 🎯 Xcode-inspired layout and controls")
        print("• 📱 Retina display optimization")
        print()
        print("💡 Usage Tips:")
        print("• Click the 🎨 Themes button in the titlebar to switch themes")
        print("• Try detaching panes by clicking the detach button (↗️)")
        print("• Detached windows maintain theme consistency")
        print("• All panes can be reattached by clicking the reattach button (↙️)")
        print("• Use system theme for automatic macOS theme integration")
        print("• Supports both Intel and Apple Silicon Macs")
        print()
        print("=" * 60)

        # Create and run the demo
        demo = MacOSFlexibleTitlebarDemo()
        demo.run()

        print("\n✓ Demo completed successfully")
        return 0

    except ImportError as e:
        print(f"✗ Error importing demo modules: {e}")
        print()
        print("Troubleshooting:")
        print("1. Make sure you're running this from the project root directory")
        print("2. Ensure the threepanewindows package is properly installed:")
        print("   pip3 install -e .")
        print("3. Check that all dependencies are installed:")
        print("   pip3 install -r requirements.txt")
        print("4. Ensure tkinter is available (usually included with Python)")
        return 1

    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user (⌘+C)")
        return 0

    except Exception as e:
        print(f"✗ Error running demo: {e}")
        print()
        print("Debug information:")
        import traceback

        traceback.print_exc()
        print()
        print("If this error persists, please check:")
        print("1. Python version (3.8+ required)")
        print("2. tkinter installation (usually included with Python)")
        print("3. threepanewindows package installation")
        print("4. macOS version compatibility (10.14+ recommended)")
        print("5. Display environment (ensure GUI access is available)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
