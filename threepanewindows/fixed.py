import tkinter as tk
from typing import Any, Optional


class FixedThreePaneLayout(tk.Frame):
    def __init__(
        self,
        master: tk.Widget,
        side_width: int = 150,
        sash_width: int = 2,
        left_width: Optional[int] = None,
        right_width: Optional[int] = None,
        left_fixed_width: Optional[int] = None,
        right_fixed_width: Optional[int] = None,
        min_pane_size: int = 50,
        menu_bar: Optional[tk.Menu] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, **kwargs)

        self._validate_parameters(left_width, right_width, min_pane_size)
        self._initialize_attributes(
            side_width,
            sash_width,
            min_pane_size,
            left_width,
            right_width,
            left_fixed_width,
            right_fixed_width,
            menu_bar,
        )
        self._setup_menu_bar(master)
        self._create_panels()
        self._setup_layout()

    def _validate_parameters(
        self, left_width: Optional[int], right_width: Optional[int], min_pane_size: int
    ) -> None:
        """Validate initialization parameters."""
        if left_width is not None and left_width < 0:
            raise ValueError("left_width must be non-negative")
        if right_width is not None and right_width < 0:
            raise ValueError("right_width must be non-negative")
        if min_pane_size < 0:
            raise ValueError("min_pane_size must be non-negative")

    def _initialize_attributes(
        self,
        side_width: int,
        sash_width: int,
        min_pane_size: int,
        left_width: Optional[int],
        right_width: Optional[int],
        left_fixed_width: Optional[int],
        right_fixed_width: Optional[int],
        menu_bar: Optional[tk.Menu],
    ) -> None:
        """Initialize instance attributes."""
        self.side_width = side_width
        self.sash_width = sash_width
        self.min_pane_size = min_pane_size

        # Support both parameter names for compatibility
        self.left_width = left_width or left_fixed_width or side_width
        self.right_width = right_width or right_fixed_width or side_width
        self.left_fixed_width = left_width or left_fixed_width
        self.right_fixed_width = right_width or right_fixed_width

        self.menu_bar = menu_bar

    def _setup_menu_bar(self, master: tk.Widget) -> None:
        """Setup menu bar if provided."""
        if self.menu_bar and hasattr(master, "config"):
            master.config(menu=self.menu_bar)

    def _create_panels(self) -> None:
        """Create all panel frames and labels."""
        self._create_left_panel()
        self._create_center_panel()
        self._create_right_panel()
        self._create_sashes()

    def _create_left_panel(self) -> None:
        """Create left panel frame and label."""
        self._frame_left = tk.Frame(self, bg="#3A7CA5")
        self.label_left = tk.Label(
            self._frame_left,
            text="Left Panel",
            bg="#3A7CA5",
            fg="white",
            font=("Segoe UI", 12, "bold"),
        )
        self.label_left.pack(pady=10)

    def _create_center_panel(self) -> None:
        """Create center panel frame and label."""
        self._frame_center = tk.Frame(self, bg="#FFFFFF")
        self.label_center = tk.Label(
            self._frame_center,
            text="Center Panel",
            bg="#FFFFFF",
            font=("Segoe UI", 12, "bold"),
        )
        self.label_center.pack(pady=10)

    def _create_right_panel(self) -> None:
        """Create right panel frame and label."""
        self._frame_right = tk.Frame(self, bg="#F4A261")
        self.label_right = tk.Label(
            self._frame_right,
            text="Right Panel",
            bg="#F4A261",
            fg="black",
            font=("Segoe UI", 12, "bold"),
        )
        self.label_right.pack(pady=10)

    def _create_sashes(self) -> None:
        """Create sash frames for visual separation."""
        self._sash_left = tk.Frame(self, bg="#888888")
        self._sash_right = tk.Frame(self, bg="#888888")

    def _setup_layout(self) -> None:
        """Setup initial layout and event bindings."""
        self.place(relwidth=1, relheight=1)
        self.bind("<Configure>", self._resize)

    def _resize(self, event: Optional[tk.Event] = None) -> None:
        w = self.winfo_width()
        h = self.winfo_height()

        # Use fixed widths if specified, otherwise use default side_width
        left_width = self.left_fixed_width or self.side_width
        right_width = self.right_fixed_width or self.side_width

        center_width = w - (left_width + right_width + 2 * self.sash_width)

        self._frame_left.place(x=0, y=0, width=left_width, height=h)
        self._sash_left.place(x=left_width, y=0, width=self.sash_width, height=h)

        self._frame_center.place(
            x=left_width + self.sash_width, y=0, width=center_width, height=h
        )
        self._sash_right.place(
            x=left_width + self.sash_width + center_width,
            y=0,
            width=self.sash_width,
            height=h,
        )

        self._frame_right.place(x=w - right_width, y=0, width=right_width, height=h)

    def set_label_texts(
        self,
        left: Optional[str] = None,
        center: Optional[str] = None,
        right: Optional[str] = None,
    ) -> None:
        if left is not None:
            self.label_left.config(text=left)
        if center is not None:
            self.label_center.config(text=center)
        if right is not None:
            self.label_right.config(text=right)

    def add_to_left(self, widget: tk.Widget) -> None:
        # Reparent the widget to the left frame
        widget.pack_forget()
        widget.master = self._frame_left
        widget.pack(in_=self._frame_left, pady=5)

    def add_to_center(self, widget: tk.Widget) -> None:
        # Reparent the widget to the center frame
        widget.pack_forget()
        widget.master = self._frame_center
        widget.pack(in_=self._frame_center, fill=tk.BOTH, expand=True, pady=5)

    def add_to_right(self, widget: tk.Widget) -> None:
        # Reparent the widget to the right frame
        widget.pack_forget()
        widget.master = self._frame_right
        widget.pack(in_=self._frame_right, pady=5)

    @property
    def frame_left(self) -> tk.Frame:
        return self._frame_left

    @property
    def frame_center(self) -> tk.Frame:
        return self._frame_center

    @property
    def frame_right(self) -> tk.Frame:
        return self._frame_right

    def clear_left(self) -> None:
        for widget in self._frame_left.winfo_children():
            if widget != self.label_left:
                widget.destroy()

    def clear_center(self) -> None:
        for widget in self._frame_center.winfo_children():
            if widget != self.label_center:
                widget.destroy()

    def clear_right(self) -> None:
        for widget in self._frame_right.winfo_children():
            if widget != self.label_right:
                widget.destroy()

    def set_left_width(self, width: int) -> None:
        """Set the left pane width."""
        if width < 0:
            raise ValueError("Width must be non-negative")
        width = max(width, self.min_pane_size)
        self.left_width = width
        self.left_fixed_width = width
        self._resize()

    def set_right_width(self, width: int) -> None:
        """Set the right pane width."""
        if width < 0:
            raise ValueError("Width must be non-negative")
        width = max(width, self.min_pane_size)
        self.right_width = width
        self.right_fixed_width = width
        self._resize()

    def get_left_width(self) -> int:
        """Get the current left pane width."""
        return self.left_fixed_width or self.side_width

    def get_right_width(self) -> int:
        """Get the current right pane width."""
        return self.right_fixed_width or self.side_width

    def is_left_fixed(self) -> bool:
        """Check if left pane has fixed width."""
        return self.left_fixed_width is not None

    def is_right_fixed(self) -> bool:
        """Check if right pane has fixed width."""
        return self.right_fixed_width is not None

    @property
    def left_pane(self) -> tk.Frame:
        """Access to left pane for adding widgets."""
        return self._frame_left

    @property
    def center_pane(self) -> tk.Frame:
        """Access to center pane for adding widgets."""
        return self._frame_center

    @property
    def right_pane(self) -> tk.Frame:
        """Access to right pane for adding widgets."""
        return self._frame_right

    # Legacy property names for backward compatibility are defined above


# Modern alias - this is the preferred class name
FixedThreePaneWindow = FixedThreePaneLayout
