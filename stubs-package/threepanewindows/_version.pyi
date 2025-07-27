"""Type stubs for threepanewindows._version module."""

from typing import Tuple

__version__: str
__version_info__: Tuple[int, int, int]

MAJOR: int
MINOR: int
PATCH: int
DEV_STATUS: str
FULL_VERSION: str

def _parse_version(version_string: str) -> Tuple[int, int, int]: ...
