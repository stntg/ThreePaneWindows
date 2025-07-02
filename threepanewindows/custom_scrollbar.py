#!/usr/bin/env python3
"""
Custom scrollbar implementation for better theming control
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Any


class ThemedScrollbar(tk.Frame):
    """A custom scrollbar that responds better to theming than native scrollbars."""

    def __init__(
        self,
        parent: tk.Widget,
        orient: str = "vertical",
        command: Optional[Callable] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(parent, **kwargs)

        self.orient = orient
        self.command = command
        self._drag_start: Optional[int] = None
        self._thumb_pos = 0.0
        self._thumb_size = 0.1

        # Create the scrollbar components
        self._create_widgets()
        self._bind_events()

    def _create_widgets(self) -> None:
        """Create the scrollbar components."""
        if self.orient == "vertical":
            # Up arrow button
            self.up_button = tk.Button(
                self,
                text="▲",
                command=lambda: self._scroll("scroll", -1, "units"),
                relief="flat",
                bd=1,
                font=("Arial", 8),
            )
            self.up_button.pack(side="top", fill="x")

            # Trough (background)
            self.trough = tk.Frame(self, relief="sunken", bd=1)
            self.trough.pack(side="top", fill="both", expand=True)

            # Thumb (draggable part)
            self.thumb = tk.Frame(
                self.trough, relief="raised", bd=1, cursor="sb_v_double_arrow"
            )

            # Down arrow button
            self.down_button = tk.Button(
                self,
                text="▼",
                command=lambda: self._scroll("scroll", 1, "units"),
                relief="flat",
                bd=1,
                font=("Arial", 8),
            )
            self.down_button.pack(side="bottom", fill="x")

        else:  # horizontal
            # Left arrow button
            self.left_button = tk.Button(
                self,
                text="◀",
                command=lambda: self._scroll("scroll", -1, "units"),
                relief="flat",
                bd=1,
                font=("Arial", 8),
            )
            self.left_button.pack(side="left", fill="y")

            # Trough (background)
            self.trough = tk.Frame(self, relief="sunken", bd=1)
            self.trough.pack(side="left", fill="both", expand=True)

            # Thumb (draggable part)
            self.thumb = tk.Frame(
                self.trough, relief="raised", bd=1, cursor="sb_h_double_arrow"
            )

            # Right arrow button
            self.right_button = tk.Button(
                self,
                text="▶",
                command=lambda: self._scroll("scroll", 1, "units"),
                relief="flat",
                bd=1,
                font=("Arial", 8),
            )
            self.right_button.pack(side="right", fill="y")

    def _bind_events(self) -> None:
        """Bind mouse events for dragging."""
        self.thumb.bind("<Button-1>", self._start_drag)
        self.thumb.bind("<B1-Motion>", self._drag)
        self.thumb.bind("<ButtonRelease-1>", self._end_drag)

        # Bind trough clicks
        self.trough.bind("<Button-1>", self._trough_click)

        # Update thumb position when trough is configured
        self.trough.bind("<Configure>", self._update_thumb_position)

    def _start_drag(self, event: tk.Event) -> None:
        """Start dragging the thumb."""
        self._drag_start = event.y if self.orient == "vertical" else event.x

    def _drag(self, event: tk.Event) -> None:
        """Handle thumb dragging."""
        if self._drag_start is None:
            return

        if self.orient == "vertical":
            delta = event.y - self._drag_start
            trough_height = self.trough.winfo_height()
            thumb_height = self.thumb.winfo_height()

            if trough_height > thumb_height:
                max_pos = trough_height - thumb_height
                new_pos = max(0, min(max_pos, self.thumb.winfo_y() + delta))
                self._thumb_pos = new_pos / max_pos if max_pos > 0 else 0
        else:
            delta = event.x - self._drag_start
            trough_width = self.trough.winfo_width()
            thumb_width = self.thumb.winfo_width()

            if trough_width > thumb_width:
                max_pos = trough_width - thumb_width
                new_pos = max(0, min(max_pos, self.thumb.winfo_x() + delta))
                self._thumb_pos = new_pos / max_pos if max_pos > 0 else 0

        self._update_thumb_position()
        self._scroll("moveto", self._thumb_pos)

    def _end_drag(self, event: tk.Event) -> None:
        """End dragging the thumb."""
        self._drag_start = None

    def _trough_click(self, event: tk.Event) -> None:
        """Handle clicks on the trough."""
        if self.orient == "vertical":
            thumb_center = self.thumb.winfo_y() + self.thumb.winfo_height() // 2
            if event.y < thumb_center:
                self._scroll("scroll", -1, "pages")
            else:
                self._scroll("scroll", 1, "pages")
        else:
            thumb_center = self.thumb.winfo_x() + self.thumb.winfo_width() // 2
            if event.x < thumb_center:
                self._scroll("scroll", -1, "pages")
            else:
                self._scroll("scroll", 1, "pages")

    def _scroll(self, *args: Any) -> None:
        """Execute the scroll command."""
        if self.command:
            self.command(*args)

    def _update_thumb_position(self, event: Optional[tk.Event] = None) -> None:
        """Update the thumb position based on current values."""
        if self.orient == "vertical":
            trough_height = self.trough.winfo_height()
            thumb_height = max(20, int(trough_height * self._thumb_size))
            thumb_y = int((trough_height - thumb_height) * self._thumb_pos)

            self.thumb.place(
                x=0, y=thumb_y, width=self.trough.winfo_width(), height=thumb_height
            )
        else:
            trough_width = self.trough.winfo_width()
            thumb_width = max(20, int(trough_width * self._thumb_size))
            thumb_x = int((trough_width - thumb_width) * self._thumb_pos)

            self.thumb.place(
                x=thumb_x, y=0, width=thumb_width, height=self.trough.winfo_height()
            )

    def set(self, first: str, last: str) -> None:
        """Set the scrollbar position (called by the scrolled widget)."""
        self._thumb_pos = float(first)
        self._thumb_size = float(last) - float(first)
        self._update_thumb_position()

    def apply_theme(self, theme_colors: Any) -> None:
        """Apply theme colors to the scrollbar."""
        # Determine if it's a dark theme
        bg_color = theme_colors.panel_content_bg.lstrip("#")
        r, g, b = [int(bg_color[i : i + 2], 16) for i in (0, 2, 4)]
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        is_dark = luminance < 0.5

        if is_dark:
            # Dark theme colors
            bg_color = theme_colors.secondary_bg
            trough_color = theme_colors.panel_content_bg
            thumb_color = theme_colors.secondary_bg
            button_color = theme_colors.secondary_bg
            text_color = theme_colors.secondary_text
        else:
            # Light theme colors
            bg_color = theme_colors.panel_content_bg
            trough_color = theme_colors.accent_bg
            thumb_color = theme_colors.panel_content_bg
            button_color = theme_colors.panel_content_bg
            text_color = theme_colors.primary_text

        # Apply colors to components
        self.configure(bg=bg_color)
        self.trough.configure(bg=trough_color)
        self.thumb.configure(bg=thumb_color)

        # Apply colors to buttons
        button_style = {
            "bg": button_color,
            "fg": text_color,
            "activebackground": theme_colors.button_hover,
            "activeforeground": text_color,
            "relief": "flat",
            "bd": 1,
        }

        if self.orient == "vertical":
            self.up_button.configure(**button_style)
            self.down_button.configure(**button_style)
        else:
            self.left_button.configure(**button_style)
            self.right_button.configure(**button_style)


def create_themed_scrollbar(
    parent: tk.Widget,
    orient: str = "vertical",
    command: Optional[Callable] = None,
    use_custom: bool = False,
    theme_manager: Any = None,
) -> Any:
    """
    Create a themed scrollbar - either custom or native TTK.

    Args:
        parent: Parent widget
        orient: "vertical" or "horizontal"
        command: Scroll command callback
        use_custom: If True, use custom scrollbar; if False, use TTK
        theme_manager: Theme manager for styling

    Returns:
        Scrollbar widget
    """
    if use_custom:
        scrollbar = ThemedScrollbar(parent, orient=orient, command=command)
        if theme_manager:
            current_theme = theme_manager.get_current_theme()
            scrollbar.apply_theme(current_theme.colors)
        return scrollbar
    else:
        # Use TTK scrollbar with themed style
        style_name = (
            f"Themed.{'Vertical' if orient == 'vertical' else 'Horizontal'}.TScrollbar"
        )
        return ttk.Scrollbar(parent, orient=orient, command=command, style=style_name)  # type: ignore[arg-type]
