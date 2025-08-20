"""
Off-Screen X11 Motif Window Manager Hints Implementation

This module applies Motif hints completely off-screen and then moves the window
to its final position, eliminating all visual flashing.
"""

import logging
import re
import tkinter as tk
from typing import Tuple

from .x11_motif_hints import (
    _get_libx11,
    is_x11_available,
    logger,
    remove_window_decorations_immediate,
)


def setup_offscreen_custom_titlebar(window: tk.Tk, target_geometry: str = None) -> bool:
    """
    Setup custom titlebar completely off-screen, then move to final position.

    This approach:
    1. Positions window far off-screen (e.g., -10000, -10000)
    2. Shows window off-screen to create X11 structures
    3. Applies Motif hints while off-screen
    4. Moves window to final position

    Args:
        window: The tkinter window
        target_geometry: Final geometry (if None, uses current geometry)

    Returns:
        bool: True if setup successful
    """
    try:
        if not is_x11_available():
            return False

        # Get target geometry
        if target_geometry is None:
            target_geometry = window.geometry()

        # Parse target geometry to get final position and size
        final_width, final_height, final_x, final_y = _parse_geometry(target_geometry)

        # Position window far off-screen
        offscreen_geometry = f"{final_width}x{final_height}+-10000+-10000"
        window.geometry(offscreen_geometry)

        # Show window off-screen
        window.deiconify()
        window.update_idletasks()
        window.update()

        # Apply Motif hints while off-screen
        success = remove_window_decorations_immediate(window)

        # Move to final position
        final_geometry = f"{final_width}x{final_height}+{final_x}+{final_y}"
        window.geometry(final_geometry)

        # Bring to front
        window.lift()
        window.focus_force()

        if success:
            logger.info(
                f"Off-screen custom titlebar applied successfully, moved to {final_x},{final_y}"
            )
        else:
            logger.warning(
                "Motif hints application failed, but window positioned correctly"
            )

        return success

    except Exception as e:
        logger.error(f"Failed to setup off-screen custom titlebar: {e}")
        return False


def apply_offscreen_hints_to_existing_window(window: tk.Tk) -> bool:
    """
    Apply Motif hints to an existing window using off-screen processing.

    This saves the current position, moves off-screen, applies hints, then restores position.
    """
    try:
        if not is_x11_available():
            return False

        # Save current geometry
        current_geometry = window.geometry()
        width, height, x, y = _parse_geometry(current_geometry)

        # Move off-screen
        offscreen_geometry = f"{width}x{height}+-10000+-10000"
        window.geometry(offscreen_geometry)
        window.update_idletasks()

        # Apply hints while off-screen
        success = remove_window_decorations_immediate(window)

        # Move back to original position
        window.geometry(current_geometry)
        window.lift()
        window.focus_force()

        if success:
            logger.info("Off-screen Motif hints applied to existing window")

        return success

    except Exception as e:
        logger.debug(f"Off-screen Motif hints application failed: {e}")
        return False


def _parse_geometry(geometry: str) -> Tuple[int, int, int, int]:
    """
    Parse tkinter geometry string into width, height, x, y.

    Args:
        geometry: Geometry string like "800x600+100+50"

    Returns:
        Tuple of (width, height, x, y)
    """
    try:
        # Match pattern like "800x600+100+50" or "800x600-100-50"
        match = re.match(r"(\d+)x(\d+)([-+]\d+)([-+]\d+)", geometry)
        if match:
            width = int(match.group(1))
            height = int(match.group(2))
            x = int(match.group(3))
            y = int(match.group(4))
            return width, height, x, y
        else:
            # Fallback values
            return 800, 600, 100, 100
    except Exception:
        # Fallback values
        return 800, 600, 100, 100


# Test function
def test_offscreen_motif_hints():
    """Test the off-screen Motif hints functionality."""
    print("Testing Off-Screen X11 Motif Window Manager Hints...")

    if not is_x11_available():
        print("❌ X11 not available")
        return

    print("✅ X11 available")

    # Create test window
    root = tk.Tk()
    root.title("Off-Screen Motif Hints Test")

    # Start withdrawn to prevent any initial flash
    root.withdraw()

    # Add some content
    label = tk.Label(
        root,
        text="Off-Screen Custom Titlebar Test\nShould appear instantly without flashing!",
        font=("Arial", 14),
        bg="lightblue",
        pady=20,
    )
    label.pack(fill="both", expand=True)

    button = tk.Button(root, text="Close", command=root.destroy, font=("Arial", 12))
    button.pack(pady=10)

    # Setup off-screen custom titlebar with specific target position
    target_geometry = "600x400+300+200"
    setup_offscreen_custom_titlebar(root, target_geometry)

    print(
        "🚀 Test window created - should appear instantly at final position without any flashing"
    )
    root.mainloop()


if __name__ == "__main__":
    test_offscreen_motif_hints()
