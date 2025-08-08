#!/usr/bin/env python3
"""
Comprehensive Demo for Enhanced Flexible Layout System

This demo showcases the full functionality of the flexible layout system including:
- Complex nested layouts with multiple panes
- Theme switching that correctly themes all elements
- Detached window functionality with theme preservation
- Dynamic content that responds to theme changes
- Professional UI components and interactions

Features demonstrated:
1. Flexible layout with horizontal and vertical containers
2. Multiple theme switching (Light, Dark, Blue, Green, Purple)
3. Detachable panes with preserved theming
4. Rich content in each pane
5. Theme-aware UI components
6. Professional styling and animations
"""

import os
import platform
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, List, Optional

# Add the project root to the path so we can import the modules
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    # Import from threepanewindows package
    from threepanewindows.central_theme_manager import (
        ThemeType,
        apply_theme_to_widget,
        get_theme_manager,
        set_global_theme,
    )
    from threepanewindows.custom_menubar import CustomMenubar, MenuItem
    from threepanewindows.flexible import (
        EnhancedFlexibleLayout,
        FlexContainer,
        FlexPaneConfig,
        LayoutDirection,
    )
    from threepanewindows.themes import ThemeManager
    from threepanewindows.utils import apply_custom_titlebar, platform_handler

    print("Successfully imported from threepanewindows package")
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure you're running this from the project root directory")
    print("and that the threepanewindows package is properly installed")
    sys.exit(1)


