"""Type stubs for threepanewindows.enhanced_dockable module."""

import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from .themes import ThemeManager

@dataclass
class PaneConfig:
    """Configuration for a pane."""

    title: str
    icon: str
    window_icon: str
    custom_titlebar: bool
    custom_titlebar_shadow: bool
    detached_height: int
    detached_scrollable: bool
    min_width: int
    max_width: int
    default_width: int
    resizable: bool
    detachable: bool
    closable: bool
    fixed_width: Optional[int]

class DragHandle(tk.Frame):
    """Professional drag handle for detaching panes."""

    pane_side: str
    on_detach: Callable[[], None]
    theme_manager: ThemeManager
    is_dragging: bool
    drag_start_x: int
    drag_start_y: int
    drag_threshold: int

    def __init__(
        self,
        parent: tk.Widget,
        pane_side: str,
        on_detach: Callable[[], None],
        theme_manager: ThemeManager,
        **kwargs: Any,
    ) -> None: ...

class PaneHeader(tk.Frame):
    """Professional header for panes with title, icon, and controls."""

    config: PaneConfig
    theme_manager: ThemeManager
    on_detach: Optional[Callable[[], None]]
    on_close: Optional[Callable[[], None]]

    def __init__(
        self,
        parent: tk.Widget,
        config: PaneConfig,
        theme_manager: ThemeManager,
        on_detach: Optional[Callable[[], None]] = ...,
        on_close: Optional[Callable[[], None]] = ...,
        **kwargs: Any,
    ) -> None: ...
    def update_theme(self) -> None: ...

class DetachedWindow(tk.Toplevel):
    """Professional detached window with custom titlebar support."""

    parent_window: tk.Widget
    pane_side: str
    config: PaneConfig
    theme_manager: ThemeManager
    content_builder: Optional[Callable[[tk.Widget], None]]
    on_reattach: Callable[[], None]

    def __init__(
        self,
        parent: tk.Widget,
        pane_side: str,
        config: PaneConfig,
        theme_manager: ThemeManager,
        content_builder: Optional[Callable[[tk.Widget], None]] = ...,
        on_reattach: Optional[Callable[[], None]] = ...,
        **kwargs: Any,
    ) -> None: ...
    def update_theme(self) -> None: ...
    def close_window(self) -> None: ...

class EnhancedDockableThreePaneWindow(tk.Frame):
    """
    Enhanced dockable three-pane window with professional features.

    Features:
    - Professional theming system
    - Custom titlebars for detached windows
    - Cross-platform icon support
    - Drag & drop interface
    - Status bars and toolbars
    - Animation support
    """

    left_config: PaneConfig
    center_config: PaneConfig
    right_config: PaneConfig
    left_builder: Optional[Callable[[tk.Widget], None]]
    center_builder: Optional[Callable[[tk.Widget], None]]
    right_builder: Optional[Callable[[tk.Widget], None]]
    theme_manager: ThemeManager

    # UI Components
    main_container: tk.Frame
    paned: Optional[ttk.PanedWindow]  # Only used for fully resizable layouts
    layout_frame: Optional[tk.Frame]  # Only used for fixed pane layouts
    left_sash: Optional[tk.Frame]  # Visual sash for custom layout
    right_sash: Optional[tk.Frame]  # Visual sash for custom layout
    left_pane: tk.Frame
    center_pane: tk.Frame
    right_pane: tk.Frame
    status_bar: Optional[tk.Frame]
    toolbar: Optional[tk.Frame]

    # Layout management
    _has_fixed_panes: bool
    pane_frames: Dict[str, tk.Widget]
    pane_headers: Dict[str, PaneHeader]
    pane_positions: Dict[str, int]
    pane_visibility: Dict[str, bool]

    # Detached windows
    detached_windows: Dict[str, DetachedWindow]

    def __init__(
        self,
        master: tk.Widget,
        left_config: Optional[PaneConfig] = ...,
        center_config: Optional[PaneConfig] = ...,
        right_config: Optional[PaneConfig] = ...,
        left_builder: Optional[Callable[[tk.Widget], None]] = ...,
        center_builder: Optional[Callable[[tk.Widget], None]] = ...,
        right_builder: Optional[Callable[[tk.Widget], None]] = ...,
        theme_name: str = ...,
        show_status_bar: bool = ...,
        show_toolbar: bool = ...,
        enable_animations: bool = ...,
        **kwargs: Any,
    ) -> None: ...

    # Theme management
    def set_theme(self, theme_name: Union[str, Any]) -> None: ...
    def get_current_theme(self) -> Any: ...
    def update_theme(self) -> None: ...

    # Pane management
    def detach_left_pane(self) -> None: ...
    def detach_right_pane(self) -> None: ...
    def reattach_left_pane(self) -> None: ...
    def reattach_right_pane(self) -> None: ...
    def is_left_detached(self) -> bool: ...
    def is_right_detached(self) -> bool: ...

    # Internal layout management (private methods)
    def _create_custom_layout(self) -> None: ...
    def _create_visual_sashes(self) -> None: ...
    def _handle_custom_resize(self, event: Optional[tk.Event] = ...) -> None: ...
    def _trigger_custom_layout(self) -> None: ...
    def _detach_pane(self, pane_side: str) -> None: ...
    def _reattach_pane(self, pane_side: str) -> None: ...
    def _reattach_left_pane(self, position: int) -> None: ...
    def _reattach_right_pane(self, position: int) -> None: ...
    def _reattach_center_pane(self, position: int) -> None: ...

    # Width management
    def set_left_width(self, width: int) -> None: ...
    def set_right_width(self, width: int) -> None: ...
    def get_left_width(self) -> int: ...
    def get_right_width(self) -> int: ...

    # Content management
    def rebuild_left_content(self) -> None: ...
    def rebuild_center_content(self) -> None: ...
    def rebuild_right_content(self) -> None: ...
    def rebuild_all_content(self) -> None: ...

    # Status bar and toolbar
    def add_status_item(self, text: str, side: str = ...) -> tk.Label: ...
    def update_status(self, text: str) -> None: ...
    def add_toolbar_button(
        self,
        text: str,
        command: Callable[[], None],
        icon: Optional[str] = ...,
        side: str = ...,
    ) -> tk.Button: ...

# Utility functions
def get_recommended_icon_formats() -> List[str]: ...
def validate_icon_path(icon_path: str) -> Tuple[bool, str]: ...
def get_theme_manager() -> ThemeManager: ...
