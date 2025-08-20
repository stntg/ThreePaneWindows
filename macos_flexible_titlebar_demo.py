#!/usr/bin/env python3
"""
Standalone macOS Example: Flexible Layout with Custom Titlebar and Theme Switching

This example demonstrates:
1. Flexible layout system with complex nested layouts
2. Custom titlebar for both main window and detached panes
3. Complete theme switching through all available themes
4. macOS-optimized styling and behavior
5. Professional detached window management
6. macOS-specific features and integrations

Features:
- Main window with macOS-style custom titlebar
- Detached panes with custom titlebars
- Theme switching menu with all available themes
- macOS-native styling and fonts (SF Pro, Menlo)
- Professional UI components
- macOS-specific window management and focus handling
- System theme detection and integration
- Retina display optimization

Usage:
    python3 macos_flexible_titlebar_demo.py

Requirements:
- Python 3.8+
- tkinter (usually included with Python)
- threepanewindows package
- macOS 10.14+ (optimized for)
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


class MacOSFlexibleTitlebarDemo:
    """
    Standalone macOS demo showcasing flexible layout with custom titlebar
    and comprehensive theme switching functionality.
    """

    def __init__(self):
        """Initialize the demo application."""
        print("\n" + "=" * 60)
        print("macOS Flexible Layout + Custom Titlebar Demo")
        print("=" * 60)

        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("macOS Flexible Layout + Custom Titlebar Demo")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)

        # Hide window initially to prevent dual-window issues
        self.root.withdraw()

        # Detect platform
        self.platform_name = platform.system()
        self.is_macos = self.platform_name.lower() == "darwin"

        print(f"Platform detected: {self.platform_name}")
        print(f"macOS optimizations: {'Enabled' if self.is_macos else 'Disabled'}")

        # Initialize theme manager
        self.theme_manager = get_theme_manager()

        # Get all available themes
        self.available_themes = self.theme_manager.get_theme_names()
        print(f"Available themes: {', '.join(self.available_themes)}")

        # Set initial theme (prefer system theme on macOS)
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
        print("\nSetting up macOS custom titlebar...")

        try:
            theme = self.theme_manager.get_current_theme()

            # Convert theme to dictionary format expected by titlebar
            theme_dict = {
                "bg": theme.primary_bg,
                "fg": theme.primary_text,
                "btn_bg": theme.button_bg,
                "btn_fg": theme.button_text,
                "btn_active_bg": theme.button_hover,
                "font": (".AppleSystemUIFont", 13),  # Use macOS system font
                "height": 28,  # macOS titlebar height
            }

            # Create platform-specific titlebar
            if self.platform_name == "Darwin":  # macOS
                self.custom_titlebar = MacOSTitleBar(
                    self.root,
                    theme_dict,
                    "macOS Flexible Layout + Custom Titlebar Demo",
                )
            elif self.platform_name == "Windows":
                self.custom_titlebar = WindowsTitleBar(
                    self.root,
                    theme_dict,
                    "macOS Flexible Layout + Custom Titlebar Demo",
                )
            elif self.platform_name == "Linux":
                self.custom_titlebar = LinuxTitleBar(
                    self.root,
                    theme_dict,
                    "macOS Flexible Layout + Custom Titlebar Demo",
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
                font=(".AppleSystemUIFont", 12),
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

    def _setup_window_properties(self):
        """Setup macOS-specific window properties."""
        try:
            theme = self.theme_manager.get_current_theme()

            # Set window background
            self.root.configure(bg=theme.primary_bg)

            # macOS-specific window properties
            if self.is_macos:
                # Set window class for better integration (if supported)
                try:
                    self.root.wm_class("FlexibleTitlebarDemo", "ThreePaneWindows")
                except (tk.TclError, AttributeError):
                    pass  # wm_class not supported on all tkinter versions

                # macOS-specific attributes
                try:
                    # Enable unified title and toolbar look
                    self.root.wm_attributes("-titlepath", "")

                    # Set window level
                    self.root.wm_attributes("-topmost", False)

                    # Enable full screen
                    self.root.wm_attributes("-fullscreen", False)

                except tk.TclError:
                    pass  # Not all attributes are supported on all macOS versions

                # Set window protocol
                self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)

            print("✓ Window properties configured")

        except Exception as e:
            print(f"✗ Error setting up window properties: {e}")
            logger.error(f"Window properties setup failed: {e}")

    def _setup_window_icon(self):
        """Setup window icon."""
        try:
            # Try to find an icon file (prefer .icns on macOS)
            icon_paths = [
                os.path.join(
                    project_root, "threepanewindows", "utils", "icons", "app.icns"
                ),
                os.path.join(
                    project_root,
                    "threepanewindows",
                    "utils",
                    "icons",
                    "folder-1449.png",
                ),
                os.path.join(project_root, "sample_images", "icon.icns"),
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
            # Define a macOS-optimized layout structure
            layout_config = FlexContainer(
                direction=LayoutDirection.HORIZONTAL,
                children=[
                    # Left sidebar (25% width)
                    FlexContainer(
                        direction=LayoutDirection.VERTICAL,
                        weight=0.25,
                        children=[
                            FlexPaneConfig(
                                name="navigator",
                                title="📁 Project Navigator",
                                weight=0.6,
                                min_size=200,
                                builder=self._build_project_navigator_pane,
                                custom_titlebar=True,
                                default_width=400,
                                detached_height=500,
                                detachable=True,
                                icon="📁",
                            ),
                            FlexPaneConfig(
                                name="inspector",
                                title="🔍 Inspector",
                                weight=0.4,
                                min_size=150,
                                builder=self._build_inspector_pane,
                                custom_titlebar=True,
                                default_width=350,
                                detached_height=400,
                                detachable=True,
                                icon="🔍",
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
                                title="📝 Source Editor",
                                weight=0.7,
                                min_size=300,
                                builder=self._build_source_editor_pane,
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
                                name="utilities",
                                title="🛠️ Utilities",
                                weight=0.4,
                                min_size=150,
                                builder=self._build_utilities_pane,
                                custom_titlebar=True,
                                default_width=350,
                                detached_height=400,
                                detachable=True,
                                icon="🛠️",
                            ),
                            FlexPaneConfig(
                                name="debug_area",
                                title="🐛 Debug Area",
                                weight=0.3,
                                min_size=120,
                                builder=self._build_debug_area_pane,
                                custom_titlebar=True,
                                default_width=350,
                                detached_height=350,
                                detachable=True,
                                icon="🐛",
                            ),
                            FlexPaneConfig(
                                name="report_navigator",
                                title="📊 Report Navigator",
                                weight=0.3,
                                min_size=120,
                                builder=self._build_report_navigator_pane,
                                custom_titlebar=True,
                                default_width=350,
                                detached_height=300,
                                detachable=True,
                                icon="📊",
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

    def _build_project_navigator_pane(self, parent: tk.Frame):
        """Build the Project Navigator pane (Xcode-style)."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📁 Project Navigator",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=(".AppleSystemUIFont", 12, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Toolbar
        toolbar = tk.Frame(header, bg=theme.panel_header_bg)
        toolbar.pack(side="right", padx=5)

        for icon, tooltip in [
            ("🔍", "Search"),
            ("➕", "Add Files"),
            ("📁", "New Group"),
            ("⚙️", "Options"),
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

        # Project tree
        tree_frame = tk.Frame(parent, bg=theme.primary_bg)
        tree_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Create treeview with scrollbar
        tree = ttk.Treeview(tree_frame, show="tree")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Populate tree with Xcode-style project structure
        project = tree.insert("", "end", text="📱 MyMacApp", open=True)

        # App group
        app_group = tree.insert(project, "end", text="📁 MyMacApp", open=True)
        tree.insert(app_group, "end", text="📄 AppDelegate.swift")
        tree.insert(app_group, "end", text="📄 SceneDelegate.swift")
        tree.insert(app_group, "end", text="📄 ViewController.swift")
        tree.insert(app_group, "end", text="📄 Main.storyboard")
        tree.insert(app_group, "end", text="📄 LaunchScreen.storyboard")

        # Assets
        assets = tree.insert(app_group, "end", text="📁 Assets.xcassets", open=False)
        tree.insert(assets, "end", text="🖼️ AppIcon")
        tree.insert(assets, "end", text="🎨 AccentColor")

        # Supporting Files
        supporting = tree.insert(
            app_group, "end", text="📁 Supporting Files", open=False
        )
        tree.insert(supporting, "end", text="📄 Info.plist")
        tree.insert(supporting, "end", text="📄 MyMacApp.entitlements")

        # Products
        products = tree.insert(project, "end", text="📁 Products", open=False)
        tree.insert(products, "end", text="📱 MyMacApp.app")

        # Frameworks
        frameworks = tree.insert(project, "end", text="📁 Frameworks", open=False)
        tree.insert(frameworks, "end", text="📚 UIKit.framework")
        tree.insert(frameworks, "end", text="📚 Foundation.framework")

    def _build_source_editor_pane(self, parent: tk.Frame):
        """Build the source editor pane with Xcode-style tabs."""
        theme = self.theme_manager.get_current_theme()

        # Header with tabs
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=35)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        # Tab buttons
        tabs = ["AppDelegate.swift", "ViewController.swift", "Main.storyboard"]
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
            font=("Menlo", 12),  # macOS monospace font
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
            font=("Menlo", 12),
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

        # Sample Swift code
        sample_code = """import UIKit

class ViewController: UIViewController {

    // MARK: - Properties
    @IBOutlet weak var titleLabel: UILabel!
    @IBOutlet weak var themeButton: UIButton!

    // MARK: - Lifecycle
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        setupFlexibleLayout()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        updateTheme()
    }

    // MARK: - Setup
    private func setupUI() {
        titleLabel.text = "macOS Flexible Layout Demo"
        titleLabel.font = UIFont.systemFont(ofSize: 24, weight: .bold)

        themeButton.setTitle("🎨 Switch Theme", for: .normal)
        themeButton.addTarget(self, action: #selector(themeButtonTapped), for: .touchUpInside)
    }

    private func setupFlexibleLayout() {
        // Initialize the flexible layout system
        let layoutConfig = FlexContainer(
            direction: .horizontal,
            children: [
                // Add panes here
            ]
        )

        // Apply the layout
        view.addSubview(layoutConfig.view)
        layoutConfig.view.translatesAutoresizingMaskIntoConstraints = false
        NSLayoutConstraint.activate([
            layoutConfig.view.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            layoutConfig.view.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            layoutConfig.view.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            layoutConfig.view.bottomAnchor.constraint(equalTo: view.bottomAnchor)
        ])
    }

    // MARK: - Actions
    @objc private func themeButtonTapped() {
        // Handle theme switching
        ThemeManager.shared.switchToNextTheme()
        updateTheme()
    }

    private func updateTheme() {
        let currentTheme = ThemeManager.shared.currentTheme
        view.backgroundColor = currentTheme.primaryBackground
        titleLabel.textColor = currentTheme.primaryText
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
            font=(".AppleSystemUIFont", 12, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Terminal buttons
        btn_frame = tk.Frame(header, bg=theme.panel_header_bg)
        btn_frame.pack(side="right", padx=5)

        for text, cmd in [("Clear", "clear"), ("New Tab", "⌘T"), ("Split", "⌘D")]:
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
        terminal_frame = tk.Frame(parent, bg="#1e1e1e")  # Dark terminal background
        terminal_frame.pack(fill="both", expand=True, padx=2, pady=2)

        terminal_text = tk.Text(
            terminal_frame,
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="#ffffff",
            font=("Menlo", 11),
            wrap="word",
        )
        terminal_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Sample macOS terminal output
        terminal_output = """Last login: Mon Jan 15 14:30:15 on ttys000
user@MacBook-Pro flexible-titlebar-demo % ls -la
total 32
drwxr-xr-x   8 user  staff   256 Jan 15 14:30 .
drwxr-xr-x  15 user  staff   480 Jan 15 14:25 ..
-rw-r--r--   1 user  staff  1234 Jan 15 14:30 AppDelegate.swift
-rw-r--r--   1 user  staff   567 Jan 15 14:29 ViewController.swift
-rw-r--r--   1 user  staff   890 Jan 15 14:28 Main.storyboard
drwxr-xr-x   4 user  staff   128 Jan 15 14:27 Assets.xcassets
-rw-r--r--   1 user  staff   456 Jan 15 14:26 Info.plist

user@MacBook-Pro flexible-titlebar-demo % swift --version
swift-driver version: 1.75.2 Apple Swift version 5.9.2 (swiftlang-5.9.2.2.56 clang-1500.1.0.2.5)
Target: arm64-apple-macosx14.0

user@MacBook-Pro flexible-titlebar-demo % xcodebuild -version
Xcode 15.1
Build version 15C65

user@MacBook-Pro flexible-titlebar-demo % # Theme switching demo ready!
user@MacBook-Pro flexible-titlebar-demo % █"""

        terminal_text.insert("1.0", terminal_output)
        terminal_text.config(state="disabled")

    def _build_inspector_pane(self, parent: tk.Frame):
        """Build the inspector pane."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🔍 Inspector",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=(".AppleSystemUIFont", 12, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Inspector content
        content = tk.Frame(parent, bg=theme.primary_bg)
        content.pack(fill="both", expand=True, padx=5, pady=5)

        # Current theme info
        theme_info_frame = tk.LabelFrame(
            content,
            text="Current Theme",
            bg=theme.primary_bg,
            fg=theme.primary_text,
            font=(".AppleSystemUIFont", 11, "bold"),
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
            font=(".AppleSystemUIFont", 11),
        ).pack(anchor="w", padx=10, pady=2)

        tk.Label(
            theme_info_frame,
            text=f"Primary BG: {theme.primary_bg}",
            bg=theme.primary_bg,
            fg=theme.primary_text,
            font=(".AppleSystemUIFont", 11),
        ).pack(anchor="w", padx=10, pady=2)

        tk.Label(
            theme_info_frame,
            text=f"Accent Color: {theme.accent_text}",
            bg=theme.primary_bg,
            fg=theme.primary_text,
            font=(".AppleSystemUIFont", 11),
        ).pack(anchor="w", padx=10, pady=2)

        # macOS system info
        system_info_frame = tk.LabelFrame(
            content,
            text="System Information",
            bg=theme.primary_bg,
            fg=theme.primary_text,
            font=(".AppleSystemUIFont", 11, "bold"),
        )
        system_info_frame.pack(fill="x", pady=5)

        system_properties = [
            ("macOS", f"{platform.mac_ver()[0]}"),
            ("Architecture", platform.architecture()[0]),
            ("Processor", platform.processor() or "Apple Silicon"),
            ("Python", platform.python_version()),
            ("Retina", "Supported"),
        ]

        for prop, value in system_properties:
            prop_frame = tk.Frame(system_info_frame, bg=theme.primary_bg)
            prop_frame.pack(fill="x", padx=10, pady=1)

            tk.Label(
                prop_frame,
                text=f"{prop}:",
                bg=theme.primary_bg,
                fg=theme.secondary_text,
                font=(".AppleSystemUIFont", 11),
                width=12,
                anchor="w",
            ).pack(side="left")

            tk.Label(
                prop_frame,
                text=value,
                bg=theme.primary_bg,
                fg=theme.primary_text,
                font=(".AppleSystemUIFont", 11),
                anchor="w",
            ).pack(side="left", fill="x", expand=True)

    def _build_utilities_pane(self, parent: tk.Frame):
        """Build the utilities pane."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🛠️ Utilities",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=(".AppleSystemUIFont", 12, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Utilities content
        content = tk.Frame(parent, bg=theme.primary_bg)
        content.pack(fill="both", expand=True, padx=5, pady=5)

        # Interface Builder-style utilities
        categories = [
            (
                "Object Library",
                ["🔘 Button", "📝 Text Field", "🏷️ Label", "🖼️ Image View"],
            ),
            ("Media Library", ["🖼️ Images", "🎵 Audio", "🎬 Video", "📄 Documents"]),
            (
                "Code Snippets",
                ["🔄 For Loop", "🔀 If Statement", "🏗️ Class Template", "🔧 Function"],
            ),
            (
                "File Templates",
                ["📄 Swift File", "🖼️ Storyboard", "⚙️ Settings Bundle", "📱 App Icon"],
            ),
        ]

        for category, items in categories:
            cat_frame = tk.LabelFrame(
                content,
                text=category,
                bg=theme.primary_bg,
                fg=theme.primary_text,
                font=(".AppleSystemUIFont", 10, "bold"),
            )
            cat_frame.pack(fill="x", pady=2)

            for item in items:
                item_btn = tk.Button(
                    cat_frame,
                    text=item,
                    bg=theme.button_bg,
                    fg=theme.button_text,
                    activebackground=theme.button_hover,
                    relief="flat",
                    anchor="w",
                    padx=10,
                    command=lambda i=item: self._show_info(f"Selected: {i}"),
                )
                item_btn.pack(fill="x", padx=5, pady=1)

    def _build_debug_area_pane(self, parent: tk.Frame):
        """Build the debug area pane."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🐛 Debug Area",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=(".AppleSystemUIFont", 12, "bold"),
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
            font=("Menlo", 10),
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
        debug_output = """2024-01-15 14:30:15.123 MyMacApp[1234:567890] [DEBUG] Application launched
2024-01-15 14:30:15.124 MyMacApp[1234:567890] [INFO] Theme manager initialized
2024-01-15 14:30:15.125 MyMacApp[1234:567890] [DEBUG] Available themes: 7
2024-01-15 14:30:15.126 MyMacApp[1234:567890] [INFO] Custom titlebar created
2024-01-15 14:30:15.127 MyMacApp[1234:567890] [DEBUG] Layout configuration loaded
2024-01-15 14:30:15.128 MyMacApp[1234:567890] [INFO] Flexible layout initialized
2024-01-15 14:30:15.129 MyMacApp[1234:567890] [DEBUG] All panes created successfully
2024-01-15 14:30:15.130 MyMacApp[1234:567890] [INFO] Demo ready for interaction
2024-01-15 14:30:15.131 MyMacApp[1234:567890] [DEBUG] Waiting for user input..."""

        debug_text.config(state="normal")
        debug_text.insert("1.0", debug_output)
        debug_text.config(state="disabled")

    def _build_report_navigator_pane(self, parent: tk.Frame):
        """Build the report navigator pane."""
        theme = self.theme_manager.get_current_theme()

        # Header
        header = tk.Frame(parent, bg=theme.panel_header_bg, height=30)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📊 Report Navigator",
            bg=theme.panel_header_bg,
            fg=theme.panel_header_text,
            font=(".AppleSystemUIFont", 12, "bold"),
        ).pack(side="left", padx=10, pady=5)

        # Report content
        content = tk.Frame(parent, bg=theme.primary_bg)
        content.pack(fill="both", expand=True, padx=2, pady=2)

        # Create treeview for build reports
        report_tree = ttk.Treeview(content, show="tree", height=10)
        report_scrollbar = ttk.Scrollbar(
            content, orient="vertical", command=report_tree.yview
        )
        report_tree.configure(yscrollcommand=report_scrollbar.set)

        report_tree.pack(side="left", fill="both", expand=True)
        report_scrollbar.pack(side="right", fill="y")

        # Sample build reports
        today = report_tree.insert("", "end", text="📅 Today", open=True)
        report_tree.insert(today, "end", text="✅ Build Succeeded - 2:30 PM")
        report_tree.insert(today, "end", text="✅ Build Succeeded - 2:15 PM")
        report_tree.insert(today, "end", text="⚠️ Build with Warnings - 1:45 PM")

        yesterday = report_tree.insert("", "end", text="📅 Yesterday", open=False)
        report_tree.insert(yesterday, "end", text="✅ Build Succeeded - 5:20 PM")
        report_tree.insert(yesterday, "end", text="❌ Build Failed - 4:30 PM")
        report_tree.insert(yesterday, "end", text="✅ Build Succeeded - 3:15 PM")

        this_week = report_tree.insert("", "end", text="📅 This Week", open=False)
        report_tree.insert(this_week, "end", text="📊 Performance Tests")
        report_tree.insert(this_week, "end", text="🧪 Unit Tests")
        report_tree.insert(this_week, "end", text="🔍 Static Analysis")

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
                    "font": (".AppleSystemUIFont", 13),
                    "height": 28,
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
        theme_info = f"""Available Themes in macOS Flexible Titlebar Demo:

🎨 Theme Options:
• ☀️ Light Theme - Clean and bright interface
• 🌙 Dark Theme - Easy on the eyes for long coding sessions
• 💙 Blue Professional - Corporate and professional look
• 💚 Green Nature - Calming and natural colors
• 💜 Purple Elegance - Sophisticated and modern
• 🖥️ System Theme - Follows your macOS system theme
• 🏠 Native Theme - Uses macOS-native colors

🔧 Current Theme: {getattr(self.theme_manager.current_theme, 'value', 'unknown').title()}

💡 macOS Features:
• All themes work with custom titlebars
• Detached panes maintain theme consistency
• Real-time theme switching without restart
• macOS-optimized styling and fonts (SF Pro, Menlo)
• System theme integration
• Retina display optimization

🖱️ How to Switch:
• Use the 🎨 Themes menu in the titlebar
• All UI elements update automatically
• Detached windows update in real-time"""

        messagebox.showinfo("Theme Information", theme_info)

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
            print("\n🚀 Starting macOS Flexible Titlebar Demo...")
            print("Features:")
            print("• Flexible layout with 6 detachable panes")
            print("• macOS-style custom titlebar with theme switching menu")
            print("• All available themes supported")
            print("• macOS-optimized styling (SF Pro, Menlo fonts)")
            print("• Professional detached window management")
            print("• Xcode-inspired layout and controls")
            print("• Retina display optimization")
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
    print("macOS Flexible Layout + Custom Titlebar Demo")
    print("=" * 50)

    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Error: Python 3.8 or higher is required")
        print(f"Current version: {platform.python_version()}")
        return 1

    # Check platform
    current_os = platform.system()
    print(f"Platform: {current_os}")

    if current_os != "Darwin":
        print(f"⚠️ Warning: This demo is optimized for macOS systems.")
        print("Some features may not work as expected on other platforms.")
        print()

    try:
        # Create and run the demo
        demo = MacOSFlexibleTitlebarDemo()
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
