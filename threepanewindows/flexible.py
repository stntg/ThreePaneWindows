"""
Enhanced Flexible Layout System with Professional Detached Window Management.

This combines the flexible layout system with all the advanced detached window
functionality from the enhanced dockable module, including custom titlebars,
theming, scrollable content, and proper restoration capabilities.
"""

import platform
import tkinter as tk
from dataclasses import dataclass, field
from enum import Enum
from tkinter import ttk
from typing import Callable, Dict, List, Optional, Union

from .central_theme_manager import get_theme_manager
from .logging_config import get_logger
from .utils import platform_handler

# Initialize logger for this module
logger = get_logger(__name__)


class LayoutDirection(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


@dataclass
class FlexPaneConfig:
    """Enhanced configuration for a flexible pane with professional detached window support."""

    name: str
    title: str
    weight: float = 1.0
    min_size: int = 100
    max_size: Optional[int] = None
    detachable: bool = True
    fill_detached_space: bool = True
    builder: Optional[Callable[[tk.Frame], None]] = None

    # Enhanced detached window properties (matching enhanced_dockable.PaneConfig)
    custom_titlebar: bool = True
    default_width: int = 500
    detached_height: int = 400
    min_width: int = 300
    max_width: int = 0  # 0 means no limit
    detached_scrollable: bool = False
    window_icon: str = ""
    icon: str = ""

    # Theme and styling
    header_bg: str = "#f0f0f0"
    header_fg: str = "#333333"
    content_bg: str = "#ffffff"

    # Window behavior
    always_on_top: bool = False
    resizable: bool = True


@dataclass
class FlexContainer:
    """A container that holds panes or other containers."""

    direction: LayoutDirection
    children: List[Union["FlexContainer", FlexPaneConfig]]
    weight: float = 1.0


class FlexDetachedWindow(tk.Toplevel):
    """
    Professional detached window using the proven approach from enhanced_dockable.

    This class is based on the DetachedWindow from enhanced_dockable.py but adapted
    for the flexible layout system.
    """

    def _is_icon_file(self, path: str) -> bool:
        """Check if a string is likely an icon file path."""
        return platform_handler._is_icon_file(path)

    def __init__(
        self,
        parent,
        pane_config: FlexPaneConfig,
        content_builder: Callable,
        on_reattach: Callable,
        theme_manager,
        layout_instance=None,
        **kwargs,
    ):
        """
        Initialize detached window with configuration and callbacks.

        Args:
            parent: The parent window (usually the main application window).
            pane_config (FlexPaneConfig): Configuration object defining window behavior and appearance.
            content_builder (Callable): Function to call to build the window's content.
            on_reattach (Callable): Callback function to call when the window should be reattached.
            theme_manager: Theme manager for consistent styling.
            layout_instance: Reference to the main layout instance (optional).
            **kwargs: Additional keyword arguments passed to tk.Toplevel.
        """
        super().__init__(parent, **kwargs)
        self.pane_config = pane_config
        self.content_builder = content_builder
        self.on_reattach = on_reattach
        self.theme_manager = theme_manager
        self.layout_instance = layout_instance

        self._setup_window()
        self._setup_ui()

    def _setup_window(self):
        """Set up the detached window."""
        theme = self.theme_manager.get_current_theme()

        # Window properties
        if self.pane_config.custom_titlebar:
            # Set window title first (for taskbar identification)
            self.title(
                f"{self.pane_config.title or self.pane_config.name.title()} Panel"
            )

            # Use overrideredirect for all platforms
            self.overrideredirect(True)
        else:
            self.title(
                f"{self.pane_config.title or self.pane_config.name.title()} Panel"
            )

        # Set window size - use custom height if specified
        window_height = (
            self.pane_config.detached_height
            if self.pane_config.detached_height > 0
            else 400
        )
        self.geometry(f"{self.pane_config.default_width}x{window_height}")
        self.minsize(self.pane_config.min_width, 200)

        if self.pane_config.max_width > 0:
            self.maxsize(self.pane_config.max_width, 2000)

        # Window styling
        if self.pane_config.custom_titlebar:
            # Always create a border for custom title bar windows
            # The difference is in the border style (shadow vs clean)
            self._setup_windows_border(theme)
        else:
            self.configure(bg=theme.primary_bg)

        # Window icon (if available)
        # Use window_icon if provided, otherwise use icon only if it's a file path
        icon_path = self.pane_config.window_icon or (
            self.pane_config.icon if self._is_icon_file(self.pane_config.icon) else ""
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
            if self.pane_config.custom_titlebar:
                # On macOS, overrideredirect windows may have issues
                # Consider using attributes instead
                try:
                    self.attributes("-titlebar", False)
                except tk.TclError:
                    # Fall back to overrideredirect if attributes not supported
                    pass

        elif system == "Linux":
            # Linux-specific adjustments
            if self.pane_config.custom_titlebar:
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

    def _setup_windows_border(self, theme):
        """Set up Windows-style border for custom titlebar."""
        # Create a border frame that mimics Windows window border
        self._border_frame = tk.Frame(
            self,
            bg=theme.primary_bg,
            relief="raised",
            borderwidth=1,
            highlightbackground="#666666",
            highlightcolor="#666666",
            highlightthickness=1,
        )
        self._border_frame.pack(fill="both", expand=True, padx=1, pady=1)

    def _setup_focus_management(self):
        """Set up focus management for better user experience."""
        # Bind focus events to handle window activation properly
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

        # Also bind click events to bring window to front
        self.bind("<Button-1>", self._on_click_focus)

    def _on_click_focus(self, event):
        """Handle click to focus."""
        self.focus_set()
        self.lift()
        # Ensure it appears above the main window
        self.attributes("-topmost", True)
        self.attributes("-topmost", False)

    def _on_focus_in(self, event):
        """Handle window focus in."""
        # Bring window to front when focused
        self.lift()
        # Ensure it appears above the main window
        self.attributes("-topmost", True)
        self.attributes("-topmost", False)  # Reset topmost but keep it raised

    def _on_focus_out(self, event):
        """Handle window focus out."""
        # Could implement focus-out behavior here if needed
        pass

    def _create_control_button(
        self, parent, text: str, command, tooltip: str = ""
    ) -> tk.Button:
        """
        Create a themed control button for the pane header.

        Creates a small button with hover effects that matches the current theme.
        Used for detach and reattach actions.
        """
        theme = self.theme_manager.get_current_theme()

        btn = tk.Button(
            parent,
            text=text,
            command=command,
            width=2,
            height=1,
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            activebackground=theme.accent_bg,
            activeforeground=theme.accent_text,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            font=("Segoe UI", 8),
        )

        # Add hover effects
        def on_enter(e):
            btn.configure(bg=theme.accent_bg, fg=theme.accent_text)

        def on_leave(e):
            btn.configure(bg=theme.panel_header_bg, fg=theme.panel_header_text)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        # Mark this button as a control button to prevent theme override
        btn._is_control_button = True

        return btn

    def refresh_theme(self):
        """Refresh the detached window with current theme."""
        try:
            # Store the current content before clearing
            # We need to preserve the border frame if it exists
            border_frame_existed = hasattr(self, "_border_frame")

            # Clear existing widgets but preserve the border frame reference
            for child in self.winfo_children():
                child.destroy()

            # Reset border frame reference if it existed
            if border_frame_existed:
                self._border_frame = None

            # Get the new theme and update window styling
            theme = self.theme_manager.get_current_theme()

            # Update window background
            self.configure(bg=theme.primary_bg)

            # Recreate border frame if needed
            if self.pane_config.custom_titlebar:
                self._setup_windows_border(theme)

            # Rebuild the UI with new theme
            self._setup_ui()
        except tk.TclError:
            # Widget has been destroyed, ignore
            pass

    def _setup_ui(self):
        """Set up the UI."""
        theme = self.theme_manager.get_current_theme()

        # Determine the parent container (border frame if using Windows border,
        # otherwise self)
        parent_container = getattr(self, "_border_frame", self)

        # Header with reattach button (and custom title bar if needed)
        header_height = 32  # Keep same height for consistency
        if self.pane_config.custom_titlebar:
            # Add a header that matches Windows title bar style
            header_frame = tk.Frame(
                parent_container,
                bg=theme.panel_header_bg,
                height=header_height,
                relief="flat",
                borderwidth=0,
            )
        else:
            header_frame = tk.Frame(
                parent_container, bg=theme.panel_header_bg, height=header_height
            )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        # Custom title bar controls (if using custom title bar)
        controls_frame = None
        if self.pane_config.custom_titlebar:
            controls_frame = self._setup_custom_titlebar(header_frame, theme)

        # Title and Icon
        if self.pane_config.title:
            # For detached windows, we'll create separate icon and title elements
            # to handle both text and image icons properly

            # Check if title already includes the icon to avoid duplication
            # For text icons (emojis), check if title starts with the icon
            # For file icons, show them separately since titles won't contain images
            title_includes_icon = (
                self.pane_config.icon
                and not self._is_icon_file(self.pane_config.icon)  # Only check for text
                and self.pane_config.title.startswith(self.pane_config.icon)
            )

            # Create a container for icon and title
            title_container = tk.Frame(header_frame, bg=theme.panel_header_bg)
            title_container.pack(side="left", padx=8, pady=6, fill="x", expand=True)

            # Add icon if present and not already in title
            if self.pane_config.icon and not title_includes_icon:
                icon_label = self._create_detached_icon_label(title_container, theme)
                if icon_label:
                    icon_label.pack(side="left", padx=(0, 4))

            # Add title
            title_label = tk.Label(
                title_container,
                text=self.pane_config.title,
                bg=theme.panel_header_bg,
                fg=theme.panel_header_text,
                font=(
                    "Segoe UI",
                    9,
                    "bold",
                ),
                anchor="w",  # Left align to prevent truncation
            )
            title_label.pack(side="left", fill="x", expand=True)

            # Make title label draggable too (for custom title bar)
            if self.pane_config.custom_titlebar:
                title_label.bind("<Button-1>", self._start_drag)
                title_label.bind("<B1-Motion>", self._on_drag)

        # Reattach button - use the same method as detach button
        if self.pane_config.custom_titlebar:
            # For custom title bar, put reattach button in controls frame
            reattach_btn = self._create_control_button(
                controls_frame, "⧈", self.on_reattach, "Reattach"
            )
            reattach_btn.pack(side="right", padx=2)
        else:
            # For regular title bar, put in header frame
            reattach_btn = self._create_control_button(
                header_frame, "⧈", self.on_reattach, "Reattach"
            )
            reattach_btn.pack(side="right", padx=8, pady=4)

        # Separator
        separator = tk.Frame(parent_container, bg=theme.border, height=1)
        separator.pack(fill="x")

        # Content frame - with optional scrollbars
        if (
            self.pane_config.detached_scrollable
            and self.pane_config.detached_height > 0
        ):
            # Create scrollable content area
            self._setup_scrollable_content(theme, parent_container)
        else:
            # Regular content frame
            self.content_frame = tk.Frame(parent_container, bg=theme.panel_content_bg)
            self.content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Build content
        if self.content_builder:
            self.content_builder(self.content_frame)
            # Apply theme to the built content, but skip custom scrollbars
            # since they're already properly themed during creation
            self._apply_theme_skip_scrollbars(self.content_frame)

    def _setup_custom_titlebar(self, header_frame, theme):
        """Set up custom title bar with window controls."""
        # Make the header draggable
        self._drag_data = {"x": 0, "y": 0}
        header_frame.bind("<Button-1>", self._start_drag)
        header_frame.bind("<B1-Motion>", self._on_drag)

        # Window control buttons frame (right side)
        controls_frame = tk.Frame(header_frame, bg=theme.panel_header_bg)
        controls_frame.pack(side="right", padx=4, pady=4)

        # Note: Close button replaced by reattach button in the main UI setup
        # Note: Minimize button removed for custom title bars since overrideredirect
        # windows can't be properly minimized

        return controls_frame

    def _apply_theme_skip_scrollbars(self, widget):
        """Apply theme to widget and children, but skip custom scrollbars."""
        # Apply theme to this widget
        self.theme_manager.apply_theme_to_widget(widget, recursive=False)

        # Recursively apply to children, but skip custom scrollbars
        try:
            for child in widget.winfo_children():
                # Check if this child is a custom scrollbar
                if self._is_custom_scrollbar(child):
                    # Skip theming custom scrollbars - they're already properly themed
                    continue
                else:
                    # Recursively theme non-scrollbar children
                    self._apply_theme_skip_scrollbars(child)
        except tk.TclError:
            # Widget might be destroyed, ignore
            pass

    def _is_custom_scrollbar(self, widget):
        """Check if a widget is a custom scrollbar."""
        return (
            hasattr(widget, "apply_theme") and "scrollbar" in str(type(widget)).lower()
        )

    def _setup_scrollable_content(self, theme, parent_container):
        """Set up scrollable content area."""
        # Create canvas and scrollbar for scrollable content
        canvas = tk.Canvas(
            parent_container, bg=theme.panel_content_bg, highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            parent_container, orient="vertical", command=canvas.yview
        )
        self.content_frame = tk.Frame(canvas, bg=theme.panel_content_bg)

        # Configure scrolling
        self.content_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack scrollable components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)

    def _create_detached_icon_label(self, parent, theme):
        """Create icon label for detached window."""
        if not self.pane_config.icon:
            return None

        if self._is_icon_file(self.pane_config.icon):
            # Handle image icons
            try:
                # This would need proper image loading implementation
                # For now, just return None for image icons
                return None
            except Exception:
                return None
        else:
            # Handle text icons (emojis, symbols)
            icon_label = tk.Label(
                parent,
                text=self.pane_config.icon,
                bg=theme.panel_header_bg,
                fg=theme.panel_header_text,
                font=("Segoe UI", 9),
            )

            # Make icon draggable too (for custom title bar)
            if self.pane_config.custom_titlebar:
                icon_label.bind("<Button-1>", self._start_drag)
                icon_label.bind("<B1-Motion>", self._on_drag)

            return icon_label

    def _start_drag(self, event):
        """Start dragging the window."""
        self._drag_data = {"x": event.x_root, "y": event.y_root}

    def _on_drag(self, event):
        """Handle window dragging."""
        deltax = event.x_root - self._drag_data["x"]
        deltay = event.y_root - self._drag_data["y"]
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")
        self._drag_data["x"] = event.x_root
        self._drag_data["y"] = event.y_root

    def _on_window_close(self):
        """Handle window close - reattach the pane."""
        self.on_reattach()


class EnhancedFlexibleLayout(tk.Frame):
    """
    Enhanced flexible layout system with professional detached window management.

    Combines the intuitive flexible layout with all the advanced features from
    the enhanced dockable module including custom titlebars, theming, and
    sophisticated window management.
    """

    def __init__(
        self,
        master: tk.Widget,
        root_container: FlexContainer,
        theme_name: str = "light",
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self.root_container = root_container
        self.panes: Dict[str, FlexPaneConfig] = {}
        self.pane_widgets: Dict[str, tk.Frame] = {}
        self.detached_windows: Dict[str, FlexDetachedWindow] = {}

        # Initialize theme manager
        self.theme_manager = get_theme_manager()
        self.theme_manager.set_theme(theme_name)

        # Collect all panes from the container hierarchy
        self._collect_panes(root_container)

        # Build the initial layout
        self._build_layout()

        # Apply initial theme
        self.theme_manager.apply_theme_to_widget(self, recursive=True)

    def _collect_panes(self, container: FlexContainer):
        """Recursively collect all panes from the container hierarchy."""
        for child in container.children:
            if isinstance(child, FlexPaneConfig):
                self.panes[child.name] = child
            elif isinstance(child, FlexContainer):
                self._collect_panes(child)

    def _build_layout(self):
        """Build the layout from the container hierarchy."""
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        self.pane_widgets.clear()

        # Build the layout recursively
        self._build_container(self, self.root_container)

        # Configure weights for the root
        if self.root_container.direction == LayoutDirection.HORIZONTAL:
            self.grid_rowconfigure(0, weight=1)
        else:
            self.grid_columnconfigure(0, weight=1)

    def _build_container(self, parent: tk.Widget, container: FlexContainer):
        """Recursively build a container and its children."""
        # Collect all non-detached children and their weights
        active_children = []
        for child in container.children:
            if isinstance(child, FlexPaneConfig):
                if child.name not in self.detached_windows:
                    active_children.append(child)
            elif isinstance(child, FlexContainer):
                if self._container_has_active_panes(child):
                    active_children.append(child)

        if not active_children:
            return

        # Calculate total weight of active children
        total_weight = sum(child.weight for child in active_children)

        # Clear any existing grid weights
        self._clear_grid_weights(parent)

        current_pos = 0
        for child in active_children:
            if isinstance(child, FlexPaneConfig):
                # Create pane widget
                pane_frame = self._create_pane_widget(parent, child)
                self.pane_widgets[child.name] = pane_frame

                # Calculate proportional weight
                proportional_weight = int((child.weight / total_weight) * 1000)

                # Grid the pane
                if container.direction == LayoutDirection.HORIZONTAL:
                    pane_frame.grid(row=0, column=current_pos, sticky="nsew")
                    parent.grid_columnconfigure(current_pos, weight=proportional_weight)
                    parent.grid_rowconfigure(0, weight=1)
                else:
                    pane_frame.grid(row=current_pos, column=0, sticky="nsew")
                    parent.grid_rowconfigure(current_pos, weight=proportional_weight)
                    parent.grid_columnconfigure(0, weight=1)

                current_pos += 1

            elif isinstance(child, FlexContainer):
                # Create container frame
                container_frame = tk.Frame(parent)

                # Calculate proportional weight
                proportional_weight = int((child.weight / total_weight) * 1000)

                # Grid the container
                if container.direction == LayoutDirection.HORIZONTAL:
                    container_frame.grid(row=0, column=current_pos, sticky="nsew")
                    parent.grid_columnconfigure(current_pos, weight=proportional_weight)
                    parent.grid_rowconfigure(0, weight=1)
                else:
                    container_frame.grid(row=current_pos, column=0, sticky="nsew")
                    parent.grid_rowconfigure(current_pos, weight=proportional_weight)
                    parent.grid_columnconfigure(0, weight=1)

                # Recursively build the child container
                self._build_container(container_frame, child)
                current_pos += 1

    def _container_has_active_panes(self, container: FlexContainer) -> bool:
        """Check if a container has any non-detached panes."""
        for child in container.children:
            if isinstance(child, FlexPaneConfig):
                if child.name not in self.detached_windows:
                    return True
            elif isinstance(child, FlexContainer):
                if self._container_has_active_panes(child):
                    return True
        return False

    def _clear_grid_weights(self, parent: tk.Widget):
        """Clear existing grid weights to prevent interference."""
        try:
            grid_info = parent.grid_size()
            cols, rows = grid_info

            for i in range(cols):
                parent.grid_columnconfigure(i, weight=0)
            for i in range(rows):
                parent.grid_rowconfigure(i, weight=0)
        except:
            pass

    def _create_control_button(
        self, parent, text: str, command, tooltip: str = ""
    ) -> tk.Button:
        """
        Create a themed control button for the pane header.

        Creates a small button with hover effects that matches the current theme.
        Used for detach and reattach actions.
        """
        theme = self.theme_manager.get_current_theme()

        btn = tk.Button(
            parent,
            text=text,
            command=command,
            width=2,
            height=1,
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            activebackground=theme.accent_bg,
            activeforeground=theme.accent_text,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            font=("Segoe UI", 8),
        )

        # Add hover effects
        def on_enter(e):
            btn.configure(bg=theme.accent_bg, fg=theme.accent_text)

        def on_leave(e):
            btn.configure(bg=theme.panel_header_bg, fg=theme.panel_header_text)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        # Mark this button as a control button to prevent theme override
        btn._is_control_button = True

        return btn

    def refresh_theme(self):
        """Refresh all pane headers and detached windows with current theme."""
        try:
            # Refresh all detached windows
            for window in self.detached_windows.values():
                if hasattr(window, "refresh_theme"):
                    window.refresh_theme()

            # Rebuild attached panes to refresh theming
            self._rebuild_attached_panes()
        except Exception as e:
            # If refresh fails, continue silently
            pass

    def _rebuild_attached_panes(self):
        """Rebuild attached panes to refresh their theming."""
        try:
            # Store current state
            current_panes = {}
            for name, pane_info in self.panes.items():
                if name not in self.detached_windows:
                    current_panes[name] = pane_info

            # Clear and rebuild layout for attached panes only
            if current_panes:
                # Clear existing layout
                for child in self.winfo_children():
                    child.destroy()

                # Rebuild layout
                self._build_layout()
        except Exception:
            # If rebuild fails, continue silently
            pass

    def _create_pane_widget(self, parent: tk.Widget, pane: FlexPaneConfig) -> tk.Frame:
        """Create a widget for a pane with professional styling."""
        # Get theme colors
        theme = self.theme_manager.get_current_theme()
        header_bg = theme.panel_header_bg
        header_fg = theme.panel_header_text
        content_bg = theme.panel_content_bg
        border_color = theme.border

        # Main pane frame with border
        pane_frame = tk.Frame(parent, relief="solid", bd=1, bg=border_color)

        # Header with title and detach button (matching detached window style)
        header_height = 32  # Match detached window header height
        header = tk.Frame(
            pane_frame, bg=header_bg, height=header_height, relief="flat", borderwidth=0
        )
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)

        # Title container
        title_container = tk.Frame(header, bg=header_bg)
        title_container.pack(side="left", padx=8, pady=6, fill="x", expand=True)

        # Icon (if provided) - matching detached window style
        if pane.icon and not self._is_icon_file(pane.icon):
            icon_label = tk.Label(
                title_container,
                text=pane.icon,
                bg=header_bg,
                fg=header_fg,
                font=("Segoe UI", 9),
            )
            icon_label.pack(side="left", padx=(0, 4))

        # Title - matching detached window style
        title_label = tk.Label(
            title_container,
            text=pane.title,
            bg=header_bg,
            fg=header_fg,
            font=("Segoe UI", 9, "bold"),
            anchor="w",  # Left align to prevent truncation
        )
        title_label.pack(side="left", fill="x", expand=True)

        # Detach button - matching detached window style
        if pane.detachable:
            detach_btn = self._create_control_button(
                header, "⚏", lambda: self._detach_pane(pane.name), "Detach"
            )
            detach_btn.pack(side="right", padx=8, pady=4)

        # Separator line - matching detached window style
        separator = tk.Frame(pane_frame, bg=theme.border, height=1)
        separator.pack(fill="x")

        # Content area
        content_frame = tk.Frame(pane_frame, bg=content_bg)
        content_frame.pack(fill="both", expand=True, padx=1, pady=1)

        # Build content using the pane's builder
        if pane.builder:
            pane.builder(content_frame)
            # Apply theme to the built content
            self.theme_manager.apply_theme_to_widget(content_frame, recursive=True)
        else:
            # Default content
            default_label = tk.Label(
                content_frame,
                text=f"{pane.title}\n\nWeight: {pane.weight}\nDetachable: {pane.detachable}\nFill Space: {pane.fill_detached_space}",
                justify="center",
                bg=content_bg,
                fg=theme.primary_text,
                font=("Segoe UI", 9),
            )
            default_label.pack(fill="both", expand=True, padx=10, pady=10)

        # Apply theme to the entire pane widget
        self.theme_manager.apply_theme_to_widget(pane_frame, recursive=True)

        return pane_frame

    def _is_icon_file(self, path: str) -> bool:
        """Check if a string is likely an icon file path."""
        return platform_handler._is_icon_file(path)

    def _detach_pane(self, pane_name: str):
        """Detach a pane to a professional separate window."""
        if pane_name in self.detached_windows:
            return  # Already detached

        pane = self.panes[pane_name]

        # Create enhanced detached window using the proven approach
        detached_window = FlexDetachedWindow(
            parent=self.winfo_toplevel(),  # Use toplevel like enhanced_dockable
            pane_config=pane,
            content_builder=pane.builder,
            on_reattach=lambda: self._reattach_pane(pane_name),
            theme_manager=self.theme_manager,
            layout_instance=self,
        )

        # Store detached window IMMEDIATELY (critical for preventing garbage collection)
        self.detached_windows[pane_name] = detached_window

        # Position the window nicely (like enhanced_dockable does)
        self._position_detached_window(detached_window, pane_name)

        # Rebuild layout (remaining panes automatically expand)
        self._build_layout()

        logger.info(f"Detached pane '{pane_name}' to professional window")

    def _position_detached_window(self, window: FlexDetachedWindow, pane_name: str):
        """Position a detached window nicely."""
        # Get main window position
        main_window = self.winfo_toplevel()
        main_window.update_idletasks()

        main_x = main_window.winfo_x()
        main_y = main_window.winfo_y()
        main_width = main_window.winfo_width()
        main_height = main_window.winfo_height()

        # Calculate position based on pane name (simple offset strategy)
        offset_multiplier = len(self.detached_windows)
        base_offset = 50

        x = main_x + base_offset + (offset_multiplier * 30)
        y = main_y + base_offset + (offset_multiplier * 30)

        # Ensure window is on screen
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = max(0, min(x, screen_width - window.pane_config.default_width))
        y = max(0, min(y, screen_height - window.pane_config.detached_height))

        # Set the position
        window.geometry(
            f"{window.pane_config.default_width}x{window.pane_config.detached_height}+{x}+{y}"
        )

        # Ensure detached window appears in front and stays visible
        window.lift()
        window.focus_force()
        window.attributes("-topmost", True)
        window.after(100, lambda: window.attributes("-topmost", False))

    def _reattach_pane(self, pane_name: str):
        """Reattach a detached pane to its original position."""
        if pane_name not in self.detached_windows:
            return  # Not detached

        # Close detached window
        detached_window = self.detached_windows[pane_name]
        detached_window.destroy()
        del self.detached_windows[pane_name]

        # Rebuild layout (includes the reattached pane)
        self._build_layout()

        logger.info(f"Reattached pane '{pane_name}' to original position")

    def set_theme(self, theme_name: str):
        """Change the theme and update all components."""
        self.theme_manager.set_theme(theme_name)

        # Apply theme to the main layout
        self.theme_manager.apply_theme_to_widget(self, recursive=True)

        # Rebuild layout to apply theme to pane widgets
        self._build_layout()

        # Update detached windows with new theme
        for window in self.detached_windows.values():
            window.theme_manager = self.theme_manager
            self._update_detached_window_theme(window)

        logger.info(f"Theme changed to: {theme_name}")

    def _update_detached_window_theme(self, window: FlexDetachedWindow):
        """Update the theme of a detached window."""
        try:
            # Apply theme to the entire detached window
            self.theme_manager.apply_theme_to_widget(window, recursive=True)

            # Force update the window's UI with new theme
            window._update_theme()
        except Exception as e:
            logger.warning(f"Failed to update detached window theme: {e}")

    def refresh_theme(self):
        """Refresh the layout with the current theme."""
        self.set_theme(self.theme_manager.current_theme.value)

    def detach_pane(self, pane_name: str):
        """Public method to detach a pane."""
        self._detach_pane(pane_name)

    def reattach_pane(self, pane_name: str):
        """Public method to reattach a pane."""
        self._reattach_pane(pane_name)

    def get_detached_panes(self) -> List[str]:
        """Get list of currently detached pane names."""
        return list(self.detached_windows.keys())

    def get_available_panes(self) -> List[str]:
        """Get list of all available pane names."""
        return list(self.panes.keys())
