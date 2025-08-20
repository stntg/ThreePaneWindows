#!/usr/bin/env python3
"""
Standalone Linux Example: Flexible Layout with Custom Titlebar and Theme Switching

This example demonstrates:
1. Flexible layout system with complex nested layouts
2. Custom titlebar for both main window and detached panes
3. Complete theme switching through all available themes
4. Linux-optimized styling and behavior
5. Professional detached window management
6. Cross-platform icon support

Features:
- Main window with custom titlebar
- Detached panes with custom titlebars
- Theme switching menu with all available themes
- Linux-native styling and fonts
- Professional UI components
- Proper window management and focus handling

Usage:
    python3 linux_flexible_titlebar_demo.py

Requirements:
- Python 3.8+
- tkinter (usually included with Python)
- threepanewindows package
"""

import os
import platform
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, Dict, List, Optional

# Add the project root to the path so we can import the modules
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    # Import from threepanewindows package
    from threepanewindows.central_theme_manager import (
        ThemeType,
        get_theme_manager,
        set_global_theme,
    )
    from threepanewindows.flexible import (
        EnhancedFlexibleLayout,
        FlexContainer,
        FlexPaneConfig,
        LayoutDirection,
    )
    from threepanewindows.logging_config import get_logger
    from threepanewindows.themes import ThemeManager
    from threepanewindows.utils import platform_handler
    from threepanewindows.utils.custom_titlebar import (
        LinuxTitleBar,
        MacOSTitleBar,
        WindowsTitleBar,
    )

    print("✓ Successfully imported threepanewindows modules")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Please ensure you're running this from the project root directory")
    print("and that the threepanewindows package is properly installed")
    sys.exit(1)

# Initialize logger
logger = get_logger(__name__)


