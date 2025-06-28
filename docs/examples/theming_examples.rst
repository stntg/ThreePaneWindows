Theming Examples
================

This section demonstrates how to apply and customize themes in ThreePaneWindows applications.

Basic Theme Application
-----------------------

Apply built-in themes to your layouts. **Important**: To see theme effects, you must apply theme colors to your content widgets:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

    def create_themed_example():
        root = tk.Tk()
        root.title("Themed Three-Pane Window")
        root.geometry("1000x600")

        # Store window reference to access theme manager
        window_ref = [None]

        def build_themed_content(frame, title):
            """Build content that properly uses theme colors."""
            # Get current theme
            theme = window_ref[0].theme_manager.get_current_theme() if window_ref[0] else None

            # Apply theme background to frame
            if theme:
                frame.configure(bg=theme.colors.panel_content_bg)

            # Themed title
            title_label = tk.Label(frame, text=title, font=("Arial", 12, "bold"))
            if theme:
                title_label.configure(
                    bg=theme.colors.panel_content_bg,
                    fg=theme.colors.primary_text
                )
            title_label.pack(pady=10)

            # Themed content area
            content_frame = tk.Frame(frame)
            if theme:
                content_frame.configure(bg=theme.colors.panel_content_bg)
            content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Themed label
            sample_label = tk.Label(content_frame, text="This content uses theme colors!",
                                   font=("Arial", 10))
            if theme:
                sample_label.configure(
                    bg=theme.colors.panel_content_bg,
                    fg=theme.colors.secondary_text
                )
            sample_label.pack(pady=5)

            # Themed buttons
            for i in range(3):
                btn = tk.Button(content_frame, text=f"Themed Button {i+1}",
                              font=("Arial", 10), width=15)
                if theme:
                    btn.configure(
                        bg=theme.colors.button_bg,
                        fg=theme.colors.button_fg,
                        activebackground=theme.colors.button_hover,
                        relief="flat"
                    )
                btn.pack(pady=2)

            # Themed text area
            text_area = tk.Text(content_frame, height=4, font=("Arial", 10))
            if theme:
                text_area.configure(
                    bg=theme.colors.secondary_bg,
                    fg=theme.colors.primary_text,
                    insertbackground=theme.colors.primary_text,
                    selectbackground=theme.colors.accent_bg
                )
            text_area.pack(fill=tk.X, pady=5)
            text_area.insert("1.0", f"Themed text area in {title}")

        def create_window_with_theme(theme_name):
            """Create window with specified theme."""
            # Clear existing window
            for widget in root.winfo_children():
                if isinstance(widget, EnhancedDockableThreePaneWindow):
                    widget.destroy()

            # Configure panes
            left_config = PaneConfig(title="Navigation", icon="🧭", default_width=200)
            center_config = PaneConfig(title="Content", icon="📝")
            right_config = PaneConfig(title="Tools", icon="🔧", default_width=180)

            # Create window with theme
            window = EnhancedDockableThreePaneWindow(
                root,
                left_config=left_config,
                center_config=center_config,
                right_config=right_config,
                left_builder=lambda f: build_themed_content(f, "Navigation Panel"),
                center_builder=lambda f: build_themed_content(f, "Main Content"),
                right_builder=lambda f: build_themed_content(f, "Tool Panel"),
                theme_name=theme_name
            )

            window_ref[0] = window  # Store reference
            window.pack(fill=tk.BOTH, expand=True)
            return window

        # Create initial window
        window = create_window_with_theme("light")

        # Theme switcher
        control_frame = tk.Frame(root, bg="#f0f0f0")
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        tk.Label(control_frame, text="Theme:", font=("Arial", 10, "bold"),
                bg="#f0f0f0").pack(side=tk.LEFT, padx=10)

        for theme_name in ["light", "dark", "blue"]:
            btn = tk.Button(control_frame, text=theme_name.title(),
                           command=lambda t=theme_name: create_window_with_theme(t))
            btn.pack(side=tk.LEFT, padx=5)

        return root

    if __name__ == "__main__":
        app = create_themed_example()
        app.mainloop()

