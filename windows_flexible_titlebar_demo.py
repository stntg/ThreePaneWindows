#!/usr/bin/env python3
"""
Standalone Windows Example: Flexible Layout with Custom Titlebar and Theme Switching

This example demonstrates:
1. Flexible layout system with complex nested layouts
2. Custom titlebar for both main window and detached panes
3. Complete theme switching through all available themes
4. Windows-optimized styling and behavior
5. Professional detached window management
6. Windows-specific features and integrations

Features:
- Main window with Windows-style custom titlebar
- Detached panes with custom titlebars
- Theme switching menu with all available themes
- Windows-native styling and fonts (Segoe UI)
- Professional UI components
- Windows-specific window management and focus handling
- System theme detection and integration

Usage:
    python windows_flexible_titlebar_demo.py

Requirements:
- Python 3.8+
- tkinter (usually included with Python)
- threepanewindows package
- Windows 10/11 (optimized for)
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


class WindowsFlexibleTitlebarDemo:
    """
    Standalone Windows demo showcasing flexible layout with custom titlebar
    and comprehensive theme switching functionality.
    """

    def __init__(self):
        """Initialize the demo application."""
        print("\n" + "=" * 60)
        print("Windows Flexible Layout + Custom Titlebar Demo")
        print("=" * 60)

        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Windows Flexible Layout + Custom Titlebar Demo")
        self.root.geometry("1000x900")
        self.root.minsize(1000, 700)

        # Hide window initially to prevent dual-window issues
        self.root.withdraw()

        # Detect platform
        self.platform_name = platform.system()
        self.is_windows = self.platform_name.lower() == "windows"

        print(f"Platform detected: {self.platform_name}")
        print(f"Windows optimizations: {'Enabled' if self.is_windows else 'Disabled'}")

        # Initialize theme manager
        self.theme_manager = get_theme_manager()

        # Get all available themes
        self.available_themes = self.theme_manager.get_theme_names()
        print(f"Available themes: {', '.join(self.available_themes)}")

        # Set initial theme (prefer system theme on Windows)
        initial_theme = (
            "system"
            if self._detect_system_theme()
            else ("dark" if self._detect_dark_mode() else "light")
        )
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

        # Show the window after everything is set up
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

        print("✓ Demo initialization complete")

    def _detect_system_theme(self) -> bool:
        """Detect if system theme is available."""
        return "system" in self.available_themes

    def _detect_dark_mode(self) -> bool:
        """Detect if the system is using dark mode."""
        try:
            return platform_handler.is_dark_mode()
        except Exception:
            return False

    def _setup_custom_titlebar(self):
        """Setup custom titlebar based on platform."""
        print("\nSetting up Windows custom titlebar...")

        try:
            theme = self.theme_manager.get_current_theme()

            # Convert theme to dictionary format expected by titlebar
            theme_dict = {
                "bg": theme.primary_bg,
                "fg": theme.primary_text,
                "btn_bg": theme.button_bg,
                "btn_fg": theme.button_text,
                "btn_active_bg": theme.button_hover,
                "font": ("Segoe UI", 10),  # Use Windows-optimized font
                "height": 32,
            }

            # Create platform-specific titlebar
            if self.platform_name == "Windows":
                self.custom_titlebar = WindowsTitleBar(
                    self.root,
                    theme_dict,
                    "Windows Flexible Layout + Custom Titlebar Demo",
                )
            elif self.platform_name == "Linux":
                self.custom_titlebar = LinuxTitleBar(
                    self.root,
                    theme_dict,
                    "Windows Flexible Layout + Custom Titlebar Demo",
                )
            elif self.platform_name == "Darwin":  # macOS
                self.custom_titlebar = MacOSTitleBar(
                    self.root,
                    theme_dict,
                    "Windows Flexible Layout + Custom Titlebar Demo",
                )

            if self.custom_titlebar:
                titlebar_frame = self.custom_titlebar.create_titlebar()
                if titlebar_frame:
                    # Pack the titlebar frame to the top of the window
                    titlebar_frame.pack(side="top", fill="x")
                    titlebar_frame.pack_propagate(False)

                    # Add theme switching menu to titlebar
                    self._add_theme_menu_to_titlebar(titlebar_frame)
                    print("✓ Custom titlebar created successfully")
                else:
                    print("⚠ Custom titlebar frame not created")
                    # For Windows native titlebar, create a menu bar instead
                    if self.platform_name == "Windows":
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
                font=("Segoe UI", 9),
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

    def _setup_window_properties(self):
        """Setup Windows-specific window properties."""
        try:
            theme = self.theme_manager.get_current_theme()

            # Set window background
            self.root.configure(bg=theme.primary_bg)

            # Windows-specific window properties
            if self.is_windows:
                # Set window class for better integration (if supported)
                try:
                    self.root.wm_class("FlexibleTitlebarDemo", "ThreePaneWindows")
                except (tk.TclError, AttributeError):
                    pass  # wm_class not supported on all tkinter versions

                # Windows-specific attributes
                try:
                    # Enable DPI awareness
                    self.root.tk.call("tk", "scaling", 1.0)

                    # Set window attributes for better Windows integration
                    self.root.wm_attributes("-toolwindow", False)

                except tk.TclError:
                    pass  # Not all attributes are supported on all Windows versions

                # Set window protocol
                self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)

            print("✓ Window properties configured")

        except Exception as e:
            print(f"✗ Error setting up window properties: {e}")
            logger.error(f"Window properties setup failed: {e}")

    def _setup_window_icon(self):
        """Setup window icon."""
        try:
            # Try to find an icon file (prefer .ico on Windows)
            icon_paths = [
                os.path.join(
                    project_root, "threepanewindows", "utils", "icons", "app.ico"
                ),
                os.path.join(
                    project_root,
                    "threepanewindows",
                    "utils",
                    "icons",
                    "folder-1449.png",
                ),
                os.path.join(project_root, "sample_images", "icon.ico"),
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
            # Define a Windows-optimized layout structure
            layout_config = FlexContainer(
                direction=LayoutDirection.HORIZONTAL,
                children=[
                    # Left sidebar (25% width)
                    FlexContainer(
                        direction=LayoutDirection.VERTICAL,
                        weight=0.25,
                        children=[
                            FlexPaneConfig(
                                name="solution_explorer",
                                title="📁 Solution Explorer",
                                weight=0.6,
                                min_size=200,
                                builder=self._build_solution_explorer_pane,
                                custom_titlebar=True,
                                default_width=400,
                                detached_height=500,
                                detachable=True,
                                icon="📁",
                            ),
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
                        ],
                    ),
                    # Center area (50% width)
                    FlexContainer(
                        direction=LayoutDirection.VERTICAL,
                        weight=0.5,
                        children=[
                            FlexPaneConfig(
                                name="code_editor",
                                title="📝 Code Editor",
                                weight=0.7,
                                min_size=300,
                                builder=self._build_code_editor_pane,
                                custom_titlebar=True,
                                default_width=700,
                                detached_height=600,
                                detachable=True,
                                icon="📝",
                            ),
                            FlexPaneConfig(
                                name="command_prompt",
                                title="💻 Command Prompt",
                                weight=0.3,
                                min_size=150,
                                builder=self._build_command_prompt_pane,
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
                                name="toolbox",
                                title="🧰 Toolbox",
                                weight=0.4,
                                min_size=150,
                                builder=self._build_toolbox_pane,
                                custom_titlebar=True,
                                default_width=350,
                                detached_height=400,
                                detachable=True,
                                icon="🧰",
                            ),
                            FlexPaneConfig(
                                name="error_list",
                                title="❌ Error List",
                                weight=0.3,
                                min_size=120,
                                builder=self._build_error_list_pane,
                                custom_titlebar=True,
                                default_width=350,
                                detached_height=350,
                                detachable=True,
                                icon="❌",
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

    def _build_solution_explorer_pane(self, parent: tk.Frame):
        """Build the Solution Explorer pane (Windows-style file explorer)."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📁 Solution Explorer",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Toolbar
        toolbar = tk.Frame(header, bg=theme.panel_header_bg)
        toolbar.pack(side="right", padx=5)

        for icon, tooltip in [
            ("🔄", "Refresh"),
            ("➕", "Add Item"),
            ("📁", "New Folder"),
            ("⚙️", "Properties"),
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

        # Solution tree
        tree_frame = tk.Frame(parent, bg=theme.primary_bg)
        tree_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Create treeview with scrollbar
        tree = ttk.Treeview(tree_frame, show="tree")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Populate tree with Windows-style project structure
        solution = tree.insert("", "end", text="📁 MyWindowsApp.sln", open=True)

        project = tree.insert(solution, "end", text="📁 MyWindowsApp", open=True)
        tree.insert(project, "end", text="📄 Program.cs")
        tree.insert(project, "end", text="📄 MainWindow.xaml")
        tree.insert(project, "end", text="📄 MainWindow.xaml.cs")
        tree.insert(project, "end", text="📄 App.xaml")
        tree.insert(project, "end", text="📄 App.xaml.cs")

        properties = tree.insert(project, "end", text="📁 Properties", open=False)
        tree.insert(properties, "end", text="📄 AssemblyInfo.cs")
        tree.insert(properties, "end", text="📄 Resources.resx")
        tree.insert(properties, "end", text="📄 Settings.settings")

        references = tree.insert(project, "end", text="📁 References", open=False)
        tree.insert(references, "end", text="📚 System")
        tree.insert(references, "end", text="📚 System.Windows.Forms")
        tree.insert(references, "end", text="📚 System.Drawing")

    def _build_code_editor_pane(self, parent: tk.Frame):
        """Build the code editor pane with Windows-style tabs."""
        theme = self.theme_manager.get_current_theme()

        # Header with tabs
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=35)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        # Tab buttons
        tabs = ["Program.cs", "MainWindow.xaml", "App.config"]
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
            font=("Consolas", 10),  # Windows monospace font
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
            font=("Consolas", 10),
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

        # Sample C# code
        sample_code = """using System;
using System.Windows.Forms;

namespace MyWindowsApp
{
    class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            // Initialize the flexible layout demo
            var demo = new FlexibleLayoutDemo();

            Application.Run(demo);
        }
    }

    public partial class FlexibleLayoutDemo : Form
    {
        public FlexibleLayoutDemo()
        {
            InitializeComponent();
            SetupLayout();
        }

        private void SetupLayout()
        {
            // Setup the flexible layout system
            this.Text = "Windows Flexible Layout Demo";
            this.Size = new Size(1400, 900);
            this.MinimumSize = new Size(1000, 700);
        }
    }
}"""

        editor_text.insert("1.0", sample_code)

        # Update line numbers
        lines = sample_code.count("\n") + 1
        line_numbers.config(state="normal")
        line_numbers.delete("1.0", "end")
        for i in range(1, lines + 1):
            line_numbers.insert("end", f"{i:3d}\n")
        line_numbers.config(state="disabled")

    def _build_command_prompt_pane(self, parent: tk.Frame):
        """Build the command prompt pane."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="💻 Command Prompt",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Command prompt buttons
        btn_frame = tk.Frame(header, bg=theme.panel_header_bg)
        btn_frame.pack(side="right", padx=5)

        for text, cmd in [
            ("Clear", "cls"),
            ("New", "new"),
            ("PowerShell", "powershell"),
        ]:
            btn = tk.Button(
                btn_frame,
                text=text,
                bg=theme.button_bg,
                fg=theme.button_text,
                activebackground=theme.button_hover,
                relief="flat",
                padx=8,
                command=lambda c=cmd: self._show_info(f"Command: {c}"),
            )
            btn.pack(side="left", padx=2)

        # Command prompt content
        cmd_frame = tk.Frame(parent, bg="#000000")
        cmd_frame.pack(fill="both", expand=True, padx=2, pady=2)

        cmd_text = tk.Text(
            cmd_frame,
            bg="#000000",
            fg="#ffffff",
            insertbackground="#ffffff",
            font=("Consolas", 10),
            wrap="word",
        )
        cmd_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Sample Windows command prompt output
        cmd_output = """Microsoft Windows [Version 10.0.22621.2428]
