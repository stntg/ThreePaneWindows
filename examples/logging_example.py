#!/usr/bin/env python3
"""
Example demonstrating how to enable logging in ThreePaneWindows.

This example shows different ways to configure logging for the ThreePaneWindows
library, from basic console output to advanced file logging with custom formatting.
"""

import logging
import tkinter as tk
from pathlib import Path

# Import ThreePaneWindows components
import threepanewindows
from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig


def example_1_basic_console_logging():
    """Example 1: Enable basic console logging."""
    print("=== Example 1: Basic Console Logging ===")

    # Enable console logging for the entire library
    threepanewindows.enable_console_logging(level=logging.INFO)

    # Create a simple window - you'll now see log messages
    root = tk.Tk()
    root.title("ThreePaneWindows - Basic Logging Example")

    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=PaneConfig(title="Left Panel", width=200),
        center_config=PaneConfig(title="Center Panel"),
        right_config=PaneConfig(title="Right Panel", width=200),
    )
    window.pack(fill=tk.BOTH, expand=True)

    # Add some content
    tk.Label(window.left_pane, text="Left Content").pack(pady=20)
    tk.Label(window.center_pane, text="Center Content").pack(pady=20)
    tk.Label(window.right_pane, text="Right Content").pack(pady=20)

    # Try switching themes - you'll see log messages
    window.switch_theme("dark")

    print("Check your console - you should see ThreePaneWindows log messages!")
    print("Close the window to continue to the next example.\n")

    root.mainloop()


def example_2_custom_console_logging():
    """Example 2: Custom console logging with specific logger."""
    print("=== Example 2: Custom Console Logging ===")

    # Get the ThreePaneWindows logger directly
    logger = logging.getLogger("threepanewindows")

    # Create custom handler with detailed formatting
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    )
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    # Add handler to logger
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = True

    # Create window
    root = tk.Tk()
    root.title("ThreePaneWindows - Custom Logging Example")

    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=PaneConfig(title="Debug Panel", width=250, detachable=True),
        center_config=PaneConfig(title="Main Panel"),
        right_config=PaneConfig(title="Info Panel", width=250, detachable=True),
    )
    window.pack(fill=tk.BOTH, expand=True)

    # Add content that will generate log messages
    tk.Label(window.left_pane, text="Try detaching this panel!").pack(pady=20)
    tk.Label(window.center_pane, text="Switch themes to see debug logs").pack(pady=20)
    tk.Label(window.right_pane, text="Detach me too!").pack(pady=20)

    print(
        "This example shows detailed debug logging with function names and line numbers."
    )
    print("Try detaching panels and switching themes to see detailed logs.\n")

    root.mainloop()


def example_3_file_logging():
    """Example 3: File logging with rotation."""
    print("=== Example 3: File Logging ===")

    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "threepanewindows.log"

    # Add file logging
    threepanewindows.add_file_logging(str(log_file), level=logging.DEBUG)

    # Also enable console logging for immediate feedback
    threepanewindows.enable_console_logging(level=logging.INFO)

    # Create window
    root = tk.Tk()
    root.title("ThreePaneWindows - File Logging Example")

    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=PaneConfig(title="File Logger", width=200, detachable=True),
        center_config=PaneConfig(title="Main Content"),
        right_config=PaneConfig(title="Actions", width=200, detachable=True),
    )
    window.pack(fill=tk.BOTH, expand=True)

    # Add interactive content
    tk.Label(window.left_pane, text="All actions are\nlogged to file!").pack(pady=20)

    # Center panel with theme switcher
    center_frame = tk.Frame(window.center_pane)
    center_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    tk.Label(center_frame, text="Theme Switcher", font=("Arial", 14, "bold")).pack(
        pady=10
    )

    themes = ["light", "dark", "blue", "green", "purple"]
    for theme in themes:
        btn = tk.Button(
            center_frame,
            text=f"Switch to {theme.title()}",
            command=lambda t=theme: window.switch_theme(t),
        )
        btn.pack(pady=5)

    # Right panel with actions
    actions_frame = tk.Frame(window.right_pane)
    actions_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    tk.Label(actions_frame, text="Actions", font=("Arial", 12, "bold")).pack(pady=10)

    def show_log_file():
        """Show the log file content."""
        if log_file.exists():
            with open(log_file, "r") as f:
                content = f.read()

            # Create a new window to show log content
            log_window = tk.Toplevel(root)
            log_window.title("Log File Content")
            log_window.geometry("800x600")

            text_widget = tk.Text(log_window, wrap=tk.WORD)
            scrollbar = tk.Scrollbar(
                log_window, orient=tk.VERTICAL, command=text_widget.yview
            )
            text_widget.configure(yscrollcommand=scrollbar.set)

            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            text_widget.insert(tk.END, content)
            text_widget.config(state=tk.DISABLED)

    tk.Button(actions_frame, text="Show Log File", command=show_log_file).pack(pady=5)

    print(f"Logging to file: {log_file}")
    print(
        "Try switching themes and detaching panels, then click 'Show Log File' to see the logs."
    )
    print("Close the window to continue.\n")

    root.mainloop()