Theme Comparison Demo
---------------------

Compare different built-in themes:

.. code-block:: python

    import tkinter as tk
    from tkinter import ttk
    from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

    class ThemeComparisonDemo:
        """Demo application showing different themes."""

        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Theme Comparison Demo")
            self.root.geometry("1200x800")

            self.current_theme = "blue"
            self.setup_ui()

        def setup_ui(self):
            """Set up the user interface."""
            # Theme selector toolbar
            toolbar = tk.Frame(self.root, bg="#f0f0f0", height=40)
            toolbar.pack(fill=tk.X)
            toolbar.pack_propagate(False)

            tk.Label(toolbar, text="Theme:", font=("Arial", 10, "bold"),
                    bg="#f0f0f0").pack(side=tk.LEFT, padx=10, pady=10)

            # Theme buttons
            themes = [
                ("Blue Professional", "blue", "#3498DB"),
                ("Dark Modern", "dark", "#2C3E50"),
                ("Light Clean", "light", "#ECF0F1"),
                ("Green Nature", "green", "#27AE60"),
                ("Purple Creative", "purple", "#9B59B6")
            ]

            for theme_name, theme_key, color in themes:
                btn = tk.Button(toolbar, text=theme_name, bg=color, fg="white",
                              font=("Arial", 9), relief="flat", padx=15,
                              command=lambda t=theme_key: self.change_theme(t))
                btn.pack(side=tk.LEFT, padx=2, pady=5)

            # Create the main window
            self.create_main_window()

        def create_main_window(self):
            """Create the main three-pane window."""
            # Configure panes
            left_config = PaneConfig(
                title="File Explorer",
                icon="📁",
                default_width=250,
                detachable=True
            )

            center_config = PaneConfig(
                title="Code Editor",
                icon="📝",
                detachable=False
            )

            right_config = PaneConfig(
                title="Properties",
                icon="🔧",
                default_width=200,
                detachable=True
            )

            # Create enhanced window
            self.window = EnhancedDockableThreePaneWindow(
                self.root,
                left_config=left_config,
                center_config=center_config,
                right_config=right_config,
                left_builder=self.build_file_explorer,
                center_builder=self.build_code_editor,
                right_builder=self.build_properties,
                theme_name=self.current_theme
            )
            self.window.pack(fill=tk.BOTH, expand=True)

        def build_file_explorer(self, frame):
            """Build file explorer content."""
            # Header
            header = tk.Frame(frame, height=30)
            header.pack(fill=tk.X, padx=5, pady=5)
            header.pack_propagate(False)

            tk.Label(header, text="📁 Project Files",
                    font=("Arial", 11, "bold")).pack(side=tk.LEFT, pady=5)

            # File tree
            tree_frame = tk.Frame(frame)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            file_tree = ttk.Treeview(tree_frame)
            scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=file_tree.yview)
            file_tree.configure(yscrollcommand=scrollbar.set)

            file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Sample file structure
            project = file_tree.insert("", "end", text="📁 ThemeDemo", open=True)
            src = file_tree.insert(project, "end", text="📁 src", open=True)
            file_tree.insert(src, "end", text="📄 main.py")
            file_tree.insert(src, "end", text="📄 themes.py")
            file_tree.insert(src, "end", text="📄 utils.py")

            styles = file_tree.insert(project, "end", text="📁 styles")
            file_tree.insert(styles, "end", text="🎨 blue.css")
            file_tree.insert(styles, "end", text="🎨 dark.css")
            file_tree.insert(styles, "end", text="🎨 light.css")

        def build_code_editor(self, frame):
            """Build code editor content."""
            # Editor header
            header = tk.Frame(frame, height=35)
            header.pack(fill=tk.X)
            header.pack_propagate(False)

            tk.Label(header, text="📝 themes.py", font=("Arial", 11, "bold")).pack(
                side=tk.LEFT, padx=10, pady=8)

            # Editor area
            editor_frame = tk.Frame(frame)
            editor_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Code editor
            code_editor = tk.Text(editor_frame, wrap=tk.NONE, font=("Consolas", 11))

            # Scrollbars
            v_scroll = tk.Scrollbar(editor_frame, orient=tk.VERTICAL, command=code_editor.yview)
            h_scroll = tk.Scrollbar(editor_frame, orient=tk.HORIZONTAL, command=code_editor.xview)
            code_editor.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

            code_editor.grid(row=0, column=0, sticky="nsew")
            v_scroll.grid(row=0, column=1, sticky="ns")
            h_scroll.grid(row=1, column=0, sticky="ew")

            editor_frame.grid_rowconfigure(0, weight=1)
            editor_frame.grid_columnconfigure(0, weight=1)

            # Sample theme code
            sample_code = '''"""
Theme configuration for ThreePaneWindows.
"""

THEMES = {
    "blue": {
        "primary": "#3498DB",
        "secondary": "#2980B9",
        "background": "#ECF0F1",
        "text": "#2C3E50",
        "accent": "#E74C3C"
    },

    "dark": {
        "primary": "#2C3E50",
        "secondary": "#34495E",
        "background": "#1E1E1E",
        "text": "#ECF0F1",
        "accent": "#E67E22"
    },

    "light": {
        "primary": "#BDC3C7",
        "secondary": "#95A5A6",
        "background": "#FFFFFF",
        "text": "#2C3E50",
        "accent": "#3498DB"
    }
}

def apply_theme(window, theme_name):
    """Apply a theme to the window."""
    if theme_name in THEMES:
        theme = THEMES[theme_name]
        window.configure_theme(theme)
        return True
    return False'''

            code_editor.insert("1.0", sample_code)

        def build_properties(self, frame):
            """Build properties panel content."""
            tk.Label(frame, text="🎨 Theme Properties",
                    font=("Arial", 11, "bold")).pack(pady=10)

            # Theme info
            info_frame = tk.LabelFrame(frame, text="Current Theme",
                                     font=("Arial", 10, "bold"))
            info_frame.pack(fill=tk.X, padx=10, pady=10)

            self.theme_info_label = tk.Label(info_frame, text=f"Theme: {self.current_theme.title()}",
                                           font=("Arial", 10))
            self.theme_info_label.pack(pady=5)

            # Color palette
            palette_frame = tk.LabelFrame(frame, text="Color Palette",
                                        font=("Arial", 10, "bold"))
            palette_frame.pack(fill=tk.X, padx=10, pady=10)

            # Sample color swatches
            colors = self.get_theme_colors(self.current_theme)
            self.color_swatches = []

            for color_name, color_value in colors.items():
                swatch_frame = tk.Frame(palette_frame)
                swatch_frame.pack(fill=tk.X, padx=5, pady=2)

                color_box = tk.Frame(swatch_frame, bg=color_value, width=20, height=20)
                color_box.pack(side=tk.LEFT, padx=5)
                color_box.pack_propagate(False)

                tk.Label(swatch_frame, text=f"{color_name}: {color_value}",
                        font=("Arial", 9)).pack(side=tk.LEFT, padx=5)

                self.color_swatches.append((color_box, color_name))

            # Theme features
            features_frame = tk.LabelFrame(frame, text="Features",
                                         font=("Arial", 10, "bold"))
            features_frame.pack(fill=tk.X, padx=10, pady=10)

            features = [
                "✓ Professional appearance",
                "✓ Consistent color scheme",
                "✓ Optimized contrast",
                "✓ Modern design",
                "✓ Easy customization"
            ]

            for feature in features:
                tk.Label(features_frame, text=feature, font=("Arial", 9),
                        anchor="w").pack(fill=tk.X, padx=5, pady=1)

        def get_theme_colors(self, theme_name):
            """Get colors for a theme."""
            theme_colors = {
                "blue": {
                    "Primary": "#3498DB",
                    "Secondary": "#2980B9",
                    "Background": "#ECF0F1",
                    "Text": "#2C3E50",
                    "Accent": "#E74C3C"
                },
                "dark": {
                    "Primary": "#2C3E50",
                    "Secondary": "#34495E",
                    "Background": "#1E1E1E",
                    "Text": "#ECF0F1",
                    "Accent": "#E67E22"
                },
                "light": {
                    "Primary": "#BDC3C7",
                    "Secondary": "#95A5A6",
                    "Background": "#FFFFFF",
                    "Text": "#2C3E50",
                    "Accent": "#3498DB"
                },
                "green": {
                    "Primary": "#27AE60",
                    "Secondary": "#229954",
                    "Background": "#E8F8F5",
                    "Text": "#1B4F3C",
                    "Accent": "#F39C12"
                },
                "purple": {
                    "Primary": "#9B59B6",
                    "Secondary": "#8E44AD",
                    "Background": "#F4ECF7",
                    "Text": "#4A235A",
                    "Accent": "#E67E22"
                }
            }
            return theme_colors.get(theme_name, theme_colors["blue"])

        def change_theme(self, theme_name):
            """Change the current theme."""
            self.current_theme = theme_name

            # Destroy and recreate the window with new theme
            self.window.destroy()
            self.create_main_window()

            # Update theme info if properties panel exists
            if hasattr(self, 'theme_info_label'):
                self.theme_info_label.config(text=f"Theme: {theme_name.title()}")

        def run(self):
            """Run the demo application."""
            self.root.mainloop()

    if __name__ == "__main__":
        demo = ThemeComparisonDemo()
        demo.run()