class LinuxFlexibleTitlebarDemo:
    """
    Standalone Linux demo showcasing flexible layout with custom titlebar
    and comprehensive theme switching functionality.
    """

    def __init__(self):
        """Initialize the demo application."""
        print("\n" + "=" * 60)
        print("Linux Flexible Layout + Custom Titlebar Demo")
        print("=" * 60)

        # Detect platform first
        self.platform_name = platform.system()
        self.is_linux = self.platform_name.lower() == "linux"

        print(f"Platform detected: {self.platform_name}")
        print(f"Linux optimizations: {'Enabled' if self.is_linux else 'Disabled'}")

        # Ask for titlebar preference early (before creating main window)
        if self.platform_name == "Linux":
            self.prefer_theme_matching = self._ask_titlebar_preference_early()
        else:
            self.prefer_theme_matching = True

        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Linux Flexible Layout + Custom Titlebar Demo")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)

        # Hide window initially to prevent dual-window issues
        self.root.withdraw()

        # Initialize theme manager
        self.theme_manager = get_theme_manager()

        # Get all available themes
        self.available_themes = self.theme_manager.get_theme_names()
        print(f"Available themes: {', '.join(self.available_themes)}")

        # Set initial theme
        initial_theme = "dark" if self._detect_dark_mode() else "light"
        set_global_theme(initial_theme)
        print(f"Initial theme: {initial_theme}")

        # Custom titlebar instance
        self.custom_titlebar = None

        # Track detached windows for theme updates
        self.detached_windows = {}

        # Layout instance
        self.layout = None

        # Setup the application
        self._setup_custom_titlebar()
        self._setup_window_properties()
        self._setup_layout()
        self._setup_window_icon()

        # Apply off-screen Motif hints for Linux theme-matching titlebar
        if (
            self.platform_name == "Linux"
            and hasattr(self, "prefer_theme_matching")
            and self.prefer_theme_matching
        ):
            try:
                from threepanewindows.utils.offscreen_motif import (
                    setup_offscreen_custom_titlebar,
                )

                # Get current geometry for off-screen processing
                current_geometry = self.root.geometry()

                # Use off-screen approach - it handles showing the window
                if setup_offscreen_custom_titlebar(self.root, current_geometry):
                    print("🎨 Using off-screen custom titlebar approach")
                    return  # Don't call deiconify - off-screen setup handles it
                else:
                    print("⚠ Off-screen approach failed, using fallback")
            except Exception as e:
                print(f"Note: Off-screen approach failed: {e}")

        # Show the window after everything is set up (fallback or non-Linux)
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

        print("✓ Demo initialization complete")

    def _detect_dark_mode(self) -> bool:
        """Detect if the system is using dark mode."""
        try:
            return platform_handler.is_dark_mode()
        except Exception:
            return False

    def _setup_custom_titlebar(self):
        """Setup custom titlebar based on platform."""
        print("\nSetting up custom titlebar...")

        try:
            theme = self.theme_manager.get_current_theme()

            # Convert theme to dictionary format expected by titlebar
            theme_dict = {
                "bg": theme.primary_bg,
                "fg": theme.primary_text,
                "btn_bg": theme.button_bg,
                "btn_fg": theme.button_text,
                "btn_active_bg": theme.button_hover,
                "font": ("Ubuntu", 11),  # Use Linux-optimized font
                "height": 32,
            }

            # Create platform-specific titlebar
            if self.platform_name == "Linux":
                self.custom_titlebar = LinuxTitleBar(
                    self.root,
                    theme_dict,
                    "Linux Flexible Layout + Custom Titlebar Demo",
                    prefer_theme_matching=self.prefer_theme_matching,
                )
            elif self.platform_name == "Windows":
                self.custom_titlebar = WindowsTitleBar(
                    self.root,
                    theme_dict,
                    "Linux Flexible Layout + Custom Titlebar Demo",
                )
            elif self.platform_name == "Darwin":  # macOS
                self.custom_titlebar = MacOSTitleBar(
                    self.root,
                    theme_dict,
                    "Linux Flexible Layout + Custom Titlebar Demo",
                )

            if self.custom_titlebar:
                titlebar_frame = self.custom_titlebar.create_titlebar()
                if titlebar_frame:
                    # Add theme switching menu to titlebar
                    self._add_theme_menu_to_titlebar(titlebar_frame)
                    print("✓ Custom titlebar created successfully")
                else:
                    print("⚠ Custom titlebar frame not created")
                    # For Linux native titlebar, create a menu bar instead
                    if self.platform_name == "Linux":
                        self._create_menu_bar()
                        print("✓ Menu bar created for theme switching")
            else:
                print("⚠ Custom titlebar not supported on this platform")

        except Exception as e:
            print(f"✗ Error setting up custom titlebar: {e}")
            logger.error(f"Custom titlebar setup failed: {e}")

    def _add_theme_menu_to_titlebar(self, titlebar_frame: tk.Frame):
        """Add theme switching menu to the titlebar."""
        try:
            theme = self.theme_manager.get_current_theme()

            # Create theme menu button
            theme_button = tk.Menubutton(
                titlebar_frame,
                text="🎨 Themes",
                bg=theme.button_bg,
                fg=theme.button_text,
                activebackground=theme.button_hover,
                activeforeground=theme.button_text,
                relief="flat",
                borderwidth=0,
                cursor="hand2",
                font=("Ubuntu", 10),
            )
            theme_button.pack(side="right", padx=5, pady=2)

            # Create theme menu
            theme_menu = tk.Menu(theme_button, tearoff=0)
            theme_button.config(menu=theme_menu)

            # Add all available themes to menu
            theme_display_names = {
                "light": "☀️ Light Theme",
                "dark": "🌙 Dark Theme",
                "blue": "💙 Blue Professional",
                "green": "💚 Green Nature",
                "purple": "💜 Purple Elegance",
                "system": "🖥️ System Theme",
                "native": "🏠 Native Theme",
                "native_light": "🏠☀️ Native Light",
                "native_dark": "🏠🌙 Native Dark",
            }

            for theme_name in self.available_themes:
                display_name = theme_display_names.get(
                    theme_name, f"🎨 {theme_name.title()}"
                )
                theme_menu.add_command(
                    label=display_name,
                    command=lambda t=theme_name: self._switch_theme(t),
                )

            theme_menu.add_separator()
            theme_menu.add_command(
                label="ℹ️ About Themes", command=self._show_theme_info
            )

            print("✓ Theme menu added to titlebar")

        except Exception as e:
            print(f"✗ Error adding theme menu to titlebar: {e}")
            logger.error(f"Theme menu setup failed: {e}")

    def _create_menu_bar(self):
        """Create a menu bar for theme switching when using native titlebar."""
        try:
            # Create menu bar
            menubar = tk.Menu(self.root)
            self.root.config(menu=menubar)

            # Create themes menu
            themes_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="🎨 Themes", menu=themes_menu)

            # Add all available themes to menu
            theme_display_names = {
                "light": "☀️ Light Theme",
                "dark": "🌙 Dark Theme",
                "blue": "💙 Blue Professional",
                "green": "💚 Green Nature",
                "purple": "💜 Purple Elegance",
                "system": "🖥️ System Theme",
                "native": "🏠 Native Theme",
                "native_light": "🏠☀️ Native Light",
                "native_dark": "🏠🌙 Native Dark",
            }

            for theme_name in self.available_themes:
                display_name = theme_display_names.get(
                    theme_name, f"🎨 {theme_name.title()}"
                )
                themes_menu.add_command(
                    label=display_name,
                    command=lambda t=theme_name: self._switch_theme(t),
                )

            themes_menu.add_separator()
            themes_menu.add_command(
                label="ℹ️ About Themes", command=self._show_theme_info
            )

            # Create help menu
            help_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Help", menu=help_menu)
            help_menu.add_command(label="About", command=self._show_about)

        except Exception as e:
            print(f"✗ Error creating menu bar: {e}")
            logger.error(f"Menu bar creation failed: {e}")

    def _ask_titlebar_preference_early(self) -> bool:
        """Ask user for titlebar preference on Linux before creating main window."""
        try:
            # Create a temporary root for the dialog
            temp_root = tk.Tk()
            temp_root.withdraw()  # Hide the temporary window

            from tkinter import messagebox

            choice = messagebox.askyesnocancel(
                "Linux Titlebar Options",
                "Choose your preferred titlebar approach:\n\n"
                "🎨 YES: Theme-matching titlebar\n"
                "   • Titlebar colors match your selected theme\n"
                "   • May not appear in taskbar/dock\n"
                "   • Minimize may not work properly\n\n"
                "🖥️ NO: System integration titlebar\n"
                "   • Perfect taskbar and window manager integration\n"
                "   • Titlebar follows system theme (not app theme)\n"
                "   • All window controls work perfectly\n\n"
                "CANCEL: Use default (theme-matching)",
            )

            temp_root.destroy()  # Clean up temporary window

            if choice is None:  # Cancel
                return True  # Default to theme-matching
            else:
                return choice  # True for theme-matching, False for system integration

        except Exception as e:
            print(f"Error asking titlebar preference: {e}")
            return True  # Default to theme-matching

    def _ask_titlebar_preference(self) -> bool:
        """Ask user for titlebar preference on Linux."""
        try:
            from tkinter import messagebox

            choice = messagebox.askyesnocancel(
                "Linux Titlebar Options",
                "Choose your preferred titlebar approach:\n\n"
                "🎨 YES: Theme-matching titlebar\n"
                "   • Titlebar colors match your selected theme\n"
                "   • May not appear in taskbar/dock\n"
                "   • Minimize may not work properly\n\n"
                "🖥️ NO: System integration titlebar\n"
                "   • Perfect taskbar and window manager integration\n"
                "   • Titlebar follows system theme (not app theme)\n"
                "   • All window controls work perfectly\n\n"
                "CANCEL: Use default (theme-matching)",
            )

            if choice is None:  # Cancel
                return True  # Default to theme-matching
            else:
                return choice  # True for theme-matching, False for system integration

        except Exception as e:
            print(f"Error asking titlebar preference: {e}")
            return True  # Default to theme-matching

    def _setup_window_properties(self):
        """Setup Linux-specific window properties."""
        try:
            theme = self.theme_manager.get_current_theme()

            # Set window background
            self.root.configure(bg=theme.primary_bg)

            # Linux-specific window properties
            if self.is_linux:
                # Set window class for better integration
                self.root.wm_class("FlexibleTitlebarDemo", "ThreePaneWindows")

                # Set window manager hints
                try:
                    self.root.wm_attributes("-type", "normal")
                except tk.TclError:
                    pass  # Not all window managers support this

                # Set window protocol
                self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)

            print("✓ Window properties configured")

        except Exception as e:
            print(f"✗ Error setting up window properties: {e}")
            logger.error(f"Window properties setup failed: {e}")

    def _setup_window_icon(self):
        """Setup window icon."""
        try:
            # Try to find an icon file
            icon_paths = [
                os.path.join(
                    project_root,
                    "threepanewindows",
                    "utils",
                    "icons",
                    "folder-1449.png",
                ),
                os.path.join(project_root, "sample_images", "icon.png"),
            ]

            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    success = platform_handler.set_window_icon(self.root, icon_path)
                    if success:
                        print(f"✓ Window icon set: {icon_path}")
                        return

            print("⚠ No suitable icon found")

        except Exception as e:
            print(f"✗ Error setting window icon: {e}")
            logger.error(f"Window icon setup failed: {e}")

    def _setup_layout(self):
        """Setup the flexible layout with multiple panes."""
        print("\nSetting up flexible layout...")

        try:
            # Define a complex layout structure
            layout_config = FlexContainer(
                direction=LayoutDirection.HORIZONTAL,
                children=[
                    # Left sidebar (25% width)
                    FlexContainer(
                        direction=LayoutDirection.VERTICAL,
                        weight=0.25,
                        children=[
                            FlexPaneConfig(
                                name="explorer",
                                title="📁 File Explorer",
                                weight=0.6,
                                min_size=200,
                                builder=self._build_explorer_pane,
                                custom_titlebar=True,
                                default_width=400,
                                detached_height=500,
                                detachable=True,
                                icon="📁",
                            ),
                            FlexPaneConfig(
                                name="outline",
                                title="📋 Document Outline",
                                weight=0.4,
                                min_size=150,
                                builder=self._build_outline_pane,
                                custom_titlebar=True,
                                default_width=350,
                                detached_height=400,
                                detachable=True,
                                icon="📋",
                            ),
                        ],
                    ),
                    # Center area (50% width)
                    FlexContainer(
                        direction=LayoutDirection.VERTICAL,
                        weight=0.5,
                        children=[
                            FlexPaneConfig(
                                name="editor",
                                title="📝 Code Editor",
                                weight=0.7,
                                min_size=300,
                                builder=self._build_editor_pane,
                                custom_titlebar=True,
                                default_width=700,
                                detached_height=600,
                                detachable=True,
                                icon="📝",
                            ),
                            FlexPaneConfig(
                                name="terminal",
                                title="💻 Terminal",
                                weight=0.3,
                                min_size=150,
                                builder=self._build_terminal_pane,
                                custom_titlebar=True,
                                default_width=700,
                                detached_height=300,
                                detachable=True,
                                icon="💻",
                            ),
                        ],
                    ),
                    # Right sidebar (25% width)
                    FlexContainer(
                        direction=LayoutDirection.VERTICAL,
                        weight=0.25,
                        children=[
                            FlexPaneConfig(
                                name="properties",
                                title="🔧 Properties",
                                weight=0.4,
                                min_size=150,
                                builder=self._build_properties_pane,
                                custom_titlebar=True,
                                default_width=350,
                                detached_height=400,
                                detachable=True,
                                icon="🔧",
                            ),
                            FlexPaneConfig(
                                name="debug",
                                title="🐛 Debug Console",
                                weight=0.3,
                                min_size=120,
                                builder=self._build_debug_pane,
                                custom_titlebar=True,
                                default_width=350,
                                detached_height=350,
                                detachable=True,
                                icon="🐛",
                            ),
                            FlexPaneConfig(
                                name="output",
                                title="📤 Output",
                                weight=0.3,
                                min_size=120,
                                builder=self._build_output_pane,
                                custom_titlebar=True,
                                default_width=350,
                                detached_height=300,
                                detachable=True,
                                icon="📤",
                            ),
                        ],
                    ),
                ],
            )

            # Create the layout
            current_theme = (
                self.theme_manager.current_theme.value
                if hasattr(self.theme_manager.current_theme, "value")
                else "light"
            )
            self.layout = EnhancedFlexibleLayout(
                self.root, layout_config, theme_name=current_theme
            )

            # Pack the layout (leave space for titlebar if present)
            pack_options = {"fill": "both", "expand": True, "padx": 2, "pady": 2}
            if self.custom_titlebar and hasattr(self.custom_titlebar, "titlebar_frame"):
                pack_options["pady"] = (0, 2)  # No top padding if titlebar exists

            self.layout.pack(**pack_options)

            print("✓ Flexible layout created successfully")

        except Exception as e:
            print(f"✗ Error setting up layout: {e}")
            logger.error(f"Layout setup failed: {e}")
            import traceback

            traceback.print_exc()

    def _build_explorer_pane(self, parent: tk.Frame):
        """Build the file explorer pane."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📁 Project Files",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=("Ubuntu", 11, "bold"),
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
                activebackground=theme.button_hover,
                relief="flat",
                width=3,
                command=lambda i=icon: self._show_info(f"Clicked {tooltip}"),
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
        src_folder = tree.insert("", "end", text="📁 src", open=True)
        tree.insert(src_folder, "end", text="📄 main.py")
        tree.insert(src_folder, "end", text="📄 utils.py")
        tree.insert(src_folder, "end", text="📄 config.py")

        tests_folder = tree.insert("", "end", text="📁 tests", open=True)
        tree.insert(tests_folder, "end", text="📄 test_main.py")
        tree.insert(tests_folder, "end", text="📄 test_utils.py")

        docs_folder = tree.insert("", "end", text="📁 docs", open=False)
        tree.insert(docs_folder, "end", text="📄 README.md")
        tree.insert(docs_folder, "end", text="📄 API.md")

        tree.insert("", "end", text="📄 requirements.txt")
        tree.insert("", "end", text="📄 setup.py")

    def _build_outline_pane(self, parent: tk.Frame):
        """Build the document outline pane."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📋 Document Outline",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=("Ubuntu", 11, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Content
        content = tk.Frame(parent, bg=theme.primary_bg)
        content.pack(fill="both", expand=True, padx=5, pady=5)

        # Outline tree
        outline_tree = ttk.Treeview(content, show="tree")
        outline_scrollbar = ttk.Scrollbar(
            content, orient="vertical", command=outline_tree.yview
        )
        outline_tree.configure(yscrollcommand=outline_scrollbar.set)

        outline_tree.pack(side="left", fill="both", expand=True)
        outline_scrollbar.pack(side="right", fill="y")

        # Sample outline
        class_node = outline_tree.insert(
            "", "end", text="🏛️ LinuxFlexibleTitlebarDemo", open=True
        )
        outline_tree.insert(class_node, "end", text="🔧 __init__")
        outline_tree.insert(class_node, "end", text="🎨 _setup_custom_titlebar")
        outline_tree.insert(class_node, "end", text="🖼️ _setup_layout")
        outline_tree.insert(class_node, "end", text="🎭 _switch_theme")

        functions_node = outline_tree.insert("", "end", text="📦 Functions", open=True)
        outline_tree.insert(functions_node, "end", text="🏃 main")
        outline_tree.insert(functions_node, "end", text="ℹ️ show_info")

    def _build_editor_pane(self, parent: tk.Frame):
        """Build the code editor pane."""
        theme = self.theme_manager.get_current_theme()

        # Header with tabs
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=35)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        # Tab buttons
        tabs = ["main.py", "utils.py", "config.py"]
        for i, tab in enumerate(tabs):
            tab_bg = theme.accent_bg if i == 0 else theme.panel_header_bg
            tab_fg = theme.accent_text if i == 0 else theme.panel_header_text

            tab_btn = tk.Button(
                header,
                text=f"📄 {tab}",
                bg=tab_bg,
                fg=tab_fg,
                relief="flat",
                padx=15,
                pady=5,
                command=lambda t=tab: self._show_info(f"Switched to {t}"),
            )
            tab_btn.pack(side="left", padx=1, pady=2)

        # Editor content
        editor_frame = tk.Frame(parent, bg=theme.primary_bg)
        editor_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Line numbers
        line_numbers = tk.Text(
            editor_frame,
            width=4,
            bg=theme.secondary_bg,
            fg=theme.secondary_text,
            state="disabled",
            wrap="none",
            font=("Ubuntu Mono", 11),
        )
        line_numbers.pack(side="left", fill="y")

        # Editor text area
        editor_text = tk.Text(
            editor_frame,
            bg=theme.primary_bg,
            fg=theme.primary_text,
            insertbackground=theme.accent_text,
            selectbackground=theme.accent_bg,
            selectforeground=theme.accent_text,
            wrap="none",
            font=("Ubuntu Mono", 11),
        )
        editor_text.pack(side="left", fill="both", expand=True)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(
            editor_frame, orient="vertical", command=editor_text.yview
        )
        h_scrollbar = ttk.Scrollbar(
            parent, orient="horizontal", command=editor_text.xview
        )
        editor_text.configure(
            yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set
        )

        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Sample code
        sample_code = '''#!/usr/bin/env python3
"""
Linux Flexible Layout Demo with Custom Titlebar
"""

import tkinter as tk
from threepanewindows.flexible import EnhancedFlexibleLayout

class DemoApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_layout()

    def setup_layout(self):
        """Setup the flexible layout system."""
        # Create layout configuration
        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL,
            children=[
                # Add panes here
            ]
        )

        # Create the layout
        self.layout = EnhancedFlexibleLayout(
            self.root, layout_config
        )
        self.layout.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = DemoApplication()
    app.root.mainloop()
'''

        editor_text.insert("1.0", sample_code)

        # Update line numbers
        lines = sample_code.count("\n") + 1
        line_numbers.config(state="normal")
        line_numbers.delete("1.0", "end")
        for i in range(1, lines + 1):
            line_numbers.insert("end", f"{i:3d}\n")
        line_numbers.config(state="disabled")

    def _build_terminal_pane(self, parent: tk.Frame):
        """Build the terminal pane."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="💻 Terminal",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=("Ubuntu", 11, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Terminal buttons
        btn_frame = tk.Frame(header, bg=theme.panel_header_bg)
        btn_frame.pack(side="right", padx=5)

        for text, cmd in [
            ("Clear", "clear"),
            ("New Tab", "new"),
            ("Settings", "settings"),
        ]:
            btn = tk.Button(
                btn_frame,
                text=text,
                bg=theme.button_bg,
                fg=theme.button_text,
                activebackground=theme.button_hover,
                relief="flat",
                padx=8,
                command=lambda c=cmd: self._show_info(f"Terminal: {c}"),
            )
            btn.pack(side="left", padx=2)

        # Terminal content
        terminal_frame = tk.Frame(parent, bg="#000000")
        terminal_frame.pack(fill="both", expand=True, padx=2, pady=2)

        terminal_text = tk.Text(
            terminal_frame,
            bg="#000000",
            fg="#00ff00",
            insertbackground="#00ff00",
            font=("Ubuntu Mono", 11),
            wrap="word",
        )
        terminal_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Sample terminal output
        terminal_output = """user@linux-demo:~/flexible-titlebar-demo$ ls -la
