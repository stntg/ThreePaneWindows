"""Version information for ThreePaneWindows."""

__version__ = "0.1.0"
__version_info__ = tuple(int(x) for x in __version__.split("."))

# Version components
MAJOR = __version_info__[0]
MINOR = __version_info__[1]
PATCH = __version_info__[2]

# Development status
DEV_STATUS = "beta"

# Full version string with development status
FULL_VERSION = f"{__version__}-{DEV_STATUS}" if DEV_STATUS else __version__
