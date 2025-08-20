"""
X11 Motif Window Manager Hints for Linux Custom Titlebar

This module provides a way to remove window decorations on Linux while
maintaining taskbar integration, using X11 Motif Window Manager Hints
instead of overrideredirect(True).

Based on the approach from:
- https://github.com/EDCD/EDMarketConnector/blob/main/theme.py
- https://www.tonyobryan.com//index.php?article=9
"""

import ctypes
import logging
import tkinter as tk
from typing import Optional

logger = logging.getLogger(__name__)

# X11 Types
CHAR = ctypes.c_char
BOOL = ctypes.c_bool
INT = ctypes.c_int
LONG = ctypes.c_long
ULONG = ctypes.c_ulong
PTR = ctypes.c_void_p
ATOM = LONG
WINDOW = LONG
DISPLAY = PTR
CHAR_PTR = ctypes.POINTER(CHAR)


class HINTS(ctypes.Structure):
    """Motif Window Manager Hints structure."""

    _fields_ = [
        ("flags", ULONG),
        ("functions", ULONG),
        ("decorations", ULONG),
        ("inputMode", LONG),
        ("status", ULONG),
    ]


HINTS_PTR = ctypes.POINTER(HINTS)

# Constants
PropModeReplace = 0
XA_ATOM = 4

# Global X11 library reference
_libx11 = None


def _get_libx11():
    """Get X11 library, loading it if necessary."""
    global _libx11
    if _libx11 is None:
        try:
            _libx11 = ctypes.cdll.LoadLibrary("libX11.so.6")
            _setup_x11_functions()
        except OSError as e:
            logger.error(f"Failed to load libX11.so.6: {e}")
            return None
    return _libx11


def _setup_x11_functions():
    """Setup X11 function signatures."""
    global _libx11

    # XInternAtom
    _libx11.XInternAtom.argtypes = (PTR, CHAR_PTR, BOOL)
    _libx11.XInternAtom.restype = ATOM

    # XOpenDisplay
    _libx11.XOpenDisplay.argtypes = (CHAR_PTR,)
    _libx11.XOpenDisplay.restype = DISPLAY

    # XChangeProperty
    _libx11.XChangeProperty.argtypes = (
        DISPLAY,
        WINDOW,
        ATOM,
        ATOM,
        INT,
        INT,
        HINTS_PTR,
        INT,
    )
    _libx11.XChangeProperty.restype = INT

    # XFlush
    _libx11.XFlush.argtypes = (DISPLAY,)
    _libx11.XFlush.restype = INT

    # XCloseDisplay
    _libx11.XCloseDisplay.argtypes = (DISPLAY,)
    _libx11.XCloseDisplay.restype = INT

    # XQueryTree
    _libx11.XQueryTree.argtypes = (
        DISPLAY,
        WINDOW,
        ctypes.POINTER(WINDOW),
        ctypes.POINTER(WINDOW),
        ctypes.POINTER(ctypes.POINTER(WINDOW)),
        ctypes.POINTER(ctypes.c_uint),
    )
    _libx11.XQueryTree.restype = INT

    # XSync
    _libx11.XSync.argtypes = (DISPLAY, BOOL)
    _libx11.XSync.restype = INT


def string_to_c(data: str) -> CHAR_PTR:
    """Convert Python string to C string."""
    return ctypes.create_string_buffer(data.encode())


def get_parent_window(display: DISPLAY, window_id: int) -> Optional[WINDOW]:
    """Get the parent window of a given window."""
    try:
        parent = WINDOW()
        root = WINDOW()
        children = ctypes.POINTER(WINDOW)()
        num_children = ctypes.c_uint()

        result = _libx11.XQueryTree(
            display,
            window_id,
            ctypes.byref(root),
            ctypes.byref(parent),
            ctypes.byref(children),
            ctypes.byref(num_children),
        )

        if result:
            return parent
        return None
    except Exception as e:
        logger.error(f"Failed to get parent window: {e}")
        return None


