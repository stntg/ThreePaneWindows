#!/usr/bin/env python3
"""
WSL-optimized launcher for the Linux comprehensive demo.

This script automatically configures the environment for optimal WSL experience
and launches the Linux comprehensive demo with WSL-specific optimizations.
"""

import logging
import os
import subprocess
import sys

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def check_wsl_environment():
    """Check if we're running in WSL and what X server is available."""
    print("[*] Checking WSL environment...")

    # Check if we're in WSL
    is_wsl = False
    try:
        if os.path.exists("/proc/version"):
            with open("/proc/version", "r") as f:
                version_info = f.read().lower()
                if "microsoft" in version_info or "wsl" in version_info:
                    is_wsl = True
                    print("[+] WSL detected")
    except Exception:
        pass

    if not is_wsl:
        print("[!] WSL not detected - this script is optimized for WSL")
        return False

    # Check for DISPLAY variable
    display = os.environ.get("DISPLAY")
    if not display:
        print("[-] DISPLAY environment variable not set")
        print(
            "[i] You need an X server running on Windows (like VcXsrv, Xming, or X410)"
        )
        print("    Set DISPLAY variable, e.g.: export DISPLAY=:0")
        return False
    else:
        print(f"[+] DISPLAY set to: {display}")

    # Test X server connection
    try:
        result = subprocess.run(["xset", "q"], capture_output=True, timeout=5)
        if result.returncode == 0:
            print("[+] X server connection successful")
        else:
            print("[!] X server connection test failed")
            print("[i] Make sure your X server is running and accessible")
    except (
        subprocess.TimeoutExpired,
        subprocess.CalledProcessError,
        FileNotFoundError,
    ):
        print("[!] Could not test X server connection (xset not available)")

    return True


def setup_wsl_environment():
    """Setup optimal environment variables for WSL."""
    print("[*] Setting up WSL environment...")

    # Enable custom titlebar by default for WSL (better theming control)
    if not os.environ.get("THREEPANE_CUSTOM_TITLEBAR"):
        os.environ["THREEPANE_CUSTOM_TITLEBAR"] = "1"
        print("[+] Enabled custom titlebar for better WSL theming")

    # Set WSL-specific optimizations
    os.environ["THREEPANE_WSL_MODE"] = "1"

    # Optimize for WSL X server performance
    if not os.environ.get("LIBGL_ALWAYS_INDIRECT"):
        os.environ["LIBGL_ALWAYS_INDIRECT"] = "1"
        print("[+] Set OpenGL indirect rendering for WSL compatibility")

    # Set font rendering optimizations
    if not os.environ.get("GDK_SCALE"):
        os.environ["GDK_SCALE"] = "1"

    print("[+] WSL environment configured")


def check_dependencies():
    """Check if required dependencies are available."""
    print("[*] Checking dependencies...")

    try:
        import tkinter

        print("[+] tkinter available")
    except ImportError:
        print("[-] tkinter not available")
        print("[i] Install with: sudo apt-get install python3-tk")
        return False

    try:
        # Test if we can create a simple tkinter window
        root = tkinter.Tk()
        root.withdraw()  # Hide the test window
        root.destroy()
        print("[+] tkinter GUI creation successful")
    except Exception as e:
        print(f"[-] tkinter GUI test failed: {e}")
        print("[i] Check your X server configuration")
        return False

    return True


def launch_demo():
    """Launch the Linux comprehensive demo."""
    print("[*] Launching ThreePaneWindows WSL Demo...")

    try:
        # Import and run the demo
        from examples.linux_comprehensive_demo import LinuxComprehensiveDemo

        print("[+] Demo imported successfully")
        print("[*] Starting GUI application...")
        print("[i] The demo will automatically detect WSL and optimize accordingly")
        print("[i] Custom titlebar is enabled by default for better theme control")
        print("[i] Emergency exit keys: Ctrl+Q, Alt+F4, Escape")
        print()

        # Create and run the demo
        demo = LinuxComprehensiveDemo()
        demo.run()

    except ImportError as e:
        print(f"[-] Failed to import demo: {e}")
        print("[i] Make sure you're running from the project root directory")
        return False
    except Exception as e:
        print(f"[-] Failed to launch demo: {e}")
        import traceback

        print(f"[i] Full error details:")
        traceback.print_exc()
        return False

    return True


