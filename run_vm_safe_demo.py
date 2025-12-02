#!/usr/bin/env python3
"""
Launcher for VM-Safe Linux Demo

This script launches the VM-safe version of the flexible layout demo that
is specifically designed to work in virtual machine environments without
causing segmentation faults.

Usage:
    python3 run_vm_safe_demo.py

Or make it executable and run directly:
    chmod +x run_vm_safe_demo.py
    ./run_vm_safe_demo.py
"""

import os
import platform
import sys


def main():
    """Launch the VM-Safe Linux Demo."""
    print("🖥️ VM-Safe Linux Flexible Layout Demo Launcher")
    print("=" * 60)

    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Error: Python 3.8 or higher is required")
        print(f"Current version: {platform.python_version()}")
        return 1

    # Check platform and provide appropriate guidance
    current_os = platform.system()
    print(f"Platform detected: {current_os}")

    if current_os == "Linux":
        print("✓ Running on Linux - VM-safe features enabled")
        
        # Try to detect if we're in a VM
        vm_detected = False
        try:
            # Check for common VM indicators
            with open("/sys/class/dmi/id/sys_vendor", "r") as f:
                vendor = f.read().strip()
                if any(vm in vendor.lower() for vm in ["virtualbox", "vmware", "qemu", "microsoft"]):
                    vm_detected = True
                    print(f"🖥️ Virtual machine detected: {vendor}")
        except:
            pass
            
        if vm_detected:
            print("✓ VM-safe mode will be automatically enabled")
        else:
            print("ℹ️ Running on bare metal - VM-safe mode available if needed")
            
    elif current_os == "Windows":
        print("⚠️ Running on Windows - demo will work with Windows adaptations")
    elif current_os == "Darwin":
        print("⚠️ Running on macOS - demo will work with macOS adaptations")
    else:
        print(f"⚠️ Running on {current_os} - some features may not work as expected")

    print()

    # Add project root to path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    try:
        # Import and run the VM-safe demo
        print("🔄 Loading VM-safe demo modules...")
        from linux_vm_safe_demo import LinuxVMSafeDemo

        print("✓ Modules loaded successfully")
        print()
        print("🚀 Launching VM-safe demo...")
        print()
        print("VM-Safe Demo Features:")
        print("• 📐 Flexible layout with 6 detachable panes")
        print("• 🖥️ VM-safe custom titlebar (no X11 low-level calls)")
        print("• 🌈 All available themes (Light, Dark, Blue, Green, Purple, etc.)")
        print("• 🐧 Linux-optimized styling and fonts")
        print("• 🪟 Professional detached window management")
        print("• ⚡ Real-time theme switching")
        print("• 🛡️ No segmentation faults in VMs!")
        print()
        print("💡 Usage Tips:")
        print("• Click the 🎨 Themes button to switch themes")
        print("• Try detaching panes by clicking the detach button (↗️)")
        print("• Detached windows maintain theme consistency")
        print("• All panes can be reattached by clicking the reattach button (↙️)")
        print("• Works perfectly in VirtualBox, VMware, QEMU/KVM")
        print()
        print("🔧 Technical Details:")
        print("• Uses pure Tkinter without problematic X11 Motif hints")
        print("• Automatic VM detection and safe mode activation")
        print("• Maintains professional appearance and functionality")
        print("• Full compatibility with Pop!_OS, Ubuntu, and other Linux distros")
        print()
        print("=" * 60)

        # Create and run the demo
        demo = LinuxVMSafeDemo()
        demo.run()

        print("\n✓ VM-safe demo completed successfully")
        return 0

    except ImportError as e:
        print(f"✗ Error importing demo modules: {e}")
        print()
        print("Troubleshooting:")
        print("1. Make sure you're running this from the project root directory")
        print("2. Ensure the threepanewindows package is properly installed:")
        print("   pip install -e .")
        print("3. Check that all dependencies are installed:")
        print("   pip install -r requirements.txt")
        return 1

    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user (Ctrl+C)")
        return 0

    except Exception as e:
        print(f"✗ Error running VM-safe demo: {e}")
        print()
        print("Debug information:")
        import traceback
        traceback.print_exc()
        print()
        print("If this error persists, please check:")
        print("1. Python version (3.8+ required)")
        print("2. tkinter installation (usually included with Python)")
        print("3. threepanewindows package installation")
        print("4. Display environment (for Linux: DISPLAY variable, X11/Wayland)")
        print()
        print("This VM-safe version should work even if the regular demo crashes!")
        return 1


if __name__ == "__main__":
    sys.exit(main())