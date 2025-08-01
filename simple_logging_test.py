#!/usr/bin/env python3
"""
Simple manual test to verify logging works.
"""

import threepanewindows
from threepanewindows.logging_config import get_logger


def test_basic_functionality():
    """Test basic logging functionality manually."""
    print("=== Testing ThreePaneWindows Logging ===\n")

    print("1. Testing silent by default...")
    logger = get_logger("test_module")
    logger.info("This should be silent")
    logger.warning("This should also be silent")
    print("   (You should see no log messages above)\n")

    print("2. Enabling console logging...")
    threepanewindows.enable_console_logging()
    logger.info("This should now appear in console")
    logger.warning("This warning should also appear")
    print("   (You should see log messages above)\n")

    print("3. Testing different modules...")
    enhanced_logger = get_logger("threepanewindows.enhanced_dockable")
    themes_logger = get_logger("threepanewindows.themes")

    enhanced_logger.info("Message from enhanced_dockable module")
    themes_logger.warning("Warning from themes module")
    print("   (You should see messages with different module names)\n")

    print("4. Disabling logging...")
    threepanewindows.disable_logging()
    logger.info("This should be silent again")
    logger.error("Even errors should be silent")
    print("   (You should see no log messages above)\n")

    print("5. Testing file logging...")
    import os
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
        log_file = f.name

    try:
        threepanewindows.add_file_logging(log_file)
        logger.info("This goes to file")
        logger.warning("This warning also goes to file")

        # Force flush
        import logging

        for handler in logging.getLogger("threepanewindows").handlers:
            if hasattr(handler, "flush"):
                handler.flush()

        # Read and display file content
        with open(log_file, "r") as f:
            content = f.read()

        print(f"   Log file content:\n{content}")

    finally:
        # Clean up
        try:
            os.unlink(log_file)
        except (OSError, FileNotFoundError):  # nosec B110
            pass

    print("=== Test Complete ===")
    print("If you saw log messages when expected and silence when expected,")
    print("then the logging implementation is working correctly!")


if __name__ == "__main__":
    test_basic_functionality()
