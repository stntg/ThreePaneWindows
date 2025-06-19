"""
Enhanced Professional Dockable Three-Pane Window.

This module provides a sophisticated, highly customizable three-pane window
with professional theming, smooth animations, and intuitive drag-and-drop
detaching/attaching functionality.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Dict
from dataclasses import dataclass
from .themes import ThemeManager, get_theme_manager


@dataclass
class PaneConfig:
    """Configuration for a pane."""

    title: str = ""
    icon: str = ""
    min_width: int = 100
    max_width: int = 500
    default_width: int = 200
    resizable: bool = True
    detachable: bool = True
    closable: bool = False
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
        """Setup the drag handle UI."""
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
                    width=2,
                    height=2,
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
        """Handle mouse enter."""
        theme = self.theme_manager.get_current_theme()
        self.configure(bg=theme.colors.accent_bg)
        self.grip_frame.configure(bg=theme.colors.accent_bg)

    def _on_leave(self, event):
        """Handle mouse leave."""
        if not self.is_dragging:
            theme = self.theme_manager.get_current_theme()
            self.configure(bg=theme.colors.panel_header_bg)
            self.grip_frame.configure(bg=theme.colors.panel_header_bg)

    def _on_drag_start(self, event):
        """Handle drag start."""
        self.is_dragging = False
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root

    def _on_drag_motion(self, event):
        """Handle drag motion."""
        if not self.is_dragging:
            # Check if we've moved enough to start dragging
            dx = abs(event.x_root - self.drag_start_x)
            dy = abs(event.y_root - self.drag_start_y)

            if dx > self.drag_threshold or dy > self.drag_threshold:
                self.is_dragging = True
                self._start_drag_visual()

    def _on_drag_end(self, event):
        """Handle drag end."""
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
        super().__init__(parent, **kwargs)
        self.config = config
        self.pane_side = pane_side
        self.on_detach = on_detach
        self.on_close = on_close
        self.theme_manager = theme_manager

        self._setup_ui()

    def _setup_ui(self):
        """Setup the header UI."""
        theme = self.theme_manager.get_current_theme()
        style = self.theme_manager.get_style("panel_header")

        self.configure(bg=style["bg"], height=32, relief="flat")

        # Left side - icon and title
        left_frame = tk.Frame(self, bg=style["bg"])
        left_frame.pack(side="left", fill="y", padx=8, pady=4)

        if self.config.icon:
            icon_label = tk.Label(
                left_frame,
                text=self.config.icon,
                bg=style["bg"],
                fg=style["fg"],
                font=(theme.typography.font_family, theme.typography.font_size_normal),
            )
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

    def _create_control_button(
        self, parent, text: str, command: Callable, tooltip: str
    ) -> tk.Button:
        """Create a control button."""
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


class DetachedWindow(tk.Toplevel):
    """Professional detached window for panes."""

    def __init__(
        self,
        parent,
        pane_side: str,
        config: PaneConfig,
        content_builder: Callable,
        on_reattach: Callable,
        theme_manager: ThemeManager,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        self.pane_side = pane_side
        self.config = config
        self.content_builder = content_builder
        self.on_reattach = on_reattach
        self.theme_manager = theme_manager

        self._setup_window()
        self._setup_ui()

    def _setup_window(self):
        """Setup the detached window."""
        theme = self.theme_manager.get_current_theme()

        # Window properties
        self.title(f"{self.config.title or self.pane_side.title()} Panel")
        self.geometry(f"{self.config.default_width}x400")
        self.minsize(self.config.min_width, 200)

        if self.config.max_width > 0:
            self.maxsize(self.config.max_width, 2000)

        # Window styling
        self.configure(bg=theme.colors.primary_bg)

        # Window icon (if available)
        if self.config.icon:
            try:
                # Set window icon if icon file exists
                self.iconbitmap(self.config.icon)
            except (tk.TclError, FileNotFoundError) as e:
                # Icon file not found or invalid format - continue without icon
                print(f"Warning: Could not set window icon '{self.config.icon}': {e}")
            except Exception as e:
                # Unexpected error - log it but continue
                print(f"Unexpected error setting window icon: {e}")

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_window_close)

        # Make window appear professional
        self.transient(self.master)
        self.focus_set()

    def _setup_ui(self):
        """Setup the UI."""
        theme = self.theme_manager.get_current_theme()

        # Header with reattach button
        header_frame = tk.Frame(self, bg=theme.colors.panel_header_bg, height=32)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        # Title
        if self.config.title:
            title_label = tk.Label(
                header_frame,
                text=(
                    f"{self.config.icon} {self.config.title}"
                    if self.config.icon
                    else self.config.title
                ),
                bg=theme.colors.panel_header_bg,
                fg=theme.colors.panel_header_fg,
                font=(
                    theme.typography.font_family,
                    theme.typography.font_size_normal,
                    "bold",
                ),
            )
            title_label.pack(side="left", padx=8, pady=6)

        # Reattach button
        reattach_btn = tk.Button(
            header_frame,
            text="⧈ Reattach",
            command=self.on_reattach,
            bg=theme.colors.button_bg,
            fg=theme.colors.button_fg,
            activebackground=theme.colors.button_hover,
            activeforeground=theme.colors.button_fg,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            font=(theme.typography.font_family, theme.typography.font_size_small),
        )
        reattach_btn.pack(side="right", padx=8, pady=4)

        # Separator
        separator = tk.Frame(self, bg=theme.colors.separator, height=1)
        separator.pack(fill="x")

        # Content frame
        self.content_frame = tk.Frame(self, bg=theme.colors.panel_content_bg)
        self.content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Build content
        if self.content_builder:
            self.content_builder(self.content_frame)

    def _on_window_close(self):
        """Handle window close."""
        self.on_reattach()


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
        enable_animations: bool = True,
        menu_bar: Optional[tk.Menu] = None,
        **kwargs,
    ):

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

        # Theme management
        self.theme_manager = get_theme_manager()
        self.theme_manager.set_theme(theme_name)

        # Animation settings
        self.enable_animations = enable_animations

        # Menu bar
        self.menu_bar = menu_bar

        # State tracking
        self.detached_windows: Dict[str, DetachedWindow] = {}
        self.pane_frames: Dict[str, tk.Frame] = {}
        self.pane_headers: Dict[str, PaneHeader] = {}
        self.pane_positions: Dict[str, int] = {}  # Track original positions

        # Setup
        self._setup_styles()
        self._create_widgets()

    def _setup_styles(self):
        """Setup TTK styles."""
        self.style = ttk.Style()
        self.theme_manager.apply_ttk_theme(self.style)

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

        # Create paned window
        self.paned = ttk.PanedWindow(
            self, orient=tk.HORIZONTAL, style="Themed.TPanedwindow"
        )
        self.paned.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Create panes
        self._create_left_pane()
        self._create_center_pane()
        self._create_right_pane()

    def _create_left_pane(self):
        """Create the left pane."""
        if not self.left_builder:
            return

        container = ttk.Frame(self.paned, style="Themed.TFrame")

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

        # Add to paned window with appropriate weight
        weight = 0 if self.left_config.fixed_width is not None else 1
        self.paned.add(container, weight=weight)

        # Configure pane width constraints if fixed width is set
        if self.left_config.fixed_width is not None:
            self.paned.after_idle(
                lambda: self._configure_fixed_pane_width(
                    "left", self.left_config.fixed_width
                )
            )

    def _create_center_pane(self):
        """Create the center pane."""
        if not self.center_builder:
            return

        container = ttk.Frame(self.paned, style="Themed.TFrame")

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

        # Add to paned window
        self.paned.add(container, weight=3)

    def _create_right_pane(self):
        """Create the right pane."""
        if not self.right_builder:
            return

        container = ttk.Frame(self.paned, style="Themed.TFrame")

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

        # Add to paned window with appropriate weight
        weight = 0 if self.right_config.fixed_width is not None else 1
        self.paned.add(container, weight=weight)

        # Configure pane width constraints if fixed width is set
        if self.right_config.fixed_width is not None:
            self.paned.after_idle(
                lambda: self._configure_fixed_pane_width(
                    "right", self.right_config.fixed_width
                )
            )

    def _configure_fixed_pane_width(self, pane_side: str, fixed_width: int):
        """Configure a pane to have a fixed width."""
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

        # Remove from paned window
        if pane_side in self.pane_frames:
            self.paned.forget(self.pane_frames[pane_side])
            self.pane_frames[pane_side].destroy()
            del self.pane_frames[pane_side]
            # Keep the position info for reattaching
            self.pane_positions[f"{pane_side}_detached"] = original_position

        # Create detached window
        detached_window = DetachedWindow(
            self.winfo_toplevel(),
            pane_side,
            config,
            builder,
            lambda: self._reattach_pane(pane_side),
            self.theme_manager,
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

    def _reattach_left_pane(self, position: int):
        """Reattach the left pane at the correct position."""
        if not self.left_builder:
            return

        container = ttk.Frame(self.paned, style="Themed.TFrame")

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

        # Insert at the correct position (left should always be at position 0)
        weight = 0 if self.left_config.fixed_width is not None else 1
        self.paned.insert(0, container, weight=weight)

        # Configure pane width constraints if fixed width is set
        if self.left_config.fixed_width is not None:
            self.paned.after_idle(
                lambda: self._configure_fixed_pane_width(
                    "left", self.left_config.fixed_width
                )
            )

    def _reattach_right_pane(self, position: int):
        """Reattach the right pane at the correct position."""
        if not self.right_builder:
            return

        container = ttk.Frame(self.paned, style="Themed.TFrame")

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

        # Insert at the end (right pane should be last)
        weight = 0 if self.right_config.fixed_width is not None else 1
        self.paned.add(container, weight=weight)

        # Configure pane width constraints if fixed width is set
        if self.right_config.fixed_width is not None:
            self.paned.after_idle(
                lambda: self._configure_fixed_pane_width(
                    "right", self.right_config.fixed_width
                )
            )

    def _reattach_center_pane(self, position: int):
        """Reattach the center pane at the correct position."""
        if not self.center_builder:
            return

        container = ttk.Frame(self.paned, style="Themed.TFrame")

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

        # Insert at the correct position (center should be between left and right)
        insert_position = 0
        if "left" in self.pane_frames:
            insert_position = 1

        self.paned.insert(insert_position, container, weight=3)

    def set_theme(self, theme_name: str):
        """Change the theme."""
        if self.theme_manager.set_theme(theme_name):
            self._refresh_theme()

    def _refresh_theme(self):
        """Refresh the theme for all components."""
        self._setup_styles()

        # Refresh detached windows
        for window in self.detached_windows.values():
            window.theme_manager = self.theme_manager
            # You might want to recreate the window or update its styling

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
