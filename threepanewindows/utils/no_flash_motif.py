"""
No-Flash X11 Motif Window Manager Hints Implementation

This module provides a way to apply Motif hints without visual flashing
by starting with the window withdrawn and only showing it after hints are applied.
"""

import logging
import tkinter as tk
from typing import Optional

from .x11_motif_hints import (
    _get_libx11,
    is_x11_available,
    logger,
    remove_window_decorations_immediate,
)


def setup_no_flash_custom_titlebar(window: tk.Tk) -> bool:
    """
    Setup custom titlebar without flashing by applying hints before first show.

    This approach:
    1. Ensures window starts withdrawn
    2. Waits for window to be ready
    3. Applies Motif hints while hidden
    4. Shows window only after hints are applied

    Args:
        window: The tkinter window

    Returns:
        bool: True if setup successful
    """
    try:
        if not is_x11_available():
            return False

        # Ensure window is withdrawn
        window.withdraw()

        # Schedule the no-flash process
        window.after_idle(lambda: _apply_hints_before_show(window))

        return True

    except Exception as e:
        logger.error(f"Failed to setup no-flash custom titlebar: {e}")
        return False


def _apply_hints_before_show(window: tk.Tk) -> None:
    """
    Apply Motif hints before showing the window to prevent flashing.
    """
    try:
        # Make sure window is ready but still hidden
        window.update_idletasks()

        # Brief show to create X11 structures, then immediately hide
        window.deiconify()
        window.update_idletasks()
        window.withdraw()
        window.update_idletasks()

        # Now apply Motif hints while hidden
        success = remove_window_decorations_immediate(window)

        # Show the window with hints applied
        window.deiconify()
        window.lift()
        window.focus_force()

        if success:
            logger.info("No-flash custom titlebar applied successfully")
        else:
            logger.warning("Motif hints application failed, showing window anyway")

    except Exception as e:
        logger.debug(f"No-flash process failed: {e}")
        # Fallback: just show the window
        try:
            window.deiconify()
        except:
            pass


def apply_hints_to_visible_window(window: tk.Tk) -> bool:
    """
    Apply Motif hints to an already visible window with minimal flashing.

    This uses a quick withdraw/deiconify cycle.
    """
    try:
        if not is_x11_available():
            return False

        # Save current state
        current_geometry = window.geometry()

        # Quick hide
        window.withdraw()
        window.update_idletasks()

        # Apply hints while hidden
        success = remove_window_decorations_immediate(window)

        # Show again
        window.deiconify()
        window.geometry(current_geometry)
        window.lift()
        window.focus_force()

        return success

    except Exception as e:
        logger.debug(f"Visible window Motif hints application failed: {e}")
        return False


# Test function
def test_no_flash_motif_hints():
    """Test the no-flash Motif hints functionality."""
    print("Testing No-Flash X11 Motif Window Manager Hints...")

    if not is_x11_available():
        print("❌ X11 not available")
        return

    print("✅ X11 available")

    # Create test window
    root = tk.Tk()
    root.title("No-Flash Motif Hints Test")
    root.geometry("500x300+200+200")

    # Add some content
    label = tk.Label(
        root,
        text="No-Flash Custom Titlebar Test\nShould appear without flashing!",
        font=("Arial", 14),
    )
    label.pack(pady=20)

    button = tk.Button(root, text="Close", command=root.destroy)
    button.pack(pady=10)

    # Setup no-flash custom titlebar
    setup_no_flash_custom_titlebar(root)

    print("🚀 Test window created - should appear without flashing")
    root.mainloop()


if __name__ == "__main__":
    test_no_flash_motif_hints()
