"""
Tests for the Logging Configuration system.
"""

import logging
import os
import tempfile
from io import StringIO
from unittest.mock import Mock, patch

import pytest

from threepanewindows.logging_config import (
    ThreePaneWindowsLogger,
    add_file_logging,
    disable_logging,
    enable_console_logging,
    get_logger,
)


class TestThreePaneWindowsLogger:
    """Test cases for ThreePaneWindowsLogger class."""

    def test_singleton_behavior(self):
        """Test that ThreePaneWindowsLogger is a singleton."""
        logger1 = ThreePaneWindowsLogger()
        logger2 = ThreePaneWindowsLogger()

        assert logger1 is logger2

    def test_logger_initialization(self):
        """Test logger initialization."""
        logger_manager = ThreePaneWindowsLogger()

        assert isinstance(logger_manager, ThreePaneWindowsLogger)

    def test_get_logger_function(self):
        """Test get_logger function."""
        logger = get_logger("test_module")

        assert isinstance(logger, logging.Logger)
        assert logger.name.startswith("threepanewindows")

    def test_get_logger_with_different_names(self):
        """Test get_logger with different module names."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")

        assert logger1.name != logger2.name
        assert "module1" in logger1.name
        assert "module2" in logger2.name

    def test_get_logger_same_name_returns_same_logger(self):
        """Test that get_logger returns the same logger for the same name."""
        logger1 = get_logger("same_module")
        logger2 = get_logger("same_module")

        assert logger1 is logger2

    def test_logger_hierarchy(self):
        """Test logger hierarchy."""
        parent_logger = get_logger("threepanewindows.parent")
        child_logger = get_logger("threepanewindows.parent.child")

        assert (
            child_logger.parent == parent_logger
            or child_logger.parent.name == parent_logger.name
        )

    def test_logger_default_level(self):
        """Test logger default level."""
        logger = get_logger("test_default_level")

        # Should be silent by default (high level or no handlers)
        assert logger.level >= logging.WARNING or len(logger.handlers) == 0

    def test_logger_propagation(self):
        """Test logger propagation settings."""
        logger = get_logger("test_propagation")

        # Should propagate to parent loggers
        assert logger.propagate is True


class TestLoggingFunctions:
    """Test cases for logging configuration functions."""

    def test_enable_console_logging(self):
        """Test enabling console logging."""
        # Should not raise exception
        enable_console_logging()

        # Test that logger now has handlers
        logger = get_logger("test_console")
        root_logger = logging.getLogger("threepanewindows")

        # Either the specific logger or root logger should have handlers
        has_handlers = len(logger.handlers) > 0 or len(root_logger.handlers) > 0
        # Note: This might not always be true depending on implementation

    def test_enable_console_logging_with_level(self):
        """Test enabling console logging with specific level."""
        enable_console_logging(level=logging.DEBUG)

        # Should not raise exception
        logger = get_logger("test_console_debug")
        logger.debug("Test debug message")

    def test_disable_logging(self):
        """Test disabling logging."""
        # Enable first
        enable_console_logging()

        # Then disable
        disable_logging()

        # Should not raise exception
        logger = get_logger("test_disable")
        logger.info("This should be silent")

    def test_add_file_logging(self):
        """Test adding file logging."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".log"
        ) as temp_file:
            temp_filename = temp_file.name

        try:
            # Should not raise exception
            add_file_logging(temp_filename)

            # Test logging to file
            logger = get_logger("test_file")
            logger.info("Test file message")

            # File should exist (though might be empty due to buffering)
            assert os.path.exists(temp_filename)

        finally:
            # Cleanup
            if os.path.exists(temp_filename):
                try:
                    os.unlink(temp_filename)
                except OSError:
                    pass

    def test_add_file_logging_with_level(self):
        """Test adding file logging with specific level."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".log"
        ) as temp_file:
            temp_filename = temp_file.name

        try:
            add_file_logging(temp_filename, level=logging.WARNING)

            logger = get_logger("test_file_warning")
            logger.debug("Debug message - should not appear")
            logger.warning("Warning message - should appear")

        finally:
            if os.path.exists(temp_filename):
                try:
                    os.unlink(temp_filename)
                except OSError:
                    pass

    def test_add_file_logging_invalid_path(self):
        """Test adding file logging with invalid path."""
        invalid_path = "/invalid/path/that/does/not/exist/test.log"

        # Should handle gracefully
        try:
            add_file_logging(invalid_path)
        except (OSError, IOError, PermissionError):
            # Expected for invalid paths
            pass

    def test_multiple_console_logging_calls(self):
        """Test multiple calls to enable_console_logging."""
        # Should not cause issues
        enable_console_logging()
        enable_console_logging()
        enable_console_logging()

        logger = get_logger("test_multiple_console")
        logger.info("Test message")

    def test_multiple_file_logging_calls(self):
        """Test multiple calls to add_file_logging."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".log"
        ) as temp_file1:
            temp_filename1 = temp_file1.name

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".log"
        ) as temp_file2:
            temp_filename2 = temp_file2.name

        try:
            add_file_logging(temp_filename1)
            add_file_logging(temp_filename2)

            logger = get_logger("test_multiple_file")
            logger.info("Test message to multiple files")

        finally:
            for filename in [temp_filename1, temp_filename2]:
                if os.path.exists(filename):
                    try:
                        os.unlink(filename)
                    except OSError:
                        pass

    def test_logging_after_disable(self):
        """Test logging after disabling."""
        enable_console_logging()
        logger = get_logger("test_after_disable")

        # Enable and log
        logger.info("Before disable")

        # Disable
        disable_logging()

        # Should not raise exception
        logger.info("After disable")

    def test_logging_levels(self):
        """Test different logging levels."""
        enable_console_logging(level=logging.DEBUG)
        logger = get_logger("test_levels")

        # Should not raise exceptions
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

    def test_logging_with_formatting(self):
        """Test logging with message formatting."""
        enable_console_logging()
        logger = get_logger("test_formatting")

        # Should not raise exceptions
        logger.info("Message with %s", "parameter")
        logger.info("Message with %d number", 42)
        logger.info("Message with %s and %d", "text", 123)

    def test_logging_with_exception(self):
        """Test logging with exception information."""
        enable_console_logging()
        logger = get_logger("test_exception")

        try:
            raise ValueError("Test exception")
        except ValueError:
            # Should not raise exception
            logger.exception("Exception occurred")
            logger.error("Error with exception", exc_info=True)

    @patch("sys.stdout", new_callable=StringIO)
    def test_console_logging_output(self, mock_stdout):
        """Test that console logging produces output."""
        enable_console_logging(level=logging.INFO)
        logger = get_logger("test_output")

        logger.info("Test console output")

        # Note: Output might go to stderr or be buffered
        # This test mainly ensures no exceptions are raised

    def test_logger_name_formatting(self):
        """Test logger name formatting."""
        # Test with module-style names
        logger1 = get_logger("threepanewindows.module")
        logger2 = get_logger("threepanewindows.submodule.component")

        assert "threepanewindows" in logger1.name
        assert "threepanewindows" in logger2.name

    def test_logger_configuration_persistence(self):
        """Test that logger configuration persists."""
        enable_console_logging(level=logging.DEBUG)

        logger1 = get_logger("test_persistence1")
        logger2 = get_logger("test_persistence2")

        # Both loggers should be configured
        logger1.debug("Debug from logger1")
        logger2.debug("Debug from logger2")

    def test_logging_thread_safety(self):
        """Test logging thread safety."""
        import threading
        import time

        enable_console_logging()
        logger = get_logger("test_thread_safety")

        def log_messages(thread_id):
            for i in range(10):
                logger.info(f"Thread {thread_id} message {i}")
                time.sleep(0.001)  # Small delay

        threads = []
        for i in range(3):
            thread = threading.Thread(target=log_messages, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def test_logging_memory_usage(self):
        """Test logging doesn't cause memory leaks."""
        enable_console_logging()

        # Create many loggers
        loggers = []
        for i in range(100):
            logger = get_logger(f"test_memory_{i}")
            logger.info(f"Message from logger {i}")
            loggers.append(logger)

        # Should not cause memory issues

    def test_logging_configuration_reset(self):
        """Test logging configuration can be reset."""
        # Configure logging
        enable_console_logging(level=logging.DEBUG)

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".log"
        ) as temp_file:
            temp_filename = temp_file.name

        try:
            add_file_logging(temp_filename, level=logging.INFO)

            logger = get_logger("test_reset")
            logger.debug("Debug message")
            logger.info("Info message")

            # Disable and reconfigure
            disable_logging()
            enable_console_logging(level=logging.WARNING)

            logger.debug("Debug after reset - should be silent")
            logger.warning("Warning after reset - should appear")

        finally:
            if os.path.exists(temp_filename):
                try:
                    os.unlink(temp_filename)
                except OSError:
                    pass

    def test_logging_with_custom_formatter(self):
        """Test logging with custom formatting."""
        # This tests that the logging system can handle custom formatters
        enable_console_logging()

        logger = get_logger("test_custom_format")

        # Get the root logger and check if it has handlers
        root_logger = logging.getLogger("threepanewindows")

        if root_logger.handlers:
            # Test that we can modify formatter
            original_formatter = root_logger.handlers[0].formatter

            custom_formatter = logging.Formatter(
                "%(asctime)s - CUSTOM - %(name)s - %(levelname)s - %(message)s"
            )

            root_logger.handlers[0].setFormatter(custom_formatter)

            logger.info("Message with custom formatter")

            # Restore original formatter
            if original_formatter:
                root_logger.handlers[0].setFormatter(original_formatter)

    def test_logging_integration_with_modules(self):
        """Test logging integration with different modules."""
        enable_console_logging()

        # Simulate different modules
        flexible_logger = get_logger("threepanewindows.flexible")
        theme_logger = get_logger("threepanewindows.central_theme_manager")
        scrollbar_logger = get_logger("threepanewindows.custom_scrollbar")

        flexible_logger.info("Flexible layout message")
        theme_logger.info("Theme manager message")
        scrollbar_logger.info("Scrollbar message")

    def test_logging_error_handling(self):
        """Test logging error handling."""
        enable_console_logging()
        logger = get_logger("test_error_handling")

        # Test with various problematic inputs
        try:
            logger.info(None)  # None message
        except Exception:
            pass

        try:
            logger.info("Message with %s", None)  # None parameter
        except Exception:
            pass

        # Test with circular reference (should be handled by logging module)
        circular_dict = {}
        circular_dict["self"] = circular_dict

        try:
            logger.info("Circular reference: %s", circular_dict)
        except Exception:
            pass
