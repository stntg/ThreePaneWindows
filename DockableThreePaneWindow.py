import tkinter as tk
from tkinter import ttk

class DockableThreePaneWindow(tk.Frame):
    """
    A dockable three-pane window with detachable left and right frames.
    Usage:
        window = DockableThreePaneWindow(parent, left_builder=..., center_builder=..., right_builder=...)
    """
    def __init__(self, master=None, side_width=150, left_builder=None, center_builder=None, right_builder=None, **kwargs):
        super().__init__(master, **kwargs)
        self.side_width = side_width
        self.left_builder = left_builder
        self.center_builder = center_builder
        self.right_builder = right_builder
        self.left_window = None
        self.left_placeholder = None
        self.right_window = None
        self.right_placeholder = None
        self._create_widgets()

    def _create_widgets(self):
        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        self._create_left_frame(self)
        self.paned.add(self.left_content, weight=1)

        self._create_center_frame(self.paned)
        self.paned.add(self.center_frame, weight=3)

        self._create_right_frame(self)
        self.paned.add(self.right_content, weight=1)

    def _create_left_frame(self, parent):
        self.left_content = ttk.Frame(parent, width=self.side_width)
        self.left_content.config(width=self.side_width)
        self.left_content.pack_propagate(False)
        self._add_detach_button(self.left_content, side='left')
        if self.left_builder:
            self.left_builder(self.left_content)

    def _create_center_frame(self, parent):
        self.center_frame = ttk.Frame(parent, width=300, relief=tk.SUNKEN)
        if self.center_builder:
            self.center_builder(self.center_frame)

    def _create_right_frame(self, parent):
        self.right_content = ttk.Frame(parent, width=self.side_width)
        self.right_content.config(width=self.side_width)
        self.right_content.pack_propagate(False)
        self._add_detach_button(self.right_content, side='right')
        if self.right_builder:
            self.right_builder(self.right_content)

    def _add_detach_button(self, frame, side):
        btn = ttk.Button(frame, text=f"Detach {side.title()}", command=lambda: self._detach(side))
        btn.pack(anchor='n', pady=5)

    def _detach(self, side):
        if side == 'left' and self.left_window is None:
            self.paned.forget(self.left_content)
            self.left_content.destroy()
            self.left_placeholder = ttk.Frame(self.paned, width=self.side_width)
            self.left_placeholder.config(width=self.side_width)
            self.paned.insert(0, self.left_placeholder)
            self.left_window = tk.Toplevel(self)
            self.left_window.title("Left Pane")
            self._create_left_frame(self.left_window)
            self.left_content.pack(fill=tk.BOTH, expand=True)
            btn = ttk.Button(self.left_window, text="Reattach Left", command=lambda: self._reattach('left'))
            btn.pack(anchor='s', pady=5)
            self.left_window.protocol("WM_DELETE_WINDOW", lambda: self._reattach('left'))
            self.left_window.update_idletasks()
            self.left_window.minsize(self.side_width, 100)
            self.left_window.maxsize(self.side_width, 10000)
        elif side == 'right' and self.right_window is None:
            self.paned.forget(self.right_content)
            self.right_content.destroy()
            self.right_placeholder = ttk.Frame(self.paned, width=self.side_width)
            self.right_placeholder.config(width=self.side_width)
            self.paned.add(self.right_placeholder)
            self.right_window = tk.Toplevel(self)
            self.right_window.title("Right Pane")
            self._create_right_frame(self.right_window)
            self.right_content.pack(fill=tk.BOTH, expand=True)
            btn = ttk.Button(self.right_window, text="Reattach Right", command=lambda: self._reattach('right'))
            btn.pack(anchor='s', pady=5)
            self.right_window.protocol("WM_DELETE_WINDOW", lambda: self._reattach('right'))
            self.right_window.update_idletasks()
            self.right_window.minsize(self.side_width, 100)
            self.right_window.maxsize(self.side_width, 10000)

    def _reattach(self, side):
        if side == 'left' and self.left_window is not None:
            self.left_content.pack_forget()
            self.left_content.destroy()
            self.left_content = None
            if self.left_placeholder is not None:
                self.paned.forget(self.left_placeholder)
                self.left_placeholder.destroy()
                self.left_placeholder = None
            self._create_left_frame(self)
            self.paned.insert(0, self.left_content)
            self.left_window.destroy()
            self.left_window = None
        elif side == 'right' and self.right_window is not None:
            self.right_content.pack_forget()
            self.right_content.destroy()
            self.right_content = None
            if self.right_placeholder is not None:
                self.paned.forget(self.right_placeholder)
                self.right_placeholder.destroy()
                self.right_placeholder = None
            self._create_right_frame(self)
            self.paned.add(self.right_content)
            self.right_window.destroy()
            self.right_window = None

    # Optionally, provide accessors for the panes
    def get_left_frame(self):
        return self.left_content

    def get_center_frame(self):
        return self.center_frame

    def get_right_frame(self):
        return self.right_content

# No top-level code; this file is now importable as a package module.