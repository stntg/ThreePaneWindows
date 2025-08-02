"""
Enhanced Professional Dockable Three-Pane Window.

This module provides a sophisticated, highly customizable three-pane window
with professional theming, smooth animations, and intuitive drag-and-drop
detaching/attaching functionality.
"""

import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import Callable, Dict, List, Optional, Tuple

from .logging_config import get_logger
from .themes import ThemeManager, get_theme_manager
from .utils import platform_handler

# Initialize logger for this module
logger = get_logger(__name__)


def get_recommended_icon_formats() -> List[str]:
    """
    Get recommended icon formats for the current platform.

    Returns:
        List[str]: List of file extensions in order of preference for the
                  current platform. For example, Windows returns ['.ico', '.png'],
                  while Linux/macOS return ['.png', '.ico'].
    """
    return platform_handler.get_recommended_icon_formats()


def validate_icon_path(icon_path: str) -> Tuple[bool, str]:
    """
    Validate an icon path for cross-platform compatibility.

    Args:
        icon_path (str): Path to the icon file to validate.

    Returns:
        Tuple[bool, str]: A tuple containing:
            - bool: True if the icon path is valid and supported, False otherwise
            - str: Descriptive message about the validation result
    """
    return platform_handler.validate_icon_path(icon_path)


@dataclass
class PaneConfig:
    """
    Configuration for a pane in the three-pane window.

    This class defines all the visual and behavioral properties for a pane,
    including its title, icon, sizing constraints, and interaction capabilities.
    """

    title: str = ""  # Display title for the pane header
    icon: str = ""  # Icon for the pane (emoji, text, or file path)
    window_icon: str = (
        ""  # Path to icon file for detached windows (.ico, .png, .gif, .bmp, .xbm)
    )
    custom_titlebar: bool = False  # Use custom title bar instead of system title bar
    custom_titlebar_shadow: bool = True  # Add shadow/border to custom title bar windows
    show_in_taskbar: bool = (
        True  # Whether detached windows appear in taskbar (Windows-specific)
    )
    detached_height: int = 0  # Fixed height for detached windows (0 = auto)
    detached_scrollable: bool = (
        True  # Add scrollbars if content exceeds detached window size
    )
    min_width: int = 100  # Minimum width constraint for the pane
    max_width: int = 500  # Maximum width constraint for the pane
    default_width: int = 200  # Default width when first displayed
    resizable: bool = True  # Whether the pane can be resized by the user
    detachable: bool = True  # Whether the pane can be detached into a separate window
    closable: bool = False  # Whether the pane can be closed/hidden
    fixed_width: Optional[int] = (
        None  # If set, pane will stick to this width and not be resizable
    )


class DragHandle(tk.Frame):
    """Professional drag handle for detaching panes."""

    def __init__(
        self,
        parent,
        pane_side: str,
        on_detach: Callable,
        theme_manager: ThemeManager,
        **kwargs,
    ):
        """Initialize drag handle with parent, pane side, detach callback, and theme."""
        super().__init__(parent, **kwargs)
        self.pane_side = pane_side
        self.on_detach = on_detach
        self.theme_manager = theme_manager
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_threshold = 10

        self._setup_ui()
        self._bind_events()

    def _setup_ui(self):
        """Set up the drag handle UI."""
        theme = self.theme_manager.get_current_theme()
        # Configure the handle
        self.configure(
            height=24, bg=theme.colors.panel_header_bg, relief="flat", cursor="fleur"
        )

        # Create grip dots
        self.grip_frame = tk.Frame(self, bg=theme.colors.panel_header_bg)
        self.grip_frame.pack(expand=True, fill="both")

        # Add visual grip indicators
        for i in range(3):
            for j in range(2):
                dot = tk.Frame(
                    self.grip_frame,
                    width=3,
                    height=3,
                    bg=theme.colors.secondary_text,
                    relief="flat",
                )
                dot.place(x=8 + j * 4, y=8 + i * 4)

        # Add tooltip-like title
        if hasattr(self, "title") and self.title:
            title_label = tk.Label(
                self.grip_frame,
                text=self.title,
                bg=theme.colors.panel_header_bg,
                fg=theme.colors.panel_header_fg,
                font=(theme.typography.font_family, theme.typography.font_size_small),
            )
            title_label.pack(side="right", padx=8)

    def _bind_events(self):
        """Bind mouse events for dragging."""
        self.bind("<Button-1>", self._on_drag_start)
        self.bind("<B1-Motion>", self._on_drag_motion)
        self.bind("<ButtonRelease-1>", self._on_drag_end)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

        # Bind to child widgets too
        for child in self.winfo_children():
            child.bind("<Button-1>", self._on_drag_start)
            child.bind("<B1-Motion>", self._on_drag_motion)
            child.bind("<ButtonRelease-1>", self._on_drag_end)

    def _on_enter(self, event):
        """
        Handle mouse enter event.

        Changes the drag handle appearance to provide visual feedback
        when the mouse hovers over it.

        Args:
            event: Tkinter event object containing mouse position and state.
        """
        theme = self.theme_manager.get_current_theme()
        self.configure(bg=theme.colors.accent_bg)
        self.grip_frame.configure(bg=theme.colors.accent_bg)

    def _on_leave(self, event):
        """
        Handle mouse leave event.

        Restores the drag handle to its normal appearance when the mouse
        leaves the area, unless a drag operation is currently in progress.

        Args:
            event: Tkinter event object containing mouse position and state.
        """
        if not self.is_dragging:
            theme = self.theme_manager.get_current_theme()
            self.configure(bg=theme.colors.panel_header_bg)
            self.grip_frame.configure(bg=theme.colors.panel_header_bg)

    def _on_drag_start(self, event):
        """
        Handle the start of a drag operation.

        Records the initial mouse position for calculating drag distance
        and determining when to trigger detachment.

        Args:
            event: Tkinter event object containing mouse position and state.
        """
        self.is_dragging = False
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root

    def _on_drag_motion(self, event):
        """
        Handle mouse motion during a potential drag operation.

        Monitors mouse movement and initiates visual drag feedback once
        the movement exceeds the drag threshold distance.

        Args:
            event: Tkinter event object containing current mouse position.
        """
        if not self.is_dragging:
            # Check if we've moved enough to start dragging
            dx = abs(event.x_root - self.drag_start_x)
            dy = abs(event.y_root - self.drag_start_y)

            if dx > self.drag_threshold or dy > self.drag_threshold:
                self.is_dragging = True
                self._start_drag_visual()

    def _on_drag_end(self, event):
        """
        Handle the end of a drag operation.

        Determines whether the drag distance was sufficient to trigger
        pane detachment and calls the detach callback if needed.

        Args:
            event: Tkinter event object containing final mouse position.
        """
        if self.is_dragging:
            self._end_drag_visual()
            # Check if we should detach
            dx = abs(event.x_root - self.drag_start_x)
            dy = abs(event.y_root - self.drag_start_y)

            if dx > 50 or dy > 50:  # Detach threshold
                self.on_detach()

        self.is_dragging = False

    def _start_drag_visual(self):
        """Start drag visual feedback."""
        theme = self.theme_manager.get_current_theme()
        self.configure(bg=theme.colors.drag_indicator)
        self.grip_frame.configure(bg=theme.colors.drag_indicator)

    def _end_drag_visual(self):
        """End drag visual feedback."""
        theme = self.theme_manager.get_current_theme()
        self.configure(bg=theme.colors.panel_header_bg)
        self.grip_frame.configure(bg=theme.colors.panel_header_bg)


