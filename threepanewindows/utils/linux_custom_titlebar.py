# linux custom titlebar
import tkinter as tk


class TitleBar(tk.Frame):
    def __init__(self, master, theme, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.theme = theme
        self.buttons = []  # store buttons for easy re-theming
        self._normal_geometry = None
        self._is_maximized = False

        self.configure(height=theme["height"])
        self.pack(fill="x")

        # Title label
        self.title = tk.Label(self, text=master.title())
        self.title.pack(side="left", padx=8)

        # Button container
        btn_frame = tk.Frame(self)
        btn_frame.pack(side="right")

        # Make control buttons
        for symbol, cmd in [
            ("—", self._minimize),
            ("□", self._toggle_maximize),
            ("✕", self._close),
        ]:
            btn = self._make_button(btn_frame, symbol, cmd)
            self.buttons.append(btn)

        # Bind dragging to both frame and label
        for widget in (self, self.title):
            widget.bind("<ButtonPress-1>", self._start_move)
            widget.bind("<B1-Motion>", self._on_move)

        # Apply initial styling
        self.apply_theme(theme)

    def _make_button(self, parent, symbol, command):
        btn = tk.Label(parent, text=symbol, cursor="hand2")
        btn.pack(side="right", padx=2, pady=2)
        btn.bind("<Button-1>", lambda e: command())
        return btn

    def apply_theme(self, theme):
        """Reconfigure all colors, fonts, hover behaviors."""
        self.theme = theme
        # Frame + title
        self.config(bg=theme["bg"])
        self.title.config(bg=theme["bg"], fg=theme["fg"], font=theme["font"])

        # Buttons
        for btn in self.buttons:
            btn.config(
                bg=theme["btn_bg"], fg=theme["btn_fg"], font=theme["font"], width=4
            )
            # remove old bindings then rebind hover
            btn.unbind("<Enter>")
            btn.unbind("<Leave>")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=theme["btn_active_bg"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=theme["btn_bg"]))

        # Container bg
        for frame in (self.master,):
            # master bg is content_bg—set elsewhere
            pass

    def _start_move(self, event):
        self.x, self.y = event.x, event.y

    def _on_move(self, event):
        dx = event.x_root - self.x
        dy = event.y_root - self.y
        self.master.geometry(f"+{dx}+{dy}")

    def _minimize(self):
        self.master.iconify()

    def _toggle_maximize(self):
        sw, sh = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        if not self._is_maximized:
            self._normal_geometry = self.master.geometry()
            self.master.geometry(f"{sw}x{sh}+0+0")
        else:
            self.master.geometry(self._normal_geometry)
        self._is_maximized = not self._is_maximized

    def _close(self):
        self.master.destroy()


class App:
    def __init__(self, root, theme):
        self.root = root
        self.theme = theme

        print("Setting up the main application window with a custom title bar...")

        root.title("Dynamic Themed App")
        root.overrideredirect(True)

        # Force window to appear on top initially
        root.lift()
        root.attributes("-topmost", True)
        root.after(
            100, lambda: root.attributes("-topmost", False)
        )  # Remove topmost after 100ms

        print("Window decorations removed.")

        # Title bar
        self.titlebar = TitleBar(root, theme)

        print("Title bar created with theme:", theme)

        # Main content
        self.content = tk.Frame(root)
        self.content.pack(expand=True, fill="both")

        print("Main content area created.")

        self.label = tk.Label(self.content, text="Hello, world!")
        self.label.pack(pady=20)

        print("Main label created.")

        # Theme-switch button
        self.switch_btn = tk.Button(
            self.content, text="Switch Theme", command=self.on_switch_theme
        )
        self.switch_btn.pack(pady=10)

        print("Theme switch button created.")

        # Apply initial theme
        self.apply_theme(theme)

        # Add hotkey to bring window to front (Ctrl+Shift+F)
        root.bind("<Control-Shift-F>", self.bring_to_front)

    def apply_theme(self, theme):
        """Apply theme to all widgets."""
        self.theme = theme
        # Title bar
        self.titlebar.apply_theme(theme)

        print("Title bar theme applied.")

        # Content frame
        self.content.config(bg=theme["content_bg"])

        print("Content frame theme applied.")

        # Other widgets
        for widget in (self.label, self.switch_btn):
            cfg = {"bg": theme.get("content_bg", ""), "fg": theme.get("fg", "")}

            print(f"Applying theme to widget: {widget}")

            # Buttons need relief styling too
            if isinstance(widget, tk.Button):
                widget.config(
                    **cfg, font=theme["font"], activebackground=theme["btn_active_bg"]
                )
            else:
                widget.config(**cfg, font=theme["font"])

            print(f"Widget theme applied: {widget}")

    def on_switch_theme(self):
        """Example: cycle through dark, light, green."""
        if self.theme is dark_theme:
            new = light_theme
        elif self.theme is light_theme:
            new = green_theme
        else:
            new = dark_theme
        self.apply_theme(new)

        print("Theme switched to:", new)

    def bring_to_front(self, event=None):
        """Bring window to front when Ctrl+Shift+F is pressed."""
        self.root.lift()
        self.root.focus_force()
        print("Window brought to front")


# example usage of linux custom titlebar
if __name__ == "__main__":
    # Existing themes
    dark_theme = {
        "bg": "#282c34",
        "fg": "#abb2bf",
        "btn_bg": "#21252b",
        "btn_fg": "#61afef",
        "btn_active_bg": "#61afef",
        "content_bg": "#21252b",
        "font": ("Segoe UI", 10),
        "height": 30,
    }
    light_theme = {
        "bg": "#f5f5f5",
        "fg": "#202020",
        "btn_bg": "#e0e0e0",
        "btn_fg": "#202020",
        "btn_active_bg": "#c8c8c8",
        "content_bg": "#ffffff",
        "font": ("Segoe UI", 10),
        "height": 30,
    }
    green_theme = {
        "bg": "#2e7d32",
        "fg": "#ffffff",
        "btn_bg": "#388e3c",
        "btn_fg": "#ffffff",
        "btn_active_bg": "#66bb6a",
        "content_bg": "#e8f5e9",
        "font": ("Segoe UI", 10),
        "height": 30,
    }

    print("Starting Linux Custom Titlebar Example...")

    root = tk.Tk()
    app = App(root, dark_theme)
    root.mainloop()