(c) Microsoft Corporation. All rights reserved.

C:\\Users\\User\\Documents\\FlexibleTitlebarDemo>dir
 Volume in drive C has no label.
 Volume Serial Number is 1234-5678

 Directory of C:\\Users\\User\\Documents\\FlexibleTitlebarDemo

01/15/2024  02:30 PM    <DIR>          .
01/15/2024  02:30 PM    <DIR>          ..
01/15/2024  02:30 PM             2,456 Program.cs
01/15/2024  02:29 PM               567 MainWindow.xaml
01/15/2024  02:28 PM               890 MainWindow.xaml.cs
01/15/2024  02:27 PM               234 App.config
01/15/2024  02:26 PM    <DIR>          bin
01/15/2024  02:25 PM    <DIR>          obj
               4 File(s)          4,147 bytes
               4 Dir(s)  125,234,567,890 bytes free

C:\\Users\\User\\Documents\\FlexibleTitlebarDemo>dotnet build
Microsoft (R) Build Engine version 17.8.3+195e7f5a3 for .NET
Copyright (C) Microsoft Corporation. All rights reserved.

  Determining projects to restore...
  All projects are up-to-date for restore.
  MyWindowsApp -> C:\\Users\\User\\Documents\\FlexibleTitlebarDemo\\bin\\Debug\\net6.0-windows\\MyWindowsApp.exe

