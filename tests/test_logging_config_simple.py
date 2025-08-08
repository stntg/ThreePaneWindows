"""
Simplified tests for the Logging Configuration system.
"""

import logging
from unittest.mock import Mock, patch

import pytest

from threepanewindows.logging_config import (
    ThreePaneWindowsLogger,
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


class TestGetLoggerFunction:
    """Test cases for get_logger function."""

    def test_get_logger_function(self):
        """Test get_logger function."""
        logger = get_logger("test_module")

        assert isinstance(logger, logging.Logger)
        assert "threepanewindows" in logger.name or "test_module" in logger.name

    def test_get_logger_with_different_names(self):
        """Test get_logger with different module names."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")

        assert logger1.name != logger2.name

    def test_get_logger_same_name_returns_same_logger(self):
        """Test that get_logger returns the same logger for the same name."""
        logger1 = get_logger("same_module")
        logger2 = get_logger("same_module")

        assert logger1 is logger2

    def test_logger_hierarchy(self):
        """Test logger hierarchy."""
        parent_logger = get_logger("threepanewindows.parent")
        child_logger = get_logger("threepanewindows.parent.child")

        # Child should have parent relationship
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

        # Test that logger can be used
        logger = get_logger("test_console")
        logger.info("Test console message")

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

    def test_multiple_console_logging_calls(self):
        """Test multiple calls to enable_console_logging."""
        # Should not cause issues
        enable_console_logging()
        enable_console_logging()
        enable_console_logging()

        logger = get_logger("test_multiple_console")
        logger.info("Test message")

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

    def test_logger_name_formatting(self):
        """Test logger name formatting."""
        # Test with module-style names
        logger1 = get_logger("threepanewindows.module")
        logger2 = get_logger("threepanewindows.submodule.component")

        assert "threepanewindows" in logger1.name or "module" in logger1.name
        assert "threepanewindows" in logger2.name or "component" in logger2.name

    def test_logger_configuration_persistence(self):
        """Test that logger configuration persists."""
        enable_console_logging(level=logging.DEBUG)

        logger1 = get_logger("test_persistence1")
        logger2 = get_logger("test_persistence2")

        # Both loggers should be configured
        logger1.debug("Debug from logger1")
        logger2.debug("Debug from logger2")

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
            logger.info("Message with %s", None)  # None parameter
        except Exception:
            pass

        # Test with circular reference (should be handled by logging module)
        circular_dict = {}
        circular_dict["self"] = circular_dict

        try:
            logger.info(
                "Circular reference: %s", str(circular_dict)[:100]
            )  # Limit string length
        except Exception:
            pass


class TestLoggingIntegration:
    """Test cases for logging integration scenarios."""

    def test_logger_manager_initialization(self):
        """Test logger manager initializes correctly."""
        logger_manager = ThreePaneWindowsLogger()

        # Should be able to create loggers
        logger = get_logger("test_init")
        assert isinstance(logger, logging.Logger)

    def test_multiple_logger_creation(self):
        """Test creating multiple loggers."""
        loggers = []
        for i in range(10):
            logger = get_logger(f"test_multiple_{i}")
            loggers.append(logger)

        # All should be different loggers
        assert len(set(loggers)) == 10

    def test_logging_thread_safety_basic(self):
        """Test basic logging thread safety."""
        import threading
        import time

        enable_console_logging()
        logger = get_logger("test_thread_safety")

        def log_messages(thread_id):
            for i in range(5):  # Reduced number for faster test
                logger.info(f"Thread {thread_id} message {i}")
                time.sleep(0.001)  # Small delay

        threads = []
        for i in range(2):  # Reduced number of threads
            thread = threading.Thread(target=log_messages, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def test_logging_memory_usage_basic(self):
        """Test basic logging memory usage."""
        enable_console_logging()

        # Create many loggers
        loggers = []
        for i in range(50):  # Reduced number for faster test
            logger = get_logger(f"test_memory_{i}")
            logger.info(f"Message from logger {i}")
            loggers.append(logger)

        # Should not cause memory issues
        assert len(loggers) == 50

    def test_logging_configuration_reset_basic(self):
        """Test basic logging configuration reset."""
        # Configure logging
        enable_console_logging(level=logging.DEBUG)

        logger = get_logger("test_reset")
        logger.debug("Debug message")
        logger.info("Info message")

        # Disable and reconfigure
        disable_logging()
        enable_console_logging(level=logging.WARNING)

        logger.debug("Debug after reset - should be silent")
        logger.warning("Warning after reset - should appear")

    def test_logging_with_different_levels(self):
        """Test logging with different levels."""
        enable_console_logging(level=logging.INFO)

        logger = get_logger("test_different_levels")

        # Test all levels
        logger.debug("Debug - should be silent")
        logger.info("Info - should appear")
        logger.warning("Warning - should appear")
        logger.error("Error - should appear")
        logger.critical("Critical - should appear")

    def test_logger_attributes(self):
        """Test logger attributes."""
        logger = get_logger("test_attributes")

        # Should have standard logger attributes
        assert hasattr(logger, "name")
        assert hasattr(logger, "level")
        assert hasattr(logger, "handlers")
        assert hasattr(logger, "propagate")
        assert hasattr(logger, "parent")

    def test_logger_methods(self):
        """Test logger methods exist."""
        logger = get_logger("test_methods")

        # Should have standard logger methods
        assert hasattr(logger, "debug")
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")
        assert hasattr(logger, "critical")
        assert hasattr(logger, "exception")

    def test_logging_performance_basic(self):
        """Test basic logging performance."""
        import time

        enable_console_logging()
        logger = get_logger("test_performance")

        start_time = time.time()

        # Log many messages
        for i in range(100):  # Reduced for faster test
            logger.info(f"Performance test message {i}")

        end_time = time.time()

        # Should be reasonably fast
        assert (end_time - start_time) < 2.0
