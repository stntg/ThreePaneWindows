"""Type stubs for threepanewindows.utils.base module."""

import tkinter as tk
from abc import ABC, abstractmethod
from typing import List, Tuple

class PlatformHandler(ABC):
    """Abstract base class for platform-specific functionality."""

    @abstractmethod
    def get_recommended_icon_formats(self) -> List[str]:
        """Get the recommended icon formats for this platform."""
        ...

    @abstractmethod
    def validate_icon_path(self, icon_path: str) -> Tuple[bool, str]:
        """Validate an icon path for this platform."""
        ...

    @abstractmethod
    def set_window_icon(self, window: tk.Tk, icon_path: str) -> bool:
        """Set the window icon using platform-specific methods."""
        ...

    @abstractmethod
    def configure_window_appearance(self, window: tk.Tk, **kwargs) -> None:
        """Configure platform-specific window appearance."""
        ...

    @abstractmethod
    def get_system_theme_preference(self) -> str:
        """Get the system's preferred theme (light/dark)."""
        ...

    @abstractmethod
    def supports_custom_titlebars(self) -> bool:
        """Check if the platform supports custom titlebars."""
        ...