Build succeeded.
    0 Warning(s)
    0 Error(s)

Time Elapsed 00:00:02.34

C:\\Users\\User\\Documents\\FlexibleTitlebarDemo>█"""

        cmd_text.insert("1.0", cmd_output)
        cmd_text.config(state="disabled")

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
            font=("Segoe UI", 10, "bold"),
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
            font=("Segoe UI", 9, "bold"),
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
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=10, pady=2)

        tk.Label(
            theme_info_frame,
            text=f"Primary BG: {theme.primary_bg}",
            bg=theme.primary_bg,
            fg=theme.primary_text,
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=10, pady=2)

        tk.Label(
            theme_info_frame,
            text=f"Accent Color: {theme.accent_text}",
            bg=theme.primary_bg,
            fg=theme.primary_text,
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=10, pady=2)

        # Windows system info
        system_info_frame = tk.LabelFrame(
            content,
            text="System Information",
            bg=theme.primary_bg,
            fg=theme.primary_text,
            font=("Segoe UI", 9, "bold"),
        )
        system_info_frame.pack(fill="x", pady=5)

        system_properties = [
            ("OS", f"{platform.system()} {platform.release()}"),
            ("Version", platform.version()),
            ("Architecture", platform.architecture()[0]),
            ("Processor", platform.processor() or "Unknown"),
            ("Python", platform.python_version()),
        ]

        for prop, value in system_properties:
            prop_frame = tk.Frame(system_info_frame, bg=theme.primary_bg)
            prop_frame.pack(fill="x", padx=10, pady=1)

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

    def _build_toolbox_pane(self, parent: tk.Frame):
        """Build the toolbox pane."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🧰 Toolbox",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Toolbox content
        content = tk.Frame(parent, bg=theme.primary_bg)
        content.pack(fill="both", expand=True, padx=5, pady=5)

        # Categories
        categories = [
            (
                "Common Controls",
                ["Button", "TextBox", "Label", "CheckBox", "RadioButton"],
            ),
            ("Containers", ["Panel", "GroupBox", "TabControl", "SplitContainer"]),
            ("Data", ["DataGridView", "ListBox", "ComboBox", "TreeView"]),
            (
                "Menus & Toolbars",
                ["MenuStrip", "ToolStrip", "StatusStrip", "ContextMenuStrip"],
            ),
        ]

        for category, controls in categories:
            cat_frame = tk.LabelFrame(
                content,
                text=category,
                bg=theme.primary_bg,
                fg=theme.primary_text,
                font=("Segoe UI", 9, "bold"),
            )
            cat_frame.pack(fill="x", pady=2)

            for control in controls:
                ctrl_btn = tk.Button(
                    cat_frame,
                    text=f"🔧 {control}",
                    bg=theme.button_bg,
                    fg=theme.button_text,
                    activebackground=theme.button_hover,
                    relief="flat",
                    anchor="w",
                    padx=10,
                    command=lambda c=control: self._show_info(f"Selected control: {c}"),
                )
                ctrl_btn.pack(fill="x", padx=5, pady=1)

    def _build_error_list_pane(self, parent: tk.Frame):
        """Build the error list pane."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="❌ Error List",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Filter buttons
        filter_frame = tk.Frame(header, bg=theme.panel_header_bg)
        filter_frame.pack(side="right", padx=5)

        for text, color in [("❌", "#F44336"), ("⚠️", "#FF9800"), ("ℹ️", "#2196F3")]:
            btn = tk.Button(
                filter_frame,
                text=text,
                bg=theme.button_bg,
                fg=color,
                activebackground=theme.button_hover,
                relief="flat",
                width=3,
                command=lambda t=text: self._show_info(f"Filter: {t}"),
            )
            btn.pack(side="left", padx=1)

        # Error list content
        error_frame = tk.Frame(parent, bg=theme.primary_bg)
        error_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Create treeview for errors
        columns = ("Type", "Description", "File", "Line")
        error_tree = ttk.Treeview(
            error_frame, columns=columns, show="headings", height=8
        )

        # Configure columns
        error_tree.heading("Type", text="Type")
        error_tree.heading("Description", text="Description")
        error_tree.heading("File", text="File")
        error_tree.heading("Line", text="Line")

        error_tree.column("Type", width=60)
        error_tree.column("Description", width=300)
        error_tree.column("File", width=150)
        error_tree.column("Line", width=50)

        # Add sample errors
        errors = [
            (
                "Error",
                "CS0103: The name 'undeclaredVar' does not exist",
                "Program.cs",
                "15",
            ),
            (
                "Warning",
                "CS0219: Variable 'unusedVar' is assigned but never used",
                "MainWindow.cs",
                "23",
            ),
            ("Info", "Build succeeded with warnings", "Build", ""),
        ]

        for error_type, desc, file, line in errors:
            error_tree.insert("", "end", values=(error_type, desc, file, line))

        error_tree.pack(fill="both", expand=True)

        # Scrollbar
        error_scrollbar = ttk.Scrollbar(
            error_frame, orient="vertical", command=error_tree.yview
        )
        error_tree.configure(yscrollcommand=error_scrollbar.set)
        error_scrollbar.pack(side="right", fill="y")

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
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Output controls
        controls = tk.Frame(header, bg=theme.panel_header_bg)
        controls.pack(side="right", padx=5)

        # Output source dropdown
        source_var = tk.StringVar(value="Build")
        source_combo = ttk.Combobox(
            controls,
            textvariable=source_var,
            values=["Build", "Debug", "General", "Package Manager"],
            state="readonly",
            width=12,
        )
        source_combo.pack(side="left", padx=2)

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
            font=("Consolas", 9),
            wrap="word",
            state="disabled",
        )
        output_scrollbar = ttk.Scrollbar(
            output_frame, orient="vertical", command=output_text.yview
        )
        output_text.configure(yscrollcommand=output_scrollbar.set)

        output_text.pack(side="left", fill="both", expand=True)
        output_scrollbar.pack(side="right", fill="y")

        # Sample build output
        output_content = """Build started...
