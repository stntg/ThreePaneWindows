"""
Seamless X11 Motif Window Manager Hints Implementation

This module provides a seamless way to apply Motif hints without any visual flashing
by coordinating the window creation, hint application, and display process.
"""

import logging
import tkinter as tk
from typing import Callable, Optional

from .x11_motif_hints import (
    _get_libx11,
    is_x11_available,
    logger,
    remove_window_decorations_immediate,
)


def setup_seamless_custom_titlebar(
    window: tk.Tk,
    target_geometry: str = "1400x900+100+100",
    on_ready_callback: Optional[Callable] = None,
) -> bool:
    """
    Setup custom titlebar with seamless Motif hints application.

    This approach:
    1. Keeps window withdrawn initially
    2. Applies Motif hints while hidden
    3. Shows window in final position without flashing

    Args:
        window: The tkinter window
        target_geometry: Final geometry string (e.g., "1400x900+100+100")
        on_ready_callback: Optional callback when window is ready

    Returns:
        bool: True if setup successful
    """
    try:
        if not is_x11_available():
            return False

        # Ensure window starts withdrawn
        window.withdraw()

        # Set target geometry while hidden
        window.geometry(target_geometry)
        window.update_idletasks()

        # Schedule the seamless reveal process
        window.after_idle(lambda: _seamless_reveal_process(window, on_ready_callback))

        return True

    except Exception as e:
        logger.error(f"Failed to setup seamless custom titlebar: {e}")
        return False


def _seamless_reveal_process(
    window: tk.Tk, on_ready_callback: Optional[Callable] = None
) -> None:
    """
    Execute the seamless reveal process:
    1. Show window briefly to create X11 structures
    2. Hide it immediately
    3. Apply Motif hints
    4. Show window in final position
    """
    try:
        # Step 1: Briefly show window to create X11 window structures
        window.deiconify()
        window.update_idletasks()

        # Step 2: Hide it immediately (before user can see it)
        window.withdraw()
        window.update_idletasks()

        # Step 3: Apply Motif hints while hidden
        success = remove_window_decorations_immediate(window)

        if success:
            # Step 4: Show window in final position after a brief delay
            window.after(5, lambda: _final_reveal(window, on_ready_callback))
        else:
            # If Motif hints failed, just show the window normally
            window.deiconify()
            if on_ready_callback:
                on_ready_callback()

    except Exception as e:
        logger.debug(f"Seamless reveal process failed: {e}")
        # Fallback: just show the window
        window.deiconify()
        if on_ready_callback:
            on_ready_callback()


def _final_reveal(window: tk.Tk, on_ready_callback: Optional[Callable] = None) -> None:
    """Final reveal of the window with custom titlebar applied."""
    try:
        # Show the window
        window.deiconify()
        window.lift()
        window.focus_force()

        # Call ready callback if provided
        if on_ready_callback:
            on_ready_callback()

        logger.info("Seamless custom titlebar reveal completed")

    except Exception as e:
        logger.debug(f"Final reveal failed: {e}")


def apply_motif_hints_to_existing_window(window: tk.Tk) -> bool:
    """
    Apply Motif hints to an already visible window with minimal flashing.

    This is a fallback for windows that are already shown.
    """
    try:
        if not is_x11_available():
            return False

        # Save current state
        current_geometry = window.geometry()
        was_focused = window.focus_get() == window

        # Quick hide/show cycle
        window.withdraw()
        window.update_idletasks()

        # Apply hints while hidden
        success = remove_window_decorations_immediate(window)

        # Restore window
        window.deiconify()
        window.geometry(current_geometry)

        if was_focused:
            window.focus_force()

        return success

    except Exception as e:
        logger.debug(f"Existing window Motif hints application failed: {e}")
        return False


# Test function
def test_seamless_motif_hints():
    """Test the seamless Motif hints functionality."""
    print("Testing Seamless X11 Motif Window Manager Hints...")

    if not is_x11_available():
        print("❌ X11 not available")
        return

    print("✅ X11 available")

    def on_window_ready():
        print("🎉 Window ready with custom titlebar!")

    # Create test window
    root = tk.Tk()
    root.title("Seamless Motif Hints Test")

    # Add some content
    label = tk.Label(
        root, text="Seamless Custom Titlebar Test\nNo flashing!", font=("Arial", 14)
    )
    label.pack(pady=20)

    button = tk.Button(root, text="Close", command=root.destroy)
    button.pack(pady=10)

    # Setup seamless custom titlebar
    setup_seamless_custom_titlebar(root, "500x300+200+200", on_window_ready)

    print("🚀 Test window created - should appear seamlessly without flashing")
    root.mainloop()


if __name__ == "__main__":
    test_seamless_motif_hints()
