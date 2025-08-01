"""
Type stubs for threepanewindows.logging_config module.

This module provides logging configuration and management for the ThreePaneWindows package.
"""

import logging
from typing import Optional, Union

class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log messages based on log level."""
    
    def __init__(self, fmt: Optional[str] = ..., datefmt: Optional[str] = ...) -> None: ...
    def format(self, record: logging.LogRecord) -> str: ...

class LoggingConfig:
    """Centralized logging configuration for ThreePaneWindows."""
    
    def __init__(self) -> None: ...

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name."""
    ...

def enable_console_logging(level: Union[int, str] = ...) -> None:
    """Enable console logging with the specified level."""
    ...

def disable_logging() -> None:
    """Disable all logging for the ThreePaneWindows package."""
    ...

def add_file_logging(
    filename: str,
    level: Union[int, str] = ...,
    format_string: Optional[str] = ...,
) -> None:
    """Add file logging with the specified filename and level."""
    ...