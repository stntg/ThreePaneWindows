"""Type stubs for threepanewindows.custom_scrollbar module."""

import tkinter as tk
from typing import Any, Optional

from .themes import ThemeManager

class ThemedScrollbar(tk.Frame):
    """Custom themed scrollbar widget."""

    theme_manager: ThemeManager
    target_widget: Optional[tk.Widget]
    orientation: str

    def __init__(
        self,
        parent: tk.Widget,
        theme_manager: ThemeManager,
        target_widget: Optional[tk.Widget] = ...,
        orientation: str = ...,
        **kwargs: Any,
    ) -> None: ...
    def attach_to_widget(self, widget: tk.Widget) -> None: ...
    def update_theme(self) -> None: ...
    def set_scroll_position(self, position: float) -> None: ...
    def get_scroll_position(self) -> float: ...
