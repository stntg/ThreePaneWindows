"""
Typography configuration and utilities for ThreePaneWindows.

This module provides comprehensive typography management including font families,
sizes, weights, and platform-specific font handling.
"""

import platform
import tkinter as tk
import tkinter.font
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union

from .logging_config import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


@dataclass
class Typography:
    """Typography configuration for themes."""

    # Font families
    font_family: str = "Segoe UI"
    font_family_fallback: str = "Arial"
    font_family_monospace: str = "Consolas"
    font_family_monospace_fallback: str = "Courier New"

    # Font sizes
    font_size_tiny: int = 8
    font_size_small: int = 9
    font_size_normal: int = 10
    font_size_medium: int = 11
    font_size_large: int = 12
    font_size_title: int = 14
    font_size_heading: int = 16
    font_size_display: int = 20

    # Font weights
    font_weight_light: str = "normal"
    font_weight_normal: str = "normal"
    font_weight_medium: str = "bold"
    font_weight_bold: str = "bold"

    # Line heights (multipliers)
    line_height_tight: float = 1.0
    line_height_normal: float = 1.2
    line_height_relaxed: float = 1.4
    line_height_loose: float = 1.6

    # Letter spacing (for special cases)
    letter_spacing_tight: int = -1
    letter_spacing_normal: int = 0
    letter_spacing_wide: int = 1

    def __post_init__(self):
        """Initialize platform-specific font adjustments."""
        self._apply_platform_adjustments()

    def _apply_platform_adjustments(self) -> None:
        """Apply platform-specific font adjustments."""
        system = platform.system().lower()

        if system == "darwin":  # macOS
            self.font_family = "SF Pro Display"
            self.font_family_fallback = "Helvetica Neue"
            self.font_family_monospace = "SF Mono"
            self.font_family_monospace_fallback = "Monaco"
            # macOS typically uses slightly larger fonts
            self._adjust_font_sizes(1)

        elif system == "linux":
            self.font_family = "Ubuntu"
            self.font_family_fallback = "DejaVu Sans"
            self.font_family_monospace = "Ubuntu Mono"
            self.font_family_monospace_fallback = "DejaVu Sans Mono"

        # Windows uses the defaults (Segoe UI, etc.)
        logger.debug(f"Applied {system} font adjustments")

    def _adjust_font_sizes(self, adjustment: int) -> None:
        """Adjust all font sizes by a given amount."""
        self.font_size_tiny += adjustment
        self.font_size_small += adjustment
        self.font_size_normal += adjustment
        self.font_size_medium += adjustment
        self.font_size_large += adjustment
        self.font_size_title += adjustment
        self.font_size_heading += adjustment
        self.font_size_display += adjustment

    def get_font_tuple(
        self, size: str = "normal", weight: str = "normal", family: str = "default"
    ) -> Tuple[str, int, str]:
        """
        Get a font tuple for Tkinter widgets.

        Args:
            size: Font size name (tiny, small, normal, medium, large, title, heading, display)
            weight: Font weight name (light, normal, medium, bold)
            family: Font family type (default, monospace)

        Returns:
            Tuple of (family, size, weight) for Tkinter font configuration
        """
        # Get font family
        if family == "monospace":
            font_family = self.font_family_monospace
        else:
            font_family = self.font_family

        # Get font size
        size_map = {
            "tiny": self.font_size_tiny,
            "small": self.font_size_small,
            "normal": self.font_size_normal,
            "medium": self.font_size_medium,
            "large": self.font_size_large,
            "title": self.font_size_title,
            "heading": self.font_size_heading,
            "display": self.font_size_display,
        }
        font_size = size_map.get(size, self.font_size_normal)

        # Get font weight
        weight_map = {
            "light": self.font_weight_light,
            "normal": self.font_weight_normal,
            "medium": self.font_weight_medium,
            "bold": self.font_weight_bold,
        }
        font_weight = weight_map.get(weight, self.font_weight_normal)

        return (font_family, font_size, font_weight)

    def get_font_config(
        self, size: str = "normal", weight: str = "normal", family: str = "default"
    ) -> Dict[str, Union[str, int]]:
        """
        Get a font configuration dictionary for Tkinter widgets.

        Args:
            size: Font size name
            weight: Font weight name
            family: Font family type

        Returns:
            Dictionary with font configuration
        """
        font_tuple = self.get_font_tuple(size, weight, family)
        return {"font": font_tuple}

    def apply_to_widget(
        self,
        widget: tk.Widget,
        size: str = "normal",
        weight: str = "normal",
        family: str = "default",
    ) -> None:
        """
        Apply typography settings to a Tkinter widget.

        Args:
            widget: The widget to apply typography to
            size: Font size name
            weight: Font weight name
            family: Font family type
        """
        try:
            font_config = self.get_font_config(size, weight, family)
            widget.configure(**font_config)
            logger.debug(f"Applied typography to {widget.__class__.__name__}")
        except tk.TclError as e:
            logger.debug(f"Could not apply typography to widget: {e}")
        except Exception as e:
            logger.error(f"Error applying typography: {e}", exc_info=True)