1>------ Build started: Project: MyWindowsApp, Configuration: Debug Any CPU ------
1>  MyWindowsApp -> C:\\Users\\User\\Documents\\FlexibleTitlebarDemo\\bin\\Debug\\MyWindowsApp.exe
========== Build: 1 succeeded, 0 failed, 0 up-to-date, 0 skipped ==========

Package restore started...
  Determining projects to restore...
  Restored C:\\Users\\User\\Documents\\FlexibleTitlebarDemo\\MyWindowsApp.csproj (in 234 ms).

NuGet package restore finished.

Theme switching functionality initialized.
Flexible layout system loaded successfully.
Custom titlebar integration complete.

Ready for development."""

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
                    "font": ("Segoe UI", 10),
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
        theme_info = f"""Available Themes in Windows Flexible Titlebar Demo:

🎨 Theme Options:
• ☀️ Light Theme - Clean and bright interface
• 🌙 Dark Theme - Easy on the eyes for long coding sessions
• 💙 Blue Professional - Corporate and professional look
• 💚 Green Nature - Calming and natural colors
• 💜 Purple Elegance - Sophisticated and modern
• 🖥️ System Theme - Follows your Windows system theme
• 🏠 Native Theme - Uses Windows-native colors

🔧 Current Theme: {getattr(self.theme_manager.current_theme, 'value', 'unknown').title()}