class PaneHeader(tk.Frame):
    """Professional pane header with title, icon, and controls."""

    def __init__(
        self,
        parent,
        config: PaneConfig,
        pane_side: str,
        on_detach: Callable,
        on_close: Optional[Callable],
        theme_manager: ThemeManager,
        **kwargs,
    ):
        """Initialize pane header with configuration and callbacks."""
        super().__init__(parent, **kwargs)
        self.config = config
        self.pane_side = pane_side
        self.on_detach = on_detach
        self.on_close = on_close
        self.theme_manager = theme_manager

        self._setup_ui()

    def _setup_ui(self):
        """Set up the header UI."""
        theme = self.theme_manager.get_current_theme()
        style = self.theme_manager.get_style("panel_header")

        self.configure(bg=style["bg"], height=32, relief="flat")

        # Left side - icon and title
        left_frame = tk.Frame(self, bg=style["bg"])
        left_frame.pack(side="left", fill="y", padx=8, pady=4)

        # Check if title already includes the icon to avoid duplication
        # For text icons (emojis), check if title starts with the icon
        # For file icons, show them separately since titles won't contain images
        title_includes_icon = (
            self.config.icon
            and self.config.title
            and not self._is_icon_file(self.config.icon)  # Only check for text
            and self.config.title.startswith(self.config.icon)
        )

        # Only show separate icon if title doesn't already include it
        if self.config.icon and not title_includes_icon:
            icon_label = self._create_icon_label(left_frame, style, theme)
            if icon_label:
                icon_label.pack(side="left", padx=(0, 4))

        if self.config.title:
            title_label = tk.Label(
                left_frame,
                text=self.config.title,
                bg=style["bg"],
                fg=style["fg"],
                font=style["font"],
            )
            title_label.pack(side="left")

        # Right side - controls
        right_frame = tk.Frame(self, bg=style["bg"])
        right_frame.pack(side="right", fill="y", padx=4, pady=4)

        # Close button
        if self.config.closable and self.on_close:
            close_btn = self._create_control_button(
                right_frame, "✕", self.on_close, "Close"
            )
            close_btn.pack(side="right", padx=2)

        # Detach button
        if self.config.detachable:
            detach_btn = self._create_control_button(
                right_frame, "⧉", self.on_detach, "Detach"
            )
            detach_btn.pack(side="right", padx=2)

        # Drag handle in the middle
        if self.config.detachable:
            self.drag_handle = DragHandle(
                self, self.pane_side, self.on_detach, self.theme_manager, bg=style["bg"]
            )
            self.drag_handle.pack(fill="x", expand=True, padx=8)

    def _is_icon_file(self, icon_path: str) -> bool:
        """
        Check if the icon string represents a file path rather than text/emoji.

        This method distinguishes between file-based icons (like PNG/ICO files)
        and text-based icons (like emojis or Unicode symbols).

        Args:
            icon_path (str): The icon string to check.

        Returns:
            bool: True if the string appears to be a file path, False if it's likely text/emoji.
        """
        if not icon_path:
            return False

        # Check if it looks like a file path
        import os

        if os.path.sep in icon_path or "/" in icon_path or "\\" in icon_path:
            return True

        # Check for common icon file extensions
        icon_extensions = (".ico", ".png", ".gif", ".bmp", ".xbm", ".jpg", ".jpeg")
        return any(icon_path.lower().endswith(ext) for ext in icon_extensions)

    def _create_icon_label(self, parent, style, theme):
        """
        Create an icon label widget that can display either text or image icons.

        This method handles both file-based icons (PNG, ICO, etc.) and text-based
        icons (emojis, Unicode symbols) with appropriate fallback behavior.

        Args:
            parent: The parent widget to contain the icon label.
            style: Style dictionary containing background and foreground colors.
            theme: Theme object containing typography settings.

        Returns:
            tk.Label or None: The created icon label widget, or None if no icon is configured.
        """
        if not self.config.icon:
            return None

        try:
            if self._is_icon_file(self.config.icon):
                # Try to load as image file
                import os

                if os.path.exists(self.config.icon):
                    try:
                        photo = tk.PhotoImage(file=self.config.icon)
                        # Resize if too large (optional - you can adjust these values)
                        if photo.width() > 16 or photo.height() > 16:
                            # For now, just use the image as-is
                            # You could add resizing logic here if needed
                            pass

                        icon_label = tk.Label(
                            parent,
                            image=photo,
                            bg=style["bg"],
                        )
                        # Keep a reference to prevent garbage collection
                        icon_label.image = photo
                        return icon_label
                    except tk.TclError:
                        # If image loading fails, fall back to text
                        pass

            # Use as text icon (emoji or text)
            icon_label = tk.Label(
                parent,
                text=self.config.icon,
                bg=style["bg"],
                fg=style["fg"],
                font=(theme.typography.font_family, theme.typography.font_size_normal),
            )
            return icon_label

        except Exception as e:
            logger.warning("Failed to create icon label: %s", e)
            return None

    def _create_control_button(
        self, parent, text: str, command: Callable, tooltip: str
    ) -> tk.Button:
        """
        Create a themed control button for the pane header.

        Creates a small button with hover effects that matches the current theme.
        Used for close, detach, and other pane control actions.

        Args:
            parent: The parent widget to contain the button.
            text (str): The text/symbol to display on the button.
            command (Callable): The function to call when the button is clicked.
            tooltip (str): Tooltip text for accessibility (currently unused but reserved).

        Returns:
            tk.Button: The created and configured button widget.
        """
        theme = self.theme_manager.get_current_theme()

        btn = tk.Button(
            parent,
            text=text,
            command=command,
            width=2,
            height=1,
            bg=theme.colors.panel_header_bg,
            fg=theme.colors.secondary_text,
            activebackground=theme.colors.accent_bg,
            activeforeground=theme.colors.accent_text,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            font=(theme.typography.font_family, theme.typography.font_size_small),
        )

        # Add hover effects
        def on_enter(e):
            btn.configure(bg=theme.colors.accent_bg, fg=theme.colors.accent_text)

        def on_leave(e):
            btn.configure(
                bg=theme.colors.panel_header_bg, fg=theme.colors.secondary_text
            )

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def refresh_theme(self):
        """Refresh the header with the current theme."""
        try:
            # Clear existing widgets
            for child in self.winfo_children():
                child.destroy()

            # Recreate UI with new theme
            self._setup_ui()
        except tk.TclError:
            # Widget has been destroyed, ignore
            pass


