"""Type stubs for threepanewindows.fixed module."""

import tkinter as tk
from typing import Any, Optional

class FixedThreePaneLayout(tk.Frame):
    """Fixed three-pane layout with non-resizable side panels."""

    side_width: int
    sash_width: int
    min_pane_size: int
    left_width: int
    right_width: int
    left_fixed_width: Optional[int]
    right_fixed_width: Optional[int]
    menu_bar: Optional[tk.Menu]

    label_left: tk.Label
    label_center: tk.Label
    label_right: tk.Label

    def __init__(
        self,
        master: tk.Widget,
        side_width: int = ...,
        sash_width: int = ...,
        left_width: Optional[int] = ...,
        right_width: Optional[int] = ...,
        left_fixed_width: Optional[int] = ...,
        right_fixed_width: Optional[int] = ...,
        min_pane_size: int = ...,
        menu_bar: Optional[tk.Menu] = ...,
        **kwargs: Any,
    ) -> None: ...
    def set_label_texts(
        self,
        left: Optional[str] = ...,
        center: Optional[str] = ...,
        right: Optional[str] = ...,
    ) -> None: ...
    def add_to_left(self, widget: tk.Widget) -> None: ...
    def add_to_center(self, widget: tk.Widget) -> None: ...
    def add_to_right(self, widget: tk.Widget) -> None: ...
    @property
    def frame_left(self) -> tk.Frame: ...
    @property
    def frame_center(self) -> tk.Frame: ...
    @property
    def frame_right(self) -> tk.Frame: ...
    @property
    def left_pane(self) -> tk.Frame: ...
    @property
    def center_pane(self) -> tk.Frame: ...
    @property
    def right_pane(self) -> tk.Frame: ...
    def clear_left(self) -> None: ...
    def clear_center(self) -> None: ...
    def clear_right(self) -> None: ...
    def set_left_width(self, width: int) -> None: ...
    def set_right_width(self, width: int) -> None: ...
    def get_left_width(self) -> int: ...
    def get_right_width(self) -> int: ...
    def is_left_fixed(self) -> bool: ...
    def is_right_fixed(self) -> bool: ...

# Modern alias
FixedThreePaneWindow = FixedThreePaneLayout
