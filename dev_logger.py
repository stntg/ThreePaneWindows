#!/usr/bin/env python3
"""
Development Logger Driver for ThreePaneWindows.

This script provides an easy way to enable comprehensive logging during development
of the ThreePaneWindows library. It sets up multiple logging outputs and provides
utilities for debugging.

Usage:
    # Basic usage - enable console logging
    python dev_logger.py

    # Enable with specific log level
    python dev_logger.py --level DEBUG

    # Enable file logging
    python dev_logger.py --file logs/development.log

    # Enable both console and file logging
    python dev_logger.py --level DEBUG --file logs/development.log

    # Run with a specific example
    python dev_logger.py --example basic --level DEBUG

    # Interactive mode for testing
    python dev_logger.py --interactive
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add the package to the path for development
sys.path.insert(0, str(Path(__file__).parent))

from threepanewindows.logging_config import (
    DEBUG,
    INFO,
    add_file_logging,
    enable_console_logging,
    get_logger,
)


class DevelopmentLogger:
    """Development logging driver for ThreePaneWindows."""

    def __init__(self) -> None:
        """Initialize the development logger."""
        self.logger = get_logger(__name__)
        self.log_file: Optional[str] = None

    def setup_logging(
        self,
        console_level: int = INFO,
        file_path: Optional[str] = None,
        file_level: int = DEBUG,
    ) -> None:
        """
        Set up comprehensive logging for development.

        Args:
            console_level: Logging level for console output
            file_path: Optional path for log file
            file_level: Logging level for file output
        """
        print("🔧 Setting up ThreePaneWindows development logging...")

        # Enable console logging
        enable_console_logging(console_level)
        level_name = logging.getLevelName(console_level)
        print(f"✅ Console logging enabled at {level_name} level")

        # Enable file logging if requested
        if file_path:
            # Create directory if it doesn't exist
            log_dir = Path(file_path).parent
            log_dir.mkdir(parents=True, exist_ok=True)

            add_file_logging(file_path, file_level)
            self.log_file = file_path
            file_level_name = logging.getLevelName(file_level)
            print(f"✅ File logging enabled at {file_level_name} level: {file_path}")

        # Log initial setup information
        self.logger.info("=" * 60)
        self.logger.info("ThreePaneWindows Development Logging Started")
        self.logger.info(f"Timestamp: {datetime.now().isoformat()}")
        self.logger.info(f"Library Version: {threepanewindows.__version__}")
        self.logger.info(f"Python Version: {sys.version}")
        self.logger.info(f"Console Level: {logging.getLevelName(console_level)}")
        if file_path:
            self.logger.info(f"File Level: {logging.getLevelName(file_level)}")
            self.logger.info(f"Log File: {file_path}")
        self.logger.info("=" * 60)

    def test_logging_levels(self) -> None:
        """Test all logging levels to verify setup."""
        print("\n🧪 Testing logging levels...")

        test_logger = get_logger("threepanewindows.test")

        # Use simple text to avoid Unicode issues on Windows
        test_logger.debug("DEBUG: This is a debug message")
        test_logger.info("INFO: This is an info message")
        test_logger.warning("WARNING: This is a warning message")
        test_logger.error("ERROR: This is an error message")
        test_logger.critical("CRITICAL: This is a critical message")

        print("✅ Logging level test completed")

    def run_example(self, example_name: str) -> None:
        """
        Run a specific example with logging enabled.

        Args:
            example_name: Name of the example to run
        """
        print(f"\n🚀 Running example: {example_name}")

        try:
            if example_name == "basic":
                self._run_basic_example()
            elif example_name == "dockable":
                self._run_dockable_example()
            elif example_name == "enhanced":
                self._run_enhanced_example()
            else:
                print(f"❌ Unknown example: {example_name}")
                print("Available examples: basic, dockable, enhanced")

        except Exception as e:
            self.logger.error(f"Example failed: {e}", exc_info=True)
            print(f"❌ Example failed: {e}")

    def _run_basic_example(self) -> None:
        """Run basic ThreePaneWindow example."""
        import tkinter as tk

        from threepanewindows import FixedThreePaneWindow

        logger = get_logger("threepanewindows.example.basic")
        logger.info("Starting basic example")

        root = tk.Tk()
        root.title("Basic ThreePaneWindow - Development Logging")
        root.geometry("800x600")

        logger.debug("Creating FixedThreePaneWindow")
        window = FixedThreePaneWindow(root)
        window.pack(fill=tk.BOTH, expand=True)

        # Add some content
        logger.debug("Adding content to panes")
        tk.Label(
            window.left_pane, text="Left Pane\n(Logging Enabled)", bg="lightblue"
        ).pack(fill=tk.BOTH, expand=True)
        tk.Label(
            window.center_pane, text="Center Pane\n(Check Console/Log)", bg="lightgreen"
        ).pack(fill=tk.BOTH, expand=True)
        tk.Label(
            window.right_pane, text="Right Pane\n(Development Mode)", bg="lightcoral"
        ).pack(fill=tk.BOTH, expand=True)

        logger.info("Basic example window created successfully")
        print("✅ Basic example window created. Close the window to continue.")

        root.mainloop()
        logger.info("Basic example completed")

    def _run_dockable_example(self) -> None:
        """Run dockable ThreePaneWindow example."""
        import tkinter as tk

        from threepanewindows import DockableThreePaneWindow

        logger = get_logger("threepanewindows.example.dockable")
        logger.info("Starting dockable example")

        root = tk.Tk()
        root.title("Dockable ThreePaneWindow - Development Logging")
        root.geometry("900x700")

        logger.debug("Creating DockableThreePaneWindow")
        window = DockableThreePaneWindow(root)
        window.pack(fill=tk.BOTH, expand=True)

        # Add some content
        logger.debug("Adding content to dockable panes")
        tk.Label(window.left_pane, text="Left Pane\n(Dockable)", bg="lightblue").pack(
            fill=tk.BOTH, expand=True
        )
        tk.Label(
            window.center_pane,
            text="Center Pane\n(Try dragging panes)",
            bg="lightgreen",
        ).pack(fill=tk.BOTH, expand=True)
        tk.Label(
            window.right_pane, text="Right Pane\n(Logging Active)", bg="lightcoral"
        ).pack(fill=tk.BOTH, expand=True)

        logger.info("Dockable example window created successfully")
        print(
            "✅ Dockable example window created. Try dragging panes! Close to continue."
        )

        root.mainloop()
        logger.info("Dockable example completed")

    def _run_enhanced_example(self) -> None:
        """Run enhanced ThreePaneWindow example."""
        import tkinter as tk

        from threepanewindows import EnhancedDockableThreePaneWindow

        logger = get_logger("threepanewindows.example.enhanced")
        logger.info("Starting enhanced example")

        root = tk.Tk()
        root.title("Enhanced ThreePaneWindow - Development Logging")
        root.geometry("1000x800")

        logger.debug("Creating EnhancedDockableThreePaneWindow")
        window = EnhancedDockableThreePaneWindow(root)
        window.pack(fill=tk.BOTH, expand=True)

        # Add some content
        logger.debug("Adding content to enhanced panes")
        tk.Label(
            window.left_pane, text="Left Pane\n(Enhanced Features)", bg="lightblue"
        ).pack(fill=tk.BOTH, expand=True)
        tk.Label(
            window.center_pane, text="Center Pane\n(Full Logging)", bg="lightgreen"
        ).pack(fill=tk.BOTH, expand=True)
        tk.Label(
            window.right_pane, text="Right Pane\n(Development)", bg="lightcoral"
        ).pack(fill=tk.BOTH, expand=True)

        logger.info("Enhanced example window created successfully")
        print(
            "✅ Enhanced example window created. "
            "Explore all features! Close to continue."
        )

        root.mainloop()
        logger.info("Enhanced example completed")

    def interactive_mode(self) -> None:
        """Run interactive mode for testing and debugging."""
        print("\n🔄 Entering interactive mode...")
        print("You can now import and test ThreePaneWindows components.")
        print("Logging is enabled - check console and log file for messages.")
        print("Type 'exit()' or Ctrl+C to quit.\n")

        # Make common imports available
        import tkinter as tk

        from threepanewindows import (
            DockableThreePaneWindow,
            EnhancedDockableThreePaneWindow,
            FixedThreePaneWindow,
            ThemeManager,
        )

        # Create a simple test function
        def create_test_window(window_type="fixed"):
            """Create a test window for interactive testing."""
            root = tk.Tk()
            root.title(f"Test Window - {window_type}")
            root.geometry("800x600")

            if window_type == "fixed":
                window = FixedThreePaneWindow(root)
            elif window_type == "dockable":
                window = DockableThreePaneWindow(root)
            elif window_type == "enhanced":
                window = EnhancedDockableThreePaneWindow(root)
            else:
                raise ValueError(f"Unknown window type: {window_type}")

            window.pack(fill=tk.BOTH, expand=True)

            # Add labels
            tk.Label(window.left_pane, text="Left", bg="lightblue").pack(
                fill=tk.BOTH, expand=True
            )
            tk.Label(window.center_pane, text="Center", bg="lightgreen").pack(
                fill=tk.BOTH, expand=True
            )
            tk.Label(window.right_pane, text="Right", bg="lightcoral").pack(
                fill=tk.BOTH, expand=True
            )

            return root, window

        # Add to local namespace for interactive use
        locals().update(
            {
                "tk": tk,
                "FixedThreePaneWindow": FixedThreePaneWindow,
                "DockableThreePaneWindow": DockableThreePaneWindow,
                "EnhancedDockableThreePaneWindow": EnhancedDockableThreePaneWindow,
                "ThemeManager": ThemeManager,
                "create_test_window": create_test_window,
                "logger": get_logger("threepanewindows.interactive"),
            }
        )

        try:
            import code

            code.interact(local=locals())
        except KeyboardInterrupt:
            print("\n👋 Exiting interactive mode...")

    def show_log_file(self) -> None:
        """Show the contents of the log file if it exists."""
        if not self.log_file or not os.path.exists(self.log_file):
            print("❌ No log file available")
            return

        print(f"\n📄 Log file contents ({self.log_file}):")
        print("=" * 60)
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                print(f.read())
        except Exception as e:
            print(f"❌ Error reading log file: {e}")
        print("=" * 60)


def main():
    """Run the development logger main entry point."""
    parser = argparse.ArgumentParser(
        description="Development Logger Driver for ThreePaneWindows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dev_logger.py                           # Basic console logging
  python dev_logger.py --level DEBUG            # Debug level console logging
  python dev_logger.py --file logs/dev.log      # Console + file logging
  python dev_logger.py --example basic          # Run basic example with logging
  python dev_logger.py --interactive            # Interactive mode
        """,
    )

    parser.add_argument(
        "--level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Console logging level (default: INFO)",
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Enable file logging to specified path",
    )

    parser.add_argument(
        "--file-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="DEBUG",
        help="File logging level (default: DEBUG)",
    )

    parser.add_argument(
        "--example",
        choices=["basic", "dockable", "enhanced"],
        help="Run a specific example with logging enabled",
    )

    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Enter interactive mode for testing",
    )

    parser.add_argument(
        "--test-levels",
        action="store_true",
        help="Test all logging levels",
    )

    parser.add_argument(
        "--show-log",
        action="store_true",
        help="Show log file contents (if file logging is enabled)",
    )

    args = parser.parse_args()

    # Convert level strings to logging constants
    console_level = getattr(logging, args.level)
    file_level = getattr(logging, args.file_level)

    # Create development logger
    dev_logger = DevelopmentLogger()

    # Set up logging
    dev_logger.setup_logging(
        console_level=console_level,
        file_path=args.file,
        file_level=file_level,
    )

    # Test logging levels if requested
    if args.test_levels:
        dev_logger.test_logging_levels()

    # Run example if specified
    if args.example:
        dev_logger.run_example(args.example)

    # Enter interactive mode if requested
    if args.interactive:
        dev_logger.interactive_mode()

    # Show log file if requested
    if args.show_log:
        dev_logger.show_log_file()

    # If no specific action was requested, just show that logging is enabled
    if not any([args.example, args.interactive, args.test_levels, args.show_log]):
        print("\n✅ Development logging is now enabled!")
        print("Import threepanewindows in your code and logging will be active.")
        print("Use --help to see available options.")

        # Show a quick example of how to use logging
        print("\n📝 Quick example:")
        print("  from threepanewindows.logging_config import get_logger")
        print("  logger = get_logger(__name__)")
        print("  logger.info('Your message here')")


if __name__ == "__main__":
    main()
