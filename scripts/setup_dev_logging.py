"""
Quick Development Logging Setup for ThreePaneWindows.

This is a simple script to quickly enable logging for development.
Just import this module at the top of your development scripts.

Usage:
    import setup_dev_logging  # This will automatically enable logging

    # Or customize the setup:
    import setup_dev_logging
    setup_dev_logging.setup_custom_logging(level="DEBUG", file="my_debug.log")
"""

from datetime import datetime
from pathlib import Path

from threepanewindows.logging_config import (
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    add_file_logging,
    enable_console_logging,
    get_logger,
)


def setup_default_logging():
    """Set up default development logging configuration."""
    # Enable console logging at INFO level
    enable_console_logging(INFO)

    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Enable file logging with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/dev_{timestamp}.log"
    add_file_logging(log_file, DEBUG)

    # Log the setup
    logger = get_logger("setup_dev_logging")
    logger.info("🔧 Development logging enabled")
    logger.info(f"📁 Log file: {log_file}")
    logger.info("🚀 Ready for development!")

    print("✅ Development logging enabled!")
    print("📄 Console: INFO level")
    print(f"📁 File: {log_file} (DEBUG level)")

    return log_file


def setup_custom_logging(
    console_level: str = "INFO", file: str = None, file_level: str = "DEBUG"
):
    """
    Set up custom logging configuration.

    Args:
        console_level: Console logging level (DEBUG, INFO, WARNING, ERROR)
        file: Optional log file path
        file_level: File logging level (DEBUG, INFO, WARNING, ERROR)
    """
    # Convert string levels to logging constants
    level_map = {
        "DEBUG": DEBUG,
        "INFO": INFO,
        "WARNING": WARNING,
        "ERROR": ERROR,
    }

    console_lvl = level_map.get(console_level.upper(), INFO)
    file_lvl = level_map.get(file_level.upper(), DEBUG)

    # Enable console logging
    enable_console_logging(console_lvl)

    # Enable file logging if requested
    if file:
        # Create directory if needed
        log_path = Path(file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        add_file_logging(file, file_lvl)

    # Log the setup
    logger = get_logger("setup_dev_logging")
    logger.info(f"🔧 Custom logging enabled - Console: {console_level}")
    if file:
        logger.info(f"📁 File logging: {file} ({file_level})")

    print("✅ Custom logging enabled!")
    print(f"📄 Console: {console_level} level")
    if file:
        print(f"📁 File: {file} ({file_level} level)")


def quick_test():
    """Quick test of the logging setup."""
    logger = get_logger("threepanewindows.test")

    logger.debug("🐛 Debug message")
    logger.info("ℹ️  Info message")
    logger.warning("⚠️  Warning message")
    logger.error("❌ Error message")

    print("🧪 Logging test completed - check console and log file")


# Automatically set up default logging when this module is imported
if __name__ != "__main__":
    setup_default_logging()
else:
    # If run as a script, provide interactive setup
    print("🔧 ThreePaneWindows Development Logging Setup")
    print("=" * 50)

    choice = input(
        "Choose setup type:\n"
        "1. Default (INFO console + DEBUG file)\n"
        "2. Custom\n"
        "3. Test only\n"
        "Choice (1-3): "
    ).strip()

    if choice == "1":
        setup_default_logging()
        quick_test()
    elif choice == "2":
        console_level = (
            input("Console level (DEBUG/INFO/WARNING/ERROR) [INFO]: ").strip() or "INFO"
        )
        file_path = input("Log file path (optional): ").strip() or None
        file_level = (
            input("File level (DEBUG/INFO/WARNING/ERROR) [DEBUG]: ").strip() or "DEBUG"
        )

        setup_custom_logging(console_level, file_path, file_level)
        quick_test()
    elif choice == "3":
        enable_console_logging(DEBUG)
        quick_test()
    else:
        print("Invalid choice. Setting up default logging.")
        setup_default_logging()
        quick_test()
