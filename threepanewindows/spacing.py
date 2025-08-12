"""
Spacing configuration and utilities for ThreePaneWindows.

This module provides comprehensive spacing management including padding, margins,
borders, and layout utilities for consistent UI spacing.
"""

import platform
import tkinter as tk
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Union

from .logging_config import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


@dataclass
class Spacing:
    """Spacing configuration for themes."""

    # Padding values
    padding_none: int = 0
    padding_tiny: int = 2
    padding_small: int = 4
    padding_normal: int = 8
    padding_medium: int = 12
    padding_large: int = 16
    padding_xl: int = 24
    padding_xxl: int = 32

    # Margin values
    margin_none: int = 0
    margin_tiny: int = 1
    margin_small: int = 2
    margin_normal: int = 4
    margin_medium: int = 6
    margin_large: int = 8
    margin_xl: int = 12
    margin_xxl: int = 16

    # Border widths
    border_none: int = 0
    border_thin: int = 1
    border_normal: int = 2
    border_thick: int = 3
    border_heavy: int = 4

    # Separator widths
    separator_thin: int = 1
    separator_normal: int = 2
    separator_thick: int = 3

    # Corner radius values
    radius_none: int = 0
    radius_small: int = 2
    radius_normal: int = 4
    radius_medium: int = 6
    radius_large: int = 8
    radius_xl: int = 12
    radius_round: int = 999  # For fully rounded elements

    # Layout spacing
    layout_gap_tiny: int = 2
    layout_gap_small: int = 4
    layout_gap_normal: int = 8
    layout_gap_medium: int = 12
    layout_gap_large: int = 16
    layout_gap_xl: int = 24

    # Component-specific spacing
    button_padding_x: int = 12
    button_padding_y: int = 6
    input_padding_x: int = 8
    input_padding_y: int = 4
    panel_padding: int = 16
    panel_margin: int = 8
    header_padding: int = 12
    content_padding: int = 16

    # Scrollbar dimensions
    scrollbar_width: int = 16
    scrollbar_min_thumb: int = 20

    def __post_init__(self):
        """Initialize platform-specific spacing adjustments."""
        self._apply_platform_adjustments()

    def _apply_platform_adjustments(self) -> None:
        """Apply platform-specific spacing adjustments."""
        system = platform.system().lower()

        if system == "darwin":  # macOS
            # macOS typically uses slightly more generous spacing
            self._scale_spacing(1.1)
            # macOS scrollbars are typically thinner
            self.scrollbar_width = 14

        elif system == "linux":
            # Linux often uses more compact spacing
            self._scale_spacing(0.9)

        # Windows uses the defaults
        logger.debug(f"Applied {system} spacing adjustments")

    def _scale_spacing(self, factor: float) -> None:
        """Scale spacing values by a factor."""
        # Scale padding
        self.padding_tiny = max(1, int(self.padding_tiny * factor))
        self.padding_small = max(2, int(self.padding_small * factor))
        self.padding_normal = max(4, int(self.padding_normal * factor))
        self.padding_medium = max(6, int(self.padding_medium * factor))
        self.padding_large = max(8, int(self.padding_large * factor))
        self.padding_xl = max(12, int(self.padding_xl * factor))
        self.padding_xxl = max(16, int(self.padding_xxl * factor))

        # Scale margins
        self.margin_tiny = max(1, int(self.margin_tiny * factor))
        self.margin_small = max(1, int(self.margin_small * factor))
        self.margin_normal = max(2, int(self.margin_normal * factor))
        self.margin_medium = max(3, int(self.margin_medium * factor))
        self.margin_large = max(4, int(self.margin_large * factor))
        self.margin_xl = max(6, int(self.margin_xl * factor))
        self.margin_xxl = max(8, int(self.margin_xxl * factor))

        # Scale layout gaps
        self.layout_gap_tiny = max(1, int(self.layout_gap_tiny * factor))
        self.layout_gap_small = max(2, int(self.layout_gap_small * factor))
        self.layout_gap_normal = max(4, int(self.layout_gap_normal * factor))
        self.layout_gap_medium = max(6, int(self.layout_gap_medium * factor))
        self.layout_gap_large = max(8, int(self.layout_gap_large * factor))
        self.layout_gap_xl = max(12, int(self.layout_gap_xl * factor))

    def get_padding(self, size: str = "normal") -> int:
        """
        Get padding value by size name.

        Args:
            size: Padding size name (none, tiny, small, normal, medium, large, xl, xxl)

        Returns:
            Padding value in pixels
        """
        padding_map = {
            "none": self.padding_none,
            "tiny": self.padding_tiny,
            "small": self.padding_small,
            "normal": self.padding_normal,
            "medium": self.padding_medium,
            "large": self.padding_large,
            "xl": self.padding_xl,
            "xxl": self.padding_xxl,
        }
        return padding_map.get(size, self.padding_normal)

    def get_margin(self, size: str = "normal") -> int:
        """
        Get margin value by size name.

        Args:
            size: Margin size name (none, tiny, small, normal, medium, large, xl, xxl)

        Returns:
            Margin value in pixels
        """
        margin_map = {
            "none": self.margin_none,
            "tiny": self.margin_tiny,
            "small": self.margin_small,
            "normal": self.margin_normal,
            "medium": self.margin_medium,
            "large": self.margin_large,
            "xl": self.margin_xl,
            "xxl": self.margin_xxl,
        }
        return margin_map.get(size, self.margin_normal)

    def get_border_width(self, size: str = "normal") -> int:
        """
        Get border width by size name.

        Args:
            size: Border size name (none, thin, normal, thick, heavy)

        Returns:
            Border width in pixels
        """
        border_map = {
            "none": self.border_none,
            "thin": self.border_thin,
            "normal": self.border_normal,
            "thick": self.border_thick,
            "heavy": self.border_heavy,
        }
        return border_map.get(size, self.border_normal)

    def get_radius(self, size: str = "normal") -> int:
        """
        Get corner radius by size name.

        Args:
            size: Radius size name (none, small, normal, medium, large, xl, round)

        Returns:
            Corner radius in pixels
        """
        radius_map = {
            "none": self.radius_none,
            "small": self.radius_small,
            "normal": self.radius_normal,
            "medium": self.radius_medium,
            "large": self.radius_large,
            "xl": self.radius_xl,
            "round": self.radius_round,
        }
        return radius_map.get(size, self.radius_normal)

    def get_layout_gap(self, size: str = "normal") -> int:
        """
        Get layout gap by size name.

        Args:
            size: Gap size name (tiny, small, normal, medium, large, xl)

        Returns:
            Layout gap in pixels
        """
        gap_map = {
            "tiny": self.layout_gap_tiny,
            "small": self.layout_gap_small,
            "normal": self.layout_gap_normal,
            "medium": self.layout_gap_medium,
            "large": self.layout_gap_large,
            "xl": self.layout_gap_xl,
        }
        return gap_map.get(size, self.layout_gap_normal)


