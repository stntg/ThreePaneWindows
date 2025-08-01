"""
Logging configuration for ThreePaneWindows library.

This module provides a centralized logging system that remains silent by default
unless developers using the library explicitly configure handlers for the
'threepanewindows' logger.

Usage for library developers:
    from .logging_config import get_logger
    logger = get_logger(__name__)
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")

Usage for library users (to enable logging):
    import logging
    import threepanewindows

    # Enable all threepanewindows logging to console
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('threepanewindows')
    logger.setLevel(logging.DEBUG)

    # Or create custom handler
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(handler)
"""

import logging
from typing import Optional


class ThreePaneWindowsLogger:
    """
    Singleton logger manager for ThreePaneWindows library.

    This ensures consistent logging configuration across the entire library
    while remaining silent by default unless explicitly configured by users.
    """

    _instance: Optional["ThreePaneWindowsLogger"] = None
    _initialized: bool = False

    def __new__(cls) -> "ThreePaneWindowsLogger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            self._setup_logging()
            self._initialized = True

    def _setup_logging(self) -> None:
        """Initialize the logging configuration."""
        # Create the main logger for the library
        self.main_logger = logging.getLogger("threepanewindows")

        # Set to DEBUG level - handlers will control what actually gets output
        self.main_logger.setLevel(logging.DEBUG)

        # Prevent propagation to root logger by default
        # This ensures the library stays silent unless explicitly configured
        self.main_logger.propagate = False

        # Add a NullHandler to prevent "No handlers found" warnings
        # This is the recommended practice for libraries
        if not self.main_logger.handlers:
            self.main_logger.addHandler(logging.NullHandler())

    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a logger for a specific module.

        Args:
            name: Usually __name__ from the calling module

        Returns:
            Logger instance configured for the module
        """
        # Create child logger under the main threepanewindows logger
        if name.startswith("threepanewindows."):
            logger_name = name
        else:
            # Handle cases where __name__ might not include the package name
            module_name = name.split(".")[-1] if "." in name else name
            logger_name = f"threepanewindows.{module_name}"

        return logging.getLogger(logger_name)

    def enable_console_logging(self, level: int = logging.INFO) -> None:
        """
        Convenience method to enable console logging for the library.

        Args:
            level: Logging level (logging.DEBUG, logging.INFO, etc.)
        """
        # Remove NullHandler if present
        for handler in self.main_logger.handlers[:]:
            if isinstance(handler, logging.NullHandler):
                self.main_logger.removeHandler(handler)

        # Add console handler if not already present
        has_console_handler = any(
            isinstance(h, logging.StreamHandler) and h.stream.name == "<stderr>"
            for h in self.main_logger.handlers
        )

        if not has_console_handler:
            console_handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(formatter)
            console_handler.setLevel(level)
            self.main_logger.addHandler(console_handler)

        self.main_logger.setLevel(level)
        self.main_logger.propagate = True

    def disable_logging(self) -> None:
        """Disable all logging for the library."""
        # Remove all handlers except NullHandler
        for handler in self.main_logger.handlers[:]:
            if not isinstance(handler, logging.NullHandler):
                self.main_logger.removeHandler(handler)

        # Ensure NullHandler is present
        if not any(
            isinstance(h, logging.NullHandler) for h in self.main_logger.handlers
        ):
            self.main_logger.addHandler(logging.NullHandler())

        self.main_logger.propagate = False

    def add_file_logging(self, filepath: str, level: int = logging.DEBUG) -> None:
        """
        Add file logging for the library.

        Args:
            filepath: Path to log file
            level: Logging level for file output
        """
        file_handler = logging.FileHandler(filepath)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        self.main_logger.addHandler(file_handler)

        # Ensure main logger level allows the file level
        if self.main_logger.level > level:
            self.main_logger.setLevel(level)


# Global instance
_logger_manager = ThreePaneWindowsLogger()


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for the specified module.

    This is the main function that should be used throughout the library.

    Args:
        name: Module name (usually __name__)

    Returns:
        Configured logger instance

    Example:
        from .logging_config import get_logger
        logger = get_logger(__name__)
        logger.info("This is an info message")
    """
    return _logger_manager.get_logger(name)


def enable_console_logging(level: int = logging.INFO) -> None:
    """
    Enable console logging for the entire library.

    Args:
        level: Minimum logging level to display
    """
    _logger_manager.enable_console_logging(level)


def disable_logging() -> None:
    """Disable all logging for the library."""
    _logger_manager.disable_logging()


def add_file_logging(filepath: str, level: int = logging.DEBUG) -> None:
    """
    Add file logging for the library.

    Args:
        filepath: Path to log file
        level: Minimum logging level for file output
    """
    _logger_manager.add_file_logging(filepath, level)


# Logging level constants for convenience
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