def example_4_selective_logging():
    """Example 4: Selective logging for specific modules."""
    print("=== Example 4: Selective Module Logging ===")

    # Enable logging only for specific modules
    enhanced_logger = logging.getLogger("threepanewindows.enhanced_dockable")
    themes_logger = logging.getLogger("threepanewindows.themes")

    # Create handler
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    # Configure specific loggers
    enhanced_logger.addHandler(handler)
    enhanced_logger.setLevel(logging.DEBUG)
    enhanced_logger.propagate = False

    themes_logger.addHandler(handler)
    themes_logger.setLevel(logging.INFO)
    themes_logger.propagate = False

    # Create window
    root = tk.Tk()
    root.title("ThreePaneWindows - Selective Logging Example")

    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=PaneConfig(title="Enhanced Only", width=200),
        center_config=PaneConfig(title="Main Panel"),
        right_config=PaneConfig(title="Themes Only", width=200),
    )
    window.pack(fill=tk.BOTH, expand=True)

    tk.Label(window.left_pane, text="Enhanced module\nlogging only").pack(pady=20)
    tk.Label(window.center_pane, text="Selective logging example").pack(pady=20)
    tk.Label(window.right_pane, text="Themes module\nlogging only").pack(pady=20)

    print("This example only logs messages from enhanced_dockable and themes modules.")
    print("Other modules (like utils) won't show log messages.\n")

    root.mainloop()


def example_5_disable_logging():
    """Example 5: Disable logging completely."""
    print("=== Example 5: Disable Logging ===")

    # First enable logging to show it works
    threepanewindows.enable_console_logging(level=logging.INFO)

    root = tk.Tk()
    root.title("ThreePaneWindows - Disable Logging Example")

    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=PaneConfig(title="Before Disable", width=200),
        center_config=PaneConfig(title="Control Panel"),
        right_config=PaneConfig(title="After Disable", width=200),
    )
    window.pack(fill=tk.BOTH, expand=True)

    # Control panel
    control_frame = tk.Frame(window.center_pane)
    control_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    tk.Label(control_frame, text="Logging Control", font=("Arial", 14, "bold")).pack(
        pady=10
    )

    def disable_logging():
        threepanewindows.disable_logging()
        status_label.config(text="Logging DISABLED - no more log messages!")

    def enable_logging():
        threepanewindows.enable_console_logging(level=logging.INFO)
        status_label.config(text="Logging ENABLED - you'll see log messages again!")

    tk.Button(control_frame, text="Disable Logging", command=disable_logging).pack(
        pady=5
    )
    tk.Button(control_frame, text="Enable Logging", command=enable_logging).pack(pady=5)

    # Test action
    tk.Button(
        control_frame,
        text="Switch Theme (Test Logging)",
        command=lambda: window.switch_theme("dark"),
    ).pack(pady=10)

    status_label = tk.Label(
        control_frame,
        text="Logging is currently ENABLED",
        fg="green",
        font=("Arial", 10, "bold"),
    )
    status_label.pack(pady=10)

    tk.Label(window.left_pane, text="Logging enabled\n(you see messages)").pack(pady=20)
    tk.Label(window.right_pane, text="Logging disabled\n(no messages)").pack(pady=20)

    print("Use the buttons to enable/disable logging and test with theme switching.")

    root.mainloop()


def main():
    """Run all logging examples."""
    print("ThreePaneWindows Logging Examples")
    print("=" * 50)
    print()
    print("This script demonstrates various ways to configure logging")
    print("for the ThreePaneWindows library.")
    print()

    examples = [
        example_1_basic_console_logging,
        example_2_custom_console_logging,
        example_3_file_logging,
        example_4_selective_logging,
        example_5_disable_logging,
    ]

    for i, example in enumerate(examples, 1):
        print(f"Running Example {i}...")
        try:
            example()
        except KeyboardInterrupt:
            print("Example interrupted by user.")
            break
        except Exception as e:
            print(f"Example {i} failed: {e}")

        # Reset logging state between examples
        threepanewindows.disable_logging()
        print()

    print("All examples completed!")


if __name__ == "__main__":
    main()