class FlexibleLayoutDemo:
    """Main demo application showcasing flexible layout functionality."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Enhanced Flexible Layout Demo - Professional Theme Switching")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # Detect platform
        self.is_windows = platform.system().lower() == "windows"
        self.is_macos = platform.system().lower() == "darwin"
        self.is_linux = platform.system().lower() == "linux"

        # Initialize theme manager
        self.theme_manager = get_theme_manager()
        self.theme_manager.set_theme("light")

        # Track detached windows for theme updates
        self.detached_windows = {}

        # Custom menubar for Windows (native menubar can't be themed)
        self.custom_menubar = None

        # Create the demo
        self._setup_ui()
        self._apply_initial_theme()
        self._apply_platform_specific_features()

    def _setup_ui(self):
        """Set up the main UI with menu and layout."""
        self._create_menu()
        self._create_layout()

    def _create_menu(self):
        """Create the main menu with theme switching options."""
        if self.is_windows:
            # Use custom menubar on Windows for better theming
            self._create_custom_menubar()
        else:
            # Use native menubar on macOS and Linux
            self._create_native_menubar()

    def _create_custom_menubar(self):
        """Create a custom themeable menubar for Windows."""
        self.custom_menubar = CustomMenubar(self.root)
        self.custom_menubar.pack(fill="x", side="top")

        # Theme menu items
        theme_items = [
            MenuItem("Light Theme", command=lambda: self._switch_theme("light")),
            MenuItem("Dark Theme", command=lambda: self._switch_theme("dark")),
            MenuItem("Blue Professional", command=lambda: self._switch_theme("blue")),
            MenuItem("Green Nature", command=lambda: self._switch_theme("green")),
            MenuItem("Purple Elegance", command=lambda: self._switch_theme("purple")),
            MenuItem("", separator=True),
            MenuItem("About Themes", command=self._show_theme_info),
        ]

        # Layout menu items
        layout_items = [
            MenuItem("Reset Layout", command=self._reset_layout),
            MenuItem("Detach All Panes", command=self._detach_all_panes),
            MenuItem("Reattach All Panes", command=self._reattach_all_panes),
        ]

        # Help menu items
        help_items = [
            MenuItem("About Demo", command=self._show_about),
            MenuItem("Keyboard Shortcuts", command=self._show_shortcuts),
        ]

        # Add menus to the custom menubar
        self.custom_menubar.add_menu("Themes", theme_items)
        self.custom_menubar.add_menu("Layout", layout_items)
        self.custom_menubar.add_menu("Help", help_items)

    def _create_native_menubar(self):
        """Create a native menubar for macOS and Linux."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Theme menu
        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Themes", menu=theme_menu)

        themes = [
            ("Light Theme", "light"),
            ("Dark Theme", "dark"),
            ("Blue Professional", "blue"),
            ("Green Nature", "green"),
            ("Purple Elegance", "purple"),
        ]

        for theme_name, theme_key in themes:
            theme_menu.add_command(
                label=theme_name, command=lambda t=theme_key: self._switch_theme(t)
            )

        theme_menu.add_separator()
        theme_menu.add_command(label="About Themes", command=self._show_theme_info)

        # Layout menu
        layout_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Layout", menu=layout_menu)

        layout_menu.add_command(label="Reset Layout", command=self._reset_layout)
        layout_menu.add_command(
            label="Detach All Panes", command=self._detach_all_panes
        )
        layout_menu.add_command(
            label="Reattach All Panes", command=self._reattach_all_panes
        )

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)

        help_menu.add_command(label="About Demo", command=self._show_about)
        help_menu.add_command(label="Keyboard Shortcuts", command=self._show_shortcuts)

    def _create_layout(self):
        """Create the flexible layout with multiple panes."""
        # Define the layout structure
        # Main container: Horizontal split
        # Left side: Vertical split with Explorer and Properties
        # Right side: Vertical split with Editor and Output/Console

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL,
            children=[
                # Left panel container (30% width)
                FlexContainer(
                    direction=LayoutDirection.VERTICAL,
                    weight=0.3,
                    children=[
                        FlexPaneConfig(
                            name="explorer",
                            title="📁 Project Explorer",
                            weight=0.7,
                            min_size=150,
                            builder=self._build_explorer_pane,
                            default_width=400,
                            detached_height=500,
                        ),
                        FlexPaneConfig(
                            name="properties",
                            title="🔧 Properties",
                            weight=0.3,
                            min_size=100,
                            builder=self._build_properties_pane,
                            default_width=350,
                            detached_height=300,
                        ),
                    ],
                ),
                # Right panel container (70% width)
                FlexContainer(
                    direction=LayoutDirection.VERTICAL,
                    weight=0.7,
                    children=[
                        FlexPaneConfig(
                            name="editor",
                            title="📝 Code Editor",
                            weight=0.7,
                            min_size=200,
                            builder=self._build_editor_pane,
                            default_width=700,
                            detached_height=500,
                        ),
                        # Bottom container: Horizontal split for Output and Console
                        FlexContainer(
                            direction=LayoutDirection.HORIZONTAL,
                            weight=0.3,
                            children=[
                                FlexPaneConfig(
                                    name="output",
                                    title="📤 Output",
                                    weight=0.5,
                                    min_size=100,
                                    builder=self._build_output_pane,
                                    default_width=500,
                                    detached_height=300,
                                ),
                                FlexPaneConfig(
                                    name="console",
                                    title="💻 Console",
                                    weight=0.5,
                                    min_size=100,
                                    builder=self._build_console_pane,
                                    default_width=500,
                                    detached_height=300,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

        # Create the layout
        self.layout = EnhancedFlexibleLayout(
            self.root, layout_config, theme_name="light"
        )
        self.layout.pack(fill="both", expand=True, padx=5, pady=5)

    def _build_explorer_pane(self, parent: tk.Frame):
        """Build the project explorer pane with a file tree."""
        # Create a themed frame
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Project Files",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Toolbar
        toolbar = tk.Frame(header, bg=theme.panel_header_bg)
        toolbar.pack(side="right", padx=5)

        for icon, tooltip in [
            ("🔄", "Refresh"),
            ("➕", "New File"),
            ("📁", "New Folder"),
        ]:
            btn = tk.Button(
                toolbar,
                text=icon,
                bg=theme.button_bg,
                fg=theme.button_text,
                relief="flat",
                width=3,
                command=lambda: None,
            )
            btn.pack(side="left", padx=1)

        # File tree
        tree_frame = tk.Frame(parent, bg=theme.primary_bg)
        tree_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Create treeview with scrollbar
        tree = ttk.Treeview(tree_frame, show="tree")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Populate tree with sample data
        folders = tree.insert("", "end", text="📁 src", open=True)
        tree.insert(folders, "end", text="📄 main.py")
        tree.insert(folders, "end", text="📄 utils.py")
        tree.insert(folders, "end", text="📄 config.py")

        tests = tree.insert("", "end", text="📁 tests", open=True)
        tree.insert(tests, "end", text="📄 test_main.py")
        tree.insert(tests, "end", text="📄 test_utils.py")

        tree.insert("", "end", text="📄 README.md")
        tree.insert("", "end", text="📄 requirements.txt")

    def _build_properties_pane(self, parent: tk.Frame):
        """Build the properties pane with editable properties."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Properties",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Properties content
        content = tk.Frame(parent, bg=theme.primary_bg)
        content.pack(fill="both", expand=True, padx=5, pady=5)

        # Sample properties
        properties = [
            ("Name", "main.py"),
            ("Type", "Python File"),
            ("Size", "2.4 KB"),
            ("Modified", "2024-01-15 14:30"),
            ("Encoding", "UTF-8"),
            ("Lines", "87"),
        ]

        for i, (prop, value) in enumerate(properties):
            prop_frame = tk.Frame(content, bg=theme.primary_bg)
            prop_frame.pack(fill="x", pady=2)

            tk.Label(
                prop_frame,
                text=f"{prop}:",
                bg=theme.primary_bg,
                fg=theme.secondary_text,
                font=("Segoe UI", 9),
                width=12,
                anchor="w",
            ).pack(side="left")

            tk.Label(
                prop_frame,
                text=value,
                bg=theme.primary_bg,
                fg=theme.primary_text,
                font=("Segoe UI", 9),
                anchor="w",
            ).pack(side="left", fill="x", expand=True)

        # Add some interactive elements
        tk.Label(
            content,
            text="Tags:",
            bg=theme.primary_bg,
            fg=theme.secondary_text,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(10, 2))

        tag_entry = tk.Entry(content, bg=theme.secondary_bg, fg=theme.primary_text)
        tag_entry.pack(fill="x", pady=2)
        tag_entry.insert(0, "python, main, entry-point")

    def _build_editor_pane(self, parent: tk.Frame):
        """Build the code editor pane with syntax highlighting simulation."""
        theme = self.theme_manager.get_current_theme()

        # Header with tabs
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=35)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        # Tab bar
        tab_frame = tk.Frame(header, bg=theme.panel_header_bg)
        tab_frame.pack(side="left", fill="x", expand=True, pady=2)

        tabs = ["main.py", "utils.py", "config.py"]
        for i, tab in enumerate(tabs):
            tab_bg = theme.accent_bg if i == 0 else theme.panel_header_bg
            tab_fg = theme.accent_text if i == 0 else theme.panel_header_text

            tab_btn = tk.Button(
                tab_frame,
                text=f"📄 {tab}",
                bg=tab_bg,
                fg=tab_fg,
                relief="flat",
                padx=15,
                pady=5,
                font=("Segoe UI", 9),
            )
            tab_btn.pack(side="left", padx=1)

        # Editor toolbar
        toolbar = tk.Frame(header, bg=theme.panel_header_bg)
        toolbar.pack(side="right", padx=5)

        for icon, tooltip in [
            ("💾", "Save"),
            ("↶", "Undo"),
            ("↷", "Redo"),
            ("🔍", "Find"),
        ]:
            btn = tk.Button(
                toolbar,
                text=icon,
                bg=theme.button_bg,
                fg=theme.button_text,
                relief="flat",
                width=3,
            )
            btn.pack(side="left", padx=1)

        # Editor content
        editor_frame = tk.Frame(parent, bg=theme.primary_bg)
        editor_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Line numbers
        line_frame = tk.Frame(editor_frame, bg=theme.secondary_bg, width=40)
        line_frame.pack(side="left", fill="y")
        line_frame.pack_propagate(False)

        # Text editor
        text_widget = tk.Text(
            editor_frame,
            bg=theme.primary_bg,
            fg=theme.primary_text,
            insertbackground=theme.accent_text,
            selectbackground=theme.accent_bg,
            font=("Consolas", 11),
            wrap="none",
        )
        text_widget.pack(side="left", fill="both", expand=True)

        # Scrollbars
        v_scroll = ttk.Scrollbar(
            editor_frame, orient="vertical", command=text_widget.yview
        )
        h_scroll = ttk.Scrollbar(parent, orient="horizontal", command=text_widget.xview)
        text_widget.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")

        # Sample code with syntax highlighting simulation
        sample_code = '''#!/usr/bin/env python3
"""
Enhanced Flexible Layout Demo
A comprehensive demonstration of the flexible layout system.
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

class FlexibleLayoutDemo:
    """Main demo application."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Flexible Layout Demo")
        self.root.geometry("1200x800")

        # Initialize theme manager
        self.theme_manager = get_theme_manager()
        self._setup_ui()

    def _setup_ui(self):
        """Set up the main UI."""
        self._create_menu()
        self._create_layout()

    def _switch_theme(self, theme_name):
        """Switch to a different theme."""
        self.theme_manager.set_theme(theme_name)
        self._apply_theme_to_all()

if __name__ == "__main__":
    demo = FlexibleLayoutDemo()
    demo.run()
'''

        text_widget.insert("1.0", sample_code)

        # Add line numbers
        lines = sample_code.count("\n") + 1
        line_numbers = "\n".join(str(i) for i in range(1, lines + 1))

        line_text = tk.Text(
            line_frame,
            bg=theme.secondary_bg,
            fg=theme.secondary_text,
            font=("Consolas", 11),
            width=4,
            state="disabled",
            wrap="none",
        )
        line_text.pack(fill="both", expand=True)
        line_text.config(state="normal")
        line_text.insert("1.0", line_numbers)
        line_text.config(state="disabled")

    def _build_output_pane(self, parent: tk.Frame):
        """Build the output pane with build/run results."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Build Output",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Clear button
        clear_btn = tk.Button(
            header,
            text="🗑️ Clear",
            bg=theme.button_bg,
            fg=theme.button_text,
            relief="flat",
            padx=10,
        )
        clear_btn.pack(side="right", padx=5, pady=2)

        # Output content
        output_frame = tk.Frame(parent, bg=theme.primary_bg)
        output_frame.pack(fill="both", expand=True, padx=2, pady=2)

        output_text = tk.Text(
            output_frame,
            bg=theme.primary_bg,
            fg=theme.primary_text,
            font=("Consolas", 10),
            wrap="word",
            state="disabled",
        )
        output_scroll = ttk.Scrollbar(
            output_frame, orient="vertical", command=output_text.yview
        )
        output_text.configure(yscrollcommand=output_scroll.set)

        output_text.pack(side="left", fill="both", expand=True)
        output_scroll.pack(side="right", fill="y")

        # Sample output
        sample_output = """Building project...
✓ Checking dependencies
✓ Compiling source files
✓ Running tests
✓ Generating documentation

Build completed successfully!

Time: 2.3 seconds
Warnings: 0
Errors: 0

Ready for deployment.
"""

        output_text.config(state="normal")
        output_text.insert("1.0", sample_output)
        output_text.config(state="disabled")

    def _build_console_pane(self, parent: tk.Frame):
        """Build the interactive console pane."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Interactive Console",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Console controls
        controls = tk.Frame(header, bg=theme.panel_header_bg)
        controls.pack(side="right", padx=5)

        for icon, tooltip in [("🔄", "Restart"), ("⏹️", "Stop"), ("🗑️", "Clear")]:
            btn = tk.Button(
                controls,
                text=icon,
                bg=theme.button_bg,
                fg=theme.button_text,
                relief="flat",
                width=3,
            )
            btn.pack(side="left", padx=1)

        # Console content
        console_frame = tk.Frame(parent, bg=theme.primary_bg)
        console_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Console output area
        console_output = tk.Text(
            console_frame,
            bg="#000000",  # Console typically has black background
            fg="#00ff00",  # Green text for console
            font=("Consolas", 10),
            wrap="word",
        )
        console_scroll = ttk.Scrollbar(
            console_frame, orient="vertical", command=console_output.yview
        )
        console_output.configure(yscrollcommand=console_scroll.set)

        console_output.pack(fill="both", expand=True)
        console_scroll.pack(side="right", fill="y")

        # Sample console session
        console_session = """Python 3.11.0 (main, Oct 24 2022, 18:26:48)
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>> import tkinter as tk
>>> print("Hello, Flexible Layout!")
Hello, Flexible Layout!

>>> # Theme switching demo
>>> theme_manager.set_theme("dark")
Theme switched to: Dark

>>> # Layout operations
>>> layout.detach_pane("editor")
Pane 'editor' detached successfully

>>> # Check available themes
>>> theme_manager.get_available_themes()
['light', 'dark', 'blue', 'green', 'purple']

>>>
"""

        console_output.insert("1.0", console_session)

        # Input area
        input_frame = tk.Frame(parent, bg=theme.primary_bg, height=30)
        input_frame.pack(fill="x", padx=2, pady=2)
        input_frame.pack_propagate(False)

        tk.Label(
            input_frame,
            text=">>>",
            bg=theme.primary_bg,
            fg=theme.accent_text,
            font=("Consolas", 10, "bold"),
        ).pack(side="left", padx=5)

        console_input = tk.Entry(
            input_frame,
            bg=theme.secondary_bg,
            fg=theme.primary_text,
            font=("Consolas", 10),
        )
        console_input.pack(side="left", fill="x", expand=True, padx=5)

    def _switch_theme(self, theme_name: str):
        """Switch to a different theme and update all UI elements."""
        print(f"Switching to theme: {theme_name}")

        # Set the theme
        self.theme_manager.set_theme(theme_name)

        # Apply theme to the main window
        self._apply_theme_to_main_window()

        # Update the layout and all its components
        if hasattr(self, "layout"):
            self.layout.refresh_theme()

        # Update custom menubar if on Windows
        if self.is_windows and self.custom_menubar:
            self._update_custom_menubar_theme()

        # Update platform-specific features
        self._apply_platform_specific_features()

        # Update any detached windows
        self._update_detached_windows_theme()

        print(f"Theme switched to: {theme_name}")

    def _update_custom_menubar_theme(self):
        """Update the custom menubar with the current theme."""
        if not self.custom_menubar:
            return

        theme = self.theme_manager.get_current_theme()

        # Apply theme to the custom menubar
        try:
            self.custom_menubar.configure(bg=theme.menu_bg)
            apply_theme_to_widget(self.custom_menubar, recursive=True)
            print("✅ Updated custom menubar theme")
        except Exception as e:
            print(f"⚠️ Could not update custom menubar theme: {e}")

    def _apply_theme_to_main_window(self):
        """Apply the current theme to the main window."""
        theme = self.theme_manager.get_current_theme()

        # Update root window
        self.root.configure(bg=theme.primary_bg)

        # Update menu - get the actual menu widget
        menu_name = self.root["menu"]
        if menu_name:
            try:
                menu_widget = self.root.nametowidget(menu_name)
                apply_theme_to_widget(menu_widget, recursive=True)
            except tk.TclError:
                # Menu widget not found, skip theming
                pass

    def _update_detached_windows_theme(self):
        """Update theme for any detached windows."""
        if hasattr(self, "layout") and self.layout:
            # The layout handles updating detached windows automatically
            pass

    def _apply_initial_theme(self):
        """Apply the initial theme to all components."""
        self._apply_theme_to_main_window()

    def _apply_platform_specific_features(self):
        """Apply platform-specific features like titlebar theming."""
        theme = self.theme_manager.get_current_theme()

        if self.is_windows:
            # Apply Windows-specific titlebar theming
            try:
                apply_custom_titlebar(self.root, theme)
                print("✅ Applied Windows titlebar theming")
            except Exception as e:
                print(f"⚠️ Could not apply Windows titlebar theming: {e}")

        # Apply platform-specific window icon if available
        try:
            icon_path = self._get_platform_icon()
            if icon_path and os.path.exists(icon_path):
                platform_handler.set_window_icon(self.root, icon_path)
                print(f"✅ Applied platform-specific icon: {icon_path}")
        except Exception as e:
            print(f"⚠️ Could not set platform icon: {e}")

    def _get_platform_icon(self) -> Optional[str]:
        """Get the appropriate icon for the current platform."""
        # Look for platform-specific icons in the utils/icons directory
        icons_dir = os.path.join(
            os.path.dirname(__file__), "threepanewindows", "utils", "icons"
        )

        if self.is_windows:
            # Prefer .ico on Windows
            ico_path = os.path.join(icons_dir, "app.ico")
            if os.path.exists(ico_path):
                return ico_path
            # Fallback to PNG
            png_path = os.path.join(icons_dir, "app.png")
            if os.path.exists(png_path):
                return png_path
        else:
            # Use PNG on other platforms
            png_path = os.path.join(icons_dir, "app.png")
            if os.path.exists(png_path):
                return png_path

        return None

    def _update_detached_windows_theme(self):
        """Update theme for all detached windows."""
        if hasattr(self, "layout"):
            for window in self.layout.detached_windows.values():
                if hasattr(window, "refresh_theme"):
                    try:
                        window.refresh_theme()
                    except tk.TclError:
                        # Window was destroyed, ignore
                        pass

    def _reset_layout(self):
        """Reset the layout to its original state."""
        if hasattr(self, "layout"):
            # Reattach all detached panes
            for pane_name in list(self.layout.detached_windows.keys()):
                self.layout.reattach_pane(pane_name)

            messagebox.showinfo(
                "Layout Reset", "Layout has been reset to its original state."
            )

    def _detach_all_panes(self):
        """Detach all panes for demonstration."""
        if hasattr(self, "layout"):
            pane_names = list(self.layout.panes.keys())
            for pane_name in pane_names:
                if pane_name not in self.layout.detached_windows:
                    self.layout.detach_pane(pane_name)

            messagebox.showinfo(
                "Panes Detached", f"All {len(pane_names)} panes have been detached."
            )

    def _reattach_all_panes(self):
        """Reattach all detached panes."""
        if hasattr(self, "layout"):
            detached_count = len(self.layout.detached_windows)
            for pane_name in list(self.layout.detached_windows.keys()):
                self.layout.reattach_pane(pane_name)

            messagebox.showinfo(
                "Panes Reattached",
                f"All {detached_count} detached panes have been reattached.",
            )

    def _show_theme_info(self):
        """Show information about the current theme."""
        theme = self.theme_manager.get_current_theme()
        current_theme_name = self.theme_manager.current_theme_name

        info = f"""Current Theme: {current_theme_name.title()}

Theme Details:
• Primary Background: {theme.primary_bg}
• Primary Text: {theme.primary_text}
• Accent Color: {theme.accent_bg}
• Button Color: {theme.button_bg}

Available Themes:
• Light Theme - Clean and bright
• Dark Theme - Easy on the eyes
• Blue Professional - Corporate look
• Green Nature - Calm and natural
• Purple Elegance - Sophisticated style

Features:
✓ All UI elements are themed consistently
✓ Detached windows preserve theme settings
✓ Theme changes apply instantly to all components
✓ Professional color schemes and typography
"""

        messagebox.showinfo("Theme Information", info)

    def _show_about(self):
        """Show information about the demo."""
        about_text = """Enhanced Flexible Layout Demo
Version 1.0

This demo showcases the comprehensive functionality of the Enhanced Flexible Layout System:

🎨 Theme Features:
• 5 professional themes with instant switching
• Consistent theming across all UI elements
• Theme preservation in detached windows
• Automatic theme application to new components

🪟 Layout Features:
• Flexible nested container system
• Detachable panes with professional styling
• Drag & drop interface for window management
• Automatic layout recalculation
• Minimum and maximum size constraints

💻 UI Components:
• Project Explorer with file tree
• Properties panel with editable fields
• Code Editor with syntax highlighting simulation
• Build Output with formatted results
• Interactive Console with command history

🔧 Professional Features:
• Cross-platform compatibility
• Keyboard shortcuts support
• Context menus and tooltips
• Professional window management
• Memory-efficient theme switching

Built with Python and Tkinter
© 2024 ThreePaneWindows Project
"""

        messagebox.showinfo("About Demo", about_text)

    def _show_shortcuts(self):
        """Show keyboard shortcuts."""
        shortcuts = """Keyboard Shortcuts

Theme Switching:
• Ctrl+1 - Light Theme
• Ctrl+2 - Dark Theme
• Ctrl+3 - Blue Theme
• Ctrl+4 - Green Theme
• Ctrl+5 - Purple Theme

Layout Operations:
• Ctrl+R - Reset Layout
• Ctrl+D - Detach All Panes
• Ctrl+A - Reattach All Panes

Window Management:
• F11 - Toggle Fullscreen
• Ctrl+Q - Quit Application
• Ctrl+H - Show/Hide Help

Note: Some shortcuts may vary by platform.
"""

        messagebox.showinfo("Keyboard Shortcuts", shortcuts)

    def _setup_keyboard_shortcuts(self):
        """Set up keyboard shortcuts."""
        # Theme shortcuts
        self.root.bind("<Control-1>", lambda e: self._switch_theme("light"))
        self.root.bind("<Control-2>", lambda e: self._switch_theme("dark"))
        self.root.bind("<Control-3>", lambda e: self._switch_theme("blue"))
        self.root.bind("<Control-4>", lambda e: self._switch_theme("green"))
        self.root.bind("<Control-5>", lambda e: self._switch_theme("purple"))

        # Layout shortcuts
        self.root.bind("<Control-r>", lambda e: self._reset_layout())
        self.root.bind("<Control-d>", lambda e: self._detach_all_panes())
        self.root.bind("<Control-a>", lambda e: self._reattach_all_panes())

        # Application shortcuts
        self.root.bind("<Control-q>", lambda e: self.root.quit())
        self.root.bind("<F11>", self._toggle_fullscreen)
        self.root.bind("<Control-h>", lambda e: self._show_shortcuts())

    def _toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode."""
        current_state = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not current_state)

    def run(self):
        """Run the demo application."""
        self._setup_keyboard_shortcuts()

        # Show welcome message
        self.root.after(
            500,
            lambda: messagebox.showinfo(
                "Welcome to Flexible Layout Demo",
                "Welcome to the Enhanced Flexible Layout Demo!\n\n"
                "• Try switching themes from the Themes menu\n"
                "• Detach panes by clicking the detach button (⧉)\n"
                "• Reattach panes using the reattach button (🔗)\n"
                "• Use keyboard shortcuts for quick operations\n\n"
                "All theme changes will be preserved in detached windows!",
            ),
        )

        print("Starting Enhanced Flexible Layout Demo...")
        print("Available themes: light, dark, blue, green, purple")
        print("Use the Themes menu to switch between themes")
        print("Try detaching panes to see theme preservation in action!")

        self.root.mainloop()


def main():
    """Main entry point for the demo."""
    try:
        demo = FlexibleLayoutDemo()
        demo.run()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Error running demo: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