Custom Theme Creation
---------------------

Create your own custom themes:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

    def create_custom_theme_example():
        """Example of creating custom themes."""

        class CustomThemeWindow(EnhancedDockableThreePaneWindow):
            """Extended window with custom theme support."""

            def __init__(self, parent, **kwargs):
                # Define custom themes
                self.custom_themes = {
                    "ocean": {
                        "primary": "#006994",
                        "secondary": "#004d6b",
                        "background": "#e6f3ff",
                        "text": "#003d52",
                        "accent": "#ff6b35",
                        "panel_bg": "#cce7ff",
                        "border": "#0080b3"
                    },
                    "sunset": {
                        "primary": "#ff6b35",
                        "secondary": "#e55a2b",
                        "background": "#fff5f0",
                        "text": "#8b2500",
                        "accent": "#4ecdc4",
                        "panel_bg": "#ffe6d9",
                        "border": "#ff8c5a"
                    },
                    "forest": {
                        "primary": "#2d5016",
                        "secondary": "#1e3610",
                        "background": "#f0f8e8",
                        "text": "#1a2e0d",
                        "accent": "#ff9500",
                        "panel_bg": "#e1f0d4",
                        "border": "#4a7c2a"
                    }
                }

                super().__init__(parent, **kwargs)

            def apply_custom_theme(self, theme_name):
                """Apply a custom theme."""
                if theme_name in self.custom_themes:
                    theme = self.custom_themes[theme_name]
                    self.configure_custom_colors(theme)

            def configure_custom_colors(self, theme):
                """Configure colors based on theme."""
                # Apply theme colors to the window
                self.configure(bg=theme["background"])

                # Apply to pane headers if they exist
                for pane in [self.left_pane, self.center_pane, self.right_pane]:
                    if hasattr(pane, 'header'):
                        pane.header.configure(bg=theme["primary"], fg="white")

                # Apply to content areas
                for pane in [self.left_pane, self.center_pane, self.right_pane]:
                    if hasattr(pane, 'content_frame'):
                        pane.content_frame.configure(bg=theme["panel_bg"])

        root = tk.Tk()
        root.title("Custom Theme Example")
        root.geometry("1000x600")

        def build_theme_demo(frame, theme_name):
            """Build content to demonstrate the theme."""
            # Theme header
            header = tk.Frame(frame, height=40)
            header.pack(fill=tk.X, padx=5, pady=5)
            header.pack_propagate(False)

            tk.Label(header, text=f"🎨 {theme_name.title()} Theme",
                    font=("Arial", 12, "bold")).pack(pady=10)

            # Sample content
            content_frame = tk.Frame(frame)
            content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Sample widgets to show theme colors
            tk.Label(content_frame, text="Sample Text",
                    font=("Arial", 11)).pack(pady=5)

            btn_frame = tk.Frame(content_frame)
            btn_frame.pack(pady=10)

            tk.Button(btn_frame, text="Primary Button",
                     font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Secondary Button",
                     font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

            # Sample list
            listbox = tk.Listbox(content_frame, height=6)
            listbox.pack(fill=tk.X, pady=10)

            for i in range(5):
                listbox.insert(tk.END, f"Sample Item {i+1}")

        # Configure panes
        left_config = PaneConfig(title="Ocean Theme", icon="🌊", default_width=200)
        center_config = PaneConfig(title="Sunset Theme", icon="🌅")
        right_config = PaneConfig(title="Forest Theme", icon="🌲", default_width=200)

        # Create custom themed window
        window = CustomThemeWindow(
            root,
            left_config=left_config,
            center_config=center_config,
            right_config=right_config,
            left_builder=lambda f: build_theme_demo(f, "ocean"),
            center_builder=lambda f: build_theme_demo(f, "sunset"),
            right_builder=lambda f: build_theme_demo(f, "forest")
        )
        window.pack(fill=tk.BOTH, expand=True)

        # Theme selector
        theme_frame = tk.Frame(root, bg="#f0f0f0", height=35)
        theme_frame.pack(fill=tk.X)
        theme_frame.pack_propagate(False)

        tk.Label(theme_frame, text="Custom Themes:", font=("Arial", 10, "bold"),
                bg="#f0f0f0").pack(side=tk.LEFT, padx=10, pady=8)

        themes = [("Ocean", "ocean"), ("Sunset", "sunset"), ("Forest", "forest")]
        for theme_name, theme_key in themes:
            btn = tk.Button(theme_frame, text=theme_name, font=("Arial", 9),
                          command=lambda t=theme_key: window.apply_custom_theme(t))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        return root

    if __name__ == "__main__":
        app = create_custom_theme_example()
        app.mainloop()

Theme Best Practices
--------------------

Guidelines for effective theming:

1. **Consistent Color Palette**: Use a limited, harmonious color scheme
2. **Sufficient Contrast**: Ensure text is readable against backgrounds
3. **Semantic Colors**: Use colors that convey meaning (red for errors, green for success)
4. **Accessibility**: Consider color-blind users and high contrast needs
5. **Brand Alignment**: Match your application's brand colors and style

Available Built-in Themes
--------------------------

ThreePaneWindows includes these built-in themes:

**Blue Professional**
- Primary: Professional blue tones
- Use case: Business applications, productivity tools
- Characteristics: Clean, trustworthy, professional

**Dark Modern**
- Primary: Dark grays and blacks
- Use case: Code editors, creative tools, night mode
- Characteristics: Reduced eye strain, modern, sleek

**Light Clean**
- Primary: Light grays and whites
- Use case: Document editors, general applications
- Characteristics: Bright, clean, minimalist

**System**
- Primary: Follows system theme preferences
- Use case: Applications that should match OS appearance
- Characteristics: Adaptive, native feel

Theme Configuration
-------------------

Configure themes in your applications:

.. code-block:: python

    # Apply built-in theme
    window = EnhancedDockableThreePaneWindow(
        root,
        theme_name="dark"  # or "blue", "light", "system"
    )

    # Create custom theme
    custom_theme = {
        "primary": "#your_color",
        "secondary": "#your_color",
        "background": "#your_color",
        "text": "#your_color",
        "accent": "#your_color"
    }

    # Apply custom theme
    window.apply_custom_theme(custom_theme)

Common Theming Issues and Solutions
------------------------------------

**Issue: Themes don't seem to work or look the same**

This is usually because user content widgets aren't using theme colors. The ThreePaneWindows framework (headers, separators, containers) gets themed automatically, but content you add to panes needs manual theming.

**Solution**: Always apply theme colors to your widgets:

.. code-block:: python

    def build_properly_themed_content(frame):
        # Get the current theme
        theme = window.theme_manager.get_current_theme()

        # Apply theme to frame
        frame.configure(bg=theme.colors.panel_content_bg)

        # Apply theme to widgets
        label = tk.Label(frame, text="Themed Label")
        label.configure(
            bg=theme.colors.panel_content_bg,
            fg=theme.colors.primary_text
        )

        button = tk.Button(frame, text="Themed Button")
        button.configure(
            bg=theme.colors.button_bg,
            fg=theme.colors.button_fg,
            activebackground=theme.colors.button_hover
        )

**Issue: Blue theme looks the same as light theme**

The built-in "blue" and "light" themes have subtle differences. For more dramatic theming, create custom themes:

.. code-block:: python

    from threepanewindows.themes import Theme, ColorScheme

    # Create dramatic custom theme
    dramatic_colors = ColorScheme(
        primary_bg="#000080",      # Navy blue
        secondary_bg="#0000cc",    # Bright blue
        panel_content_bg="#e6f0ff", # Light blue
        primary_text="#ffffff",    # White text
        button_bg="#ff4500",       # Orange buttons
        button_fg="#ffffff"        # White button text
    )

    custom_theme = Theme(name="Dramatic Blue", colors=dramatic_colors)

    # Register and use
    window.theme_manager.register_theme(custom_theme)
    window.theme_manager.set_theme("dramatic blue")

**Issue: Themes work on some platforms but not others**

Different operating systems handle widget styling differently:

- **Windows**: May require explicit color setting for all widgets
- **macOS**: Better automatic theme inheritance
- **Linux**: Varies by desktop environment
- **Android (Pydroid)**: Different default styling

**Solution**: Always explicitly set theme colors for cross-platform consistency.

Theme Helper Function
---------------------

Create a helper function to easily apply themes to your widgets:

.. code-block:: python

    def apply_theme_to_widget(widget, widget_type="default", theme_manager=None):
        """Apply current theme to a widget."""
        if not theme_manager:
            return

        theme = theme_manager.get_current_theme()

        if widget_type == "label":
            widget.configure(
                bg=theme.colors.panel_content_bg,
                fg=theme.colors.primary_text
            )
        elif widget_type == "button":
            widget.configure(
                bg=theme.colors.button_bg,
                fg=theme.colors.button_fg,
                activebackground=theme.colors.button_hover,
                activeforeground=theme.colors.button_fg,
                relief="flat"
            )
        elif widget_type == "text":
            widget.configure(
                bg=theme.colors.secondary_bg,
                fg=theme.colors.primary_text,
                insertbackground=theme.colors.primary_text,
                selectbackground=theme.colors.accent_bg
            )
        elif widget_type == "frame":
            widget.configure(bg=theme.colors.panel_content_bg)

    # Usage
    label = tk.Label(frame, text="My Label")
    apply_theme_to_widget(label, "label", window.theme_manager)

Best Practices for Theming
---------------------------

1. **Always Theme User Content**: Framework components are themed automatically, but your content needs manual theming
2. **Use Theme Colors Consistently**: Don't mix hardcoded colors with theme colors
3. **Test on Multiple Platforms**: Themes may look different on Windows, macOS, and Linux
4. **Provide Theme Switching**: Allow users to change themes at runtime
5. **Create Dramatic Custom Themes**: For better visual feedback during development
6. **Use Helper Functions**: Create utilities to apply themes consistently

Next Steps
----------

Explore more customization options:

- :doc:`custom_widgets` - Creating themed custom widgets
- :doc:`real_world_applications` - Themed complete applications
- Advanced CSS-like styling for complex themes
