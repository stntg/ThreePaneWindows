#!/usr/bin/env python3
"""
Typography and Spacing Demo

This example demonstrates the new typography, spacing, and style utilities
modules in the ThreePaneWindows package.
"""

import tkinter as tk
from tkinter import ttk

from threepanewindows import (  # Core components; Typography system; Spacing system; Style utilities; Theming
    GENEROUS_SPACING,
    LARGE_TYPOGRAPHY,
    FixedThreePaneWindow,
    Spacing,
    StyleManager,
    ThemeManager,
    ThemeType,
    Typography,
    create_styled_button,
    create_styled_entry,
    create_styled_label,
    get_spacing_manager,
    get_style_manager,
    get_typography_manager,
    style_as_body,
    style_as_caption,
    style_as_heading,
    style_as_title,
)


class TypographySpacingDemo:
    """Demo application showcasing typography and spacing features."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typography and Spacing Demo")
        self.root.geometry("1000x700")

        # Initialize managers
        self.typography_manager = get_typography_manager()
        self.spacing_manager = get_spacing_manager()
        self.style_manager = get_style_manager()
        self.theme_manager = ThemeManager()

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        # Create main three-pane window
        self.main_window = FixedThreePaneWindow(self.root)
        self.main_window.pack(fill=tk.BOTH, expand=True)

        # Set up each pane
        self.setup_left_pane()
        self.setup_center_pane()
        self.setup_right_pane()

    def setup_left_pane(self):
        """Set up the left pane with typography examples."""
        pane = self.main_window.left_pane

        # Title
        title = create_styled_label(pane, "Typography Examples", "title")
        title.pack(pady=self.spacing_manager.spacing.get_padding("large"))

        # Different text styles
        styles = [
            ("Heading Style", "heading"),
            ("Body Text Style", "body"),
            ("Caption Style", "caption"),
            ("Code Style", "code"),
        ]

        for text, style in styles:
            label = create_styled_label(pane, text, style)
            label.pack(pady=self.spacing_manager.spacing.get_padding("small"))

        # Font size examples
        heading = create_styled_label(pane, "Font Sizes", "heading")
        heading.pack(
            pady=(
                self.spacing_manager.spacing.get_padding("large"),
                self.spacing_manager.spacing.get_padding("small"),
            )
        )

        sizes = ["tiny", "small", "normal", "medium", "large", "title", "heading"]
        for size in sizes:
            label = tk.Label(pane, text=f"{size.title()} Text")
            self.typography_manager.typography.apply_to_widget(label, size, "normal")
            label.pack(pady=2)

        # Font weights
        heading = create_styled_label(pane, "Font Weights", "heading")
        heading.pack(
            pady=(
                self.spacing_manager.spacing.get_padding("large"),
                self.spacing_manager.spacing.get_padding("small"),
            )
        )

        weights = ["light", "normal", "medium", "bold"]
        for weight in weights:
            label = tk.Label(pane, text=f"{weight.title()} Weight")
            self.typography_manager.typography.apply_to_widget(label, "normal", weight)
            label.pack(pady=2)

    def setup_center_pane(self):
        """Set up the center pane with spacing examples."""
        pane = self.main_window.center_pane

        # Title
        title = create_styled_label(pane, "Spacing Examples", "title")
        title.pack(pady=self.spacing_manager.spacing.get_padding("large"))

        # Padding examples
        padding_frame = tk.LabelFrame(pane, text="Padding Examples")
        style_as_heading(padding_frame)
        padding_frame.pack(fill=tk.X, padx=10, pady=10)

        padding_sizes = ["tiny", "small", "normal", "medium", "large"]
        for size in padding_sizes:
            button = tk.Button(padding_frame, text=f"{size.title()} Padding")
            self.spacing_manager.apply_padding_to_widget(button, size)
            button.pack(pady=2)

        # Margin examples
        margin_frame = tk.LabelFrame(pane, text="Margin Examples")
        style_as_heading(margin_frame)
        margin_frame.pack(fill=tk.X, padx=10, pady=10)

        for i, size in enumerate(["tiny", "small", "normal", "medium", "large"]):
            label = tk.Label(
                margin_frame, text=f"{size.title()} Margin", bg="lightblue"
            )
            self.spacing_manager.apply_margin_to_widget(label, size)
            label.pack()

        # Layout gaps
        gap_frame = tk.LabelFrame(pane, text="Layout Gaps")
        style_as_heading(gap_frame)
        gap_frame.pack(fill=tk.X, padx=10, pady=10)

        # Create grid with different gap sizes
        for gap_size in ["small", "normal", "large"]:
            gap_label = tk.Label(gap_frame, text=f"{gap_size.title()} Gap Grid:")
            gap_label.pack(anchor="w")

            grid = self.spacing_manager.create_layout_grid(gap_frame, 2, 3, gap_size)
            grid.pack(fill=tk.X, pady=5)

            for i in range(2):
                for j in range(3):
                    btn = tk.Button(grid, text=f"{i},{j}", width=5, height=1)
                    btn.grid(row=i, column=j, sticky="nsew")

    def setup_right_pane(self):
        """Set up the right pane with interactive controls."""
        pane = self.main_window.right_pane

        # Title
        title = create_styled_label(pane, "Interactive Controls", "title")
        title.pack(pady=self.spacing_manager.spacing.get_padding("large"))

        # Theme selection
        theme_frame = tk.LabelFrame(pane, text="Theme Selection")
        style_as_heading(theme_frame)
        theme_frame.pack(fill=tk.X, padx=10, pady=10)

        self.theme_var = tk.StringVar(value="light")
        themes = ["light", "dark", "blue"]

        for theme in themes:
            rb = tk.Radiobutton(
                theme_frame,
                text=theme.title(),
                variable=self.theme_var,
                value=theme,
                command=self.change_theme,
            )
            style_as_body(rb)
            rb.pack(anchor="w")

        # Typography scaling
        scale_frame = tk.LabelFrame(pane, text="Typography Scaling")
        style_as_heading(scale_frame)
        scale_frame.pack(fill=tk.X, padx=10, pady=10)

        scale_label = create_styled_label(scale_frame, "Font Scale:", "body")
        scale_label.pack()

        self.font_scale = tk.Scale(
            scale_frame,
            from_=0.8,
            to=1.5,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            command=self.scale_fonts,
        )
        self.font_scale.set(1.0)
        self.font_scale.pack(fill=tk.X)

        # Spacing scaling
        spacing_scale_frame = tk.LabelFrame(pane, text="Spacing Scaling")
        style_as_heading(spacing_scale_frame)
        spacing_scale_frame.pack(fill=tk.X, padx=10, pady=10)

        spacing_label = create_styled_label(
            spacing_scale_frame, "Spacing Scale:", "body"
        )
        spacing_label.pack()

        self.spacing_scale = tk.Scale(
            spacing_scale_frame,
            from_=0.8,
            to=1.5,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            command=self.scale_spacing,
        )
        self.spacing_scale.set(1.0)
        self.spacing_scale.pack(fill=tk.X)

        # Form example
        form_frame = tk.LabelFrame(pane, text="Styled Form Example")
        style_as_heading(form_frame)
        form_frame.pack(fill=tk.X, padx=10, pady=10)

        # Create form using style utilities
        fields = [
            {"name": "name", "type": "entry", "label": "Name:"},
            {"name": "email", "type": "entry", "label": "Email:"},
            {
                "name": "submit",
                "type": "button",
                "label": "Submit",
                "command": self.submit_form,
            },
        ]

        self.form_frame, self.form_widgets = self.style_manager.create_form_layout(
            form_frame, fields, "small"
        )
        self.form_frame.pack(fill=tk.X, padx=5, pady=5)

        # Reset button
        reset_btn = create_styled_button(
            pane, "Reset All Settings", command=self.reset_settings, style="button"
        )
        reset_btn.pack(pady=self.spacing_manager.spacing.get_padding("large"))

    def change_theme(self):
        """Change the application theme."""
        theme_name = self.theme_var.get()
        if theme_name == "light":
            self.theme_manager.set_theme(ThemeType.LIGHT)
        elif theme_name == "dark":
            self.theme_manager.set_theme(ThemeType.DARK)
        elif theme_name == "blue":
            self.theme_manager.set_theme(ThemeType.BLUE)

        # Apply theme to main window
        current_theme = self.theme_manager.get_current_theme()
        self.root.configure(bg=current_theme.colors.primary_bg)

        print(f"Changed theme to: {theme_name}")

    def scale_fonts(self, value):
        """Scale all fonts by the given factor."""
        scale_factor = float(value)

        # Reset to original size first
        self.typography_manager = get_typography_manager()

        # Apply scaling
        self.typography_manager.scale_fonts(scale_factor)

        print(f"Scaled fonts by factor: {scale_factor}")

    def scale_spacing(self, value):
        """Scale all spacing by the given factor."""
        scale_factor = float(value)

        # Reset to original size first
        self.spacing_manager = get_spacing_manager()

        # Apply scaling
        self.spacing_manager.scale_spacing(scale_factor)

        print(f"Scaled spacing by factor: {scale_factor}")

    def submit_form(self):
        """Handle form submission."""
        name = self.form_widgets["name"].get()
        email = self.form_widgets["email"].get()
        print(f"Form submitted - Name: {name}, Email: {email}")

    def reset_settings(self):
        """Reset all settings to defaults."""
        self.theme_var.set("light")
        self.font_scale.set(1.0)
        self.spacing_scale.set(1.0)

        # Reset managers
        from threepanewindows import (
            DEFAULT_SPACING,
            DEFAULT_TYPOGRAPHY,
            set_global_spacing,
            set_global_typography,
        )

        set_global_typography(DEFAULT_TYPOGRAPHY)
        set_global_spacing(DEFAULT_SPACING)

        self.change_theme()
        print("Reset all settings to defaults")

    def run(self):
        """Run the demo application."""
        print("Typography and Spacing Demo")
        print("=" * 40)
        print("This demo showcases:")
        print("- Typography management with different sizes and weights")
        print("- Spacing utilities for consistent layouts")
        print("- Style presets for common UI patterns")
        print("- Integration with the theming system")
        print("- Interactive controls for testing")
        print()
        print(
            "Use the controls in the right pane to experiment with different settings."
        )

        self.root.mainloop()


def main():
    """Run the typography and spacing demo."""
    demo = TypographySpacingDemo()
    demo.run()


if __name__ == "__main__":
    main()