class SpacingManager:
    """Manages spacing configurations and provides layout utilities."""

    def __init__(self, spacing: Optional[Spacing] = None):
        """
        Initialize spacing manager.

        Args:
            spacing: Spacing configuration to use
        """
        self.spacing = spacing or Spacing()

    def apply_padding_to_widget(
        self,
        widget: tk.Widget,
        size: str = "normal",
        x_size: Optional[str] = None,
        y_size: Optional[str] = None,
    ) -> None:
        """
        Apply padding to a Tkinter widget.

        Args:
            widget: The widget to apply padding to
            size: Default padding size for both x and y
            x_size: Specific padding size for x-axis (overrides size)
            y_size: Specific padding size for y-axis (overrides size)
        """
        try:
            padx = self.spacing.get_padding(x_size or size)
            pady = self.spacing.get_padding(y_size or size)

            # Apply padding based on widget type
            if hasattr(widget, "configure"):
                if "padx" in widget.configure():
                    widget.configure(padx=padx, pady=pady)
                elif "ipadx" in widget.configure():
                    widget.configure(ipadx=padx, ipady=pady)

            logger.debug(
                f"Applied padding ({padx}, {pady}) to {widget.__class__.__name__}"
            )

        except Exception as e:
            logger.error(f"Error applying padding to widget: {e}", exc_info=True)

    def apply_margin_to_widget(
        self,
        widget: tk.Widget,
        size: str = "normal",
        x_size: Optional[str] = None,
        y_size: Optional[str] = None,
    ) -> None:
        """
        Apply margin to a Tkinter widget using pack or grid.

        Args:
            widget: The widget to apply margin to
            size: Default margin size for both x and y
            x_size: Specific margin size for x-axis (overrides size)
            y_size: Specific margin size for y-axis (overrides size)
        """
        try:
            padx = self.spacing.get_margin(x_size or size)
            pady = self.spacing.get_margin(y_size or size)

            # Get current pack/grid info
            pack_info = widget.pack_info()
            grid_info = widget.grid_info()

            if pack_info:
                # Widget is packed, update pack options
                current_padx = pack_info.get("padx", 0)
                current_pady = pack_info.get("pady", 0)
                widget.pack_configure(padx=padx, pady=pady)

            elif grid_info:
                # Widget is gridded, update grid options
                current_padx = grid_info.get("padx", 0)
                current_pady = grid_info.get("pady", 0)
                widget.grid_configure(padx=padx, pady=pady)

            logger.debug(
                f"Applied margin ({padx}, {pady}) to {widget.__class__.__name__}"
            )

        except Exception as e:
            logger.error(f"Error applying margin to widget: {e}", exc_info=True)

    def create_spacer(
        self, parent: tk.Widget, size: str = "normal", orientation: str = "horizontal"
    ) -> tk.Frame:
        """
        Create a spacer widget for layout.

        Args:
            parent: Parent widget
            size: Spacer size name
            orientation: "horizontal" or "vertical"

        Returns:
            Spacer frame widget
        """
        spacer = tk.Frame(parent)
        gap = self.spacing.get_layout_gap(size)

        if orientation == "horizontal":
            spacer.configure(width=gap, height=1)
        else:  # vertical
            spacer.configure(width=1, height=gap)

        logger.debug(f"Created {orientation} spacer of size {gap}")
        return spacer

    def get_button_padding(self) -> Tuple[int, int]:
        """Get standard button padding (x, y)."""
        return (self.spacing.button_padding_x, self.spacing.button_padding_y)

    def get_input_padding(self) -> Tuple[int, int]:
        """Get standard input padding (x, y)."""
        return (self.spacing.input_padding_x, self.spacing.input_padding_y)

    def get_panel_spacing(self) -> Dict[str, int]:
        """Get standard panel spacing configuration."""
        return {
            "padding": self.spacing.panel_padding,
            "margin": self.spacing.panel_margin,
            "header_padding": self.spacing.header_padding,
            "content_padding": self.spacing.content_padding,
        }

    def scale_spacing(self, scale_factor: float) -> None:
        """
        Scale all spacing values by a factor.

        Args:
            scale_factor: Factor to scale spacing by (e.g., 1.2 for 20% larger)
        """
        if scale_factor <= 0:
            logger.warning("Invalid scale factor, ignoring")
            return

        self.spacing._scale_spacing(scale_factor)
        logger.info(f"Scaled spacing by factor {scale_factor}")

    def create_layout_grid(
        self, parent: tk.Widget, rows: int, cols: int, gap_size: str = "normal"
    ) -> tk.Frame:
        """
        Create a grid layout with consistent spacing.

        Args:
            parent: Parent widget
            rows: Number of rows
            cols: Number of columns
            gap_size: Gap size between grid cells

        Returns:
            Frame configured for grid layout
        """
        frame = tk.Frame(parent)
        gap = self.spacing.get_layout_gap(gap_size)

        # Configure grid weights for responsive layout
        for i in range(rows):
            frame.grid_rowconfigure(i, weight=1, pad=gap)
        for j in range(cols):
            frame.grid_columnconfigure(j, weight=1, pad=gap)

        logger.debug(f"Created {rows}x{cols} grid layout with gap {gap}")
        return frame


