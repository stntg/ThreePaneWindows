"""
Style utilities for combining typography and spacing in common UI patterns.

This module provides convenient functions and classes for applying consistent
styling across different UI components using the typography and spacing modules.
"""

import tkinter as tk
from typing import Dict, Optional, Tuple, Union

from .logging_config import get_logger
from .spacing import Spacing, SpacingManager, get_spacing_manager
from .typography import Typography, TypographyManager, get_typography_manager

# Initialize logger for this module
logger = get_logger(__name__)


class StylePreset:
    """A preset that combines typography and spacing for specific UI components."""

    def __init__(
        self,
        name: str,
        typography_size: str = "normal",
        typography_weight: str = "normal",
        typography_family: str = "default",
        padding_size: str = "normal",
        margin_size: str = "normal",
        border_size: str = "normal",
    ):
        """
        Initialize a style preset.

        Args:
            name: Name of the preset
            typography_size: Typography size name
            typography_weight: Typography weight name
            typography_family: Typography family type
            padding_size: Padding size name
            margin_size: Margin size name
            border_size: Border size name
        """
        self.name = name
        self.typography_size = typography_size
        self.typography_weight = typography_weight
        self.typography_family = typography_family
        self.padding_size = padding_size
        self.margin_size = margin_size
        self.border_size = border_size

    def apply_to_widget(
        self,
        widget: tk.Widget,
        typography_manager: Optional[TypographyManager] = None,
        spacing_manager: Optional[SpacingManager] = None,
    ) -> None:
        """
        Apply this preset to a widget.

        Args:
            widget: Widget to apply preset to
            typography_manager: Typography manager to use (uses global if None)
            spacing_manager: Spacing manager to use (uses global if None)
        """
        if typography_manager is None:
            typography_manager = get_typography_manager()
        if spacing_manager is None:
            spacing_manager = get_spacing_manager()

        try:
            # Apply typography
            typography_manager.typography.apply_to_widget(
                widget,
                self.typography_size,
                self.typography_weight,
                self.typography_family,
            )

            # Apply spacing
            spacing_manager.apply_padding_to_widget(widget, self.padding_size)

            logger.debug(f"Applied preset '{self.name}' to {widget.__class__.__name__}")

        except Exception as e:
            logger.error(f"Error applying preset '{self.name}': {e}", exc_info=True)


# Predefined style presets
TITLE_PRESET = StylePreset(
    name="title",
    typography_size="title",
    typography_weight="bold",
    padding_size="large",
    margin_size="medium",
)

HEADING_PRESET = StylePreset(
    name="heading",
    typography_size="heading",
    typography_weight="medium",
    padding_size="medium",
    margin_size="small",
)

BODY_PRESET = StylePreset(
    name="body",
    typography_size="normal",
    typography_weight="normal",
    padding_size="small",
    margin_size="tiny",
)

CAPTION_PRESET = StylePreset(
    name="caption",
    typography_size="small",
    typography_weight="normal",
    padding_size="tiny",
    margin_size="tiny",
)

BUTTON_PRESET = StylePreset(
    name="button",
    typography_size="normal",
    typography_weight="medium",
    padding_size="medium",
    margin_size="small",
)

INPUT_PRESET = StylePreset(
    name="input",
    typography_size="normal",
    typography_weight="normal",
    padding_size="small",
    margin_size="tiny",
)

CODE_PRESET = StylePreset(
    name="code",
    typography_size="small",
    typography_weight="normal",
    typography_family="monospace",
    padding_size="small",
    margin_size="tiny",
)


