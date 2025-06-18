import tkinter as tk

class FixedThreePaneLayout(tk.Frame):
    def __init__(self, master, side_width=150, sash_width=2, **kwargs):
        super().__init__(master, **kwargs)
        self.side_width = side_width
        self.sash_width = sash_width

        # Left panel
        self._frame_left = tk.Frame(self, bg="#3A7CA5")
        self.label_left = tk.Label(self._frame_left, text="Left Panel", bg="#3A7CA5", fg="white", font=("Segoe UI", 12, "bold"))
        self.label_left.pack(pady=10)

        self._sash_left = tk.Frame(self, bg="#888888")

        # Center panel
        self._frame_center = tk.Frame(self, bg="#FFFFFF")
        self.label_center = tk.Label(self._frame_center, text="Center Panel", bg="#FFFFFF", font=("Segoe UI", 12, "bold"))
        self.label_center.pack(pady=10)

        self._sash_right = tk.Frame(self, bg="#888888")

        # Right panel
        self._frame_right = tk.Frame(self, bg="#F4A261")
        self.label_right = tk.Label(self._frame_right, text="Right Panel", bg="#F4A261", fg="black", font=("Segoe UI", 12, "bold"))
        self.label_right.pack(pady=10)

        self.place(relwidth=1, relheight=1)
        self.bind("<Configure>", self._resize)

    def _resize(self, event=None):
        w = self.winfo_width()
        h = self.winfo_height()
        center_width = w - 2 * (self.side_width + self.sash_width)

        self._frame_left.place(x=0, y=0, width=self.side_width, height=h)
        self._sash_left.place(x=self.side_width, y=0, width=self.sash_width, height=h)

        self._frame_center.place(x=self.side_width + self.sash_width, y=0, width=center_width, height=h)
        self._sash_right.place(x=self.side_width + self.sash_width + center_width, y=0, width=self.sash_width, height=h)

        self._frame_right.place(x=w - self.side_width, y=0, width=self.side_width, height=h)

    def set_label_texts(self, left=None, center=None, right=None):
        if left is not None:
            self.label_left.config(text=left)
        if center is not None:
            self.label_center.config(text=center)
        if right is not None:
            self.label_right.config(text=right)
    
    def add_to_left(self, widget):
        widget.pack(in_=self._frame_left, pady=5)

    def add_to_center(self, widget):
        widget.pack(in_=self._frame_center, fill=tk.BOTH, expand=True, pady=5)

    def add_to_right(self, widget):
        widget.pack(in_=self._frame_right, pady=5)

    @property
    def frame_left(self):
        return self._frame_left

    @property
    def frame_center(self):
        return self._frame_center

    @property
    def frame_right(self):
        return self._frame_right
    
    def clear_left(self):
        for widget in self._frame_left.winfo_children():
            if widget != self.label_left:
                widget.destroy()

    def clear_center(self):
        for widget in self._frame_center.winfo_children():
            if widget != self.label_center:
                widget.destroy()

    def clear_right(self):
        for widget in self._frame_right.winfo_children():
            if widget != self.label_right:
                widget.destroy()

    @property
    def frame_left(self): return self._frame_left

    @property
    def frame_center(self): return self._frame_center

    @property
    def frame_right(self): return self._frame_right

''' Example usage: 

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")
    layout = FixedThreePaneLayout(root)
    layout.pack(fill=tk.BOTH, expand=True)

    # Example usage
    layout.set_label_texts(center="🎨 Workspace")
    layout.add_to_center(tk.Text(root))
    layout.clear_right()
    layout.add_to_right(tk.Label(root, text="Live Preview"))

    root.mainloop()'''
