#!/usr/bin/env python3
"""
Utility functions for proper window sizing and positioning.
"""

import tkinter as tk
from typing import Tuple


def get_safe_window_size(root: tk.Tk, preferred_width: int = 1000, preferred_height: int = 650) -> Tuple[int, int]:
    """
    Calculate a safe window size that fits on screen with proper margins.
    
    Args:
        root: The tkinter root window
        preferred_width: Preferred window width
        preferred_height: Preferred window height
    
    Returns:
        Tuple of (width, height) that will fit safely on screen
    """
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Reserve space for taskbar and window decorations
    taskbar_height = 60  # Typical taskbar height
    titlebar_height = 30  # Window title bar
    border_margin = 20   # Margin from screen edges
    
    # Calculate available space
    available_width = screen_width - (border_margin * 2)
    available_height = screen_height - taskbar_height - titlebar_height - (border_margin * 2)
    
    # Use preferred size but constrain to available space
    safe_width = min(preferred_width, available_width)
    safe_height = min(preferred_height, available_height)
    
    # Ensure minimum usable size
    safe_width = max(800, safe_width)
    safe_height = max(500, safe_height)
    
    return safe_width, safe_height


def center_window(root: tk.Tk, width: int, height: int) -> None:
    """
    Center a window on screen with safe positioning.
    
    Args:
        root: The tkinter root window
        width: Window width
        height: Window height
    """
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate center position
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Ensure window stays on screen with margins
    margin = 20
    taskbar_height = 60
    
    x = max(margin, min(x, screen_width - width - margin))
    y = max(margin, min(y, screen_height - height - taskbar_height - margin))
    
    root.geometry(f"{width}x{height}+{x}+{y}")


def setup_window_geometry(root: tk.Tk, title: str, preferred_width: int = 1000, 
                         preferred_height: int = 650, min_width: int = 800, 
                         min_height: int = 500) -> None:
    """
    Setup window with proper title, size, and positioning.
    
    Args:
        root: The tkinter root window
        title: Window title
        preferred_width: Preferred window width
        preferred_height: Preferred window height
        min_width: Minimum window width
        min_height: Minimum window height
    """
    root.title(title)
    
    # Get safe window size
    width, height = get_safe_window_size(root, preferred_width, preferred_height)
    
    # Set minimum size
    root.minsize(min_width, min_height)
    
    # Center and size the window
    center_window(root, width, height)
    
    # Make sure window is visible
    root.update_idletasks()


def print_window_info(root: tk.Tk) -> None:
    """Print window and screen information for debugging."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    root.update_idletasks()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    window_x = root.winfo_x()
    window_y = root.winfo_y()
    
    print(f"Screen: {screen_width}x{screen_height}")
    print(f"Window: {window_width}x{window_height} at ({window_x}, {window_y})")
    print(f"Window bottom: {window_y + window_height} (screen height: {screen_height})")
    
    if window_y + window_height > screen_height - 60:
        print("WARNING: Window may be behind taskbar!")
    if window_y < 0:
        print("WARNING: Window title bar may be off screen!")


if __name__ == "__main__":
    # Test the utility functions
    root = tk.Tk()
    setup_window_geometry(root, "Test Window", 1000, 650)
    
    tk.Label(root, text="Test Window\nProper sizing and positioning", 
             font=("Arial", 16), justify="center").pack(expand=True)
    
    print_window_info(root)
    
    root.mainloop()