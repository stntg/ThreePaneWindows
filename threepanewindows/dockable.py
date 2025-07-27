"""
Dockable three-pane window implementation.

This module provides a dockable three-pane window layout with detachable
left and right frames for flexible UI arrangements.
"""

import tkinter as tk
from tkinter import ttk


class DockableThreePaneWindow(tk.Frame):
    """A dockable three-pane window with detachable left and right frames.

    Usage:
        window = DockableThreePaneWindow(parent, left_builder=...,
                                         center_builder=..., right_builder=...)
    """

    def __init__(
        self,
        master=None,
        side_width=150,
        left_builder=None,
        center_builder=None,
        right_builder=None,
        left_fixed_width=None,
        right_fixed_width=None,
        menu_bar=None,
        **kwargs,
    ):
        """Initialize dockable three-pane window with configuration options."""
        super().__init__(master, **kwargs)
        self.side_width = side_width
        self.left_builder = left_builder
        self.center_builder = center_builder
        self.right_builder = right_builder
        self.left_fixed_width = left_fixed_width
        self.right_fixed_width = right_fixed_width
        self.menu_bar = menu_bar
        self.left_window = None
        self.left_placeholder = None
        self.right_window = None
        self.right_placeholder = None
        self._create_widgets()

    def _create_widgets(self):
        # Add menu bar if provided
        if self.menu_bar and hasattr(self.master, "config"):
            self.master.config(menu=self.menu_bar)

        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        self._create_left_frame(self)
        left_weight = 0 if self.left_fixed_width is not None else 1
        self.paned.add(self.left_content, weight=left_weight)

        self._create_center_frame(self.paned)
        self.paned.add(self.center_frame, weight=3)

        self._create_right_frame(self)
        right_weight = 0 if self.right_fixed_width is not None else 1
        self.paned.add(self.right_content, weight=right_weight)

        # Configure fixed widths after widgets are created
        if self.left_fixed_width is not None:
            self.after_idle(
                lambda: self._configure_fixed_width("left", self.left_fixed_width)
            )
        if self.right_fixed_width is not None:
            self.after_idle(
                lambda: self._configure_fixed_width("right", self.right_fixed_width)
            )

    def _create_left_frame(self, parent, is_detached=False):
        width = self.left_fixed_width or self.side_width
        self.left_content = ttk.Frame(parent, width=width)
        self.left_content.config(width=width)

        # Always prevent propagation for consistent sizing
        self.left_content.pack_propagate(False)

        # Only add detach button if not already detached
        if not is_detached:
            self._add_detach_button(self.left_content, side="left")
        if self.left_builder:
            self.left_builder(self.left_content)

    def _create_center_frame(self, parent):
        self.center_frame = ttk.Frame(parent, width=300, relief=tk.SUNKEN)
        if self.center_builder:
            self.center_builder(self.center_frame)

    def _create_right_frame(self, parent, is_detached=False):
        width = self.right_fixed_width or self.side_width
        self.right_content = ttk.Frame(parent, width=width)
        self.right_content.config(width=width)

        # Always prevent propagation for consistent sizing
        self.right_content.pack_propagate(False)

        # Only add detach button if not already detached
        if not is_detached:
            self._add_detach_button(self.right_content, side="right")
        if self.right_builder:
            self.right_builder(self.right_content)

    def _configure_fixed_width(self, side: str, fixed_width: int):
        """Configure a pane to have a fixed width."""
        if side == "left" and hasattr(self, "left_content"):
            container = self.left_content
        elif side == "right" and hasattr(self, "right_content"):
            container = self.right_content
        else:
            return

        # Get the pane index in the PanedWindow
        pane_index = None
        for i, child in enumerate(self.paned.winfo_children()):
            if child == container:
                pane_index = i
                break

        if pane_index is not None:
            try:
                # Set minimum size to prevent resizing below fixed width
                self.paned.paneconfig(
                    pane_index, minsize=fixed_width, width=fixed_width
                )
                # Try to set maximum size if supported
                try:
                    self.paned.paneconfig(pane_index, maxsize=fixed_width)
                except tk.TclError:
                    # Some versions don't support maxsize
                    pass
            except tk.TclError:
                # Fallback: just set the width
                container.configure(width=fixed_width)

    def _add_detach_button(self, frame, side):
        btn = ttk.Button(
            frame, text=f"Detach {side.title()}", command=lambda: self._detach(side)
        )
        btn.pack(anchor="n", pady=5)

    def _detach(self, side):
        if side == "left" and self.left_window is None:
            self.paned.forget(self.left_content)
            self.left_content.destroy()
            # Don't create a placeholder - let center panel expand
            self.left_placeholder = None
            self.left_window = tk.Toplevel(self)
            self.left_window.title("Left Pane")
            self._create_left_frame(self.left_window, is_detached=True)
            self.left_content.pack(fill=tk.BOTH, expand=True)
            btn = ttk.Button(
                self.left_window,
                text="Reattach Left",
                command=lambda: self._reattach("left"),
            )
            btn.pack(anchor="s", pady=5)
            self.left_window.protocol(
                "WM_DELETE_WINDOW", lambda: self._reattach("left")
            )
            self.left_window.update_idletasks()
            self.left_window.minsize(self.side_width, 100)
            self.left_window.maxsize(self.side_width, 10000)
        elif side == "right" and self.right_window is None:
            self.paned.forget(self.right_content)
            self.right_content.destroy()
            # Don't create a placeholder - let center panel expand
            self.right_placeholder = None
            self.right_window = tk.Toplevel(self)
            self.right_window.title("Right Pane")
            self._create_right_frame(self.right_window, is_detached=True)
            self.right_content.pack(fill=tk.BOTH, expand=True)
            btn = ttk.Button(
                self.right_window,
                text="Reattach Right",
                command=lambda: self._reattach("right"),
            )
            btn.pack(anchor="s", pady=5)
            self.right_window.protocol(
                "WM_DELETE_WINDOW", lambda: self._reattach("right")
            )
            self.right_window.update_idletasks()
            self.right_window.minsize(self.side_width, 100)
            self.right_window.maxsize(self.side_width, 10000)

    def _reattach(self, side):
        if side == "left" and self.left_window is not None:
            self.left_content.pack_forget()
            self.left_content.destroy()
            self.left_content = None
            # No placeholder to remove since we don't create one anymore
            self.left_placeholder = None
            self._create_left_frame(self)
            left_weight = 0 if self.left_fixed_width is not None else 1
            self.paned.insert(0, self.left_content, weight=left_weight)

            # Configure fixed width if needed
            if self.left_fixed_width is not None:
                self.after_idle(
                    lambda: self._configure_fixed_width("left", self.left_fixed_width)
                )

            self.left_window.destroy()
            self.left_window = None
        elif side == "right" and self.right_window is not None:
            self.right_content.pack_forget()
            self.right_content.destroy()
            self.right_content = None
            # No placeholder to remove since we don't create one anymore
            self.right_placeholder = None
            self._create_right_frame(self)
            right_weight = 0 if self.right_fixed_width is not None else 1
            self.paned.add(self.right_content, weight=right_weight)

            # Configure fixed width if needed
            if self.right_fixed_width is not None:
                self.after_idle(
                    lambda: self._configure_fixed_width("right", self.right_fixed_width)
                )

            self.right_window.destroy()
            self.right_window = None

    # Optionally, provide accessors for the panes
    def get_left_frame(self):
        """Get the left frame widget."""
        return self.left_content

    def get_center_frame(self):
        """Get the center frame widget."""
        return self.center_frame

    def get_right_frame(self):
        """Get the right frame widget."""
        return self.right_content

    def set_left_fixed_width(self, width: int):
        """Set the left pane to a fixed width."""
        self.left_fixed_width = width
        if hasattr(self, "left_content") and self.left_content:
            self.left_content.configure(width=width)
            self.after_idle(lambda: self._configure_fixed_width("left", width))

    def set_right_fixed_width(self, width: int):
        """Set the right pane to a fixed width."""
        self.right_fixed_width = width
        if hasattr(self, "right_content") and self.right_content:
            self.right_content.configure(width=width)
            self.after_idle(lambda: self._configure_fixed_width("right", width))

    def clear_left_fixed_width(self):
        """Remove fixed width constraint from left pane."""
        self.left_fixed_width = None
        if hasattr(self, "left_content") and self.left_content:
            # Reset to resizable by setting weight back to 1
            for i, child in enumerate(self.paned.winfo_children()):
                if child == self.left_content:
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

    def clear_right_fixed_width(self):
        """Remove fixed width constraint from right pane."""
        self.right_fixed_width = None
        if hasattr(self, "right_content") and self.right_content:
            # Reset to resizable by setting weight back to 1
            for i, child in enumerate(self.paned.winfo_children()):
                if child == self.right_content:
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

    def is_left_fixed(self) -> bool:
        """Check if left pane has fixed width."""
        return self.left_fixed_width is not None

    def is_right_fixed(self) -> bool:
        """Check if right pane has fixed width."""
        return self.right_fixed_width is not None


# No top-level code; this file is now importable as a package module.