class DetachedWindow(tk.Toplevel):
    """
    Professional detached window for displaying pane content in a separate window.

    This class creates a standalone window that can display pane content when
    a pane is detached from the main three-pane layout. It supports custom
    titlebars, theming, scrollable content, and reattachment functionality.
    """

    def _is_icon_file(self, path: str) -> bool:
        """Check if a string is likely an icon file path."""
        return platform_handler._is_icon_file(path)

    def __init__(
        self,
        parent,
        pane_side: str,
        config: PaneConfig,
        content_builder: Callable,
        on_reattach: Callable,
        theme_manager: ThemeManager,
        layout_instance=None,
        **kwargs,
    ):
        """
        Initialize detached window with configuration and callbacks.

        Args:
            parent: The parent window (usually the main application window).
            pane_side (str): Which pane this window represents ('left', 'center', 'right').
            config (PaneConfig): Configuration object defining window behavior and appearance.
            content_builder (Callable): Function to call to build the window's content.
            on_reattach (Callable): Callback function to call when the window should be reattached.
            theme_manager (ThemeManager): Theme manager for consistent styling.
            layout_instance: Reference to the main layout instance (optional).
            **kwargs: Additional keyword arguments passed to tk.Toplevel.
        """
        super().__init__(parent, **kwargs)
        self.pane_side = pane_side
        self.config = config
        self.content_builder = content_builder
        self.on_reattach = on_reattach
        self.theme_manager = theme_manager
        self.layout_instance = layout_instance  # Reference to the main layout

        self._setup_window()
        self._setup_ui()

    def _setup_window(self):
        """Set up the detached window."""
        theme = self.theme_manager.get_current_theme()

        # Window properties
        if self.config.custom_titlebar:
            # Set window title first (for taskbar identification)
            self.title(f"{self.config.title or self.pane_side.title()} Panel")

            # Try platform-specific custom titlebar with taskbar support
            import platform

            # Use overrideredirect for all platforms
            self.overrideredirect(True)
        else:
            self.title(f"{self.config.title or self.pane_side.title()} Panel")

        # Set window size - use custom height if specified
        window_height = (
            self.config.detached_height if self.config.detached_height > 0 else 400
        )
        self.geometry(f"{self.config.default_width}x{window_height}")
        self.minsize(self.config.min_width, 200)

        if self.config.max_width > 0:
            self.maxsize(self.config.max_width, 2000)

        # Window styling
        if self.config.custom_titlebar:
            # Always create a border for custom title bar windows
            # The difference is in the border style (shadow vs clean)
            self._setup_windows_border(theme)
        else:
            self.configure(bg=theme.colors.primary_bg)

        # Window icon (if available)
        # Use window_icon if provided, otherwise use icon only if it's a file path
        icon_path = self.config.window_icon or (
            self.config.icon if self._is_icon_file(self.config.icon) else ""
        )
        if icon_path:
            self._set_window_icon(icon_path)

        # Setup focus management for better user experience
        self._setup_focus_management()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_window_close)

        # Make window appear professional
        self.transient(self.master)

        # Platform-specific window behavior
        self._setup_platform_specific_behavior()

        self.focus_set()

    def _setup_platform_specific_behavior(self):
        """Set up platform-specific window behavior."""
        import platform

        system = platform.system()

        if system == "Darwin":  # macOS
            # macOS-specific adjustments
            if self.config.custom_titlebar:
                # On macOS, overrideredirect windows may have issues
                # Consider using attributes instead
                try:
                    self.attributes("-titlebar", False)
                except tk.TclError:
                    # Fall back to overrideredirect if attributes not supported
                    pass

        elif system == "Linux":
            # Linux-specific adjustments
            if self.config.custom_titlebar:
                # Some Linux window managers handle overrideredirect differently
                try:
                    # Try to set window type hint for better behavior
                    self.attributes("-type", "dialog")
                except tk.TclError:
                    pass

        elif system == "Windows":
            # Windows-specific adjustments are now handled in _setup_window
            pass

    def _set_window_icon(self, icon_path: str):
        """Set window icon with cross-platform compatibility."""
        platform_handler.set_window_icon(self, icon_path)

    def _setup_ui(self):
        """Set up the UI."""
        theme = self.theme_manager.get_current_theme()

        # Determine the parent container (border frame if using Windows border,
        # otherwise self)
        parent_container = getattr(self, "_border_frame", self)

        # Header with reattach button (and custom title bar if needed)
        header_height = 32  # Keep same height for consistency
        if self.config.custom_titlebar:
            # Add a header that matches Windows title bar style
            header_frame = tk.Frame(
                parent_container,
                bg=theme.colors.panel_header_bg,
                height=header_height,
                relief="flat",
                borderwidth=0,
            )
        else:
            header_frame = tk.Frame(
                parent_container, bg=theme.colors.panel_header_bg, height=header_height
            )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        # Custom title bar controls (if using custom title bar)
        controls_frame = None
        if self.config.custom_titlebar:
            controls_frame = self._setup_custom_titlebar(header_frame, theme)

        # Title and Icon
        if self.config.title:
            # For detached windows, we'll create separate icon and title elements
            # to handle both text and image icons properly

            # Check if title already includes the icon to avoid duplication
            # For text icons (emojis), check if title starts with the icon
            # For file icons, show them separately since titles won't contain images
            title_includes_icon = (
                self.config.icon
                and not self._is_icon_file(self.config.icon)  # Only check for text
                and self.config.title.startswith(self.config.icon)
            )

            # Create a container for icon and title
            title_container = tk.Frame(header_frame, bg=theme.colors.panel_header_bg)
            title_container.pack(side="left", padx=8, pady=6, fill="x", expand=True)

            # Add icon if present and not already in title
            if self.config.icon and not title_includes_icon:
                icon_label = self._create_detached_icon_label(title_container, theme)
                if icon_label:
                    icon_label.pack(side="left", padx=(0, 4))

            # Add title
            title_label = tk.Label(
                title_container,
                text=self.config.title,
                bg=theme.colors.panel_header_bg,
                fg=theme.colors.panel_header_fg,
                font=(
                    theme.typography.font_family,
                    theme.typography.font_size_normal,
                    "bold",
                ),
                anchor="w",  # Left align to prevent truncation
            )
            title_label.pack(side="left", fill="x", expand=True)

            # Make title label draggable too (for custom title bar)
            if self.config.custom_titlebar:
                title_label.bind("<Button-1>", self._start_drag)
                title_label.bind("<B1-Motion>", self._on_drag)

        # Reattach button - match the detach button style exactly
        if self.config.custom_titlebar:
            # For custom title bar, put reattach button in controls frame
            # instead of close button
            reattach_btn = tk.Button(
                controls_frame,  # Use controls_frame instead of header_frame
                text="⧈",
                command=self.on_reattach,
                width=2,
                height=1,
                bg=theme.colors.panel_header_bg,
                fg=theme.colors.secondary_text,
                activebackground=theme.colors.accent_bg,
                activeforeground=theme.colors.accent_text,
                relief="flat",
                borderwidth=0,
                cursor="hand2",
                font=(theme.typography.font_family, theme.typography.font_size_small),
            )
            reattach_btn.pack(side="right", padx=2)
        else:
            # For regular title bar, put in header frame
            reattach_btn = tk.Button(
                header_frame,
                text="⧈",
                command=self.on_reattach,
                width=2,
                height=1,
                bg=theme.colors.panel_header_bg,
                fg=theme.colors.secondary_text,
                activebackground=theme.colors.accent_bg,
                activeforeground=theme.colors.accent_text,
                relief="flat",
                borderwidth=0,
                cursor="hand2",
                font=(theme.typography.font_family, theme.typography.font_size_small),
            )
            reattach_btn.pack(side="right", padx=8, pady=4)

        # Add hover effects to match detach button
        def on_enter_reattach(e):
            reattach_btn.configure(
                bg=theme.colors.accent_bg, fg=theme.colors.accent_text
            )

        def on_leave_reattach(e):
            reattach_btn.configure(
                bg=theme.colors.panel_header_bg, fg=theme.colors.secondary_text
            )

        reattach_btn.bind("<Enter>", on_enter_reattach)
        reattach_btn.bind("<Leave>", on_leave_reattach)

        # Separator
        separator = tk.Frame(parent_container, bg=theme.colors.separator, height=1)
        separator.pack(fill="x")

        # Content frame - with optional scrollbars
        if self.config.detached_scrollable and self.config.detached_height > 0:
            # Create scrollable content area
            self._setup_scrollable_content(theme, parent_container)
        else:
            # Regular content frame
            self.content_frame = tk.Frame(
                parent_container, bg=theme.colors.panel_content_bg
            )
            self.content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Build content
        if self.content_builder:
            self.content_builder(self.content_frame)

    def _setup_custom_titlebar(self, header_frame, theme):
        """Set up custom title bar with window controls."""
        # Make the header draggable
        self._drag_data = {"x": 0, "y": 0}
        header_frame.bind("<Button-1>", self._start_drag)
        header_frame.bind("<B1-Motion>", self._on_drag)

        # Window control buttons frame (right side)
        controls_frame = tk.Frame(header_frame, bg=theme.colors.panel_header_bg)
        controls_frame.pack(side="right", padx=4, pady=4)

        # Note: Close button replaced by reattach button in the main UI setup
        # Note: Minimize button removed for custom title bars since overrideredirect
        # windows can't be properly minimized

        return controls_frame

    def _setup_windows_border(self, theme):
        """Set up Windows-style border for custom title bar windows."""
        if self.config.custom_titlebar_shadow:
            # Windows-style border with shadow effect
            border_bg = "#2d2d30"  # Slightly darker for shadow effect
            border_color = "#3c3c3c"  # Windows-like border color
        else:
            # Clean border without shadow
            border_bg = "#404040"  # Clean dark border
            border_color = "#505050"  # Lighter border for clean look

        # Configure the main window with border
        self.configure(
            bg=border_bg,
            highlightbackground=border_color,
            highlightthickness=1,
            relief="flat",
        )

        # Create an inner frame that will contain all content
        self._border_frame = tk.Frame(
            self, bg=theme.colors.primary_bg, relief="flat", borderwidth=0
        )
        self._border_frame.pack(fill="both", expand=True, padx=1, pady=1)

        # Update the parent for all subsequent UI elements
        self._content_parent = self._border_frame

    def _setup_scrollable_content(self, theme, parent=None):
        """Set up scrollable content area for detached windows."""
        if parent is None:
            parent = self

        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(
            parent, bg=theme.colors.panel_content_bg, highlightthickness=0
        )
        scrollbar_v = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollbar_h = tk.Scrollbar(parent, orient="horizontal", command=canvas.xview)

        # Configure canvas scrolling
        canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        # Create the actual content frame inside the canvas
        self.content_frame = tk.Frame(canvas, bg=theme.colors.panel_content_bg)

        # Add content frame to canvas
        canvas_window = canvas.create_window(
            (0, 0), window=self.content_frame, anchor="nw"
        )

        # Pack scrollbars and canvas
        scrollbar_v.pack(side="right", fill="y")
        scrollbar_h.pack(side="bottom", fill="x")
        canvas.pack(fill="both", expand=True)

        # Update scroll region when content changes
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Also update the canvas window width to match canvas width
            canvas_width = canvas.winfo_width()
            if canvas_width > 1:  # Avoid issues during initialization
                canvas.itemconfig(canvas_window, width=canvas_width)

        self.content_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_scroll_region)

        # Enable mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Bind mouse wheel to canvas and content frame
        canvas.bind("<MouseWheel>", on_mousewheel)
        self.content_frame.bind("<MouseWheel>", on_mousewheel)

        # Store references for cleanup
        self._canvas = canvas
        self._scrollbar_v = scrollbar_v
        self._scrollbar_h = scrollbar_h

    def _start_drag(self, event):
        """Start dragging the window and bring it to front."""
        # Bring window to front and give it focus when clicked
        self.lift()
        self.focus_set()

        # Store drag data for dragging functionality
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _on_drag(self, event):
        """Handle window dragging."""
        x = self.winfo_x() + (event.x - self._drag_data["x"])
        y = self.winfo_y() + (event.y - self._drag_data["y"])
        self.geometry(f"+{x}+{y}")

    def _setup_focus_management(self):
        """Set up comprehensive focus management for the detached window."""

        def bring_to_front(event=None):
            """Bring the window to front and give it focus."""
            try:
                self.lift()
                self.focus_set()
                # Temporarily set topmost to ensure it comes to front, then remove it
                self.attributes("-topmost", True)
                self.after_idle(lambda: self.attributes("-topmost", False))
            except (tk.TclError, AttributeError):
                # Ignore specific errors in focus management (window may be destroyed)
                # Log could be added here if needed for debugging
                pass  # nosec B110

        def bind_focus_recursively(widget):
            """Recursively bind focus events to all child widgets."""
            try:
                # Bind click events to bring window to front
                widget.bind("<Button-1>", lambda e: bring_to_front(), add=True)
                widget.bind("<FocusIn>", bring_to_front, add=True)

                # Recursively bind to all children
                for child in widget.winfo_children():
                    bind_focus_recursively(child)
            except (tk.TclError, AttributeError):
                # Ignore specific binding errors for widgets that don't support events
                # Log could be added here if needed for debugging
                pass  # nosec B110

        # Bind to the main window
        self.bind("<Button-1>", lambda e: bring_to_front(), add=True)
        self.bind("<FocusIn>", bring_to_front, add=True)

        # Bind to all child widgets
        bind_focus_recursively(self)

    def _on_window_close(self):
        """Handle window close."""
        self.on_reattach()

    def refresh_theme(self):
        """Refresh the detached window with the current theme."""
        try:
            # Update the theme manager reference to ensure it's current
            _ = self.theme_manager.get_current_theme()

            # Clear and recreate the UI with new theme
            for child in self.winfo_children():
                child.destroy()

            # Reset any internal references that might have been destroyed
            if hasattr(self, "_border_frame"):
                delattr(self, "_border_frame")
            if hasattr(self, "_content_parent"):
                delattr(self, "_content_parent")

            # Recreate the window setup (including borders for custom titlebar)
            self._setup_window()
            self._setup_ui()

            # Note: The content frame is recreated in _setup_ui() with the new theme,
            # so no additional theme update is needed for the content

        except tk.TclError:
            # Window has been destroyed, ignore
            pass
        except Exception as e:
            logger.error("Error refreshing detached window theme: %s", e)

    def create_themed_scrollbar(
        self, parent, orient="vertical", command=None, **kwargs
    ):
        """Create a platform-appropriate themed scrollbar for detached window.

        Delegates to the main layout instance if available.
        """
        if self.layout_instance:
            return self.layout_instance.create_themed_scrollbar(
                parent, orient, command, **kwargs
            )
        else:
            # Fallback to theme manager method
            return self.theme_manager.create_themed_scrollbar_auto(
                parent, orient, command, **kwargs
            )

    def get_platform_info(self):
        """Get platform information. Delegates to layout instance if available."""
        if self.layout_instance:
            return self.layout_instance.get_platform_info()
        else:
            return self.theme_manager.get_platform_info()

    def _create_detached_icon_label(self, parent, theme):
        """Create an icon label for detached window (text or image)."""
        if not self.config.icon:
            return None

        try:
            if self._is_icon_file(self.config.icon):
                # Try to load as image file
                import os

                if os.path.exists(self.config.icon):
                    try:
                        photo = tk.PhotoImage(file=self.config.icon)
                        # Resize if too large (optional - you can adjust these values)
                        if photo.width() > 16 or photo.height() > 16:
                            # For now, just use the image as-is
                            # You could add resizing logic here if needed
                            pass

                        icon_label = tk.Label(
                            parent,
                            image=photo,
                            bg=theme.colors.panel_header_bg,
                        )
                        # Keep a reference to prevent garbage collection
                        icon_label.image = photo
                        return icon_label
                    except tk.TclError:
                        # If image loading fails, fall back to text
                        pass

            # Use as text icon (emoji or text)
            icon_label = tk.Label(
                parent,
                text=self.config.icon,
                bg=theme.colors.panel_header_bg,
                fg=theme.colors.panel_header_fg,
                font=(theme.typography.font_family, theme.typography.font_size_normal),
            )
            return icon_label

        except Exception as e:
            logger.warning("Failed to create detached icon label: %s", e)
            return None


