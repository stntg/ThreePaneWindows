#!/usr/bin/env python3
"""
Example: Using ThreePaneWindows with Development Logging.

This example demonstrates how to use the development logging system
while working with ThreePaneWindows components.

Run this script to see logging in action!
"""

import tkinter as tk

# Method 1: Quick setup (automatic logging)
from threepanewindows import FixedThreePaneWindow
from threepanewindows.logging_config import get_logger

# Method 2: Manual setup (uncomment to use instead)
# from threepanewindows.logging_config import enable_console_logging, DEBUG
# enable_console_logging(DEBUG)


# Get a logger for this module
logger = get_logger(__name__)


def create_sample_application():
    """Create a sample application with logging."""
    logger.info("Starting sample application creation")

    # Create main window
    logger.debug("Creating main Tkinter window")
    root = tk.Tk()
    root.title("ThreePaneWindows - Development Logging Example")
    root.geometry("800x600")

    # Create the three-pane window
    logger.debug("Creating FixedThreePaneWindow")
    try:
        window = FixedThreePaneWindow(root)
        logger.info("FixedThreePaneWindow created successfully")
    except Exception as e:
        logger.error(f"Failed to create FixedThreePaneWindow: {e}", exc_info=True)
        return None, None

    # Pack the window
    logger.debug("Packing three-pane window")
    window.pack(fill=tk.BOTH, expand=True)

    # Add content to panes
    logger.debug("Adding content to left pane")
    left_frame = tk.Frame(window.left_pane, bg="lightblue")
    left_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    tk.Label(
        left_frame, text="Left Pane", font=("Arial", 14, "bold"), bg="lightblue"
    ).pack(pady=10)
    tk.Label(left_frame, text="Development logging is active!", bg="lightblue").pack()
    tk.Label(
        left_frame, text="Check your console for log messages", bg="lightblue"
    ).pack()

    logger.debug("Adding content to center pane")
    center_frame = tk.Frame(window.center_pane, bg="lightgreen")
    center_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    tk.Label(
        center_frame, text="Center Pane", font=("Arial", 14, "bold"), bg="lightgreen"
    ).pack(pady=10)

    # Add a button that logs when clicked
    def on_button_click():
        logger.info("Button clicked in center pane")
        logger.debug("Button click event handled")

    button = tk.Button(
        center_frame, text="Click me (logs to console)", command=on_button_click
    )
    button.pack(pady=10)

    logger.debug("Adding content to right pane")
    right_frame = tk.Frame(window.right_pane, bg="lightcoral")
    right_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    tk.Label(
        right_frame, text="Right Pane", font=("Arial", 14, "bold"), bg="lightcoral"
    ).pack(pady=10)
    tk.Label(right_frame, text="All operations are logged", bg="lightcoral").pack()

    # Add some interactive elements
    logger.debug("Adding interactive elements")

    def on_entry_change(event):
        logger.debug(f"Entry text changed: {event.widget.get()}")

    entry = tk.Entry(right_frame)
    entry.pack(pady=5)
    entry.bind("<KeyRelease>", on_entry_change)

    tk.Label(
        right_frame,
        text="Type above to see debug logs",
        bg="lightcoral",
        font=("Arial", 8),
    ).pack()

    logger.info("Sample application created successfully")
    return root, window


def main():
    """Run the main example function."""
    logger.info("=" * 50)
    logger.info("ThreePaneWindows Development Logging Example")
    logger.info("=" * 50)

    # Create the application
    root, window = create_sample_application()

    if root is None:
        logger.error("Failed to create application")
        return

    # Set up window close handler
    def on_closing():
        logger.info("Application closing")
        logger.debug("Destroying main window")
        root.destroy()
        logger.info("Application closed successfully")

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Show instructions
    print("\n" + "=" * 60)
    print("🚀 ThreePaneWindows Development Logging Example")
    print("=" * 60)
    print("📋 Instructions:")
    print("  • Watch the console for log messages")
    print("  • Click the button in the center pane")
    print("  • Type in the text field in the right pane")
    print("  • Close the window when done")
    print("📁 Log files are saved in the logs/ directory")
    print("=" * 60)

    logger.info("Starting main event loop")

    # Run the application
    try:
        root.mainloop()
    except KeyboardInterrupt:
        logger.warning("Application interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}", exc_info=True)

    logger.info("Example completed")


if __name__ == "__main__":
    main()
