#!/usr/bin/env python3
"""
VM-Safe Linux Demo: Flexible Layout with Safe Custom Titlebar

This demo is specifically designed to work in virtual machines (VirtualBox, VMware, etc.)
on Linux systems like Pop!_OS. It avoids problematic X11 Motif hints that can cause
segmentation faults in VM environments.

Features:
- Flexible layout system with complex nested layouts
- VM-safe custom titlebar implementation
- Complete theme switching through all available themes
- Linux-optimized styling and behavior
- Professional detached window management
- No X11 low-level calls that cause segfaults in VMs

Usage:
    python3 linux_vm_safe_demo.py

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

    print("✓ Successfully imported threepanewindows modules")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Please ensure you're running this from the project root directory")
    print("and that the threepanewindows package is properly installed")
    sys.exit(1)

# Initialize logger
logger = get_logger(__name__)


class VMSafeCustomTitleBar:
    """
    VM-safe custom titlebar that uses pure Tkinter without X11 calls.
    
    This implementation uses overrideredirect(True) but with special handling
    to maintain window manager integration where possible.
    """
    
    def __init__(self, window: tk.Tk, theme: Dict[str, Any], title: str = ""):
        self.window = window
        self.theme = theme
        self.title = title or window.title()
        self.titlebar_frame = None
        self.title_label = None
        self.is_maximized = False
        self.normal_geometry = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # VM detection
        self.is_vm = self._detect_vm_environment()
        if self.is_vm:
            print("🖥️ Virtual machine detected - using VM-safe titlebar mode")
        
    def _detect_vm_environment(self) -> bool:
        """Detect if running in a virtual machine."""
        try:
            # Check for common VM indicators
            vm_indicators = [
                # VirtualBox
                "VirtualBox",
                "vboxguest",
                "vboxsf",
                # VMware
                "VMware",
                "vmware",
                "vmxnet",
                # QEMU/KVM
                "QEMU",
                "qemu",
                "virtio",
                # Hyper-V
                "Microsoft Corporation",
                "Hyper-V",
            ]
            
            # Check DMI information
            try:
                with open("/sys/class/dmi/id/sys_vendor", "r") as f:
                    vendor = f.read().strip()
                    if any(indicator in vendor for indicator in vm_indicators):
                        return True
            except:
                pass
                
            try:
                with open("/sys/class/dmi/id/product_name", "r") as f:
                    product = f.read().strip()
                    if any(indicator in product for indicator in vm_indicators):
                        return True
            except:
                pass
            
            # Check for VM-specific modules
            try:
                with open("/proc/modules", "r") as f:
                    modules = f.read()
                    if any(indicator in modules for indicator in vm_indicators):
                        return True
            except:
                pass
                
            return False
            
        except Exception:
            # If we can't detect, assume VM for safety
            return True
    
    def create_titlebar(self) -> Optional[tk.Frame]:
        """Create VM-safe custom titlebar."""
        try:
            if self.is_vm:
                # In VM: Use a simple themed frame without overrideredirect
                return self._create_simple_titlebar()
            else:
                # On bare metal: Can try more advanced features
                return self._create_advanced_titlebar()
                
        except Exception as e:
            logger.error(f"Failed to create titlebar: {e}")
            return self._create_fallback_titlebar()
    
    def _create_simple_titlebar(self) -> tk.Frame:
        """Create simple titlebar safe for VMs."""
        # Create titlebar frame at the top
        self.titlebar_frame = tk.Frame(
            self.window,
            bg=self.theme.get("bg", "#2b2b2b"),
            height=32,
            relief="flat"
        )
        self.titlebar_frame.pack(side="top", fill="x")
        self.titlebar_frame.pack_propagate(False)
        
        # Title label
        self.title_label = tk.Label(
            self.titlebar_frame,
            text=self.title,
            bg=self.theme.get("bg", "#2b2b2b"),
            fg=self.theme.get("fg", "#ffffff"),
            font=self.theme.get("font", ("Ubuntu", 11)),
            anchor="w"
        )
        self.title_label.pack(side="left", padx=10, pady=6, fill="x", expand=True)
        
        # Add window controls (minimize, maximize, close)
        self._add_window_controls()
        
        # Make titlebar draggable
        self._make_draggable()
        
        return self.titlebar_frame
    
    def _create_advanced_titlebar(self) -> tk.Frame:
        """Create advanced titlebar for bare metal systems."""
        # For now, use the same as simple - can be enhanced later
        return self._create_simple_titlebar()
    
    def _create_fallback_titlebar(self) -> tk.Frame:
        """Create minimal fallback titlebar."""
        self.titlebar_frame = tk.Frame(
            self.window,
            bg="#333333",
            height=28
        )
        self.titlebar_frame.pack(side="top", fill="x")
        
        tk.Label(
            self.titlebar_frame,
            text=self.title,
            bg="#333333",
            fg="#ffffff",
            font=("Arial", 10)
        ).pack(side="left", padx=5, pady=4)
        
        return self.titlebar_frame
    
    def _add_window_controls(self):
        """Add minimize, maximize, close buttons."""
        controls_frame = tk.Frame(
            self.titlebar_frame,
            bg=self.theme.get("bg", "#2b2b2b")
        )
        controls_frame.pack(side="right", padx=5)
        
        # Close button
        close_btn = tk.Button(
            controls_frame,
            text="✕",
            bg=self.theme.get("btn_bg", "#404040"),
            fg=self.theme.get("btn_fg", "#ffffff"),
            activebackground="#e74c3c",
            activeforeground="#ffffff",
            relief="flat",
            borderwidth=0,
            width=3,
            height=1,
            font=("Arial", 10),
            command=self.window.quit
        )
        close_btn.pack(side="right", padx=1)
        
        # Maximize button
        max_btn = tk.Button(
            controls_frame,
            text="□",
            bg=self.theme.get("btn_bg", "#404040"),
            fg=self.theme.get("btn_fg", "#ffffff"),
            activebackground=self.theme.get("btn_active_bg", "#505050"),
            activeforeground="#ffffff",
            relief="flat",
            borderwidth=0,
            width=3,
            height=1,
            font=("Arial", 10),
            command=self._toggle_maximize
        )
        max_btn.pack(side="right", padx=1)
        
        # Minimize button
        min_btn = tk.Button(
            controls_frame,
            text="−",
            bg=self.theme.get("btn_bg", "#404040"),
            fg=self.theme.get("btn_fg", "#ffffff"),
            activebackground=self.theme.get("btn_active_bg", "#505050"),
            activeforeground="#ffffff",
            relief="flat",
            borderwidth=0,
            width=3,
            height=1,
            font=("Arial", 10),
            command=self._minimize_window
        )
        min_btn.pack(side="right", padx=1)
    
    def _make_draggable(self):
        """Make the titlebar draggable."""
        def start_drag(event):
            self.drag_start_x = event.x_root
            self.drag_start_y = event.y_root
        
        def do_drag(event):
            if not self.is_maximized:
                x = self.window.winfo_x() + (event.x_root - self.drag_start_x)
                y = self.window.winfo_y() + (event.y_root - self.drag_start_y)
                self.window.geometry(f"+{x}+{y}")
                self.drag_start_x = event.x_root
                self.drag_start_y = event.y_root
        
        # Bind drag events to titlebar and title label
        for widget in [self.titlebar_frame, self.title_label]:
            widget.bind("<Button-1>", start_drag)
            widget.bind("<B1-Motion>", do_drag)
            widget.bind("<Double-Button-1>", lambda e: self._toggle_maximize())
    
    def _toggle_maximize(self):
        """Toggle window maximize state."""
        if self.is_maximized:
            if self.normal_geometry:
                self.window.geometry(self.normal_geometry)
            self.is_maximized = False
        else:
            self.normal_geometry = self.window.geometry()
            self.window.state('zoomed')  # Cross-platform maximize
            self.is_maximized = True
    
    def _minimize_window(self):
        """Minimize the window."""
        self.window.iconify()
    
    def apply_theme(self, theme: Dict[str, Any]):
        """Apply new theme to titlebar."""
        self.theme = theme
        if self.titlebar_frame:
            self.titlebar_frame.config(bg=theme.get("bg", "#2b2b2b"))
        if self.title_label:
            self.title_label.config(
                bg=theme.get("bg", "#2b2b2b"),
                fg=theme.get("fg", "#ffffff")
            )


class LinuxVMSafeDemo:
    """
    VM-safe Linux demo showcasing flexible layout with safe custom titlebar.
    Designed specifically to work in virtual machine environments.
    """

    def __init__(self):
        """Initialize the VM-safe demo application."""
        print("\n" + "=" * 60)
        print("Linux VM-Safe Flexible Layout Demo")
        print("=" * 60)

        # Detect platform and VM
        self.platform_name = platform.system()
        self.is_linux = self.platform_name.lower() == "linux"

        print(f"Platform detected: {self.platform_name}")
        print(f"Linux optimizations: {'Enabled' if self.is_linux else 'Disabled'}")

        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Linux VM-Safe Flexible Layout Demo")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)

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

        print("✓ VM-safe demo initialization complete")

    def _detect_dark_mode(self) -> bool:
        """Detect if the system is using dark mode."""
        try:
            return platform_handler.is_dark_mode()
        except Exception:
            return False

    def _setup_custom_titlebar(self):
        """Setup VM-safe custom titlebar."""
        print("\nSetting up VM-safe custom titlebar...")

        try:
            theme = self.theme_manager.get_current_theme()

            # Convert theme to dictionary format expected by titlebar
            theme_dict = {
                "bg": theme.primary_bg,
                "fg": theme.primary_text,
                "btn_bg": theme.button_bg,
                "btn_fg": theme.button_text,
                "btn_active_bg": theme.button_hover,
                "font": ("Ubuntu", 11),
                "height": 32,
            }

            # Create VM-safe titlebar
            self.custom_titlebar = VMSafeCustomTitleBar(
                self.root,
                theme_dict,
                "Linux VM-Safe Flexible Layout Demo"
            )

            titlebar_frame = self.custom_titlebar.create_titlebar()
            if titlebar_frame:
                # Add theme switching menu to titlebar
                self._add_theme_menu_to_titlebar(titlebar_frame)
                print("✓ VM-safe custom titlebar created successfully")
            else:
                print("⚠ Custom titlebar frame not created, using menu bar")
                self._create_menu_bar()

        except Exception as e:
            print(f"✗ Error setting up custom titlebar: {e}")
            logger.error(f"Custom titlebar setup failed: {e}")
            # Fallback to menu bar
            self._create_menu_bar()

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
        """Create a menu bar for theme switching."""
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
        """Setup Linux-specific window properties."""
        try:
            theme = self.theme_manager.get_current_theme()

            # Set window background
            self.root.configure(bg=theme.primary_bg)

            # Linux-specific window properties
            if self.is_linux:
                # Set window class for better integration
                self.root.wm_class("VMSafeFlexibleDemo", "ThreePaneWindows")

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

        # Create a treeview for file explorer
        tree_frame = tk.Frame(parent, bg=theme.primary_bg)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Treeview
        tree = ttk.Treeview(tree_frame, show="tree headings", columns=("size",))
        tree.heading("#0", text="Name", anchor="w")
        tree.heading("size", text="Size", anchor="e")
        tree.column("#0", width=200)
        tree.column("size", width=80)

        # Add some sample items
        folders = tree.insert("", "end", text="📁 src", values=("",))
        tree.insert(folders, "end", text="📄 main.py", values=("2.1 KB",))
        tree.insert(folders, "end", text="📄 utils.py", values=("1.5 KB",))

        docs = tree.insert("", "end", text="📁 docs", values=("",))
        tree.insert(docs, "end", text="📄 README.md", values=("3.2 KB",))

        tree.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def _build_outline_pane(self, parent: tk.Frame):
        """Build the document outline pane."""
        theme = self.theme_manager.get_current_theme()

        outline_frame = tk.Frame(parent, bg=theme.primary_bg)
        outline_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Outline tree
        outline_tree = ttk.Treeview(outline_frame, show="tree")
        
        # Add sample outline items
        class_item = outline_tree.insert("", "end", text="🏛️ LinuxVMSafeDemo")
        outline_tree.insert(class_item, "end", text="🔧 __init__")
        outline_tree.insert(class_item, "end", text="🎨 _setup_custom_titlebar")
        outline_tree.insert(class_item, "end", text="📐 _setup_layout")
        outline_tree.insert(class_item, "end", text="▶️ run")

        outline_tree.pack(fill="both", expand=True)

    def _build_editor_pane(self, parent: tk.Frame):
        """Build the code editor pane."""
        theme = self.theme_manager.get_current_theme()

        editor_frame = tk.Frame(parent, bg=theme.primary_bg)
        editor_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Text editor
        text_editor = tk.Text(
            editor_frame,
            bg=theme.secondary_bg,
            fg=theme.primary_text,
            insertbackground=theme.primary_text,
            selectbackground=theme.accent_color,
            font=("Ubuntu Mono", 11),
            wrap="none"
        )

        # Sample code
        sample_code = '''#!/usr/bin/env python3
"""
VM-Safe Linux Demo
This demo works perfectly in virtual machines!
"""

import tkinter as tk
from threepanewindows import *

class VMSafeDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()
    
    def setup_ui(self):
        # VM-safe implementation
        print("Setting up VM-safe UI...")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    demo = VMSafeDemo()
    demo.run()
'''
        text_editor.insert("1.0", sample_code)
        text_editor.pack(fill="both", expand=True)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(editor_frame, orient="vertical", command=text_editor.yview)
        text_editor.configure(yscrollcommand=v_scrollbar.set)
        v_scrollbar.pack(side="right", fill="y")

        h_scrollbar = ttk.Scrollbar(editor_frame, orient="horizontal", command=text_editor.xview)
        text_editor.configure(xscrollcommand=h_scrollbar.set)
        h_scrollbar.pack(side="bottom", fill="x")

    def _build_terminal_pane(self, parent: tk.Frame):
        """Build the terminal pane."""
        theme = self.theme_manager.get_current_theme()

        terminal_frame = tk.Frame(parent, bg=theme.primary_bg)
        terminal_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Terminal text area
        terminal = tk.Text(
            terminal_frame,
            bg="#1e1e1e",
            fg="#00ff00",
            insertbackground="#00ff00",
            font=("Ubuntu Mono", 10),
            state="disabled"
        )

        # Sample terminal output
        terminal.config(state="normal")
        terminal.insert("end", "user@pop-os:~/projects/threepanewindows$ python3 linux_vm_safe_demo.py\n")
        terminal.insert("end", "✓ Successfully imported threepanewindows modules\n")
        terminal.insert("end", "Platform detected: Linux\n")
        terminal.insert("end", "🖥️ Virtual machine detected - using VM-safe titlebar mode\n")
        terminal.insert("end", "✓ VM-safe custom titlebar created successfully\n")
        terminal.insert("end", "✓ Flexible layout created successfully\n")
        terminal.insert("end", "🚀 Starting Linux VM-Safe Demo...\n")
        terminal.insert("end", "user@pop-os:~/projects/threepanewindows$ ")
        terminal.config(state="disabled")

        terminal.pack(fill="both", expand=True)

        # Scrollbar
        term_scrollbar = ttk.Scrollbar(terminal_frame, orient="vertical", command=terminal.yview)
        terminal.configure(yscrollcommand=term_scrollbar.set)
        term_scrollbar.pack(side="right", fill="y")

    def _build_properties_pane(self, parent: tk.Frame):
        """Build the properties pane."""
        theme = self.theme_manager.get_current_theme()

        props_frame = tk.Frame(parent, bg=theme.primary_bg)
        props_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Properties list
        props_text = tk.Text(
            props_frame,
            bg=theme.secondary_bg,
            fg=theme.primary_text,
            font=("Ubuntu", 10),
            height=10,
            state="disabled"
        )

        props_text.config(state="normal")
        props_text.insert("end", "🖥️ System Properties\n")
        props_text.insert("end", "=" * 20 + "\n")
        props_text.insert("end", f"Platform: {platform.system()}\n")
        props_text.insert("end", f"Python: {platform.python_version()}\n")
        props_text.insert("end", f"Architecture: {platform.machine()}\n")
        props_text.insert("end", "\n🎨 Theme Properties\n")
        props_text.insert("end", "=" * 20 + "\n")
        props_text.insert("end", f"Current Theme: {self.theme_manager.current_theme.value}\n")
        props_text.insert("end", f"Available Themes: {len(self.available_themes)}\n")
        props_text.insert("end", f"VM-Safe Mode: Enabled\n")
        props_text.config(state="disabled")

        props_text.pack(fill="both", expand=True)

    def _build_debug_pane(self, parent: tk.Frame):
        """Build the debug console pane."""
        theme = self.theme_manager.get_current_theme()

        debug_frame = tk.Frame(parent, bg=theme.primary_bg)
        debug_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Debug console
        debug_console = tk.Text(
            debug_frame,
            bg="#2d1b69",
            fg="#ffffff",
            insertbackground="#ffffff",
            font=("Ubuntu Mono", 9),
            height=8,
            state="disabled"
        )

        debug_console.config(state="normal")
        debug_console.insert("end", "[DEBUG] VM-Safe Demo initialized\n")
        debug_console.insert("end", "[INFO] Custom titlebar: VM-safe mode\n")
        debug_console.insert("end", "[INFO] X11 Motif hints: Disabled (VM-safe)\n")
        debug_console.insert("end", "[INFO] Layout: 6 panes configured\n")
        debug_console.insert("end", "[INFO] Theme system: Active\n")
        debug_console.insert("end", "[DEBUG] All systems operational\n")
        debug_console.config(state="disabled")

        debug_console.pack(fill="both", expand=True)

    def _build_output_pane(self, parent: tk.Frame):
        """Build the output pane."""
        theme = self.theme_manager.get_current_theme()

        output_frame = tk.Frame(parent, bg=theme.primary_bg)
        output_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Output text area
        output_text = tk.Text(
            output_frame,
            bg=theme.secondary_bg,
            fg=theme.primary_text,
            font=("Ubuntu Mono", 10),
            height=6,
            state="disabled"
        )

        output_text.config(state="normal")
        output_text.insert("end", "📤 Application Output\n")
        output_text.insert("end", "=" * 25 + "\n")
        output_text.insert("end", "✓ VM-safe demo started successfully\n")
        output_text.insert("end", "✓ All panes loaded without errors\n")
        output_text.insert("end", "✓ Theme switching enabled\n")
        output_text.insert("end", "✓ Detachable panes ready\n")
        output_text.insert("end", "\n💡 Try switching themes and detaching panes!\n")
        output_text.config(state="disabled")

        output_text.pack(fill="both", expand=True)

    def _switch_theme(self, theme_name: str):
        """Switch to a different theme."""
        try:
            print(f"🎨 Switching to theme: {theme_name}")
            set_global_theme(theme_name)
            
            # Update custom titlebar
            if self.custom_titlebar:
                theme = self.theme_manager.get_current_theme()
                theme_dict = {
                    "bg": theme.primary_bg,
                    "fg": theme.primary_text,
                    "btn_bg": theme.button_bg,
                    "btn_fg": theme.button_text,
                    "btn_active_bg": theme.button_hover,
                    "font": ("Ubuntu", 11),
                }
                self.custom_titlebar.apply_theme(theme_dict)
            
            # Update layout theme
            if self.layout:
                self.layout.apply_theme(theme_name)
            
            # Update window background
            theme = self.theme_manager.get_current_theme()
            self.root.configure(bg=theme.primary_bg)
            
            print(f"✓ Theme switched to: {theme_name}")
            
        except Exception as e:
            print(f"✗ Error switching theme: {e}")
            logger.error(f"Theme switching failed: {e}")

    def _show_theme_info(self):
        """Show information about available themes."""
        theme_info = f"""VM-Safe Demo Theme Information

