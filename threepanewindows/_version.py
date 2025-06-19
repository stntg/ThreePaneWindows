"""Version information for ThreePaneWindows."""

__version__ = "0.1.0"

def _parse_version(version_string):
    """Parse version string into numeric components, handling pre-release suffixes."""
    # Split by dots and handle pre-release suffixes
    parts = version_string.split(".")
    numeric_parts = []
    
    for part in parts:
        # Extract only the numeric portion of each part
        numeric_part = ""
        for char in part:
            if char.isdigit():
                numeric_part += char
            else:
                break  # Stop at first non-digit character
        
        if numeric_part:
            numeric_parts.append(int(numeric_part))
        else:
            numeric_parts.append(0)  # Default to 0 if no numeric part found
    
    # Ensure we have at least 3 components (major, minor, patch)
    while len(numeric_parts) < 3:
        numeric_parts.append(0)
    
    return tuple(numeric_parts[:3])  # Return only first 3 components

__version_info__ = _parse_version(__version__)

# Version components
MAJOR = __version_info__[0]
MINOR = __version_info__[1]
PATCH = __version_info__[2]

# Development status
DEV_STATUS = "beta"

# Full version string with development status
FULL_VERSION = f"{__version__}-{DEV_STATUS}" if DEV_STATUS else __version__
