#!/usr/bin/env python3
"""
Simple test script to verify the logging implementation works correctly.
"""

import io
import logging
import sys
import time
from contextlib import redirect_stderr, redirect_stdout

# Import the library
import threepanewindows
from threepanewindows.logging_config import get_logger


def test_silent_by_default():
    """Test that logging is silent by default."""
    print("Testing: Logging is silent by default...")

    # Capture stderr to check for any unwanted output
    stderr_capture = io.StringIO()

    with redirect_stderr(stderr_capture):
        # Get a logger and log some messages
        logger = get_logger("test_module")
        logger.debug("This debug message should be silent")
        logger.info("This info message should be silent")
        logger.warning("This warning message should be silent")
        logger.error("This error message should be silent")

    captured = stderr_capture.getvalue()

    if captured:
        print(f"❌ FAILED: Expected no output, but got: {captured}")
        return False
    else:
        print("✅ PASSED: No output when logging is not configured")
        return True


def test_enable_console_logging():
    """Test that console logging can be enabled."""
    print("\nTesting: Console logging can be enabled...")

    # Enable console logging
    threepanewindows.enable_console_logging(level=logging.INFO)

    # Capture both stdout and stderr to check for log output
    stderr_capture = io.StringIO()
    stdout_capture = io.StringIO()

    with redirect_stderr(stderr_capture), redirect_stdout(stdout_capture):
        logger = get_logger("test_module")
        logger.info("This info message should appear")
        logger.warning("This warning message should appear")
        logger.debug("This debug message should NOT appear (level too low)")

        # Force flush
        for handler in logging.getLogger("threepanewindows").handlers:
            if hasattr(handler, "flush"):
                handler.flush()

    captured = stderr_capture.getvalue() + stdout_capture.getvalue()

    # Check that we got the expected messages
    if (
        "This info message should appear" in captured
        and "This warning message should appear" in captured
    ):
        if "This debug message should NOT appear" not in captured:
            print("✅ PASSED: Console logging works correctly with level filtering")
            return True
        else:
            print("❌ FAILED: Debug message appeared when it shouldn't")
            return False
    else:
        print(f"❌ FAILED: Expected messages not found in output: '{captured}'")
        return False


def test_disable_logging():
    """Test that logging can be disabled."""
    print("\nTesting: Logging can be disabled...")

    # First enable logging
    threepanewindows.enable_console_logging(level=logging.INFO)

    # Then disable it
    threepanewindows.disable_logging()

    # Capture stderr to check for any output
    stderr_capture = io.StringIO()

    with redirect_stderr(stderr_capture):
        logger = get_logger("test_module")
        logger.info("This message should be silent after disable")
        logger.error("This error should also be silent")

    captured = stderr_capture.getvalue()

    if captured:
        print(f"❌ FAILED: Expected no output after disable, but got: {captured}")
        return False
    else:
        print("✅ PASSED: Logging successfully disabled")
        return True


def test_file_logging():
    """Test that file logging works."""
    print("\nTesting: File logging...")

    import os
    import tempfile

    # Create a temporary file for logging
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log") as f:
        log_file = f.name

    try:
        # Add file logging
        threepanewindows.add_file_logging(log_file, level=logging.DEBUG)

        # Log some messages
        logger = get_logger("test_module")
        logger.debug("Debug message to file")
        logger.info("Info message to file")
        logger.warning("Warning message to file")
        logger.error("Error message to file")

        # Force flush and close handlers
        main_logger = logging.getLogger("threepanewindows")
        for handler in main_logger.handlers[:]:
            if hasattr(handler, "flush"):
                handler.flush()
            if hasattr(handler, "close") and hasattr(handler, "stream"):
                handler.close()
                main_logger.removeHandler(handler)

        # Small delay to ensure file is written
        time.sleep(0.1)

        # Read the log file
        with open(log_file, "r") as f:
            content = f.read()

        # Check that all messages are present
        expected_messages = [
            "Debug message to file",
            "Info message to file",
            "Warning message to file",
            "Error message to file",
        ]

        all_present = all(msg in content for msg in expected_messages)

        if all_present:
            print("✅ PASSED: File logging works correctly")
            return True
        else:
            print(f"❌ FAILED: Not all messages found in log file. Content: {content}")
            return False

    except Exception as e:
        print(f"❌ FAILED: File logging test raised exception: {e}")
        return False
    finally:
        # Clean up - try multiple times if needed
        for _ in range(3):
            try:
                if os.path.exists(log_file):
                    os.unlink(log_file)
                break
            except OSError:
                time.sleep(0.1)
                continue


def test_logger_hierarchy():
    """Test that logger hierarchy works correctly."""
    print("\nTesting: Logger hierarchy...")

    # Enable console logging
    threepanewindows.enable_console_logging(level=logging.DEBUG)

    # Capture both stderr and stdout
    stderr_capture = io.StringIO()
    stdout_capture = io.StringIO()

    with redirect_stderr(stderr_capture), redirect_stdout(stdout_capture):
        # Test different module loggers
        enhanced_logger = get_logger("threepanewindows.enhanced_dockable")
        themes_logger = get_logger("threepanewindows.themes")
        utils_logger = get_logger("threepanewindows.utils.windows")

        enhanced_logger.info("Enhanced module message")
        themes_logger.info("Themes module message")
        utils_logger.info("Utils module message")

        # Force flush
        for handler in logging.getLogger("threepanewindows").handlers:
            if hasattr(handler, "flush"):
                handler.flush()

    captured = stderr_capture.getvalue() + stdout_capture.getvalue()

    # Check that all messages appear with correct logger names
    expected_loggers = [
        "threepanewindows.enhanced_dockable",
        "threepanewindows.themes",
        "threepanewindows.utils.windows",
    ]

    all_present = all(logger_name in captured for logger_name in expected_loggers)

    if all_present:
        print("✅ PASSED: Logger hierarchy works correctly")
        return True
    else:
        print(f"❌ FAILED: Not all logger names found. Content: '{captured}'")
        return False


def main():
    """Run all tests."""
    print("ThreePaneWindows Logging Implementation Test")
    print("=" * 50)

    tests = [
        test_silent_by_default,
        test_enable_console_logging,
        test_disable_logging,
        test_file_logging,
        test_logger_hierarchy,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ FAILED: {test.__name__} raised exception: {e}")

        # Reset logging state between tests
        threepanewindows.disable_logging()

    print(f"\nTest Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Logging implementation is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