def test_custom_titlebar():
    """Test custom titlebar functionality."""
    print("[*] Testing custom titlebar functionality...")

    try:
        import tkinter as tk

        # Create test window
        root = tk.Tk()
        root.title("Custom Titlebar Test")
        root.geometry("400x300+200+200")

        # Test overrideredirect
        print("[*] Testing overrideredirect...")
        root.overrideredirect(True)

        # Create simple titlebar
        titlebar = tk.Frame(root, bg="#2d2d30", height=30)
        titlebar.pack(fill="x", side="top")
        titlebar.pack_propagate(False)

        # Add title
        title_label = tk.Label(
            titlebar, text="Test Titlebar", bg="#2d2d30", fg="white", font=("Arial", 10)
        )
        title_label.pack(side="left", padx=10, pady=5)

        # Add close button
        close_btn = tk.Button(
            titlebar,
            text="×",
            command=root.quit,
            bg="#2d2d30",
            fg="white",
            relief="flat",
            width=3,
            font=("Arial", 12, "bold"),
        )
        close_btn.pack(side="right", padx=5, pady=2)

        # Add content
        content = tk.Label(
            root,
            text="Custom titlebar test\nPress × to close or Ctrl+Q",
            font=("Arial", 12),
            justify="center",
        )
        content.pack(expand=True)

        # Add emergency exit
        root.bind("<Control-q>", lambda e: root.quit())

        # Make draggable
        def start_drag(event):
            root.x = event.x
            root.y = event.y

        def drag_window(event):
            x = root.winfo_pointerx() - root.x
            y = root.winfo_pointery() - root.y
            root.geometry(f"+{x}+{y}")

        titlebar.bind("<Button-1>", start_drag)
        titlebar.bind("<B1-Motion>", drag_window)
        title_label.bind("<Button-1>", start_drag)
        title_label.bind("<B1-Motion>", drag_window)

        print("[+] Custom titlebar test window created")
        print("[i] Try dragging the titlebar and closing with × or Ctrl+Q")

        root.mainloop()
        return True

    except Exception as e:
        print(f"[-] Custom titlebar test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Main launcher function."""
    import sys

    # Check for test mode
    if len(sys.argv) > 1 and sys.argv[1] == "--test-titlebar":
        print("=" * 60)
        print("Custom Titlebar Test Mode")
        print("=" * 60)
        print()

        if test_custom_titlebar():
            print("[+] Custom titlebar test completed")
            return 0
        else:
            print("[-] Custom titlebar test failed")
            return 1

    print("=" * 60)
    print("ThreePaneWindows WSL Demo Launcher")
    print("=" * 60)
    print()

    # Check WSL environment
    if not check_wsl_environment():
        print()
        print("[-] WSL environment check failed")
        print("[i] Please ensure you have:")
        print("    1. An X server running on Windows (VcXsrv, Xming, X410)")
        print("    2. DISPLAY environment variable set")
        print("    3. X server configured to allow connections")
        print()
        print("[i] You can test custom titlebar functionality with:")
        print("    python3 run_wsl_demo.py --test-titlebar")
        return 1

    print()

    # Setup WSL environment
    setup_wsl_environment()
    print()

    # Check dependencies
    if not check_dependencies():
        print()
        print("[-] Dependency check failed")
        return 1

    print()

    # Launch demo
    if not launch_demo():
        print()
        print("[-] Demo launch failed")
        print("[i] Troubleshooting options:")
        print(
            "    python3 run_wsl_demo.py --test-titlebar    # Test titlebar functionality"
        )
        print(
            "    python3 debug_titlebar.py                  # Run detailed debug tests"
        )
        print(
            "    THREEPANE_CUSTOM_TITLEBAR=0 python3 examples/linux_comprehensive_demo.py  # Disable custom titlebar"
        )
        print()
        print("[i] See WSL_TITLEBAR_TROUBLESHOOTING.md for detailed help")
        return 1

    print()
    print("[+] Demo completed successfully")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        sys.exit(1)