💡 Windows Features:
• All themes work with custom titlebars
• Detached panes maintain theme consistency
• Real-time theme switching without restart
• Windows-optimized styling and fonts (Segoe UI, Consolas)
• System theme integration

🖱️ How to Switch:
• Use the 🎨 Themes menu in the titlebar
• All UI elements update automatically
• Detached windows update in real-time"""

        messagebox.showinfo("Theme Information", theme_info)

    def _show_about(self):
        """Show about dialog."""
        about_info = """Windows Flexible Layout + Custom Titlebar Demo

🪟 ThreePaneWindows Library
Version: Latest Development Build

✨ Features:
• Flexible layout system with detachable panes
• Cross-platform custom titlebar support
• Professional theme system with real-time switching
• Windows-optimized styling and behavior
• Visual Studio-inspired interface design

🛠️ Built with:
• Python 3.8+
• tkinter (native GUI framework)
• Windows API integration for native titlebar theming

💡 This demo showcases the full capabilities of the ThreePaneWindows library
with Windows-specific optimizations and native titlebar integration.

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
            print("\n🚀 Starting Windows Flexible Titlebar Demo...")
            print("Features:")
            print("• Flexible layout with 6 detachable panes")
            print("• Windows-style custom titlebar with theme switching menu")
            print("• All available themes supported")
            print("• Windows-optimized styling (Segoe UI, Consolas fonts)")
            print("• Professional detached window management")
            print("• Visual Studio-inspired layout and controls")
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
    print("Windows Flexible Layout + Custom Titlebar Demo")
    print("=" * 50)

    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Error: Python 3.8 or higher is required")
        print(f"Current version: {platform.python_version()}")
        return 1

    # Check platform
    current_os = platform.system()
    print(f"Platform: {current_os}")

    if current_os != "Windows":
        print(f"⚠️ Warning: This demo is optimized for Windows systems.")
        print("Some features may not work as expected on other platforms.")
        print()

    try:
        # Create and run the demo
        demo = WindowsFlexibleTitlebarDemo()
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
