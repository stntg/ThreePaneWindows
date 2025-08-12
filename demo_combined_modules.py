#!/usr/bin/env python3
"""
Visual Demo: Using Typography, Spacing, and Central Theme Manager Together

This demo shows how all three modules can work together independently:
- Typography module for font management
- Spacing module for layout and padding
- Central Theme Manager for colors and overall theming

Each module operates independently but they complement each other perfectly.
"""

import tkinter as tk
from tkinter import ttk

from threepanewindows.central_theme_manager import CentralThemeManager, ThemeType
from threepanewindows.spacing import Spacing, SpacingManager, get_spacing_manager
from threepanewindows.typography import (
    Typography,
    TypographyManager,
    get_typography_manager,
)


class CombinedModulesDemo:
    """Demo application showing all three modules working together."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typography + Spacing + Central Theme Manager Demo")
        self.root.geometry("800x600")

        # Initialize all three modules independently
        self.setup_modules()

        # Create the UI
        self.create_ui()

        # Apply initial theme
        self.apply_theme("light")

    def setup_modules(self):
        """Set up all three modules independently."""

        # 1. Typography Module - Custom font configuration
        self.custom_typography = Typography(
            font_family="Segoe UI",
            font_size_normal=11,
            font_size_large=14,
            font_size_title=18,
            font_size_heading=22,
        )
        self.typography_manager = TypographyManager(self.custom_typography)

        # 2. Spacing Module - Custom spacing configuration
        self.custom_spacing = Spacing(
            padding_normal=12,
            padding_large=20,
            margin_normal=8,
            margin_large=16,
            button_padding_x=16,
            button_padding_y=8,
        )
        self.spacing_manager = SpacingManager(self.custom_spacing)

        # 3. Central Theme Manager - Color theming
        self.theme_manager = CentralThemeManager()

        print("✓ All three modules initialized independently!")

    def create_ui(self):
        """Create the user interface using all three modules."""

        # Main container with spacing
        main_frame = tk.Frame(self.root)
        main_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=self.spacing_manager.spacing.get_padding("large"),
            pady=self.spacing_manager.spacing.get_padding("large"),
        )

        # Title section
        self.create_title_section(main_frame)

        # Demo sections
        self.create_typography_section(main_frame)
        self.create_spacing_section(main_frame)
        self.create_theme_section(main_frame)

        # Controls section
        self.create_controls_section(main_frame)

    def create_title_section(self, parent):
        """Create title section demonstrating typography."""
        title_frame = tk.Frame(parent)
        title_frame.pack(
            fill=tk.X, pady=(0, self.spacing_manager.spacing.get_margin("large"))
        )

        # Main title using typography
        self.title_label = tk.Label(title_frame, text="Combined Modules Demo")
        self.typography_manager.typography.apply_to_widget(
            self.title_label, size="heading", weight="bold"
        )
        self.title_label.pack()

        # Subtitle
        self.subtitle_label = tk.Label(
            title_frame,
            text="Typography + Spacing + Central Theme Manager working together",
        )
        self.typography_manager.typography.apply_to_widget(
            self.subtitle_label, size="large", weight="normal"
        )
        self.subtitle_label.pack(
            pady=(self.spacing_manager.spacing.get_margin("small"), 0)
        )

    def create_typography_section(self, parent):
        """Create section demonstrating typography module."""
        # Section frame with spacing
        section_frame = tk.LabelFrame(parent, text="Typography Module Demo")
        section_frame.pack(
            fill=tk.X, pady=self.spacing_manager.spacing.get_margin("medium")
        )

        # Configure section frame padding
        section_frame.configure(
            padx=self.spacing_manager.spacing.get_padding("normal"),
            pady=self.spacing_manager.spacing.get_padding("normal"),
        )

        # Different font sizes
        font_sizes = [
            ("Tiny Text", "tiny"),
            ("Small Text", "small"),
            ("Normal Text", "normal"),
            ("Large Text", "large"),
            ("Title Text", "title"),
        ]

        self.typography_labels = []
        for text, size in font_sizes:
            label = tk.Label(section_frame, text=f"{text} (size: {size})")
            self.typography_manager.typography.apply_to_widget(label, size=size)
            label.pack(
                anchor=tk.W, pady=self.spacing_manager.spacing.get_margin("tiny")
            )
            self.typography_labels.append(label)

        # Font weights demo
        weights_frame = tk.Frame(section_frame)
        weights_frame.pack(
            fill=tk.X, pady=self.spacing_manager.spacing.get_margin("small")
        )

        self.weight_labels = []
        for weight in ["normal", "bold"]:
            label = tk.Label(weights_frame, text=f"Weight: {weight}")
            self.typography_manager.typography.apply_to_widget(
                label, size="normal", weight=weight
            )
            label.pack(
                side=tk.LEFT, padx=self.spacing_manager.spacing.get_padding("medium")
            )
            self.weight_labels.append(label)

    def create_spacing_section(self, parent):
        """Create section demonstrating spacing module."""
        section_frame = tk.LabelFrame(parent, text="Spacing Module Demo")
        section_frame.pack(
            fill=tk.X, pady=self.spacing_manager.spacing.get_margin("medium")
        )

        # Configure section frame padding
        section_frame.configure(
            padx=self.spacing_manager.spacing.get_padding("normal"),
            pady=self.spacing_manager.spacing.get_padding("normal"),
        )

        # Buttons with different spacing
        buttons_frame = tk.Frame(section_frame)
        buttons_frame.pack(fill=tk.X)

        self.spacing_buttons = []
        spacing_sizes = ["small", "normal", "large"]

        for size in spacing_sizes:
            button = tk.Button(buttons_frame, text=f"Padding: {size}")

            # Apply spacing using spacing manager
            padx, pady = self.spacing_manager.get_button_padding()
            if size == "small":
                padx, pady = padx // 2, pady // 2
            elif size == "large":
                padx, pady = int(padx * 1.5), int(pady * 1.5)

            button.configure(padx=padx, pady=pady)
            button.pack(
                side=tk.LEFT,
                padx=self.spacing_manager.spacing.get_margin(size),
                pady=self.spacing_manager.spacing.get_margin("normal"),
            )
            self.spacing_buttons.append(button)

        # Entry fields with spacing
        entries_frame = tk.Frame(section_frame)
        entries_frame.pack(
            fill=tk.X, pady=self.spacing_manager.spacing.get_margin("medium")
        )

        self.spacing_entries = []
        for i, size in enumerate(["normal", "large"]):
            label = tk.Label(entries_frame, text=f"Entry {i+1}:")
            label.pack(anchor=tk.W)

            entry = tk.Entry(entries_frame)
            # Apply spacing to entry
            self.spacing_manager.apply_padding_to_widget(entry, size=size)
            entry.pack(fill=tk.X, pady=self.spacing_manager.spacing.get_margin(size))
            self.spacing_entries.append(entry)

    def create_theme_section(self, parent):
        """Create section demonstrating central theme manager."""
        section_frame = tk.LabelFrame(parent, text="Central Theme Manager Demo")
        section_frame.pack(
            fill=tk.X, pady=self.spacing_manager.spacing.get_margin("medium")
        )

        # Configure section frame padding
        section_frame.configure(
            padx=self.spacing_manager.spacing.get_padding("normal"),
            pady=self.spacing_manager.spacing.get_padding("normal"),
        )

        # Color demonstration
        colors_frame = tk.Frame(section_frame)
        colors_frame.pack(fill=tk.X)

        self.theme_labels = []
        color_types = [
            ("Primary Background", "primary_bg"),
            ("Secondary Background", "secondary_bg"),
            ("Accent Color", "accent_bg"),
            ("Button Color", "button_bg"),
        ]

        for text, color_type in color_types:
            label = tk.Label(colors_frame, text=text, width=15, relief=tk.RAISED)
            label.pack(
                side=tk.LEFT,
                padx=self.spacing_manager.spacing.get_margin("small"),
                pady=self.spacing_manager.spacing.get_margin("small"),
            )
            self.theme_labels.append((label, color_type))

    def create_controls_section(self, parent):
        """Create controls for switching themes and demonstrating integration."""
        controls_frame = tk.LabelFrame(
            parent, text="Controls - All Modules Working Together"
        )
        controls_frame.pack(
            fill=tk.X, pady=self.spacing_manager.spacing.get_margin("large")
        )

        # Configure controls frame padding
        controls_frame.configure(
            padx=self.spacing_manager.spacing.get_padding("normal"),
            pady=self.spacing_manager.spacing.get_padding("normal"),
        )

        # Theme selection
        theme_frame = tk.Frame(controls_frame)
        theme_frame.pack(
            fill=tk.X, pady=self.spacing_manager.spacing.get_margin("small")
        )

        theme_label = tk.Label(theme_frame, text="Select Theme:")
        self.typography_manager.typography.apply_to_widget(theme_label, weight="bold")
        theme_label.pack(side=tk.LEFT)

        self.theme_buttons = []
        themes = ["light", "dark", "blue"]
        for theme in themes:
            button = tk.Button(
                theme_frame,
                text=theme.title(),
                command=lambda t=theme: self.apply_theme(t),
            )

            # Apply button spacing
            padx, pady = self.spacing_manager.get_button_padding()
            button.configure(padx=padx, pady=pady)
            button.pack(
                side=tk.LEFT, padx=self.spacing_manager.spacing.get_margin("small")
            )
            self.theme_buttons.append(button)

        # Font scaling
        font_frame = tk.Frame(controls_frame)
        font_frame.pack(
            fill=tk.X, pady=self.spacing_manager.spacing.get_margin("small")
        )

        font_label = tk.Label(font_frame, text="Font Scale:")
        self.typography_manager.typography.apply_to_widget(font_label, weight="bold")
        font_label.pack(side=tk.LEFT)

        scale_buttons = [("Small", 0.9), ("Normal", 1.0), ("Large", 1.2)]

        for text, scale in scale_buttons:
            button = tk.Button(
                font_frame, text=text, command=lambda s=scale: self.scale_fonts(s)
            )
            padx, pady = self.spacing_manager.get_button_padding()
            button.configure(padx=padx, pady=pady)
            button.pack(
                side=tk.LEFT, padx=self.spacing_manager.spacing.get_margin("small")
            )

        # Status
        self.status_label = tk.Label(controls_frame, text="All modules ready!")
        self.typography_manager.typography.apply_to_widget(
            self.status_label, size="small", weight="normal"
        )
        self.status_label.pack(pady=self.spacing_manager.spacing.get_margin("medium"))

    def apply_theme(self, theme_name):
        """Apply theme using central theme manager."""
        try:
            # Set the theme first
            self.theme_manager.set_theme(theme_name)

            # Apply theme to root window
            self.theme_manager.apply_window_theme(self.root)

            # Apply comprehensive theme to all widgets
            self.theme_manager.apply_comprehensive_theme(self.root)

            # Update color demonstration labels
            current_colors = self.theme_manager.get_current_theme()
            if current_colors:
                for label, color_type in self.theme_labels:
                    color = getattr(current_colors, color_type, "#FFFFFF")
                    label.configure(bg=color)
                    # Adjust text color for contrast
                    if self.is_dark_color(color):
                        label.configure(fg="white")
                    else:
                        label.configure(fg="black")

            self.status_label.configure(text=f"Applied {theme_name.title()} theme!")
            print(f"✓ Applied {theme_name} theme using Central Theme Manager")

        except Exception as e:
            self.status_label.configure(text=f"Error applying theme: {e}")
            print(f"❌ Error applying theme: {e}")

    def scale_fonts(self, scale_factor):
        """Scale fonts using typography manager."""
        try:
            # Create new typography with scaled fonts
            base_sizes = {
                "tiny": 8,
                "small": 9,
                "normal": 11,
                "medium": 12,
                "large": 14,
                "title": 18,
                "heading": 22,
                "display": 26,
            }

            scaled_typography = Typography(
                font_family=self.custom_typography.font_family,
                font_size_tiny=int(base_sizes["tiny"] * scale_factor),
                font_size_small=int(base_sizes["small"] * scale_factor),
                font_size_normal=int(base_sizes["normal"] * scale_factor),
                font_size_medium=int(base_sizes["medium"] * scale_factor),
                font_size_large=int(base_sizes["large"] * scale_factor),
                font_size_title=int(base_sizes["title"] * scale_factor),
                font_size_heading=int(base_sizes["heading"] * scale_factor),
                font_size_display=int(base_sizes["display"] * scale_factor),
            )

            # Update typography manager
            self.typography_manager = TypographyManager(scaled_typography)

            # Reapply fonts to all widgets
            self.typography_manager.typography.apply_to_widget(
                self.title_label, size="heading", weight="bold"
            )
            self.typography_manager.typography.apply_to_widget(
                self.subtitle_label, size="large", weight="normal"
            )

            # Update typography demo labels
            font_sizes = ["tiny", "small", "normal", "large", "title"]
            for label, size in zip(self.typography_labels, font_sizes):
                self.typography_manager.typography.apply_to_widget(label, size=size)

            # Update weight labels
            for i, label in enumerate(self.weight_labels):
                weight = "normal" if i == 0 else "bold"
                self.typography_manager.typography.apply_to_widget(
                    label, size="normal", weight=weight
                )

            self.status_label.configure(text=f"Scaled fonts by {scale_factor}x!")
            print(f"✓ Scaled fonts by {scale_factor}x using Typography Manager")

        except Exception as e:
            self.status_label.configure(text=f"Error scaling fonts: {e}")
            print(f"❌ Error scaling fonts: {e}")

    def is_dark_color(self, color):
        """Check if a color is dark (simple heuristic)."""
        try:
            # Remove # if present
            color = color.lstrip("#")
            # Convert to RGB
            r, g, b = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
            # Calculate luminance
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            return luminance < 128
        except:
            return False

    def run(self):
        """Run the demo application."""
        print("\n" + "=" * 60)
        print("🎨 COMBINED MODULES DEMO STARTED")
        print("=" * 60)
        print("This demo shows:")
        print("✓ Typography Module - Independent font management")
        print("✓ Spacing Module - Independent layout and spacing")
        print("✓ Central Theme Manager - Independent color theming")
        print("✓ All three working together harmoniously!")
        print("=" * 60)
        print("\nTry the controls to see each module in action!")

        self.root.mainloop()


def main():
    """Run the combined modules demo."""
    try:
        demo = CombinedModulesDemo()
        demo.run()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