def remove_window_decorations(window: tk.Tk) -> bool:
    """
    Remove window decorations using X11 Motif Window Manager Hints.

    This approach maintains taskbar integration while removing the titlebar,
    unlike overrideredirect(True) which breaks taskbar integration.

    Args:
        window: The tkinter window to modify

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        libx11 = _get_libx11()
        if libx11 is None:
            logger.warning("X11 library not available")
            return False

        # Wait for window to be mapped
        window.update_idletasks()
        if not window.winfo_ismapped():
            window.deiconify()
            window.update_idletasks()

        # Open X11 display
        display = libx11.XOpenDisplay(None)
        if not display:
            logger.error("Failed to open X11 display")
            return False

        try:
            # Get the window ID and find its parent (the window manager frame)
            window_id = window.winfo_id()
            parent_window = get_parent_window(display, window_id)

            if not parent_window:
                logger.error("Failed to get parent window")
                return False

            # Get the Motif WM hints atom
            motif_hints_atom = libx11.XInternAtom(
                display, string_to_c("_MOTIF_WM_HINTS"), False
            )

            if not motif_hints_atom:
                logger.error("Failed to get _MOTIF_WM_HINTS atom")
                return False

            # Create hints structure
            hints = HINTS()
            hints.flags = 2  # MWM_HINTS_DECORATIONS
            hints.decorations = 0  # No decorations

            # Apply the hints to remove decorations
            result = libx11.XChangeProperty(
                display,
                parent_window,
                motif_hints_atom,
                XA_ATOM,
                32,
                PropModeReplace,
                ctypes.byref(hints),
                5,
            )

            if result:
                # Flush changes
                libx11.XFlush(display)
                logger.info("Successfully removed window decorations using Motif hints")
                return True
            else:
                logger.error("Failed to change window property")
                return False

        finally:
            # Clean up
            libx11.XCloseDisplay(display)

    except Exception as e:
        logger.error(f"Failed to remove window decorations: {e}")
        return False


def setup_aggressive_decoration_removal(window: tk.Tk) -> bool:
    """
    Setup aggressive decoration removal with off-screen processing.

    This moves the window off-screen, applies Motif hints, refreshes,
    then moves it back to prevent visual flashing.
    """
    try:
        libx11 = _get_libx11()
        if libx11 is None:
            return False

        def wait_and_remove_offscreen():
            """Wait for window to be mapped and then remove decorations off-screen."""
            try:
                # Wait for window to be mapped
                def wait_for_mapped():
                    if window.winfo_ismapped():
                        # Window is mapped, now process off-screen
                        process_window_offscreen(window)
                    else:
                        # Not mapped yet, check again soon
                        window.after(1, wait_for_mapped)

                wait_for_mapped()

            except Exception as e:
                logger.debug(f"Wait and remove failed: {e}")

        # Start the waiting process
        window.after_idle(wait_and_remove_offscreen)

        return True

    except Exception as e:
        logger.error(f"Failed to setup aggressive decoration removal: {e}")
        return False


def process_window_offscreen(window: tk.Tk) -> None:
    """
    Process window decorations off-screen to prevent visual flashing.

    1. Save current position
    2. Move window off-screen
    3. Apply Motif hints
    4. Refresh window
    5. Move window back to original position
    """
    try:
        # Save current geometry
        current_geometry = window.geometry()

        # Parse geometry to get position
        import re

        match = re.match(r"(\d+)x(\d+)\+(-?\d+)\+(-?\d+)", current_geometry)
        if match:
            width, height, x, y = match.groups()
            original_x, original_y = int(x), int(y)
        else:
            # Fallback if geometry parsing fails
            original_x, original_y = 100, 100

        # Move window far off-screen (negative coordinates)
        window.geometry(f"{width}x{height}+-5000+-5000")
        window.update_idletasks()

        # Apply Motif hints while off-screen
        success = remove_window_decorations_immediate(window)

        if success:
            # Give the window manager time to process the change
            window.after(
                10, lambda: _restore_window_position(window, original_x, original_y)
            )
        else:
            # If Motif hints failed, just restore position
            window.geometry(f"{width}x{height}+{original_x}+{original_y}")

    except Exception as e:
        logger.debug(f"Off-screen processing failed: {e}")
        # Fallback to immediate processing
        remove_window_decorations_immediate(window)


def _restore_window_position(window: tk.Tk, x: int, y: int) -> None:
    """Restore window to its original position after off-screen processing."""
    try:
        # Get current size
        current_geometry = window.geometry()
        import re

        match = re.match(r"(\d+)x(\d+)", current_geometry)
        if match:
            width, height = match.groups()
            # Move back to original position
            window.geometry(f"{width}x{height}+{x}+{y}")

            # Force focus and bring to front
            window.deiconify()
            window.lift()
            window.focus_force()

            logger.debug(f"Window restored to position {x},{y}")

    except Exception as e:
        logger.debug(f"Position restoration failed: {e}")


def remove_window_decorations_immediate(window: tk.Tk) -> bool:
    """
    Remove window decorations immediately without waiting or retrying.

    This is called when we know the window is ready.
    """
    try:
        libx11 = _get_libx11()
        if libx11 is None:
            return False

        # Open X11 display
        display = libx11.XOpenDisplay(None)
        if not display:
            return False

        try:
            # Get the window ID and find its parent (the window manager frame)
            window_id = window.winfo_id()
            parent_window = get_parent_window(display, window_id)

            if not parent_window:
                return False

            # Get the Motif WM hints atom
            motif_hints_atom = libx11.XInternAtom(
                display, string_to_c("_MOTIF_WM_HINTS"), False
            )

            if not motif_hints_atom:
                return False

            # Create hints structure
            hints = HINTS()
            hints.flags = 2  # MWM_HINTS_DECORATIONS
            hints.decorations = 0  # No decorations

            # Apply the hints to remove decorations
            result = libx11.XChangeProperty(
                display,
                parent_window,
                motif_hints_atom,
                XA_ATOM,
                32,
                PropModeReplace,
                ctypes.byref(hints),
                5,
            )

            if result:
                # Flush changes immediately
                libx11.XFlush(display)
                logger.info(
                    "Successfully removed window decorations using Motif hints (immediate)"
                )
                return True

            return False

        finally:
            # Clean up
            libx11.XCloseDisplay(display)

    except Exception as e:
        logger.debug(f"Immediate decoration removal failed: {e}")
        return False


def _force_window_refresh(window: tk.Tk) -> None:
    """
    Force the window manager to refresh and process the Motif hints change.

    This uses several techniques to nudge the window manager into updating
    the window decorations without requiring user interaction.
    """
    try:
        # Method 1: Force a geometry update
        current_geometry = window.geometry()
        window.geometry(current_geometry)

        # Method 2: Withdraw and deiconify (most effective)
        window.withdraw()
        window.after(1, lambda: window.deiconify())

        # Method 3: Force updates
        window.update_idletasks()
        window.update()

        # Method 4: Focus manipulation to trigger window manager attention
        window.after(10, lambda: _trigger_focus_refresh(window))

    except Exception as e:
        logger.debug(f"Window refresh failed: {e}")


def _trigger_focus_refresh(window: tk.Tk) -> None:
    """Trigger focus-based refresh to force window manager update."""
    try:
        # Save current focus state
        try:
            current_focus = window.focus_get()
        except:
            current_focus = None

        # Brief focus manipulation
        window.focus_force()
        window.after(1, lambda: _restore_focus(window, current_focus))

    except Exception as e:
        logger.debug(f"Focus refresh failed: {e}")


def _restore_focus(window: tk.Tk, previous_focus) -> None:
    """Restore previous focus state."""
    try:
        if previous_focus and previous_focus.winfo_exists():
            previous_focus.focus_set()
        else:
            window.focus_set()
    except Exception:
        pass  # Focus restoration is not critical


def _force_x11_refresh(window: tk.Tk) -> None:
    """Force X11-level window refresh to trigger window manager update."""
    try:
        libx11 = _get_libx11()
        if libx11 is None:
            return

        # Open a new display connection for this operation
        display = libx11.XOpenDisplay(None)
        if not display:
            return

        try:
            window_id = window.winfo_id()
            parent_window = get_parent_window(display, window_id)

            if parent_window:
                # Force a sync to make sure all changes are processed
                libx11.XSync(display, False)
                libx11.XFlush(display)

        finally:
            libx11.XCloseDisplay(display)

    except Exception as e:
        logger.debug(f"X11 refresh failed: {e}")


def is_x11_available() -> bool:
    """Check if X11 is available on this system."""
    try:
        libx11 = _get_libx11()
        return libx11 is not None
    except Exception:
        return False


# Test function
def test_motif_hints():
    """Test the Motif hints functionality."""
    print("Testing X11 Motif Window Manager Hints...")

    if not is_x11_available():
        print("❌ X11 not available")
        return

    print("✅ X11 available")

    # Create test window
    root = tk.Tk()
    root.title("Motif Hints Test")
    root.geometry("400x300")

    # Add some content
    label = tk.Label(
        root, text="Testing Motif Hints\nCustom Titlebar", font=("Arial", 14)
    )
    label.pack(pady=20)

    button = tk.Button(root, text="Close", command=root.destroy)
    button.pack(pady=10)

    # Remove decorations
    root.after(100, lambda: remove_window_decorations(root))

    print(
        "🚀 Test window created - check if titlebar is removed but taskbar integration works"
    )
    root.mainloop()


if __name__ == "__main__":
    test_motif_hints()