# Global spacing manager instance
_global_spacing_manager: Optional[SpacingManager] = None


def get_spacing_manager() -> SpacingManager:
    """Get the global spacing manager instance."""
    global _global_spacing_manager
    if _global_spacing_manager is None:
        _global_spacing_manager = SpacingManager()
    return _global_spacing_manager


def set_global_spacing(spacing: Spacing) -> None:
    """Set the global spacing configuration."""
    global _global_spacing_manager
    _global_spacing_manager = SpacingManager(spacing)
    logger.info("Global spacing configuration updated")


# Predefined spacing configurations
DEFAULT_SPACING = Spacing()

COMPACT_SPACING = Spacing(
    padding_tiny=1,
    padding_small=2,
    padding_normal=4,
    padding_medium=6,
    padding_large=8,
    padding_xl=12,
    padding_xxl=16,
    margin_tiny=1,
    margin_small=1,
    margin_normal=2,
    margin_medium=3,
    margin_large=4,
    margin_xl=6,
    margin_xxl=8,
    layout_gap_tiny=1,
    layout_gap_small=2,
    layout_gap_normal=4,
    layout_gap_medium=6,
    layout_gap_large=8,
    layout_gap_xl=12,
    button_padding_x=8,
    button_padding_y=4,
    input_padding_x=6,
    input_padding_y=3,
    panel_padding=12,
    panel_margin=6,
)

GENEROUS_SPACING = Spacing(
    padding_tiny=4,
    padding_small=8,
    padding_normal=16,
    padding_medium=20,
    padding_large=24,
    padding_xl=32,
    padding_xxl=48,
    margin_tiny=2,
    margin_small=4,
    margin_normal=8,
    margin_medium=12,
    margin_large=16,
    margin_xl=24,
    margin_xxl=32,
    layout_gap_tiny=4,
    layout_gap_small=8,
    layout_gap_normal=16,
    layout_gap_medium=20,
    layout_gap_large=24,
    layout_gap_xl=32,
    button_padding_x=16,
    button_padding_y=8,
    input_padding_x=12,
    input_padding_y=6,
    panel_padding=24,
    panel_margin=16,
)

ACCESSIBILITY_SPACING = Spacing(
    padding_tiny=6,
    padding_small=12,
    padding_normal=20,
    padding_medium=24,
    padding_large=28,
    padding_xl=36,
    padding_xxl=52,
    margin_tiny=3,
    margin_small=6,
    margin_normal=10,
    margin_medium=14,
    margin_large=18,
    margin_xl=26,
    margin_xxl=36,
    layout_gap_tiny=6,
    layout_gap_small=12,
    layout_gap_normal=20,
    layout_gap_medium=24,
    layout_gap_large=28,
    layout_gap_xl=36,
    button_padding_x=20,
    button_padding_y=10,
    input_padding_x=16,
    input_padding_y=8,
    panel_padding=28,
    panel_margin=20,
    scrollbar_width=20,  # Wider scrollbars for accessibility
)
