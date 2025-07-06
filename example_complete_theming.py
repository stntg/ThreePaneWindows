#!/usr/bin/env python3
"""
Complete theming example demonstrating fully functional cross-platform theming.

This example shows:
- Automatic widget theming (both TTK and TK widgets)
- Platform-native themes with proper integration
- Real-time theme switching
- Comprehensive widget coverage
- Professional appearance across platforms
"""

import os
import platform
import sys
import tkinter as tk
from tkinter import ttk

# Add the package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from threepanewindows.platform import platform_handler
from threepanewindows.themes import ThemeManager, ThemeType


class CompleteThemingDemo:
    """Complete demonstration of the theming system."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"Complete Theming Demo - {platform.system()}")
        self.root.geometry("1000x700")

        # Initialize theme manager with native theme
        self.theme_manager = ThemeManager(theme=ThemeType.NATIVE)

        # Create the UI
        self.create_ui()

        # Apply initial theme
        self.apply_theme("native")

    def create_ui(self):
        """Create the complete user interface."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Complete Cross-Platform Theming Demo",
            font=("default", 18, "bold"),
        )
        title_label.pack(pady=(0, 20))

        # Theme selection panel
        self.create_theme_panel(main_frame)

        # Create tabbed interface
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, pady=(10, 0))

        # TTK Widgets tab
        self.create_ttk_widgets_tab(notebook)

        # TK Widgets tab
        self.create_tk_widgets_tab(notebook)

        # Mixed Layout tab
        self.create_mixed_layout_tab(notebook)

        # Platform Info tab
        self.create_platform_info_tab(notebook)

    def create_theme_panel(self, parent):
        """Create theme selection panel."""
        theme_frame = ttk.LabelFrame(parent, text="Theme Selection")
        theme_frame.pack(fill="x", pady=(0, 10))

        # Get available themes
        available_themes = self.theme_manager.get_available_themes()

        # Organize themes
        standard_themes = [
            t
            for t in ["light", "dark", "blue", "green", "purple"]
            if t in available_themes
        ]
        system_themes = [t for t in ["system"] if t in available_themes]
        native_themes = [
            t
            for t in ["native", "native_light", "native_dark"]
            if t in available_themes
        ]

        button_frame = ttk.Frame(theme_frame)
        button_frame.pack(fill="x", padx=10, pady=10)

        row = 0
        col = 0

        # Standard themes
        if standard_themes:
            std_label = ttk.Label(
                button_frame, text="Standard:", font=("default", 9, "bold")
            )
            std_label.grid(row=row, column=0, sticky="w", padx=(0, 10))
            col = 1

            for theme in standard_themes:
                btn = ttk.Button(
                    button_frame,
                    text=theme.title(),
                    command=lambda t=theme: self.apply_theme(t),
                    width=8,
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                col += 1
                if col > 6:
                    row += 1
                    col = 0

            if col > 0:
                row += 1

        # System themes
        if system_themes:
            sys_label = ttk.Label(
                button_frame, text="System:", font=("default", 9, "bold")
            )
            sys_label.grid(row=row, column=0, sticky="w", padx=(0, 10))
            col = 1

            for theme in system_themes:
                btn = ttk.Button(
                    button_frame,
                    text=theme.title(),
                    command=lambda t=theme: self.apply_theme(t),
                    width=8,
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                col += 1

            row += 1

        # Native themes
        if native_themes:
            native_label = ttk.Label(
                button_frame, text="Native:", font=("default", 9, "bold")
            )
            native_label.grid(row=row, column=0, sticky="w", padx=(0, 10))
            col = 1

            for theme in native_themes:
                display_name = theme.replace("_", " ").title()
                btn = ttk.Button(
                    button_frame,
                    text=display_name,
                    command=lambda t=theme: self.apply_theme(t),
                    width=10,
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                col += 1

        # Current theme display
        self.current_theme_var = tk.StringVar()
        current_label = ttk.Label(
            theme_frame,
            textvariable=self.current_theme_var,
            font=("default", 10, "bold"),
        )
        current_label.pack(pady=5)

        # Refresh button
        refresh_btn = ttk.Button(
            theme_frame, text="Refresh System Theme", command=self.refresh_theme
        )
        refresh_btn.pack(pady=2)

    def create_ttk_widgets_tab(self, notebook):
        """Create TTK widgets demonstration tab."""
        ttk_frame = ttk.Frame(notebook)
        notebook.add(ttk_frame, text="TTK Widgets")

        # Create scrollable frame
        canvas = tk.Canvas(ttk_frame)
        scrollbar = ttk.Scrollbar(ttk_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Labels section
        labels_frame = ttk.LabelFrame(scrollable_frame, text="Labels")
        labels_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(labels_frame, text="Normal TTK Label").pack(
            anchor="w", padx=5, pady=2
        )
        ttk.Label(
            labels_frame, text="Bold TTK Label", font=("default", 10, "bold")
        ).pack(anchor="w", padx=5, pady=2)
        ttk.Label(labels_frame, text="Large TTK Label", font=("default", 12)).pack(
            anchor="w", padx=5, pady=2
        )

        # Buttons section
        buttons_frame = ttk.LabelFrame(scrollable_frame, text="Buttons")
        buttons_frame.pack(fill="x", padx=10, pady=5)

        btn_container = ttk.Frame(buttons_frame)
        btn_container.pack(fill="x", padx=5, pady=5)

        ttk.Button(btn_container, text="Normal Button").pack(side="left", padx=2)
        ttk.Button(btn_container, text="Disabled Button", state="disabled").pack(
            side="left", padx=2
        )

        # Entry widgets section
        entry_frame = ttk.LabelFrame(scrollable_frame, text="Entry Widgets")
        entry_frame.pack(fill="x", padx=10, pady=5)

        entry_container = ttk.Frame(entry_frame)
        entry_container.pack(fill="x", padx=5, pady=5)

        ttk.Label(entry_container, text="Entry:").grid(
            row=0, column=0, sticky="w", padx=(0, 5)
        )
        entry = ttk.Entry(entry_container, width=20)
        entry.insert(0, "Sample text")
        entry.grid(row=0, column=1, padx=5)

        ttk.Label(entry_container, text="Combobox:").grid(
            row=0, column=2, sticky="w", padx=(10, 5)
        )
        combo = ttk.Combobox(
            entry_container, values=["Option 1", "Option 2", "Option 3"], width=15
        )
        combo.set("Option 1")
        combo.grid(row=0, column=3, padx=5)

        # Selection widgets section
        selection_frame = ttk.LabelFrame(scrollable_frame, text="Selection Widgets")
        selection_frame.pack(fill="x", padx=10, pady=5)

        sel_container = ttk.Frame(selection_frame)
        sel_container.pack(fill="x", padx=5, pady=5)

        # Checkbuttons
        check_var1 = tk.BooleanVar(value=True)
        check_var2 = tk.BooleanVar()
        ttk.Checkbutton(sel_container, text="Checked", variable=check_var1).pack(
            side="left", padx=5
        )
        ttk.Checkbutton(sel_container, text="Unchecked", variable=check_var2).pack(
            side="left", padx=5
        )

        # Radiobuttons
        radio_var = tk.StringVar(value="1")
        ttk.Radiobutton(
            sel_container, text="Option 1", variable=radio_var, value="1"
        ).pack(side="left", padx=10)
        ttk.Radiobutton(
            sel_container, text="Option 2", variable=radio_var, value="2"
        ).pack(side="left", padx=5)

        # Progress and Scale section
        progress_frame = ttk.LabelFrame(scrollable_frame, text="Progress & Scale")
        progress_frame.pack(fill="x", padx=10, pady=5)

        prog_container = ttk.Frame(progress_frame)
        prog_container.pack(fill="x", padx=5, pady=5)

        ttk.Label(prog_container, text="Progress:").pack(side="left")
        progress = ttk.Progressbar(prog_container, length=200, value=65)
        progress.pack(side="left", padx=5)

        ttk.Label(prog_container, text="Scale:").pack(side="left", padx=(20, 0))
        scale = ttk.Scale(prog_container, from_=0, to=100, length=150, value=35)
        scale.pack(side="left", padx=5)

        # Treeview section
        tree_frame = ttk.LabelFrame(scrollable_frame, text="Treeview")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        tree = ttk.Treeview(tree_frame, height=6)
        tree.heading("#0", text="File Explorer")

        # Add sample items
        folder1 = tree.insert("", "end", text="Documents", open=True)
        tree.insert(folder1, "end", text="file1.txt")
        tree.insert(folder1, "end", text="file2.pdf")

        folder2 = tree.insert("", "end", text="Projects", open=True)
        tree.insert(folder2, "end", text="project1")
        tree.insert(folder2, "end", text="project2")

        tree.pack(fill="both", expand=True, padx=5, pady=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_tk_widgets_tab(self, notebook):
        """Create TK widgets demonstration tab."""
        tk_frame = ttk.Frame(notebook)
        notebook.add(tk_frame, text="TK Widgets")

        # Create scrollable frame
        canvas = tk.Canvas(tk_frame)
        scrollbar = ttk.Scrollbar(tk_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Text widget section
        text_frame = ttk.LabelFrame(scrollable_frame, text="Text Widget")
        text_frame.pack(fill="x", padx=10, pady=5)

        text_widget = tk.Text(text_frame, height=6, width=60, wrap=tk.WORD)
        text_widget.insert(
            "1.0",
            """This is a TK Text widget that demonstrates theming.

The text widget should adapt to the current theme:
• Background color matches the theme
• Text color is appropriate for the theme
• Font is consistent with the theme typography

Try switching themes to see the changes!""",
        )
        text_widget.pack(fill="x", padx=5, pady=5)

        # Listbox section
        listbox_frame = ttk.LabelFrame(scrollable_frame, text="Listbox")
        listbox_frame.pack(fill="x", padx=10, pady=5)

        list_container = ttk.Frame(listbox_frame)
        list_container.pack(fill="x", padx=5, pady=5)

        listbox = tk.Listbox(list_container, height=6)
        list_scroll = ttk.Scrollbar(
            list_container, orient="vertical", command=listbox.yview
        )
        listbox.configure(yscrollcommand=list_scroll.set)

        for i in range(15):
            listbox.insert("end", f"Themed List Item {i+1}")

        listbox.pack(side="left", fill="both", expand=True)
        list_scroll.pack(side="right", fill="y")

        # TK Controls section
        controls_frame = ttk.LabelFrame(scrollable_frame, text="TK Controls")
        controls_frame.pack(fill="x", padx=10, pady=5)

        controls_container = ttk.Frame(controls_frame)
        controls_container.pack(fill="x", padx=5, pady=5)

        # TK Labels
        tk.Label(controls_container, text="TK Label").pack(side="left", padx=5)

        # TK Buttons
        tk.Button(controls_container, text="TK Button").pack(side="left", padx=5)

        # TK Entry
        tk_entry = tk.Entry(controls_container, width=20)
        tk_entry.insert(0, "TK Entry")
        tk_entry.pack(side="left", padx=5)

        # Canvas section
        canvas_frame = ttk.LabelFrame(scrollable_frame, text="Canvas")
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

        demo_canvas = tk.Canvas(canvas_frame, height=120, width=400)
        demo_canvas.pack(fill="x", padx=5, pady=5)

        # Draw some shapes
        demo_canvas.create_rectangle(
            20, 20, 80, 80, fill="blue", outline="darkblue", width=2
        )
        demo_canvas.create_oval(
            100, 20, 160, 80, fill="red", outline="darkred", width=2
        )
        demo_canvas.create_line(180, 20, 240, 80, fill="green", width=3)
        demo_canvas.create_text(
            300, 50, text="Themed Canvas", font=("default", 12, "bold")
        )

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Store references for theming
        self.tk_widgets = {
            "text_widget": text_widget,
            "listbox": listbox,
            "demo_canvas": demo_canvas,
        }

    def create_mixed_layout_tab(self, notebook):
        """Create mixed layout demonstration tab."""
        mixed_frame = ttk.Frame(notebook)
        notebook.add(mixed_frame, text="Mixed Layout")

        # Create a realistic application layout
        # Toolbar
        toolbar = ttk.Frame(mixed_frame)
        toolbar.pack(fill="x", padx=5, pady=5)

        ttk.Button(toolbar, text="New").pack(side="left", padx=2)
        ttk.Button(toolbar, text="Open").pack(side="left", padx=2)
        ttk.Button(toolbar, text="Save").pack(side="left", padx=2)
        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=5)
        ttk.Button(toolbar, text="Cut").pack(side="left", padx=2)
        ttk.Button(toolbar, text="Copy").pack(side="left", padx=2)
        ttk.Button(toolbar, text="Paste").pack(side="left", padx=2)

        # Main content area
        content_paned = ttk.PanedWindow(mixed_frame, orient="horizontal")
        content_paned.pack(fill="both", expand=True, padx=5, pady=5)

        # Left sidebar
        left_frame = ttk.Frame(content_paned)
        content_paned.add(left_frame, weight=1)

        ttk.Label(left_frame, text="Explorer", font=("default", 10, "bold")).pack(
            pady=5
        )

        explorer_tree = ttk.Treeview(left_frame)
        explorer_tree.heading("#0", text="Files")

        root_item = explorer_tree.insert("", "end", text="Project", open=True)
        src_item = explorer_tree.insert(root_item, "end", text="src", open=True)
        explorer_tree.insert(src_item, "end", text="main.py")
        explorer_tree.insert(src_item, "end", text="utils.py")
        explorer_tree.insert(root_item, "end", text="README.md")

        explorer_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Center editor area
        center_frame = ttk.Frame(content_paned)
        content_paned.add(center_frame, weight=3)

        editor_notebook = ttk.Notebook(center_frame)
        editor_notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Editor tab 1
        editor1 = ttk.Frame(editor_notebook)
        editor_notebook.add(editor1, text="main.py")

        editor_text = tk.Text(editor1, wrap=tk.NONE, font=("Consolas", 10))
        editor_text.insert(
            "1.0",
            '''#!/usr/bin/env python3
"""
Sample Python file demonstrating theming in a code editor.
"""

import tkinter as tk
from tkinter import ttk

class ThemedApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Themed App")

        # Create theme manager
        from threepanewindows.themes import ThemeManager
        self.theme_manager = ThemeManager()

    def run(self):
        # Apply theme to window
        self.theme_manager.apply_theme_to_window(self.root)
        self.root.mainloop()

if __name__ == "__main__":
    app = ThemedApplication()
    app.run()
''',
        )

        # Add scrollbars to editor
        editor_scroll_y = ttk.Scrollbar(
            editor1, orient="vertical", command=editor_text.yview
        )
        editor_scroll_x = ttk.Scrollbar(
            editor1, orient="horizontal", command=editor_text.xview
        )
        editor_text.configure(
            yscrollcommand=editor_scroll_y.set, xscrollcommand=editor_scroll_x.set
        )

        editor_text.pack(side="left", fill="both", expand=True)
        editor_scroll_y.pack(side="right", fill="y")
        editor_scroll_x.pack(side="bottom", fill="x")

        # Editor tab 2
        editor2 = ttk.Frame(editor_notebook)
        editor_notebook.add(editor2, text="README.md")

        readme_text = tk.Text(editor2, wrap=tk.WORD)
        readme_text.insert(
            "1.0",
            """# Themed Application

This is a demonstration of the cross-platform theming system.

## Features

- **Cross-platform compatibility**: Works on Windows, macOS, and Linux
- **Native integration**: Uses platform-specific colors and fonts
- **Automatic theming**: Both TTK and TK widgets are themed
- **Real-time updates**: Themes can be changed dynamically

## Usage

```python
from threepanewindows.themes import ThemeManager, ThemeType

# Create theme manager
theme_manager = ThemeManager(theme=ThemeType.NATIVE)

# Apply to window
theme_manager.apply_theme_to_window(root)
```

## Supported Themes

- Light, Dark, Blue, Green, Purple (standard themes)
- System (follows OS theme)
- Native, Native Light, Native Dark (platform-specific)
""",
        )
        readme_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Right properties panel
        right_frame = ttk.Frame(content_paned)
        content_paned.add(right_frame, weight=1)

        ttk.Label(right_frame, text="Properties", font=("default", 10, "bold")).pack(
            pady=5
        )

        props_frame = ttk.Frame(right_frame)
        props_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Properties list
        properties = [
            ("File", "main.py"),
            ("Size", "2.1 KB"),
            ("Lines", "45"),
            ("Language", "Python"),
            ("Encoding", "UTF-8"),
            ("Modified", "2024-01-15 14:30"),
        ]

        for prop, value in properties:
            prop_container = ttk.Frame(props_frame)
            prop_container.pack(fill="x", pady=2)

            ttk.Label(
                prop_container, text=f"{prop}:", font=("default", 9, "bold")
            ).pack(side="left")
            ttk.Label(prop_container, text=value, font=("default", 9)).pack(
                side="right"
            )

        # Status bar
        status_frame = ttk.Frame(mixed_frame)
        status_frame.pack(fill="x", side="bottom")

        ttk.Label(status_frame, text="Ready").pack(side="left", padx=5)
        ttk.Separator(status_frame, orient="vertical").pack(
            side="left", fill="y", padx=2
        )
        ttk.Label(status_frame, text="Line 1, Col 1").pack(side="left", padx=5)
        ttk.Label(status_frame, text="UTF-8").pack(side="right", padx=5)

        # Store references
        self.mixed_widgets = {
            "editor_text": editor_text,
            "readme_text": readme_text,
            "explorer_tree": explorer_tree,
        }

    def create_platform_info_tab(self, notebook):
        """Create platform information tab."""
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text="Platform Info")

        # Platform information
        info_text = tk.Text(info_frame, wrap=tk.WORD, height=20)
        info_scroll = ttk.Scrollbar(
            info_frame, orient="vertical", command=info_text.yview
        )
        info_text.configure(yscrollcommand=info_scroll.set)

        # Get platform info
        platform_info = self.theme_manager.get_platform_info()

        info_content = []
        info_content.append(f"Platform: {platform.system()} {platform.release()}")
        info_content.append(f"Architecture: {platform.architecture()[0]}")
        info_content.append(f"Python: {platform.python_version()}")
        info_content.append("")
        info_content.append("Theming Capabilities:")
        info_content.append("=" * 30)

        for key, value in platform_info.items():
            formatted_key = key.replace("_", " ").title()
            info_content.append(f"{formatted_key}: {value}")

        info_content.append("")
        info_content.append("Available Themes:")
        info_content.append("-" * 20)
        for theme in self.theme_manager.get_available_themes():
            info_content.append(f"• {theme}")

        info_text.insert("1.0", "\n".join(info_content))
        info_text.configure(state="disabled")

        info_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        info_scroll.pack(side="right", fill="y")

        self.info_text = info_text

    def apply_theme(self, theme_name):
        """Apply a theme to the entire application."""
        try:
            print(f"Applying theme: {theme_name}")

            # Set the theme (this will automatically apply it to the window)
            success = self.theme_manager.set_theme(theme_name, window=self.root)

            if success:
                # Update current theme display
                current_theme = self.theme_manager.get_current_theme()
                self.current_theme_var.set(f"Current: {current_theme.name}")

                print(f"✓ Successfully applied theme: {theme_name}")
            else:
                print(f"✗ Failed to apply theme: {theme_name}")

        except Exception as e:
            print(f"✗ Error applying theme: {e}")
            import traceback

            traceback.print_exc()

    def refresh_theme(self):
        """Refresh the current theme."""
        try:
            success = self.theme_manager.refresh_system_theme()
            if success:
                self.theme_manager.apply_theme_to_window(self.root)
                print("✓ Theme refreshed")
            else:
                print("✗ Failed to refresh theme")
        except Exception as e:
            print(f"✗ Error refreshing theme: {e}")

    def run(self):
        """Run the demo application."""
        print("Complete Cross-Platform Theming Demo")
        print("=" * 40)
        print("This demo shows the fully functional theming system:")
        print("• All TTK widgets are automatically themed")
        print("• All TK widgets are automatically themed")
        print("• Platform-native themes work correctly")
        print("• Real-time theme switching")
        print("• Professional appearance across platforms")
        print("")
        print(
            "Try switching between different themes to see the complete theming in action!"
        )
        print("")

        self.root.mainloop()


if __name__ == "__main__":
    try:
        demo = CompleteThemingDemo()
        demo.run()
    except Exception as e:
        print(f"Error running demo: {e}")
        import traceback

        traceback.print_exc()