Available Themes: {len(self.available_themes)}
Current Theme: {self.theme_manager.current_theme.value}

Theme List:
{chr(10).join(f"• {theme}" for theme in self.available_themes)}

VM-Safe Features:
• No X11 Motif hints (prevents segfaults)
• Pure Tkinter implementation
• Full theme switching support
• Works in all VM environments
"""
        messagebox.showinfo("Theme Information", theme_info)

    def _show_about(self):
        """Show about dialog."""
        about_text = """Linux VM-Safe Flexible Layout Demo

This demo is specifically designed to work safely in virtual machine 
environments like VirtualBox, VMware, and QEMU/KVM on Linux systems.

Features:
• VM-safe custom titlebar (no X11 low-level calls)
• Flexible layout with 6 detachable panes
• Complete theme switching system
• Professional UI components
• Cross-platform compatibility

Perfect for testing ThreePaneWindows in:
• Pop!_OS VMs
• Ubuntu VMs  
• Any Linux distribution in a VM

No more segmentation faults!
"""
        messagebox.showinfo("About VM-Safe Demo", about_text)

    def _on_window_close(self):
        """Handle window close event."""
        try:
            print("\n👋 Closing VM-safe demo...")
            if self.layout:
                self.layout.cleanup()
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print(f"Error during cleanup: {e}")
            self.root.quit()

    def run(self):
        """Run the VM-safe demo application."""
        try:
            print("\n🚀 Starting Linux VM-Safe Demo...")
            print("Features:")
            print("• VM-safe flexible layout with 6 detachable panes")
            print("• Custom titlebar without X11 low-level calls")
            print("• All available themes supported")
            print("• Linux-optimized styling")
            print("• Professional detached window management")
            print("• No segmentation faults in VMs!")
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
            print("\n👋 VM-safe demo finished")


def main():
    """Main entry point for the VM-safe demo."""
    print("Linux VM-Safe Flexible Layout Demo")
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
        print("It will work on other platforms but some features may differ.")
        print()

    try:
        # Create and run the demo
        demo = LinuxVMSafeDemo()
        demo.run()

        print("\n✓ VM-safe demo completed successfully")
        return 0

    except ImportError as e:
        print(f"✗ Error importing demo modules: {e}")
        print()
        print("Troubleshooting:")
        print("1. Make sure you're running this from the project root directory")
        print("2. Ensure the threepanewindows package is properly installed:")
        print("   pip install -e .")
        return 1

    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user (Ctrl+C)")
        return 0

    except Exception as e:
        print(f"✗ Error running demo: {e}")
        print()
        print("Debug information:")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())