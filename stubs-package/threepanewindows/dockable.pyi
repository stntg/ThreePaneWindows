"""Type stubs for threepanewindows.dockable module."""

import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Optional

class DockableThreePaneWindow(tk.Frame):
    """A dockable three-pane window with detachable left and right frames."""

    side_width: int
    left_builder: Optional[Callable[[tk.Widget], None]]
    center_builder: Optional[Callable[[tk.Widget], None]]
    right_builder: Optional[Callable[[tk.Widget], None]]
    left_fixed_width: Optional[int]
    right_fixed_width: Optional[int]
    menu_bar: Optional[tk.Menu]
    left_window: Optional[tk.Toplevel]
    left_placeholder: Optional[tk.Widget]
    right_window: Optional[tk.Toplevel]
    right_placeholder: Optional[tk.Widget]

    paned: ttk.PanedWindow
    left_content: ttk.Frame
    center_frame: ttk.Frame
    right_content: ttk.Frame

    def __init__(
        self,
        master: Optional[tk.Widget] = ...,
        side_width: int = ...,
        left_builder: Optional[Callable[[tk.Widget], None]] = ...,
        center_builder: Optional[Callable[[tk.Widget], None]] = ...,
        right_builder: Optional[Callable[[tk.Widget], None]] = ...,
        left_fixed_width: Optional[int] = ...,
        right_fixed_width: Optional[int] = ...,
        menu_bar: Optional[tk.Menu] = ...,
        **kwargs: Any,
    ) -> None: ...
    def detach_left(self) -> None: ...
    def detach_right(self) -> None: ...
    def reattach_left(self) -> None: ...
    def reattach_right(self) -> None: ...
    def is_left_detached(self) -> bool: ...
    def is_right_detached(self) -> bool: ...
    def set_left_width(self, width: int) -> None: ...
    def set_right_width(self, width: int) -> None: ...
    def get_left_width(self) -> int: ...
    def get_right_width(self) -> int: ...