class TypographyManager:
    """Manages typography configurations and provides utilities."""

    def __init__(self, typography: Optional[Typography] = None):
        """
        Initialize typography manager.

        Args:
            typography: Typography configuration to use
        """
        self.typography = typography or Typography()
        self._font_cache: Dict[str, tkinter.font.Font] = {}

    def get_font(
        self, size: str = "normal", weight: str = "normal", family: str = "default"
    ) -> tkinter.font.Font:
        """
        Get a cached Tkinter Font object.

        Args:
            size: Font size name
            weight: Font weight name
            family: Font family type

        Returns:
            Tkinter Font object
        """
        cache_key = f"{family}_{size}_{weight}"

        if cache_key not in self._font_cache:
            font_tuple = self.typography.get_font_tuple(size, weight, family)
            try:
                font_obj = tkinter.font.Font(
                    family=font_tuple[0], size=font_tuple[1], weight=font_tuple[2]
                )
                self._font_cache[cache_key] = font_obj
                logger.debug(f"Created font: {cache_key}")
            except Exception as e:
                logger.error(f"Error creating font {cache_key}: {e}")
                # Fallback to default font
                font_obj = tkinter.font.Font()
                self._font_cache[cache_key] = font_obj

        return self._font_cache[cache_key]

    def clear_cache(self) -> None:
        """Clear the font cache."""
        for font in self._font_cache.values():
            try:
                font.destroy()
            except Exception as e:
                logger.debug(f"Error destroying font: {e}")

        self._font_cache.clear()
        logger.debug("Font cache cleared")

    def get_text_metrics(
        self,
        text: str,
        size: str = "normal",
        weight: str = "normal",
        family: str = "default",
    ) -> Dict[str, int]:
        """
        Get text metrics for given typography settings.

        Args:
            text: Text to measure
            size: Font size name
            weight: Font weight name
            family: Font family type

        Returns:
            Dictionary with width and height metrics
        """
        font = self.get_font(size, weight, family)

        try:
            width = font.measure(text)
            height = font.metrics("linespace")

            return {
                "width": width,
                "height": height,
                "ascent": font.metrics("ascent"),
                "descent": font.metrics("descent"),
            }
        except Exception as e:
            logger.error(f"Error getting text metrics: {e}")
            return {"width": 0, "height": 0, "ascent": 0, "descent": 0}

    def scale_fonts(self, scale_factor: float) -> None:
        """
        Scale all font sizes by a factor.

        Args:
            scale_factor: Factor to scale fonts by (e.g., 1.2 for 20% larger)
        """
        if scale_factor <= 0:
            logger.warning("Invalid scale factor, ignoring")
            return

        # Scale all font sizes
        self.typography.font_size_tiny = int(
            self.typography.font_size_tiny * scale_factor
        )
        self.typography.font_size_small = int(
            self.typography.font_size_small * scale_factor
        )
        self.typography.font_size_normal = int(
            self.typography.font_size_normal * scale_factor
        )
        self.typography.font_size_medium = int(
            self.typography.font_size_medium * scale_factor
        )
        self.typography.font_size_large = int(
            self.typography.font_size_large * scale_factor
        )
        self.typography.font_size_title = int(
            self.typography.font_size_title * scale_factor
        )
        self.typography.font_size_heading = int(
            self.typography.font_size_heading * scale_factor
        )
        self.typography.font_size_display = int(
            self.typography.font_size_display * scale_factor
        )

        # Clear cache to force recreation with new sizes
        self.clear_cache()

        logger.info(f"Scaled fonts by factor {scale_factor}")


# Global typography manager instance
_global_typography_manager: Optional[TypographyManager] = None


def get_typography_manager() -> TypographyManager:
    """Get the global typography manager instance."""
    global _global_typography_manager
    if _global_typography_manager is None:
        _global_typography_manager = TypographyManager()
    return _global_typography_manager


def set_global_typography(typography: Typography) -> None:
    """Set the global typography configuration."""
    global _global_typography_manager
    _global_typography_manager = TypographyManager(typography)
    logger.info("Global typography configuration updated")


# Predefined typography configurations
DEFAULT_TYPOGRAPHY = Typography()

COMPACT_TYPOGRAPHY = Typography(
    font_size_tiny=7,
    font_size_small=8,
    font_size_normal=9,
    font_size_medium=10,
    font_size_large=11,
    font_size_title=12,
    font_size_heading=14,
    font_size_display=16,
)

LARGE_TYPOGRAPHY = Typography(
    font_size_tiny=10,
    font_size_small=11,
    font_size_normal=12,
    font_size_medium=13,
    font_size_large=14,
    font_size_title=16,
    font_size_heading=18,
    font_size_display=24,
)

ACCESSIBILITY_TYPOGRAPHY = Typography(
    font_size_tiny=12,
    font_size_small=14,
    font_size_normal=16,
    font_size_medium=18,
    font_size_large=20,
    font_size_title=22,
    font_size_heading=24,
    font_size_display=28,
    line_height_normal=1.5,
    line_height_relaxed=1.7,
)
