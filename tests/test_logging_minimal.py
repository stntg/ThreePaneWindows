"""
Minimal tests for the Logging Configuration system.
Only includes tests that work reliably in all environments.
"""

import logging

import pytest

from threepanewindows.logging_config import (
    ThreePaneWindowsLogger,
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

    def test_multiple_logger_creation(self):
        """Test creating multiple loggers."""
        loggers = []
        for i in range(5):  # Reduced number
            logger = get_logger(f"test_multiple_{i}")
            loggers.append(logger)

        # All should be different loggers
        assert len(set(loggers)) == 5