total 24
drwxr-xr-x  3 user user 4096 Jan 15 14:30 .
drwxr-xr-x 15 user user 4096 Jan 15 14:25 ..
-rw-r--r--  1 user user 1234 Jan 15 14:30 main.py
-rw-r--r--  1 user user  567 Jan 15 14:29 utils.py
-rw-r--r--  1 user user  890 Jan 15 14:28 config.py
drwxr-xr-x  2 user user 4096 Jan 15 14:27 tests

user@linux-demo:~/flexible-titlebar-demo$ python3 main.py
✓ Successfully imported threepanewindows modules
Platform detected: Linux
Available themes: light, dark, blue, green, purple, system, native
✓ Demo initialization complete

user@linux-demo:~/flexible-titlebar-demo$ # Theme switching demo ready!
user@linux-demo:~/flexible-titlebar-demo$ █"""

        terminal_text.insert("1.0", terminal_output)
        terminal_text.config(state="disabled")

    def _build_properties_pane(self, parent: tk.Frame):
        """Build the properties pane."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🔧 Properties",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=("Ubuntu", 11, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Properties content
        content = tk.Frame(parent, bg=theme.primary_bg)
        content.pack(fill="both", expand=True, padx=5, pady=5)

        # Current theme info
        theme_info_frame = tk.LabelFrame(
            content,
            text="Current Theme",
            bg=theme.primary_bg,
            fg=theme.primary_text,
            font=("Ubuntu", 10, "bold"),
        )
        theme_info_frame.pack(fill="x", pady=5)

        current_theme_name = getattr(
            self.theme_manager.current_theme, "value", "unknown"
        )
        tk.Label(
            theme_info_frame,
            text=f"Name: {current_theme_name.title()}",
            bg=theme.primary_bg,
            fg=theme.primary_text,
            font=("Ubuntu", 11),
        ).pack(anchor="w", padx=10, pady=2)

        tk.Label(
            theme_info_frame,
            text=f"Primary BG: {theme.primary_bg}",
            bg=theme.primary_bg,
            fg=theme.primary_text,
            font=("Ubuntu", 11),
        ).pack(anchor="w", padx=10, pady=2)

        tk.Label(
            theme_info_frame,
            text=f"Accent Color: {theme.accent_text}",
            bg=theme.primary_bg,
            fg=theme.primary_text,
            font=("Ubuntu", 11),
        ).pack(anchor="w", padx=10, pady=2)

        # File properties
        file_info_frame = tk.LabelFrame(
            content,
            text="Selected File",
            bg=theme.primary_bg,
            fg=theme.primary_text,
            font=("Ubuntu", 10, "bold"),
        )
        file_info_frame.pack(fill="x", pady=5)

        file_properties = [
            ("Name", "main.py"),
            ("Type", "Python File"),
            ("Size", "2.4 KB"),
            ("Modified", "2024-01-15 14:30"),
            ("Encoding", "UTF-8"),
            ("Lines", "87"),
        ]

        for prop, value in file_properties:
            prop_frame = tk.Frame(file_info_frame, bg=theme.primary_bg)
            prop_frame.pack(fill="x", padx=10, pady=1)

            tk.Label(
                prop_frame,
                text=f"{prop}:",
                bg=theme.primary_bg,
                fg=theme.secondary_text,
                font=("Ubuntu", 11),
                width=10,
                anchor="w",
            ).pack(side="left")

            tk.Label(
                prop_frame,
                text=value,
                bg=theme.primary_bg,
                fg=theme.primary_text,
                font=("Ubuntu", 11),
                anchor="w",
            ).pack(side="left", fill="x", expand=True)

    def _build_debug_pane(self, parent: tk.Frame):
        """Build the debug console pane."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🐛 Debug Console",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=("Ubuntu", 11, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Debug controls
        controls = tk.Frame(header, bg=theme.panel_header_bg)
        controls.pack(side="right", padx=5)

        for text, color in [("▶️", "#4CAF50"), ("⏸️", "#FF9800"), ("⏹️", "#F44336")]:
            btn = tk.Button(
                controls,
                text=text,
                bg=theme.button_bg,
                fg=color,
                activebackground=theme.button_hover,
                relief="flat",
                width=3,
                command=lambda t=text: self._show_info(f"Debug: {t}"),
            )
            btn.pack(side="left", padx=1)

        # Debug content
        debug_frame = tk.Frame(parent, bg=theme.primary_bg)
        debug_frame.pack(fill="both", expand=True, padx=2, pady=2)

        debug_text = tk.Text(
            debug_frame,
            bg=theme.secondary_bg,
            fg=theme.primary_text,
            font=("Ubuntu Mono", 10),
            wrap="word",
            state="disabled",
        )
        debug_scrollbar = ttk.Scrollbar(
            debug_frame, orient="vertical", command=debug_text.yview
        )
        debug_text.configure(yscrollcommand=debug_scrollbar.set)

        debug_text.pack(side="left", fill="both", expand=True)
        debug_scrollbar.pack(side="right", fill="y")

        # Sample debug output
        debug_output = """[14:30:15] DEBUG: Application initialized
[14:30:15] INFO: Theme manager loaded
[14:30:15] DEBUG: Available themes: 9
[14:30:16] INFO: Custom titlebar created
[14:30:16] DEBUG: Layout configuration loaded
[14:30:16] INFO: Flexible layout initialized
[14:30:16] DEBUG: All panes created successfully
[14:30:16] INFO: Demo ready for interaction
[14:30:17] DEBUG: Waiting for user input..."""

        debug_text.config(state="normal")
        debug_text.insert("1.0", debug_output)
        debug_text.config(state="disabled")

    def _build_output_pane(self, parent: tk.Frame):
        """Build the output pane."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📤 Output",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=("Ubuntu", 11, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Output controls
        controls = tk.Frame(header, bg=theme.panel_header_bg)
        controls.pack(side="right", padx=5)

        for text, tooltip in [("🗑️", "Clear"), ("💾", "Save"), ("📋", "Copy")]:
            btn = tk.Button(
                controls,
                text=text,
                bg=theme.button_bg,
                fg=theme.button_text,
                activebackground=theme.button_hover,
                relief="flat",
                width=3,
                command=lambda t=tooltip: self._show_info(f"Output: {t}"),
            )
            btn.pack(side="left", padx=1)

        # Output content
        output_frame = tk.Frame(parent, bg=theme.primary_bg)
        output_frame.pack(fill="both", expand=True, padx=2, pady=2)

        output_text = tk.Text(
            output_frame,
            bg=theme.primary_bg,
            fg=theme.primary_text,
            font=("Ubuntu Mono", 11),
            wrap="word",
            state="disabled",
        )
        output_scrollbar = ttk.Scrollbar(
            output_frame, orient="vertical", command=output_text.yview
        )
        output_text.configure(yscrollcommand=output_scrollbar.set)

        output_text.pack(side="left", fill="both", expand=True)
        output_scrollbar.pack(side="right", fill="y")

        # Sample output
        output_content = """Build started...
✓ Checking dependencies
✓ Compiling source files
✓ Running tests
  - test_flexible_layout.py ✓
  - test_custom_titlebar.py ✓
  - test_theme_switching.py ✓
✓ Generating documentation
✓ Creating distribution package

Build completed successfully!
Time: 2.3 seconds
Output: dist/linux-flexible-titlebar-demo-1.0.0.tar.gz

Ready for deployment."""

        output_text.config(state="normal")
        output_text.insert("1.0", output_content)
        output_text.config(state="disabled")

    def _switch_theme(self, theme_name: str):
        """Switch to a different theme."""
        try:
            print(f"\nSwitching to theme: {theme_name}")

            # Set the global theme
            set_global_theme(theme_name)

            # Update custom titlebar theme
            if self.custom_titlebar:
                theme = self.theme_manager.get_current_theme()
                theme_dict = {
                    "bg": theme.primary_bg,
                    "fg": theme.primary_text,
                    "btn_bg": theme.button_bg,
                    "btn_fg": theme.button_text,
                    "btn_active_bg": theme.button_hover,
                    "font": ("Ubuntu", 11),
                    "height": 32,
                }
                self.custom_titlebar.apply_theme(theme_dict)

            # Update window background
            theme = self.theme_manager.get_current_theme()
            self.root.configure(bg=theme.primary_bg)

            # Update layout theme
            if self.layout:
                self.layout.refresh_theme()

            # Update any detached windows
            for window in self.detached_windows.values():
                if hasattr(window, "refresh_theme"):
                    window.refresh_theme()

            print(f"✓ Theme switched to: {theme_name}")

        except Exception as e:
            print(f"✗ Error switching theme: {e}")
            logger.error(f"Theme switching failed: {e}")
            messagebox.showerror("Theme Error", f"Failed to switch theme: {e}")

    def _show_theme_info(self):
        """Show information about available themes."""
        theme_info = f"""Available Themes in Linux Flexible Titlebar Demo:

🎨 Theme Options:
• ☀️ Light Theme - Clean and bright interface
• 🌙 Dark Theme - Easy on the eyes for long coding sessions
• 💙 Blue Professional - Corporate and professional look
• 💚 Green Nature - Calming and natural colors
• 💜 Purple Elegance - Sophisticated and modern
• 🖥️ System Theme - Follows your system's theme
• 🏠 Native Theme - Uses platform-native colors

🔧 Current Theme: {getattr(self.theme_manager.current_theme, 'value', 'unknown').title()}

💡 Features:
• All themes work with custom titlebars
• Detached panes maintain theme consistency
• Real-time theme switching without restart
• Linux-optimized styling and fonts

🖱️ How to Switch:
• Use the 🎨 Themes menu in the titlebar
• All UI elements update automatically
• Detached windows update in real-time"""

        messagebox.showinfo("Theme Information", theme_info)

    def _show_about(self):
        """Show about dialog."""
        about_info = """Linux Flexible Layout + Custom Titlebar Demo

🐧 ThreePaneWindows Library
Version: Latest Development Build

✨ Features:
• Flexible layout system with detachable panes
• Cross-platform custom titlebar support
• Professional theme system with real-time switching
• Linux-optimized styling and behavior
• Native titlebar integration for perfect taskbar support

🛠️ Built with:
• Python 3.8+
• tkinter (native GUI framework)
• Linux desktop environment integration

💡 This demo showcases the full capabilities of the ThreePaneWindows library
with Linux-specific optimizations and native titlebar integration following
CustomTkinter's approach for perfect taskbar and window manager integration.

For more information, visit the project repository."""

        messagebox.showinfo("About", about_info)

    def _show_info(self, message: str):
        """Show an info message."""
        print(f"Info: {message}")
        # You could also show a status bar message or tooltip here

    def _on_window_close(self):
        """Handle window close event."""
        try:
            # Clean up custom titlebar
            if self.custom_titlebar:
                self.custom_titlebar.destroy()

            # Close any detached windows
            for window in list(self.detached_windows.values()):
                try:
                    window.destroy()
                except tk.TclError:
                    pass  # Window already destroyed

            # Quit the application
            self.root.quit()
            self.root.destroy()

        except Exception as e:
            print(f"Error during cleanup: {e}")
            self.root.quit()

    def run(self):
        """Run the demo application."""
        try:
            print("\n🚀 Starting Linux Flexible Titlebar Demo...")
            print("Features:")
            print("• Flexible layout with 6 detachable panes")
            print("• Custom titlebar with theme switching menu")
            print("• All available themes supported")
            print("• Linux-optimized styling")
            print("• Professional detached window management")
            print("\n💡 Try detaching panes and switching themes!")
            print("=" * 60)

            self.root.mainloop()

        except KeyboardInterrupt:
            print("\n⚠️ Demo interrupted by user")
        except Exception as e:
            print(f"✗ Error running demo: {e}")
            logger.error(f"Demo execution failed: {e}")
            import traceback

            traceback.print_exc()
        finally:
            print("\n👋 Demo finished")


def main():
    """Main entry point for the demo."""
    print("Linux Flexible Layout + Custom Titlebar Demo")
    print("=" * 50)

    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Error: Python 3.8 or higher is required")
        print(f"Current version: {platform.python_version()}")
        return 1

    # Check platform
    current_os = platform.system()
    print(f"Platform: {current_os}")

    if current_os != "Linux":
        print(f"⚠️ Warning: This demo is optimized for Linux systems.")
        print("Some features may not work as expected on other platforms.")
        print()

    try:
        # Create and run the demo
        demo = LinuxFlexibleTitlebarDemo()
        demo.run()
        return 0

    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Make sure the threepanewindows package is properly installed")
        return 1
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
        return 0
    except Exception as e:
        print(f"✗ Error running demo: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
