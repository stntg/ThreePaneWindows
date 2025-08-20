#!/usr/bin/env python3
"""
Minimal debug script for custom titlebar on WSL.
This isolates the titlebar creation to identify the exact issue.
"""

import logging
import os
import sys
import tkinter as tk

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def test_basic_window():
    """Test basic window creation."""
    logger.info("=== Testing Basic Window Creation ===")

    try:
        root = tk.Tk()
        root.title("Basic Test")
        root.geometry("300x200+100+100")

        label = tk.Label(root, text="Basic window test\nPress any key to continue")
        label.pack(expand=True)

        def next_test(event=None):
            root.quit()

        root.bind("<Key>", next_test)
        root.focus_set()

        logger.info("Basic window created successfully")
        root.mainloop()
        root.destroy()
        return True

    except Exception as e:
        logger.error(f"Basic window test failed: {e}")
        return False


def test_frame_creation():
    """Test frame creation without overrideredirect."""
    logger.info("=== Testing Frame Creation ===")

    try:
        root = tk.Tk()
        root.title("Frame Test")
        root.geometry("400x300+150+150")

        # Create a frame similar to titlebar
        test_frame = tk.Frame(root, bg="#2d2d30", height=32, relief="flat")
        test_frame.pack(fill="x", side="top")
        test_frame.pack_propagate(False)

        # Add label to frame
        test_label = tk.Label(test_frame, text="Test Frame", bg="#2d2d30", fg="white")
        test_label.pack(side="left", padx=10, pady=6)

        # Add button to frame
        test_button = tk.Button(
            test_frame,
            text="×",
            command=root.quit,
            bg="#2d2d30",
            fg="white",
            relief="flat",
        )
        test_button.pack(side="right", padx=5, pady=2)

        # Content area
        content = tk.Label(root, text="Frame test successful\nClick × to continue")
        content.pack(expand=True)

        root.update_idletasks()
        frame_height = test_frame.winfo_height()
        logger.info(f"Frame created successfully: height={frame_height}")

        root.mainloop()
        root.destroy()
        return True

    except Exception as e:
        logger.error(f"Frame creation test failed: {e}")
        import traceback

        logger.error(traceback.format_exc())
        return False


def test_overrideredirect():
    """Test overrideredirect with custom titlebar."""
    logger.info("=== Testing Override Redirect ===")

    try:
        root = tk.Tk()
        root.title("Override Test")
        root.geometry("500x400+200+200")

        # Create titlebar FIRST
        logger.info("Creating titlebar before overrideredirect...")
        titlebar = tk.Frame(root, bg="#2d2d30", height=32, relief="flat")
        titlebar.pack(fill="x", side="top")
        titlebar.pack_propagate(False)

        # Add title
        title_label = tk.Label(
            titlebar,
            text="Custom Titlebar Test",
            bg="#2d2d30",
            fg="white",
            font=("Arial", 10, "bold"),
        )
        title_label.pack(side="left", padx=10, pady=6)

        # Add close button
        close_btn = tk.Button(
            titlebar,
            text="×",
            command=root.quit,
            bg="#2d2d30",
            fg="white",
            relief="flat",
            width=3,
        )
        close_btn.pack(side="right", padx=5, pady=2)

        # Content area
        content = tk.Label(
            root,
            text="Titlebar created\nNow testing overrideredirect...",
            font=("Arial", 12),
        )
        content.pack(expand=True)

        # Force update
        root.update_idletasks()
        root.update()

        initial_height = titlebar.winfo_height()
        logger.info(f"Titlebar height before overrideredirect: {initial_height}")

        if initial_height <= 1:
            raise Exception(
                f"Titlebar height invalid before overrideredirect: {initial_height}"
            )

        # Now remove decorations
        logger.info("Applying overrideredirect...")
        root.overrideredirect(True)

        # Force update again
        root.update_idletasks()
        root.update()

        final_height = titlebar.winfo_height()
        logger.info(f"Titlebar height after overrideredirect: {final_height}")

        if not titlebar.winfo_exists():
            raise Exception("Titlebar destroyed after overrideredirect")

        if final_height <= 1:
            raise Exception(
                f"Titlebar height invalid after overrideredirect: {final_height}"
            )

        # Update content
        content.configure(
            text="Override redirect successful!\nTitlebar should be visible\nClick × to close"
        )

        # Make draggable
        def start_drag(event):
            root.x = event.x
            root.y = event.y

        def drag_window(event):
            try:
                x = root.winfo_pointerx() - root.x
                y = root.winfo_pointery() - root.y
                root.geometry(f"+{x}+{y}")
            except:
                pass

        titlebar.bind("<Button-1>", start_drag)
        titlebar.bind("<B1-Motion>", drag_window)
        title_label.bind("<Button-1>", start_drag)
        title_label.bind("<B1-Motion>", drag_window)

        # Emergency exit
        root.bind("<Control-q>", lambda e: root.quit())
        root.bind("<Escape>", lambda e: root.quit())

        logger.info("Override redirect test setup complete")
        root.mainloop()
        root.destroy()
        return True

    except Exception as e:
        logger.error(f"Override redirect test failed: {e}")
        import traceback

        logger.error(traceback.format_exc())

        # Try to restore
        try:
            root.overrideredirect(False)
            root.mainloop()
            root.destroy()
        except:
            pass
        return False


def check_environment():
    """Check the environment for WSL and X server."""
    logger.info("=== Environment Check ===")

    logger.info(f"Platform: {sys.platform}")
    logger.info(f"Python: {sys.version}")
    logger.info(f"DISPLAY: {os.environ.get('DISPLAY', 'Not set')}")
    logger.info(f"WSL_DISTRO_NAME: {os.environ.get('WSL_DISTRO_NAME', 'Not set')}")

    # Check for WSL
    is_wsl = False
    try:
        if os.path.exists("/proc/version"):
            with open("/proc/version", "r") as f:
                version_info = f.read().lower()
                if "microsoft" in version_info or "wsl" in version_info:
                    is_wsl = True
                    logger.info("WSL detected")
    except:
        pass

    if not is_wsl:
        logger.info("WSL not detected")

    # Test X server
    try:
        import subprocess

        result = subprocess.run(["xset", "q"], capture_output=True, timeout=5)
        if result.returncode == 0:
            logger.info("X server connection successful")
        else:
            logger.warning("X server connection failed")
    except:
        logger.warning("Could not test X server (xset not available)")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Custom Titlebar Debug Script")
    print("=" * 60)

    check_environment()
    print()

    # Test 1: Basic window
    if not test_basic_window():
        logger.error("Basic window test failed - stopping")
        return 1

    print()

    # Test 2: Frame creation
    if not test_frame_creation():
        logger.error("Frame creation test failed - stopping")
        return 1

    print()

    # Test 3: Override redirect
    if not test_overrideredirect():
        logger.error("Override redirect test failed")
        return 1

    print()
    logger.info("All tests passed!")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