class EnhancedDockableThreePaneWindow(tk.Frame):
    """
    Enhanced professional dockable three-pane window with theming and advanced UI.

    Features:
    - Professional theming system
    - Drag-and-drop detaching
    - Smooth animations
    - Customizable pane configurations
    - Professional visual feedback
    """

    def __init__(
        self,
        master=None,
        left_config: Optional[PaneConfig] = None,
        center_config: Optional[PaneConfig] = None,
        right_config: Optional[PaneConfig] = None,
        left_builder: Optional[Callable] = None,
        center_builder: Optional[Callable] = None,
        right_builder: Optional[Callable] = None,
        theme_name: str = "light",
        theme=None,  # Alternative parameter name for theme_name
        enable_animations: bool = True,
        menu_bar: Optional[tk.Menu] = None,
        show_status_bar: bool = False,
        show_toolbar: bool = False,
        **kwargs,
    ):
        """
        Initialize enhanced dockable three-pane window with configuration options.

        Args:
            master: Parent widget (usually the root window).
            left_config (Optional[PaneConfig]): Configuration for the left pane.
            center_config (Optional[PaneConfig]): Configuration for the center pane.
            right_config (Optional[PaneConfig]): Configuration for the right pane.
            left_builder (Optional[Callable]): Function to build left pane content.
            center_builder (Optional[Callable]): Function to build center pane content.
            right_builder (Optional[Callable]): Function to build right pane content.
            theme_name (str): Name of the theme to use ("light", "dark", "blue", "native").
            theme: Alternative parameter for theme_name (supports ThemeType enum).
            enable_animations (bool): Whether to enable smooth animations.
            menu_bar (Optional[tk.Menu]): Menu bar to attach to the parent window.
            show_status_bar (bool): Whether to show a status bar at the bottom.
            show_toolbar (bool): Whether to show a toolbar at the top.
            **kwargs: Additional keyword arguments passed to tk.Frame.
        """
        super().__init__(master, **kwargs)

        # Configuration
        self.left_config = left_config or PaneConfig(title="Left Panel", icon="📁")
        self.center_config = center_config or PaneConfig(
            title="Main Content", icon="📝", detachable=False
        )
        self.right_config = right_config or PaneConfig(title="Right Panel", icon="🔧")

        # Builders
        self.left_builder = left_builder
        self.center_builder = center_builder
        self.right_builder = right_builder

        # Theme management - handle both theme_name and theme parameters
        # Use the global theme manager to ensure synchronization
        self.theme_manager = get_theme_manager()
        if theme is not None:
            # Handle ThemeType enum or string
            if hasattr(theme, "value"):
                theme_name = theme.value
            else:
                theme_name = str(theme)

        # Validate theme name and set titlebar color
        if not self.theme_manager.set_theme(theme_name, window=master):
            raise ValueError(f"Invalid theme: {theme_name}")

        # Animation settings
        self.enable_animations = enable_animations

        # Menu bar
        self.menu_bar = menu_bar

        # UI components
        self.show_status_bar = show_status_bar
        self.show_toolbar = show_toolbar
        self.status_bar = None
        self.toolbar = None

        # State tracking
        self.detached_windows: Dict[str, DetachedWindow] = {}
        self.pane_frames: Dict[str, tk.Frame] = {}
        self.pane_headers: Dict[str, PaneHeader] = {}
        self.pane_positions: Dict[str, int] = {}  # Track original positions
        self.pane_visibility: Dict[str, bool] = (
            {}
        )  # Track visibility (winfo_children() doesn't update immediately)

        # Setup
        self._setup_styles()
        self._create_widgets()

    def _setup_styles(self):
        """Set up TTK styles."""
        self.style = ttk.Style()
        self.theme_manager.apply_ttk_theme(self.style)

        # Try to create a custom style for non-resizable paned windows
        try:
            # Create a style that makes sashes less visible/interactive
            self.style.configure(
                "FixedSash.TPanedwindow", sashwidth=1, sashrelief="flat"
            )
            self.style.map(
                "FixedSash.TPanedwindow",
                background=[
                    (
                        "active",
                        self.theme_manager.get_current_theme().colors.secondary_bg,
                    )
                ],
            )
        except tk.TclError:
            pass

    def _create_widgets(self):
        """Create the main widget structure."""
        theme = self.theme_manager.get_current_theme()

        # Main container
        self.configure(bg=theme.colors.secondary_bg)

        # Add menu bar if provided
        if self.menu_bar:
            # Create a frame to hold the menu bar
            menu_frame = tk.Frame(self, bg=theme.colors.primary_bg, height=25)
            menu_frame.pack(fill=tk.X, padx=0, pady=0)
            menu_frame.pack_propagate(False)

            # Configure the menu bar for this window
            if hasattr(self.master, "config"):
                self.master.config(menu=self.menu_bar)

        # Add toolbar if requested
        if self.show_toolbar:
            self._create_toolbar()

        # Determine if we need custom layout for fixed panes
        # Only use custom layout if we have truly fixed panes
        # (fixed_width or resizable=False)
        self._has_fixed_panes = (
            self.left_builder
            and (
                self.left_config.fixed_width is not None
                or not self.left_config.resizable
            )
        ) or (
            self.right_builder
            and (
                self.right_config.fixed_width is not None
                or not self.right_config.resizable
            )
        )

        if self._has_fixed_panes:
            # Use custom layout for fixed panes
            self._create_custom_layout()
        else:
            # Use standard TTK PanedWindow for fully resizable layout
            self.paned = ttk.PanedWindow(
                self, orient=tk.HORIZONTAL, style="Themed.TPanedwindow"
            )
            self.paned.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Create panes
        self._create_left_pane()
        self._create_center_pane()
        self._create_right_pane()

        # Add status bar if requested
        if self.show_status_bar:
            self._create_status_bar()

        # Configure behavior after everything is created
        if self._has_fixed_panes:
            self.after_idle(self._trigger_custom_layout)
        else:
            self.after_idle(self._setup_fixed_pane_behavior)

    def _create_left_pane(self):
        """Create the left pane."""
        if not self.left_builder:
            return

        # Choose parent based on layout type
        parent = self.layout_frame if self._has_fixed_panes else self.paned
        container = ttk.Frame(parent, style="Themed.TFrame")

        # Configure width based on settings
        width = self.left_config.fixed_width or self.left_config.default_width
        container.configure(width=width)

        # If fixed width is set, prevent resizing
        if self.left_config.fixed_width is not None:
            container.pack_propagate(False)

        # Header
        header = PaneHeader(
            container,
            self.left_config,
            "left",
            lambda: self._detach_pane("left"),
            None,  # No close callback for now
            self.theme_manager,
        )
        header.pack(fill="x", padx=0, pady=0)

        # Content frame
        content_frame = tk.Frame(
            container, bg=self.theme_manager.get_current_theme().colors.panel_content_bg
        )
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Build content
        self.left_builder(content_frame)

        # Store references
        self.pane_frames["left"] = container
        self.pane_headers["left"] = header
        self.pane_positions["left"] = 0  # Left pane is always at position 0
        self.pane_visibility["left"] = True

        # Add to layout
        if self._has_fixed_panes:
            # Custom layout - pane will be positioned by _handle_custom_resize
            pass
        else:
            # Add to paned window with appropriate weight
            weight = 0 if self.left_config.fixed_width is not None else 1
            self.paned.add(container, weight=weight)

        # Configure pane width constraints if fixed width is set
        # (only for TTK PanedWindow)
        if not self._has_fixed_panes and self.left_config.fixed_width is not None:
            self.paned.after_idle(
                lambda: self._configure_fixed_pane_width(
                    "left", self.left_config.fixed_width
                )
            )

    def _create_center_pane(self):
        """Create the center pane."""
        if not self.center_builder:
            return

        # Choose parent based on layout type
        parent = self.layout_frame if self._has_fixed_panes else self.paned
        container = ttk.Frame(parent, style="Themed.TFrame")

        # Header (if title is provided)
        if self.center_config.title:
            header = PaneHeader(
                container,
                self.center_config,
                "center",
                lambda: (
                    self._detach_pane("center")
                    if self.center_config.detachable
                    else None
                ),
                None,
                self.theme_manager,
            )
            header.pack(fill="x", padx=0, pady=0)
            self.pane_headers["center"] = header

        # Content frame
        content_frame = tk.Frame(
            container, bg=self.theme_manager.get_current_theme().colors.panel_content_bg
        )
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Build content
        self.center_builder(content_frame)

        # Store references
        self.pane_frames["center"] = container
        center_position = 1  # Center is typically at position 1
        if "left" not in self.pane_frames:
            center_position = 0  # If no left pane, center starts at 0
        self.pane_positions["center"] = center_position
        self.pane_visibility["center"] = True

        # Add to layout
        if self._has_fixed_panes:
            # Custom layout - pane will be positioned by _handle_custom_resize
            pass
        else:
            # Add to paned window
            self.paned.add(container, weight=3)

    def _create_right_pane(self):
        """Create the right pane."""
        if not self.right_builder:
            return

        # Choose parent based on layout type
        parent = self.layout_frame if self._has_fixed_panes else self.paned
        container = ttk.Frame(parent, style="Themed.TFrame")

        # Configure width based on settings
        width = self.right_config.fixed_width or self.right_config.default_width
        container.configure(width=width)

        # If fixed width is set, prevent resizing
        if self.right_config.fixed_width is not None:
            container.pack_propagate(False)

        # Header
        header = PaneHeader(
            container,
            self.right_config,
            "right",
            lambda: self._detach_pane("right"),
            None,  # No close callback for now
            self.theme_manager,
        )
        header.pack(fill="x", padx=0, pady=0)

        # Content frame
        content_frame = tk.Frame(
            container, bg=self.theme_manager.get_current_theme().colors.panel_content_bg
        )
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Build content
        self.right_builder(content_frame)

        # Store references
        self.pane_frames["right"] = container
        self.pane_headers["right"] = header
        # Right pane position depends on what other panes exist
        right_position = len(self.pane_frames)  # Will be the last position
        self.pane_positions["right"] = right_position
        self.pane_visibility["right"] = True

        # Add to layout
        if self._has_fixed_panes:
            # Custom layout - pane will be positioned by _handle_custom_resize
            pass
        else:
            # Add to paned window with appropriate weight
            weight = 0 if self.right_config.fixed_width is not None else 1
            self.paned.add(container, weight=weight)

        # Configure pane width constraints if fixed width is set
        # (only for TTK PanedWindow)
        if not self._has_fixed_panes and self.right_config.fixed_width is not None:
            self.paned.after_idle(
                lambda: self._configure_fixed_pane_width(
                    "right", self.right_config.fixed_width
                )
            )

    def _configure_pane_width(self, pane_side: str, width: int):
        """Configure a pane to have a specific width (but still resizable)."""
        if pane_side not in self.pane_frames:
            return

        container = self.pane_frames[pane_side]

        # Get the pane index in the PanedWindow
        pane_index = None
        for i, child in enumerate(self.paned.winfo_children()):
            if child == container:
                pane_index = i
                break

        if pane_index is not None:
            try:
                # Force update the layout first
                self.paned.update_idletasks()

                # Set the initial width but allow resizing
                self.paned.paneconfig(pane_index, width=width)

                # Set reasonable minimum size
                config = getattr(self, f"{pane_side}_config", None)
                if config:
                    self.paned.paneconfig(pane_index, minsize=config.min_width)

                # Force the paned window to respect the width multiple times
                for delay in [10, 50, 100, 200, 500]:
                    self.paned.after(
                        delay,
                        lambda w=width, idx=pane_index: self.paned.paneconfig(
                            idx, width=w
                        ),
                    )

                # Also try to force the container width
                container.configure(width=width)
                self.paned.after(10, lambda: container.configure(width=width))

            except tk.TclError:
                # Fallback: just set the container width
                container.configure(width=width)
                container.pack_propagate(False)

    def _configure_fixed_pane_width(self, pane_side: str, fixed_width: int):
        """
        Configure a pane to have a fixed width that cannot be resized by the user.

        This method sets both minimum and maximum width constraints to the same value,
        effectively preventing the pane from being resized through the sash.

        Args:
            pane_side (str): Which pane to configure ('left', 'center', 'right').
            fixed_width (int): The fixed width in pixels to set for the pane.
        """
        if pane_side not in self.pane_frames:
            return

        container = self.pane_frames[pane_side]

        # Get the pane index in the PanedWindow
        pane_index = None
        for i, child in enumerate(self.paned.winfo_children()):
            if child == container:
                pane_index = i
                break

        if pane_index is not None:
            # Configure the pane to have fixed width
            try:
                # Set minimum and maximum width to the same value to prevent resizing
                self.paned.paneconfig(
                    pane_index, minsize=fixed_width, width=fixed_width
                )
                # Try to set a maximum size if the ttk version supports it
                try:
                    self.paned.paneconfig(pane_index, maxsize=fixed_width)
                except tk.TclError:
                    # Some versions of ttk don't support maxsize, that's okay
                    pass
            except tk.TclError:
                # Fallback: just set the width
                container.configure(width=fixed_width)

    def _setup_fixed_pane_behavior(self):
        """Set up behavior for fixed-width and non-resizable panes."""
        try:
            # Force layout update
            self.paned.update_idletasks()

            # Configure each pane and store sash positions for fixed panes
            pane_configs = [
                ("left", self.left_config),
                ("center", self.center_config),
                ("right", self.right_config),
            ]

            for i, (pane_side, config) in enumerate(pane_configs):
                if pane_side not in self.pane_frames:
                    continue

                container = self.pane_frames[pane_side]

                # Find pane index in the PanedWindow
                pane_index = None
                for j, child in enumerate(self.paned.winfo_children()):
                    if child == container:
                        pane_index = j
                        break

                if pane_index is None:
                    continue

                # Configure pane constraints
                if config.fixed_width is not None:
                    # Fixed width pane
                    self.paned.paneconfig(
                        pane_index, minsize=config.fixed_width, width=config.fixed_width
                    )
                    try:
                        self.paned.paneconfig(pane_index, maxsize=config.fixed_width)
                    except tk.TclError:
                        pass

                elif not config.resizable:
                    # Non-resizable pane (use default width as fixed)
                    fixed_width = config.default_width
                    self.paned.paneconfig(
                        pane_index, minsize=fixed_width, width=fixed_width
                    )
                    try:
                        self.paned.paneconfig(pane_index, maxsize=fixed_width)
                    except tk.TclError:
                        pass

                else:
                    # Resizable pane - set reasonable constraints
                    self.paned.paneconfig(
                        pane_index, minsize=config.min_width, width=config.default_width
                    )

            # More aggressive approach: continuously monitor and reset sash positions
            self._monitor_sash_positions()

        except (tk.TclError, AttributeError):
            # Layout might not be ready yet
            pass

    def _monitor_sash_positions(self):
        """Continuously monitor and reset sash positions for fixed panes."""
        try:
            # Calculate expected sash positions based on fixed pane widths
            expected_positions = self._calculate_expected_sash_positions()

            # Check and reset sash positions if they've moved
            num_panes = len(self.paned.winfo_children())
            for i in range(num_panes - 1):  # Number of sashes = number of panes - 1
                try:
                    current_pos = self.paned.sashpos(i)
                    expected_pos = expected_positions.get(i)

                    if expected_pos is not None and abs(current_pos - expected_pos) > 2:
                        # Sash has moved from expected position, reset it
                        self.paned.sashpos(i, expected_pos)

                except tk.TclError:
                    pass

            # Schedule next check
            self.after(50, self._monitor_sash_positions)

        except (tk.TclError, AttributeError):
            # Widget might be destroyed, stop monitoring
            pass

    def _calculate_expected_sash_positions(self):
        """Calculate where sashes should be positioned based on fixed pane widths."""
        expected_positions = {}

        try:
            pane_configs = [
                ("left", self.left_config),
                ("center", self.center_config),
                ("right", self.right_config),
            ]

            # Get visible panes in order
            visible_panes = []
            for pane_side, config in pane_configs:
                if pane_side in self.pane_frames:
                    visible_panes.append((pane_side, config))

            # Calculate cumulative widths to determine sash positions
            cumulative_width = 0

            for i, (pane_side, config) in enumerate(
                visible_panes[:-1]
            ):  # Exclude last pane
                # Determine width for this pane
                if config.fixed_width is not None:
                    pane_width = config.fixed_width
                elif not config.resizable:
                    pane_width = config.default_width
                else:
                    # For resizable panes, get current width from the paned window
                    try:
                        container = self.pane_frames[pane_side]
                        pane_index = None
                        for j, child in enumerate(self.paned.winfo_children()):
                            if child == container:
                                pane_index = j
                                break
                        if pane_index is not None:
                            pane_width = container.winfo_width()
                        else:
                            pane_width = config.default_width
                    except (tk.TclError, AttributeError):
                        pane_width = config.default_width

                cumulative_width += pane_width
                expected_positions[i] = cumulative_width

        except (AttributeError, IndexError):
            pass

        return expected_positions

    def _setup_sash_disabling(self):
        """Try to disable sash interaction using various methods."""
        try:
            # Method 1: Override the sash cursor to indicate non-resizable
            self.paned.configure(cursor="arrow")  # Instead of resize cursor

            # Method 2: Bind to all mouse events on the paned window to
            # intercept sash interactions
            self.paned.bind("<Button-1>", self._intercept_sash_click, add=True)
            self.paned.bind("<B1-Motion>", self._intercept_sash_drag, add=True)
            self.paned.bind(
                "<Double-Button-1>", self._intercept_sash_double_click, add=True
            )

        except tk.TclError:
            pass

    def _intercept_sash_click(self, event):
        """Intercept sash clicks and prevent them for fixed panes."""
        try:
            # Check if click is on a sash that should be disabled
            if self._is_click_on_disabled_sash(event):
                return "break"  # Prevent the event from propagating
        except (tk.TclError, AttributeError):
            pass

    def _intercept_sash_drag(self, event):
        """Intercept sash drags and prevent them for fixed panes."""
        try:
            # Check if drag is on a sash that should be disabled
            if self._is_click_on_disabled_sash(event):
                return "break"  # Prevent the event from propagating
        except (tk.TclError, AttributeError):
            pass

    def _intercept_sash_double_click(self, event):
        """Intercept sash double-clicks and prevent them for fixed panes."""
        try:
            # Check if double-click is on a sash that should be disabled
            if self._is_click_on_disabled_sash(event):
                return "break"  # Prevent the event from propagating
        except (tk.TclError, AttributeError):
            pass

    def _is_click_on_disabled_sash(self, event):
        """Check if a click/drag event is on a sash that should be disabled."""
        try:
            num_panes = len(self.paned.winfo_children())

            for i in range(num_panes - 1):
                try:
                    sash_pos = self.paned.sashpos(i)
                    # Check if click is near this sash (within 5 pixels)
                    if abs(event.x - sash_pos) <= 5:
                        # Check if either adjacent pane is fixed
                        left_pane_fixed = self._is_pane_at_index_fixed(i)
                        right_pane_fixed = self._is_pane_at_index_fixed(i + 1)

                        if left_pane_fixed or right_pane_fixed:
                            return True  # This sash should be disabled

                except tk.TclError:
                    pass

        except (tk.TclError, AttributeError):
            pass

        return False

    def _is_pane_at_index_fixed(self, pane_index):
        """Check if a pane at the given index is fixed (non-resizable)."""
        try:
            pane_configs = [
                ("left", self.left_config),
                ("center", self.center_config),
                ("right", self.right_config),
            ]

            # Map pane index to config
            visible_panes = []
            for pane_side, config in pane_configs:
                if pane_side in self.pane_frames:
                    visible_panes.append((pane_side, config))

            if 0 <= pane_index < len(visible_panes):
                _, config = visible_panes[pane_index]
                return config.fixed_width is not None or not config.resizable

        except (AttributeError, IndexError):
            pass

        return False

    def _create_custom_layout(self):
        """Create custom layout for windows with fixed panes."""
        # Create a main container frame
        self.layout_frame = tk.Frame(
            self, bg=self.theme_manager.get_current_theme().colors.secondary_bg
        )
        self.layout_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Bind to resize events to handle layout
        self.layout_frame.bind("<Configure>", self._handle_custom_resize)

        # Create visual sashes (non-interactive)
        self._create_visual_sashes()

    def _create_visual_sashes(self):
        """
        Create visual sashes that look like PanedWindow sashes but aren't interactive.
        """
        theme = self.theme_manager.get_current_theme()

        # Left sash (between left and center)
        if self.left_builder and self.center_builder:
            self.left_sash = tk.Frame(
                self.layout_frame,
                bg=theme.colors.border,
                width=2,
                cursor="arrow",  # Non-resize cursor
            )

        # Right sash (between center and right)
        if self.center_builder and self.right_builder:
            self.right_sash = tk.Frame(
                self.layout_frame,
                bg=theme.colors.border,
                width=2,
                cursor="arrow",  # Non-resize cursor
            )

    def _handle_custom_resize(self, event=None):
        """Handle resize events for custom layout."""
        if not hasattr(self, "layout_frame"):
            return

        try:
            container_width, container_height = self._get_container_dimensions()
            if not self._is_container_ready(container_width, container_height):
                return

            # Get attachment states and calculate dimensions
            attachment_states = self._get_pane_attachment_states()
            pane_widths = self._calculate_pane_widths(
                container_width, attachment_states
            )

            # Position all panes
            self._position_panes(pane_widths, container_height, attachment_states)

        except (tk.TclError, AttributeError):
            # Layout not ready or widget destroyed
            pass

    def _get_container_dimensions(self):
        """Get the container dimensions."""
        container_width = self.layout_frame.winfo_width()
        container_height = self.layout_frame.winfo_height()
        return container_width, container_height

    def _is_container_ready(self, width, height):
        """Check if container dimensions are ready for layout."""
        return width > 1 and height > 1

    def _get_pane_attachment_states(self):
        """Get the attachment state for all panes."""
        return {
            "left": self.left_builder and "left" in self.pane_frames,
            "center": self.center_builder and "center" in self.pane_frames,
            "right": self.right_builder and "right" in self.pane_frames,
        }

    def _calculate_pane_widths(self, container_width, attachment_states):
        """Calculate widths for all panes based on their configurations."""
        sash_width = 2

        # Calculate individual pane widths
        left_width = self._calculate_left_pane_width(attachment_states["left"])
        right_width = self._calculate_right_pane_width(attachment_states["right"])

        # Calculate sashes width
        sashes_width = self._calculate_sashes_width(attachment_states, sash_width)

        # Calculate center width (remaining space)
        center_width = container_width - left_width - right_width - sashes_width
        center_width = max(center_width, 50)  # Ensure minimum width

        return {
            "left": left_width,
            "center": center_width,
            "right": right_width,
            "sash": sash_width,
        }

    def _calculate_left_pane_width(self, left_attached):
        """Calculate the width for the left pane."""
        if not left_attached:
            return 0

        if self.left_config.fixed_width is not None:
            return self.left_config.fixed_width
        else:
            return self.left_config.default_width

    def _calculate_right_pane_width(self, right_attached):
        """Calculate the width for the right pane."""
        if not right_attached:
            return 0

        if self.right_config.fixed_width is not None:
            return self.right_config.fixed_width
        else:
            return self.right_config.default_width

    def _calculate_sashes_width(self, attachment_states, sash_width):
        """Calculate the total width needed for sashes."""
        sashes_width = 0
        if attachment_states["left"] and attachment_states["center"]:
            sashes_width += sash_width
        if attachment_states["center"] and attachment_states["right"]:
            sashes_width += sash_width
        return sashes_width

    def _position_panes(self, pane_widths, container_height, attachment_states):
        """Position all panes and sashes."""
        x_pos = 0

        # Position left pane and its sash
        if attachment_states["left"]:
            x_pos = self._position_left_pane(
                x_pos, pane_widths, container_height, attachment_states
            )

        # Position center pane and its sash
        if attachment_states["center"]:
            x_pos = self._position_center_pane(
                x_pos, pane_widths, container_height, attachment_states
            )

        # Position right pane
        if attachment_states["right"]:
            self._position_right_pane(x_pos, pane_widths, container_height)

    def _position_left_pane(
        self, x_pos, pane_widths, container_height, attachment_states
    ):
        """Position the left pane and its sash."""
        # Position left pane
        self.pane_frames["left"].place(
            x=x_pos, y=0, width=pane_widths["left"], height=container_height
        )
        x_pos += pane_widths["left"]

        # Position left sash if center is attached
        if attachment_states["center"] and hasattr(self, "left_sash"):
            self.left_sash.place(
                x=x_pos, y=0, width=pane_widths["sash"], height=container_height
            )
            x_pos += pane_widths["sash"]
        elif hasattr(self, "left_sash"):
            self.left_sash.place_forget()

        return x_pos

    def _position_center_pane(
        self, x_pos, pane_widths, container_height, attachment_states
    ):
        """Position the center pane and its sash."""
        # Position center pane
        self.pane_frames["center"].place(
            x=x_pos, y=0, width=pane_widths["center"], height=container_height
        )
        x_pos += pane_widths["center"]

        # Position right sash if right is attached
        if attachment_states["right"] and hasattr(self, "right_sash"):
            self.right_sash.place(
                x=x_pos, y=0, width=pane_widths["sash"], height=container_height
            )
            x_pos += pane_widths["sash"]
        elif hasattr(self, "right_sash"):
            self.right_sash.place_forget()

        return x_pos

    def _position_right_pane(self, x_pos, pane_widths, container_height):
        """Position the right pane."""
        self.pane_frames["right"].place(
            x=x_pos, y=0, width=pane_widths["right"], height=container_height
        )

    def _trigger_custom_layout(self):
        """Trigger the initial custom layout."""
        if hasattr(self, "layout_frame"):
            self._handle_custom_resize()

    def _detach_pane(self, pane_side: str):
        """Detach a pane to a separate window."""
        if pane_side in self.detached_windows:
            return  # Already detached

        # Get configuration and builder
        config = getattr(self, f"{pane_side}_config")
        builder = getattr(self, f"{pane_side}_builder")

        if not config.detachable or not builder:
            return

        # Store the original position before removing
        original_position = self.pane_positions.get(pane_side, 0)

        # Remove from layout
        if pane_side in self.pane_frames:
            if self._has_fixed_panes:
                # Custom layout - just hide the pane
                self.pane_frames[pane_side].place_forget()
            else:
                # TTK PanedWindow layout
                self.paned.forget(self.pane_frames[pane_side])

            self.pane_frames[pane_side].destroy()
            del self.pane_frames[pane_side]
            # Keep the position info for reattaching
            self.pane_positions[f"{pane_side}_detached"] = original_position

            # Trigger layout update for custom layout
            if self._has_fixed_panes:
                self.after_idle(self._handle_custom_resize)

        # Create detached window
        detached_window = DetachedWindow(
            self.winfo_toplevel(),
            pane_side,
            config,
            builder,
            lambda: self._reattach_pane(pane_side),
            self.theme_manager,
            layout_instance=self,
        )

        self.detached_windows[pane_side] = detached_window

        # Position the window nicely
        self._position_detached_window(detached_window, pane_side)

    def _reattach_pane(self, pane_side: str):
        """Reattach a detached pane."""
        if pane_side not in self.detached_windows:
            return

        # Get the original position
        original_position = self.pane_positions.get(f"{pane_side}_detached", 0)

        # Destroy detached window
        self.detached_windows[pane_side].destroy()
        del self.detached_windows[pane_side]

        # Clean up position tracking
        if f"{pane_side}_detached" in self.pane_positions:
            del self.pane_positions[f"{pane_side}_detached"]

        # Recreate the pane at the correct position
        if pane_side == "left":
            self._reattach_left_pane(original_position)
        elif pane_side == "right":
            self._reattach_right_pane(original_position)
        elif pane_side == "center":
            self._reattach_center_pane(original_position)

    def _position_detached_window(self, window: DetachedWindow, pane_side: str):
        """Position a detached window nicely."""
        # Get main window position
        main_window = self.winfo_toplevel()
        main_window.update_idletasks()

        main_x = main_window.winfo_x()
        main_y = main_window.winfo_y()
        main_width = main_window.winfo_width()

        # Calculate position based on pane side
        if pane_side == "left":
            x = main_x - window.config.default_width - 10
            y = main_y
        elif pane_side == "right":
            x = main_x + main_width + 10
            y = main_y
        else:  # center
            x = main_x + (main_width - window.config.default_width) // 2
            y = main_y - 50

        # Ensure window is on screen
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = max(0, min(x, screen_width - window.config.default_width))
        y = max(0, min(y, screen_height - 400))

        window.geometry(f"{window.config.default_width}x400+{x}+{y}")

        # Ensure detached window appears in front
        window.lift()
        window.focus_force()
        window.attributes("-topmost", True)
        window.after(100, lambda: window.attributes("-topmost", False))

    def _reattach_left_pane(self, position: int):
        """Reattach the left pane at the correct position."""
        if not self.left_builder:
            return

        # Choose parent based on layout type
        parent = self.layout_frame if self._has_fixed_panes else self.paned
        container = ttk.Frame(parent, style="Themed.TFrame")

        # Configure width based on settings
        width = self.left_config.fixed_width or self.left_config.default_width
        container.configure(width=width)

        # If fixed width is set, prevent resizing
        if self.left_config.fixed_width is not None:
            container.pack_propagate(False)

        # Header
        header = PaneHeader(
            container,
            self.left_config,
            "left",
            lambda: self._detach_pane("left"),
            None,
            self.theme_manager,
        )
        header.pack(fill="x", padx=0, pady=0)

        # Content frame
        content_frame = tk.Frame(
            container, bg=self.theme_manager.get_current_theme().colors.panel_content_bg
        )
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Build content
        self.left_builder(content_frame)

        # Store references
        self.pane_frames["left"] = container
        self.pane_headers["left"] = header
        self.pane_positions["left"] = position

        # Add to layout
        if self._has_fixed_panes:
            # Custom layout - trigger resize to position pane
            self.after_idle(self._handle_custom_resize)
        else:
            # Insert at the correct position (left should always be at position 0)
            weight = 0 if self.left_config.fixed_width is not None else 1
            self.paned.insert(0, container, weight=weight)

            # Configure pane width constraints
            if self.left_config.fixed_width is not None:
                self.paned.after_idle(
                    lambda: self._configure_fixed_pane_width(
                        "left", self.left_config.fixed_width
                    )
                )
            else:
                # Configure default width for non-fixed panes
                self.paned.after_idle(
                    lambda: self._configure_pane_width(
                        "left", self.left_config.default_width
                    )
                )

    def _reattach_right_pane(self, position: int):
        """Reattach the right pane at the correct position."""
        if not self.right_builder:
            return

        # Choose parent based on layout type
        parent = self.layout_frame if self._has_fixed_panes else self.paned
        container = ttk.Frame(parent, style="Themed.TFrame")

        # Configure width based on settings
        width = self.right_config.fixed_width or self.right_config.default_width
        container.configure(width=width)

        # If fixed width is set, prevent resizing
        if self.right_config.fixed_width is not None:
            container.pack_propagate(False)

        # Header
        header = PaneHeader(
            container,
            self.right_config,
            "right",
            lambda: self._detach_pane("right"),
            None,
            self.theme_manager,
        )
        header.pack(fill="x", padx=0, pady=0)

        # Content frame
        content_frame = tk.Frame(
            container, bg=self.theme_manager.get_current_theme().colors.panel_content_bg
        )
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Build content
        self.right_builder(content_frame)

        # Store references
        self.pane_frames["right"] = container
        self.pane_headers["right"] = header
        self.pane_positions["right"] = position

        # Add to layout
        if self._has_fixed_panes:
            # Custom layout - trigger resize to position pane
            self.after_idle(self._handle_custom_resize)
        else:
            # Insert at the end (right pane should be last)
            weight = 0 if self.right_config.fixed_width is not None else 1
            self.paned.add(container, weight=weight)

            # Configure pane width constraints
            if self.right_config.fixed_width is not None:
                self.paned.after_idle(
                    lambda: self._configure_fixed_pane_width(
                        "right", self.right_config.fixed_width
                    )
                )
            else:
                # Configure default width for non-fixed panes
                self.paned.after_idle(
                    lambda: self._configure_pane_width(
                        "right", self.right_config.default_width
                    )
                )

    def _reattach_center_pane(self, position: int):
        """Reattach the center pane at the correct position."""
        if not self.center_builder:
            return

        # Choose parent based on layout type
        parent = self.layout_frame if self._has_fixed_panes else self.paned
        container = ttk.Frame(parent, style="Themed.TFrame")

        # Header (if title is provided)
        if self.center_config.title:
            header = PaneHeader(
                container,
                self.center_config,
                "center",
                lambda: (
                    self._detach_pane("center")
                    if self.center_config.detachable
                    else None
                ),
                None,
                self.theme_manager,
            )
            header.pack(fill="x", padx=0, pady=0)
            self.pane_headers["center"] = header

        # Content frame
        content_frame = tk.Frame(
            container, bg=self.theme_manager.get_current_theme().colors.panel_content_bg
        )
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Build content
        self.center_builder(content_frame)

        # Store references
        self.pane_frames["center"] = container
        self.pane_positions["center"] = position

        # Add to layout
        if self._has_fixed_panes:
            # Custom layout - trigger resize to position pane
            self.after_idle(self._handle_custom_resize)
        else:
            # Insert at the correct position (center should be between left and right)
            insert_position = 0
            if "left" in self.pane_frames:
                insert_position = 1

            self.paned.insert(insert_position, container, weight=3)

    def set_theme(self, theme_name):
        """Change the theme."""
        # Handle ThemeType enum or string
        if hasattr(theme_name, "value"):
            theme_name = theme_name.value
        else:
            theme_name = str(theme_name)

        if self.theme_manager.set_theme(theme_name):
            self._refresh_theme()

    def _refresh_theme(self):
        """Refresh the theme for all components."""
        self._setup_styles()
        theme = self.theme_manager.get_current_theme()

        # Update main components
        self._refresh_main_container(theme)
        self._refresh_paned_window()
        self._refresh_toolbar(theme)
        self._refresh_status_bar(theme)

        # Update pane components
        self._refresh_pane_headers()
        self._refresh_pane_content_frames(theme)
        self._refresh_detached_windows()

        # Update custom widgets and force refresh
        self._refresh_custom_widgets()
        self.update_idletasks()

    def _refresh_main_container(self, theme):
        """Refresh the main container background."""
        self.configure(bg=theme.colors.secondary_bg)

    def _refresh_paned_window(self):
        """Refresh the paned window style."""
        if hasattr(self, "paned"):
            self.paned.configure(style="Themed.TPanedwindow")

    def _refresh_toolbar(self, theme):
        """Refresh the toolbar and its buttons."""
        if not (hasattr(self, "toolbar_frame") and self.toolbar_frame):
            return

        self.toolbar_frame.configure(bg=theme.colors.primary_bg)

        # Update toolbar buttons
        for child in self.toolbar_frame.winfo_children():
            if isinstance(child, tk.Button):
                child.configure(
                    bg=theme.colors.button_bg,
                    fg=theme.colors.button_fg,
                    activebackground=theme.colors.button_hover,
                )

    def _refresh_status_bar(self, theme):
        """Refresh the status bar and its label."""
        if not (hasattr(self, "status_bar") and self.status_bar):
            return

        self.status_bar.configure(bg=theme.colors.primary_bg)

        if hasattr(self, "status_label") and self.status_label:
            self.status_label.configure(
                bg=theme.colors.primary_bg, fg=theme.colors.primary_text
            )

    def _refresh_pane_headers(self):
        """Refresh all pane headers."""
        for pane_side, header in self.pane_headers.items():
            if header:
                header.refresh_theme()

    def _refresh_pane_content_frames(self, theme):
        """Refresh pane content frames."""
        for pane_side, frame in self.pane_frames.items():
            if frame:
                self._refresh_pane_content_children(frame, theme)

    def _refresh_pane_content_children(self, frame, theme):
        """Refresh children of a pane content frame."""
        for child in frame.winfo_children():
            if isinstance(child, tk.Frame) and not isinstance(child, PaneHeader):
                child.configure(bg=theme.colors.panel_content_bg)

    def _refresh_detached_windows(self):
        """Refresh all detached windows."""
        for window in self.detached_windows.values():
            window.theme_manager = self.theme_manager
            if hasattr(window, "refresh_theme"):
                window.refresh_theme()

    def get_pane_frame(self, pane_side: str) -> Optional[tk.Frame]:
        """Get the content frame for a pane."""
        if pane_side in self.detached_windows:
            return self.detached_windows[pane_side].content_frame
        elif pane_side in self.pane_frames:
            # Find the content frame within the pane frame
            for child in self.pane_frames[pane_side].winfo_children():
                if isinstance(child, tk.Frame) and child != self.pane_headers.get(
                    pane_side
                ):
                    return child
        return None

    def is_pane_detached(self, pane_side: str) -> bool:
        """Check if a pane is detached."""
        return pane_side in self.detached_windows

    def set_pane_fixed_width(self, pane_side: str, width: int):
        """Set a pane to have a fixed width."""
        if pane_side == "left":
            self.left_config.fixed_width = width
        elif pane_side == "right":
            self.right_config.fixed_width = width
        else:
            return  # Center pane doesn't support fixed width

        # Apply the change if pane is currently attached
        if pane_side in self.pane_frames:
            container = self.pane_frames[pane_side]
            container.configure(width=width)
            container.pack_propagate(False)
            self.after_idle(lambda: self._configure_fixed_pane_width(pane_side, width))

    def clear_pane_fixed_width(self, pane_side: str):
        """Remove fixed width constraint from a pane."""
        if pane_side == "left":
            self.left_config.fixed_width = None
        elif pane_side == "right":
            self.right_config.fixed_width = None
        else:
            return  # Center pane doesn't support fixed width

        # Apply the change if pane is currently attached
        if pane_side in self.pane_frames:
            container = self.pane_frames[pane_side]
            container.pack_propagate(True)

            # Reset pane configuration to allow resizing
            for i, child in enumerate(self.paned.winfo_children()):
                if child == container:
                    try:
                        self.paned.paneconfig(i, minsize=50)  # Set reasonable minimum
                        # Remove maxsize if it was set
                        try:
                            self.paned.paneconfig(i, maxsize=0)  # 0 means no limit
                        except tk.TclError:
                            pass
                    except tk.TclError:
                        pass
                    break

    def is_pane_fixed_width(self, pane_side: str) -> bool:
        """Check if a pane has fixed width."""
        if pane_side == "left":
            return self.left_config.fixed_width is not None
        elif pane_side == "right":
            return self.right_config.fixed_width is not None
        return False

    def get_pane_width(self, pane_side: str) -> int:
        """Get the current width of a pane."""
        if pane_side == "left":
            return self.left_config.fixed_width or self.left_config.default_width
        elif pane_side == "right":
            return self.right_config.fixed_width or self.right_config.default_width
        elif pane_side == "center" and pane_side in self.pane_frames:
            return self.pane_frames[pane_side].winfo_width()
        return 0

    def _create_toolbar(self):
        """Create the toolbar."""
        theme = self.theme_manager.get_current_theme()

        self.toolbar = tk.Frame(
            self, bg=theme.colors.secondary_bg, height=32, relief="flat"
        )
        self.toolbar.pack(fill=tk.X, padx=2, pady=(2, 0))
        self.toolbar.pack_propagate(False)

        # Add some basic toolbar content
        toolbar_label = tk.Label(
            self.toolbar,
            text="Toolbar",
            bg=theme.colors.secondary_bg,
            fg=theme.colors.primary_text,
            font=(theme.typography.font_family, theme.typography.font_size_small),
        )
        toolbar_label.pack(side=tk.LEFT, padx=8, pady=4)

    def _create_status_bar(self):
        """Create the status bar."""
        theme = self.theme_manager.get_current_theme()

        self.status_bar = tk.Frame(
            self, bg=theme.colors.secondary_bg, height=24, relief="sunken", bd=1
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=2, pady=(0, 2))
        self.status_bar.pack_propagate(False)

        # Add some basic status bar content
        self.status_label = tk.Label(
            self.status_bar,
            text="Ready",
            bg=theme.colors.secondary_bg,
            fg=theme.colors.secondary_text,
            font=(theme.typography.font_family, theme.typography.font_size_small),
        )
        self.status_label.pack(side=tk.LEFT, padx=8, pady=2)

    def get_left_frame(self):
        """Get the left pane content frame."""
        return self.get_pane_frame("left")

    def get_center_frame(self):
        """Get the center pane content frame."""
        return self.get_pane_frame("center")

    def get_right_frame(self):
        """Get the right pane content frame."""
        return self.get_pane_frame("right")

    def update_status(self, message: str):
        """Update the status bar message."""
        if hasattr(self, "status_label") and self.status_label:
            self.status_label.configure(text=message)
        elif hasattr(self, "status_bar") and self.status_bar:
            # Fallback: Find the status label and update it
            for child in self.status_bar.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(text=message)
                    break
        else:
            # If no status bar, log the status message
            logger.debug("Status: %s", message)

    def show_left_pane(self):
        """Show the left pane if it's hidden."""
        if "left" in self.pane_frames and "left" not in self.detached_windows:
            # For PanedWindow, we need to add it back to the paned widget
            if not self.pane_visibility.get("left", False):
                # Insert at the beginning (left position)
                self.paned.insert(0, self.pane_frames["left"])
                self.pane_visibility["left"] = True
                # Restore proper width
                self.paned.after_idle(
                    lambda: self._configure_pane_width(
                        "left", self.left_config.default_width
                    )
                )
        elif "left" in self.detached_windows:
            # If detached, bring window to front
            self.detached_windows["left"].lift()

    def hide_left_pane(self):
        """Hide the left pane."""
        if "left" in self.pane_frames and "left" not in self.detached_windows:
            # For PanedWindow, we remove it from the paned widget
            try:
                if self.pane_visibility.get("left", False):
                    self.paned.forget(self.pane_frames["left"])
                    self.pane_visibility["left"] = False
            except tk.TclError:
                # Pane might not be managed by the PanedWindow
                pass

    def toggle_left_pane(self):
        """Toggle the visibility of the left pane."""
        if "left" in self.pane_frames and "left" not in self.detached_windows:
            # Check if it's currently visible using our tracking
            if self.pane_visibility.get("left", False):
                self.hide_left_pane()
            else:
                self.show_left_pane()
        elif "left" in self.detached_windows:
            # If detached, toggle window visibility
            detached_window = self.detached_windows["left"]
            if detached_window.state() == "normal":
                detached_window.withdraw()
            else:
                detached_window.deiconify()
                detached_window.lift()

    def show_right_pane(self):
        """Show the right pane if it's hidden."""
        if "right" in self.pane_frames and "right" not in self.detached_windows:
            # For PanedWindow, we need to add it back to the paned widget
            if not self.pane_visibility.get("right", False):
                # Insert at the end (right position)
                self.paned.add(self.pane_frames["right"])
                self.pane_visibility["right"] = True
                # Restore proper width
                self.paned.after_idle(
                    lambda: self._configure_pane_width(
                        "right", self.right_config.default_width
                    )
                )
        elif "right" in self.detached_windows:
            # If detached, bring window to front
            self.detached_windows["right"].lift()

    def hide_right_pane(self):
        """Hide the right pane."""
        if "right" in self.pane_frames and "right" not in self.detached_windows:
            # For PanedWindow, we remove it from the paned widget
            try:
                if self.pane_visibility.get("right", False):
                    self.paned.forget(self.pane_frames["right"])
                    self.pane_visibility["right"] = False
            except tk.TclError:
                # Pane might not be managed by the PanedWindow
                pass

    def toggle_right_pane(self):
        """Toggle the visibility of the right pane."""
        if "right" in self.pane_frames and "right" not in self.detached_windows:
            # Check if it's currently visible using our tracking
            if self.pane_visibility.get("right", False):
                self.hide_right_pane()
            else:
                self.show_right_pane()
        elif "right" in self.detached_windows:
            # If detached, toggle window visibility
            detached_window = self.detached_windows["right"]
            if detached_window.state() == "normal":
                detached_window.withdraw()
            else:
                detached_window.deiconify()
                detached_window.lift()

    def show_center_pane(self):
        """Show the center pane if it's hidden."""
        if "center" in self.pane_frames and "center" not in self.detached_windows:
            # For PanedWindow, we need to add it back to the paned widget
            if self.pane_frames["center"] not in self.paned.winfo_children():
                # Insert in the middle position
                children = list(self.paned.winfo_children())
                insert_pos = 1 if len(children) > 0 else 0
                self.paned.insert(insert_pos, self.pane_frames["center"])

    def hide_center_pane(self):
        """Hide the center pane."""
        if "center" in self.pane_frames and "center" not in self.detached_windows:
            # For PanedWindow, we remove it from the paned widget
            try:
                if self.pane_frames["center"] in self.paned.winfo_children():
                    self.paned.forget(self.pane_frames["center"])
            except tk.TclError:
                # Pane might not be managed by the PanedWindow
                pass

    def toggle_center_pane(self):
        """Toggle the visibility of the center pane."""
        if "center" in self.pane_frames and "center" not in self.detached_windows:
            # Check if it's currently in the paned window
            if self.pane_frames["center"] in self.paned.winfo_children():
                self.hide_center_pane()
            else:
                self.show_center_pane()

    def is_pane_visible(self, pane_side: str) -> bool:
        """
        Check if a pane is currently visible.

        Args:
            pane_side (str): Which pane to check ('left', 'center', 'right').

        Returns:
            bool: True if the pane is visible (either attached or detached), False otherwise.
        """
        if pane_side in self.pane_frames:
            if pane_side in self.detached_windows:
                # If detached, check window state
                return self.detached_windows[pane_side].state() == "normal"
            else:
                # If attached, use our visibility tracking
                return self.pane_visibility.get(pane_side, False)
        return False

    def get_status_text(self) -> str:
        """Get the current status bar text."""
        if hasattr(self, "status_label") and self.status_label:
            return self.status_label.cget("text")
        elif hasattr(self, "status_bar") and self.status_bar:
            for child in self.status_bar.winfo_children():
                if isinstance(child, tk.Label):
                    return child.cget("text")
        return ""

    def set_status_text(self, text: str):
        """Set the status bar text (alias for update_status)."""
        self.update_status(text)

    def add_toolbar_button(self, text: str, command, tooltip: str = ""):
        """
        Add a button to the toolbar.

        Args:
            text (str): The text to display on the button.
            command: The function to call when the button is clicked.
            tooltip (str): Tooltip text for the button (currently unused but reserved).
        """
        if hasattr(self, "toolbar") and self.toolbar:
            theme = self.theme_manager.get_current_theme()

            btn = tk.Button(
                self.toolbar,
                text=text,
                command=command,
                bg=theme.colors.secondary_bg,
                fg=theme.colors.primary_text,
                relief="flat",
                bd=1,
                font=(theme.typography.font_family, theme.typography.font_size_small),
            )
            btn.pack(side=tk.LEFT, padx=2, pady=2)

            # Add hover effects
            def on_enter(e):
                btn.configure(bg=theme.colors.accent_bg, fg=theme.colors.accent_text)

            def on_leave(e):
                btn.configure(
                    bg=theme.colors.secondary_bg, fg=theme.colors.primary_text
                )

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

            return btn
        return None

    def clear_toolbar(self):
        """Clear all buttons from the toolbar."""
        if hasattr(self, "toolbar") and self.toolbar:
            for child in list(self.toolbar.winfo_children()):
                if isinstance(child, tk.Button):
                    child.destroy()

    def add_status_widget(self, widget):
        """Add a widget to the status bar."""
        if hasattr(self, "status_bar") and self.status_bar:
            widget.pack(side=tk.RIGHT, padx=4, pady=2)

    def get_theme_name(self) -> str:
        """Get the current theme name."""
        return (
            self.theme_manager.current_theme.name
            if self.theme_manager.current_theme
            else "unknown"
        )

    def get_available_themes(self) -> list:
        """
        Get list of available theme names.

        Returns:
            list: List of theme names that can be used with switch_theme().
        """
        return ["light", "dark", "blue"]  # Based on the themes available

    def refresh_ui(self):
        """Refresh the entire UI (useful after theme changes)."""
        self._refresh_theme()
        self.update_idletasks()

    def _refresh_custom_widgets(self):
        """Refresh custom widgets (text, scrollbars, etc.) in all panes."""
        current_theme = self.theme_manager.get_current_theme()
        for pane_side in ["left", "center", "right"]:
            # Only update attached panes - detached panes are handled by their
            # refresh_theme method
            if pane_side not in self.detached_windows:
                frame = self.get_pane_content_frame(pane_side)
                if frame and hasattr(frame, "update_theme"):
                    try:
                        # Call the frame's update_theme method with current theme name
                        frame.update_theme(current_theme.name)
                    except Exception as e:
                        logger.error(
                            "Error updating theme for %s pane: %s", pane_side, e
                        )

    def get_pane_content_frame(self, pane_side: str) -> Optional[tk.Frame]:
        """
        Get the content frame for a specific pane.

        This method provides access to the frame where pane content is displayed,
        useful for adding widgets or updating content dynamically.

        Args:
            pane_side (str): Which pane to get ('left', 'center', 'right').

        Returns:
            Optional[tk.Frame]: The content frame for the specified pane, or None if not found.
        """
        if pane_side == "center":
            return self.get_center_frame()
        elif pane_side == "left":
            return self.get_left_frame()
        elif pane_side == "right":
            return self.get_right_frame()
        return None

    def switch_theme(self, theme_name: str, update_status: bool = True) -> bool:
        """
        Switch to a new theme and automatically update all widgets.

        Args:
            theme_name: Name of the theme to switch to
            update_status: Whether to update the status bar with theme info

        Returns:
            bool: True if theme was successfully switched, False otherwise
        """
        # Set the theme
        if self.theme_manager.set_theme(theme_name, window=self.master):
            # Refresh the UI
            self.refresh_ui()

            # Update status bar if requested and available
            if update_status and hasattr(self, "update_status"):
                platform_info = self.theme_manager.get_platform_info()
                status_text = (
                    f"Theme: {theme_name} | Platform: {platform_info['platform']} | "
                    f"Scrollbars: {platform_info['scrollbar_type']}"
                )
                self.update_status(status_text)

            return True
        else:
            logger.warning("Failed to set theme '%s'", theme_name)
            return False

    def create_themed_scrollbar(
        self, parent, orient="vertical", command=None, **kwargs
    ):
        """
        Create a platform-appropriate themed scrollbar.

        This method automatically chooses between custom and native scrollbars
        based on the current platform for optimal user experience.

        Args:
            parent: Parent widget
            orient: Scrollbar orientation ("vertical" or "horizontal")
            command: Scroll command callback
            **kwargs: Additional arguments

        Returns:
            Scrollbar widget (custom or native based on platform)
        """
        return self.theme_manager.create_themed_scrollbar_auto(
            parent=parent, orient=orient, command=command, **kwargs
        )

    def get_platform_info(self) -> Dict[str, str]:
        """
        Get platform information including recommended scrollbar type.

        Returns:
            Dict[str, str]: Dictionary containing platform details such as:
                - 'platform': Operating system name
                - 'scrollbar_type': Recommended scrollbar type for this platform
                - Other platform-specific information
        """
        return self.theme_manager.get_platform_info()