class StyleManager:
    """Manages style presets and provides high-level styling functions."""

    def __init__(
        self,
        typography_manager: Optional[TypographyManager] = None,
        spacing_manager: Optional[SpacingManager] = None,
    ):
        """
        Initialize style manager.

        Args:
            typography_manager: Typography manager to use
            spacing_manager: Spacing manager to use
        """
        self.typography_manager = typography_manager or get_typography_manager()
        self.spacing_manager = spacing_manager or get_spacing_manager()
        self.presets: Dict[str, StylePreset] = {}

        # Register default presets
        self._register_default_presets()

    def _register_default_presets(self) -> None:
        """Register default style presets."""
        default_presets = [
            TITLE_PRESET,
            HEADING_PRESET,
            BODY_PRESET,
            CAPTION_PRESET,
            BUTTON_PRESET,
            INPUT_PRESET,
            CODE_PRESET,
        ]

        for preset in default_presets:
            self.presets[preset.name] = preset

        logger.debug(f"Registered {len(default_presets)} default presets")

    def register_preset(self, preset: StylePreset) -> None:
        """
        Register a custom style preset.

        Args:
            preset: Style preset to register
        """
        self.presets[preset.name] = preset
        logger.debug(f"Registered custom preset: {preset.name}")

    def apply_preset(self, widget: tk.Widget, preset_name: str) -> None:
        """
        Apply a style preset to a widget.

        Args:
            widget: Widget to apply preset to
            preset_name: Name of preset to apply
        """
        if preset_name not in self.presets:
            logger.warning(f"Unknown preset: {preset_name}")
            return

        preset = self.presets[preset_name]
        preset.apply_to_widget(widget, self.typography_manager, self.spacing_manager)

    def style_title(self, widget: tk.Widget) -> None:
        """Apply title styling to a widget."""
        self.apply_preset(widget, "title")

    def style_heading(self, widget: tk.Widget) -> None:
        """Apply heading styling to a widget."""
        self.apply_preset(widget, "heading")

    def style_body(self, widget: tk.Widget) -> None:
        """Apply body text styling to a widget."""
        self.apply_preset(widget, "body")

    def style_caption(self, widget: tk.Widget) -> None:
        """Apply caption styling to a widget."""
        self.apply_preset(widget, "caption")

    def style_button(self, widget: tk.Widget) -> None:
        """Apply button styling to a widget."""
        self.apply_preset(widget, "button")

    def style_input(self, widget: tk.Widget) -> None:
        """Apply input styling to a widget."""
        self.apply_preset(widget, "input")

    def style_code(self, widget: tk.Widget) -> None:
        """Apply code styling to a widget."""
        self.apply_preset(widget, "code")

    def create_styled_label(
        self, parent: tk.Widget, text: str, style: str = "body", **kwargs
    ) -> tk.Label:
        """
        Create a styled label widget.

        Args:
            parent: Parent widget
            text: Label text
            style: Style preset name
            **kwargs: Additional label configuration

        Returns:
            Styled label widget
        """
        label = tk.Label(parent, text=text, **kwargs)
        self.apply_preset(label, style)
        return label

    def create_styled_button(
        self,
        parent: tk.Widget,
        text: str,
        command: Optional[callable] = None,
        style: str = "button",
        **kwargs,
    ) -> tk.Button:
        """
        Create a styled button widget.

        Args:
            parent: Parent widget
            text: Button text
            command: Button command
            style: Style preset name
            **kwargs: Additional button configuration

        Returns:
            Styled button widget
        """
        button = tk.Button(parent, text=text, command=command, **kwargs)
        self.apply_preset(button, style)
        return button

    def create_styled_entry(
        self, parent: tk.Widget, style: str = "input", **kwargs
    ) -> tk.Entry:
        """
        Create a styled entry widget.

        Args:
            parent: Parent widget
            style: Style preset name
            **kwargs: Additional entry configuration

        Returns:
            Styled entry widget
        """
        entry = tk.Entry(parent, **kwargs)
        self.apply_preset(entry, style)
        return entry

    def create_form_layout(
        self, parent: tk.Widget, fields: list, gap_size: str = "normal"
    ) -> Tuple[tk.Frame, Dict[str, tk.Widget]]:
        """
        Create a form layout with consistent styling.

        Args:
            parent: Parent widget
            fields: List of field definitions (name, type, label)
            gap_size: Gap size between form elements

        Returns:
            Tuple of (form_frame, widgets_dict)
        """
        form_frame = tk.Frame(parent)
        widgets = {}

        gap = self.spacing_manager.spacing.get_layout_gap(gap_size)

        for i, field in enumerate(fields):
            field_name = field.get("name", f"field_{i}")
            field_type = field.get("type", "entry")
            field_label = field.get("label", field_name.title())

            # Create label
            label = self.create_styled_label(form_frame, field_label, "body")
            label.grid(row=i * 2, column=0, sticky="w", pady=(gap if i > 0 else 0, 2))

            # Create input widget
            if field_type == "entry":
                widget = self.create_styled_entry(form_frame)
            elif field_type == "button":
                widget = self.create_styled_button(
                    form_frame, field_label, command=field.get("command")
                )
            else:
                widget = tk.Label(form_frame, text="Unsupported field type")

            widget.grid(row=i * 2 + 1, column=0, sticky="ew", pady=(0, gap))
            widgets[field_name] = widget

        # Configure column weight
        form_frame.grid_columnconfigure(0, weight=1)

        logger.debug(f"Created form layout with {len(fields)} fields")
        return form_frame, widgets


# Global style manager instance
_global_style_manager: Optional[StyleManager] = None


def get_style_manager() -> StyleManager:
    """Get the global style manager instance."""
    global _global_style_manager
    if _global_style_manager is None:
        _global_style_manager = StyleManager()
    return _global_style_manager


def set_global_style_manager(style_manager: StyleManager) -> None:
    """Set the global style manager instance."""
    global _global_style_manager
    _global_style_manager = style_manager
    logger.info("Global style manager updated")


# Convenience functions for common styling operations
def style_as_title(widget: tk.Widget) -> None:
    """Apply title styling to a widget."""
    get_style_manager().style_title(widget)


def style_as_heading(widget: tk.Widget) -> None:
    """Apply heading styling to a widget."""
    get_style_manager().style_heading(widget)


def style_as_body(widget: tk.Widget) -> None:
    """Apply body text styling to a widget."""
    get_style_manager().style_body(widget)


def style_as_caption(widget: tk.Widget) -> None:
    """Apply caption styling to a widget."""
    get_style_manager().style_caption(widget)


def style_as_button(widget: tk.Widget) -> None:
    """Apply button styling to a widget."""
    get_style_manager().style_button(widget)


def style_as_input(widget: tk.Widget) -> None:
    """Apply input styling to a widget."""
    get_style_manager().style_input(widget)


def style_as_code(widget: tk.Widget) -> None:
    """Apply code styling to a widget."""
    get_style_manager().style_code(widget)


def create_styled_label(
    parent: tk.Widget, text: str, style: str = "body", **kwargs
) -> tk.Label:
    """Create a styled label widget."""
    return get_style_manager().create_styled_label(parent, text, style, **kwargs)


def create_styled_button(
    parent: tk.Widget,
    text: str,
    command: Optional[callable] = None,
    style: str = "button",
    **kwargs,
) -> tk.Button:
    """Create a styled button widget."""
    return get_style_manager().create_styled_button(
        parent, text, command, style, **kwargs
    )


def create_styled_entry(parent: tk.Widget, style: str = "input", **kwargs) -> tk.Entry:
    """Create a styled entry widget."""
    return get_style_manager().create_styled_entry(parent, style, **kwargs)
