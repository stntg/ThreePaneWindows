#!/usr/bin/env python3
"""
Professional Enhanced Layout Demo using Flexible Layout with Central Theme Manager

This example demonstrates how to create a professional IDE-like interface using
the flexible layout system with the modern central_theme_manager for consistent,
professional theming that matches the original themes.py styling.

Features demonstrated:
- Flexible layout with professional pane headers and detach buttons
- Central theme manager integration with matching themes.py colors
- Professional IDE-like interface with file explorer, editor, and tools
- Menu theming and window theming
- Consistent styling across all widgets and themes
- Custom control buttons with hover effects
"""

import os
import platform
import sys
import tkinter as tk
from tkinter import messagebox, ttk

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from threepanewindows.central_theme_manager import (  # create_themed_scrollbar_auto,
        CentralThemeManager,
        ThemeType,
        get_theme_manager,
    )
    from threepanewindows.flexible import (
        EnhancedFlexibleLayout,
        FlexContainer,
        FlexPaneConfig,
        LayoutDirection,
    )

    # We'll use the theme manager's scrollbar creation method
    print("✅ Successfully imported from threepanewindows package")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)


class ProfessionalEnhancedDemo:
    """Professional demo application showcasing FlexibleThreePaneLayout with central theme manager."""

    def __init__(self):
        """Initialize the demo application."""
        self.root = tk.Tk()
        self.root.title("Professional Enhanced Layout - Central Theme Manager Demo")
        self.root.geometry("1400x800")

        # Get the central theme manager instance
        self.theme_manager = get_theme_manager()
        print(
            f"🎨 Using central theme manager: {self.theme_manager.current_theme.value} {self.theme_manager.current_theme.name} {self.theme_manager}"
        )

        # Set initial theme
        self.theme_manager.set_theme(ThemeType.LIGHT)

        # Apply theme to root window
        self.theme_manager.apply_window_theme(self.root)

        # Create the flexible layout with professional panes
        self.create_layout()

        # Apply theme to all widgets after layout creation
        self.theme_manager.apply_theme_to_widget(self.root, recursive=True)

        # Create menu bar
        self.create_menu()

        # Create status bar
        self.create_status_bar()

        print("🚀 Professional Enhanced Demo initialized")
        print(f"📋 Current theme: {self.theme_manager.current_theme.value}")
        print("🎨 Available themes:", [t.value for t in ThemeType])
        print(
            f"💻 Platform: {platform.system()} - Using {'Custom' if platform.system() == 'Windows' else 'Native'} scrollbars"
        )

    def create_layout(self):
        """Create the flexible three-pane layout with professional content."""
        # Define pane configurations
        left_pane = FlexPaneConfig(
            name="explorer",
            title="🗂️ Project Explorer",
            weight=0.2,
            detachable=True,
            builder=self.build_left_panel,
        )

        center_pane = FlexPaneConfig(
            name="editor",
            title="📝 Code Editor",
            weight=0.6,
            detachable=False,  # Main editor shouldn't be detachable
            builder=self.build_center_panel,
        )

        right_pane = FlexPaneConfig(
            name="tools",
            title="🔧 Tools & Properties",
            weight=0.2,
            detachable=True,
            builder=self.build_right_panel,
        )

        # Create the layout container
        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL,
            children=[left_pane, center_pane, right_pane],
        )

        # Create the flexible layout - pass the current theme instead of overriding
        current_theme_name = self.theme_manager.current_theme.value
        self.layout = EnhancedFlexibleLayout(
            self.root, layout_config, theme_name=current_theme_name
        )

        self.layout.pack(fill="both", expand=True, padx=5, pady=5)

    def build_left_panel(self, parent):
        """Build the left panel content - Project Explorer."""
        # Main container
        main_frame = tk.Frame(parent)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Tree view simulation
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Create a listbox to simulate file tree
        self.file_list = tk.Listbox(
            tree_frame, font=("Consolas", 9), selectmode="single"
        )

        scrollbar = self.theme_manager.create_themed_scrollbar_auto(
            tree_frame, orient="vertical", command=self.file_list.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.file_list.config(yscrollcommand=scrollbar.set)

        # Add sample files
        files = [
            "📁 src/",
            "  📄 main.py",
            "  📄 utils.py",
            "  📄 config.py",
            "  📄 models.py",
            "📁 tests/",
            "  📄 test_main.py",
            "  📄 test_utils.py",
            "  📄 test_models.py",
            "📁 docs/",
            "  📄 README.md",
            "  📄 API.md",
            "  📄 CHANGELOG.md",
            "📁 assets/",
            "  🖼️ icon.png",
            "  🖼️ logo.svg",
            "  🎨 styles.css",
            "📁 config/",
            "  ⚙️ settings.json",
            "  🔧 database.yml",
            "📄 requirements.txt",
            "📄 setup.py",
            "📄 .gitignore",
            "📄 LICENSE",
        ]

        for file in files:
            self.file_list.insert(tk.END, file)

        self.file_list.pack(fill="both", expand=True)

        # Command is already set during scrollbar creation

        # Bind selection event
        self.file_list.bind("<<ListboxSelect>>", self.on_file_select)

        # Action buttons frame
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(fill="x", pady=(5, 0))

        # Action buttons
        btn_new = tk.Button(
            buttons_frame, text="📄 New", command=self.new_file, width=8
        )
        btn_new.pack(side="left", padx=(0, 5))

        btn_open = tk.Button(
            buttons_frame, text="📂 Open", command=self.open_file, width=8
        )
        btn_open.pack(side="left", padx=(0, 5))

        btn_refresh = tk.Button(
            buttons_frame, text="🔄 Refresh", command=self.refresh_files, width=8
        )
        btn_refresh.pack(side="left")

    def build_center_panel(self, parent):
        """Build the center panel content - Code Editor."""
        # Main container
        main_frame = tk.Frame(parent)
        main_frame.pack(fill="both", expand=True)

        # Tab bar simulation
        tab_frame = tk.Frame(main_frame)
        tab_frame.pack(fill="x", padx=5, pady=(5, 0))

        # Create tab buttons
        self.tabs = ["main.py", "utils.py", "config.py", "models.py"]
        self.active_tab = 0
        self.tab_buttons = []

        for i, tab in enumerate(self.tabs):
            btn = tk.Button(
                tab_frame,
                text=f"📄 {tab}",
                command=lambda idx=i: self.switch_tab(idx),
                relief="flat" if i == self.active_tab else "raised",
                font=("Segoe UI", 9),
                padx=10,
            )
            btn.pack(side="left", padx=(0, 2))
            self.tab_buttons.append(btn)

        # Tab controls
        controls_frame = tk.Frame(tab_frame)
        controls_frame.pack(side="right")

        close_btn = tk.Button(
            controls_frame,
            text="✕",
            command=self.close_tab,
            width=3,
            font=("Segoe UI", 8),
        )
        close_btn.pack(side="right", padx=(5, 0))

        # Editor container
        editor_container = tk.Frame(main_frame)
        editor_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Editor area with line numbers
        editor_frame = tk.Frame(editor_container)
        editor_frame.pack(fill="both", expand=True)

        # Line numbers frame
        line_frame = tk.Frame(editor_frame, width=50)
        line_frame.pack(side="left", fill="y")
        line_frame.pack_propagate(False)

        # Line numbers
        self.line_numbers = tk.Text(
            line_frame,
            width=4,
            font=("Consolas", 10),
            state="disabled",
            wrap="none",
            padx=5,
        )
        self.line_numbers.pack(fill="both", expand=True)

        # Text editor with scrollbars
        text_frame = tk.Frame(editor_frame)
        text_frame.pack(side="right", fill="both", expand=True)

        # Text editor
        self.text_editor = tk.Text(
            text_frame,
            font=("Consolas", 10),
            wrap="none",
            undo=True,
            maxundo=50,
            padx=5,
            pady=5,
        )

        # Theme-managed scrollbars with commands
        v_scrollbar = self.theme_manager.create_themed_scrollbar_auto(
            text_frame, orient="vertical", command=self.text_editor.yview
        )
        v_scrollbar.pack(side="right", fill="y")

        h_scrollbar = self.theme_manager.create_themed_scrollbar_auto(
            text_frame, orient="horizontal", command=self.text_editor.xview
        )
        h_scrollbar.pack(side="bottom", fill="x")

        # Connect text widget to scrollbars
        self.text_editor.config(
            yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set
        )

        # Sample code content with syntax highlighting simulation
        sample_code = '''#!/usr/bin/env python3
"""
Professional Enhanced Layout Demo
Central Theme Manager Integration Example
"""

import tkinter as tk
from threepanewindows.flexible import EnhancedFlexibleLayout, FlexPaneConfig
from threepanewindows.central_theme_manager import get_theme_manager, ThemeType

class ProfessionalApplication:
    """A professional application with modern theming."""

    def __init__(self):
        """Initialize the application."""
        self.root = tk.Tk()
        self.root.title("Professional Application")
        self.root.geometry("1200x800")

        # Get central theme manager
        self.theme_manager = get_theme_manager()
        self.theme_manager.set_theme(ThemeType.LIGHT)

        # Apply professional theming
        self.theme_manager.apply_window_theme(self.root)

        # Create layout
        self.create_layout()

        print("🚀 Professional application initialized!")

    def create_layout(self):
        """Create the main layout."""
        # Define panes
        left_pane = FlexPaneConfig(
            name="sidebar",
            title="📁 Sidebar",
            weight=0.25,
            detachable=True,
            builder=self.build_sidebar
        )

        center_pane = FlexPaneConfig(
            name="main",
            title="📝 Main Content",
            weight=0.75,
            detachable=False,
            builder=self.build_main_content
        )

        # Create flexible layout
        self.layout = EnhancedFlexibleLayout(
            self.root,
            panes=[left_pane, center_pane]
        )
        self.layout.pack(fill="both", expand=True)

    def build_sidebar(self, parent):
        """Build sidebar content."""
        label = tk.Label(
            parent,
            text="Sidebar Content\\nWith Professional Theming",
            justify="center"
        )
        label.pack(fill="both", expand=True, padx=10, pady=10)

    def build_main_content(self, parent):
        """Build main content."""
        label = tk.Label(
            parent,
            text="Main Content Area\\nProfessional Layout System",
            justify="center"
        )
        label.pack(fill="both", expand=True, padx=10, pady=10)

    def run(self):
        """Run the application."""
        self.root.mainloop()

def main():
    """Main entry point."""
    app = ProfessionalApplication()
    app.run()

if __name__ == "__main__":
    main()
'''

        self.text_editor.insert("1.0", sample_code)
        self.text_editor.pack(fill="both", expand=True)

        # Commands are already set during scrollbar creation

        # Update line numbers
        self.update_line_numbers()
        self.text_editor.bind("<KeyRelease>", lambda e: self.update_line_numbers())
        self.text_editor.bind(
            "<Button-1>", lambda e: self.root.after(10, self.update_cursor_position)
        )

        # Status line
        status_frame = tk.Frame(main_frame)
        status_frame.pack(fill="x", padx=5, pady=(0, 5))

        self.editor_status = tk.Label(
            status_frame,
            text="Line 1, Column 1 | Python | UTF-8 | Spaces: 4 | Professional Theme",
            font=("Segoe UI", 8),
            anchor="w",
        )
        self.editor_status.pack(fill="x")

    def build_right_panel(self, parent):
        """Build the right panel content - Tools & Properties."""
        # Create notebook for multiple tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Properties tab
        self.create_properties_tab(notebook)

        # Output tab
        self.create_output_tab(notebook)

        # Tools tab
        self.create_tools_tab(notebook)

        # Debug tab
        self.create_debug_tab(notebook)

    def create_properties_tab(self, notebook):
        """Create the properties tab."""
        props_frame = tk.Frame(notebook)
        notebook.add(props_frame, text="🔧 Properties")

        # Properties content
        props_label = tk.Label(
            props_frame,
            text="📋 File Properties",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        )
        props_label.pack(fill="x", padx=10, pady=(10, 5))

        # Property entries
        props_data = [
            ("Name:", "main.py"),
            ("Size:", "3.2 KB"),
            ("Type:", "Python File"),
            ("Modified:", "2024-01-15 16:45"),
            ("Encoding:", "UTF-8"),
            ("Lines:", "67"),
            ("Language:", "Python 3.11"),
            ("Theme:", "Professional Light"),
            ("Status:", "Modified"),
        ]

        for label, value in props_data:
            prop_frame = tk.Frame(props_frame)
            prop_frame.pack(fill="x", padx=10, pady=2)

            tk.Label(
                prop_frame,
                text=label,
                font=("Segoe UI", 9, "bold"),
                width=12,
                anchor="w",
            ).pack(side="left")

            tk.Label(prop_frame, text=value, font=("Segoe UI", 9), anchor="w").pack(
                side="left", fill="x", expand=True
            )

    def create_output_tab(self, notebook):
        """Create the output tab."""
        output_frame = tk.Frame(notebook)
        notebook.add(output_frame, text="📤 Output")

        # Output content
        output_label = tk.Label(
            output_frame,
            text="🖥️ Console Output",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        )
        output_label.pack(fill="x", padx=10, pady=(10, 5))

        # Console output
        console_frame = tk.Frame(output_frame)
        console_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.console_output = tk.Text(
            console_frame, font=("Consolas", 9), state="disabled", wrap="word"
        )

        console_scroll = self.theme_manager.create_themed_scrollbar_auto(
            console_frame, orient="vertical", command=self.console_output.yview
        )
        console_scroll.pack(side="right", fill="y")
        self.console_output.config(yscrollcommand=console_scroll.set)

        # Sample output
        sample_output = """🚀 Professional Enhanced Demo started
📦 Loading modules...
✅ Central theme manager initialized
🎨 Theme set to: light
📋 Available themes: ['light', 'dark', 'blue', 'green', 'purple']
✅ Flexible layout created with professional styling
🔧 All components initialized successfully
⚡ Ready for professional development

> python main.py
Professional Enhanced Layout Demo
Central Theme Manager Integration Example
🚀 Professional application initialized!

> python -m pytest tests/ -v
========================= test session starts =========================
platform win32 -- Python 3.11.0
collected 15 items

tests/test_main.py::test_application_init PASSED        [ 6%]
tests/test_main.py::test_theme_manager PASSED           [13%]
tests/test_main.py::test_layout_creation PASSED         [20%]
tests/test_utils.py::test_file_operations PASSED        [26%]
tests/test_utils.py::test_theme_switching PASSED        [33%]
tests/test_models.py::test_data_models PASSED           [40%]
tests/test_models.py::test_validation PASSED            [46%]

========================= 15 passed in 0.67s =========================

✅ All tests passed with professional theming!
"""

        self.console_output.config(state="normal")
        self.console_output.insert("1.0", sample_output)
        self.console_output.config(state="disabled")
        self.console_output.pack(fill="both", expand=True)

        # Command is already set during scrollbar creation

    def create_tools_tab(self, notebook):
        """Create the tools tab."""
        tools_frame = tk.Frame(notebook)
        notebook.add(tools_frame, text="🛠️ Tools")

        # Tools content
        tools_label = tk.Label(
            tools_frame,
            text="🔨 Development Tools",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        )
        tools_label.pack(fill="x", padx=10, pady=(10, 5))

        # Tool buttons
        tools = [
            ("🔍 Find & Replace", self.find_replace),
            ("📊 Code Analysis", self.code_analysis),
            ("🧪 Run Tests", self.run_tests),
            ("📦 Build Project", self.build_project),
            ("🚀 Deploy", self.deploy),
            ("🎨 Theme Editor", self.theme_editor),
            ("🔧 Settings", self.show_settings),
            ("📋 Clipboard History", self.clipboard_history),
        ]

        for tool_name, command in tools:
            btn = tk.Button(
                tools_frame,
                text=tool_name,
                command=command,
                anchor="w",
                font=("Segoe UI", 9),
                padx=10,
            )
            btn.pack(fill="x", padx=10, pady=2)

    def create_debug_tab(self, notebook):
        """Create the debug tab."""
        debug_frame = tk.Frame(notebook)
        notebook.add(debug_frame, text="🐛 Debug")

        # Debug content
        debug_label = tk.Label(
            debug_frame,
            text="🐛 Debug Information",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        )
        debug_label.pack(fill="x", padx=10, pady=(10, 5))

        # Debug info
        debug_info = tk.Text(debug_frame, font=("Consolas", 9), wrap="word", height=10)
        debug_info.pack(fill="both", expand=True, padx=10, pady=5)

        debug_content = f"""Theme Manager Status:
✅ Central Theme Manager Active
🎨 Current Theme: {self.theme_manager.current_theme.value}
📋 Available Themes: {len([t for t in ThemeType])} themes
🔧 Professional Styling: Enabled
🎨 Themed Widget Types: {len(self.theme_manager.get_themed_widget_types())} types

Layout Information:
📐 Layout Type: EnhancedFlexibleLayout
🗂️ Left Pane: Project Explorer (Detachable)
📝 Center Pane: Code Editor (Fixed)
🔧 Right Pane: Tools & Properties (Detachable)

System Information:
💻 Platform: {platform.system()} ({sys.platform})
🐍 Python: {sys.version.split()[0]}
🖼️ Tkinter: Available
📜 Scrollbars: {'Custom ThemedScrollbar' if platform.system() == 'Windows' else 'Native Scrollbar'}
🎨 Theme Colors: Matching themes.py
🔧 Widget Coverage: Complete (All Tk/TTK widgets supported)

Platform Features:
{'✅ Custom scrollbars for better theming' if platform.system() == 'Windows' else '✅ Native scrollbars for system integration'}
✅ Professional pane headers with detach buttons
✅ Custom control buttons with hover effects
✅ Comprehensive widget theming (Tk + TTK)
✅ Menu and window theming
✅ Theme conflict prevention
"""

        debug_info.insert("1.0", debug_content)
        debug_info.config(state="disabled")

    def create_menu(self):
        """Create the application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(
            label="New File", command=self.new_file, accelerator="Ctrl+N"
        )
        file_menu.add_command(
            label="Open...", command=self.open_file, accelerator="Ctrl+O"
        )
        file_menu.add_command(
            label="Save", command=self.save_file, accelerator="Ctrl+S"
        )
        file_menu.add_command(
            label="Save As...", command=self.save_as, accelerator="Ctrl+Shift+S"
        )
        file_menu.add_separator()
        file_menu.add_command(label="Recent Files", command=self.recent_files)
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit", command=self.root.quit, accelerator="Ctrl+Q"
        )

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Select All", command=self.select_all, accelerator="Ctrl+A"
        )
        edit_menu.add_command(
            label="Find & Replace", command=self.find_replace, accelerator="Ctrl+H"
        )

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Explorer", command=self.toggle_explorer)
        view_menu.add_command(label="Toggle Tools", command=self.toggle_tools)
        view_menu.add_separator()
        view_menu.add_command(
            label="Zoom In", command=self.zoom_in, accelerator="Ctrl++"
        )
        view_menu.add_command(
            label="Zoom Out", command=self.zoom_out, accelerator="Ctrl+-"
        )
        view_menu.add_command(
            label="Reset Zoom", command=self.reset_zoom, accelerator="Ctrl+0"
        )

        # Themes menu
        themes_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Themes", menu=themes_menu)

        # Add theme options
        for theme in ThemeType:
            themes_menu.add_command(
                label=theme.value.title(), command=lambda t=theme: self.switch_theme(t)
            )

        themes_menu.add_separator()
        themes_menu.add_command(label="Theme Information", command=self.show_theme_info)
        themes_menu.add_command(label="Reset to Default", command=self.reset_theme)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Find & Replace", command=self.find_replace)
        tools_menu.add_command(label="Code Analysis", command=self.code_analysis)
        tools_menu.add_command(label="Run Tests", command=self.run_tests)
        tools_menu.add_separator()
        tools_menu.add_command(label="Build Project", command=self.build_project)
        tools_menu.add_command(label="Deploy", command=self.deploy)
        tools_menu.add_separator()
        tools_menu.add_command(label="Settings", command=self.show_settings)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_docs)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_command(label="About", command=self.show_about)

        # Apply theme to menu
        self.theme_manager.apply_menubar_theme(menubar, self.root)

    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = tk.Frame(self.root)
        self.status_bar.pack(side="bottom", fill="x")

        # Status sections
        self.status_left = tk.Label(
            self.status_bar,
            text="Ready - Professional Enhanced Demo",
            anchor="w",
            font=("Segoe UI", 9),
        )
        self.status_left.pack(side="left", padx=5)

        self.status_center = tk.Label(
            self.status_bar,
            text="Central Theme Manager Active",
            anchor="center",
            font=("Segoe UI", 9),
        )
        self.status_center.pack(side="left", expand=True)

        self.status_right = tk.Label(
            self.status_bar,
            text=f"Theme: {self.theme_manager.current_theme.value.title()}",
            anchor="e",
            font=("Segoe UI", 9),
        )
        self.status_right.pack(side="right", padx=5)

        # Apply theme to status bar
        self.theme_manager.apply_theme_to_widget(self.status_bar, recursive=True)

    def switch_theme(self, theme_type: ThemeType):
        """Switch to a different theme."""
        print(f"🎨 Switching to {theme_type.value} theme...")

        # Set the theme
        self.theme_manager.set_theme(theme_type)

        # Apply to root window
        self.theme_manager.apply_window_theme(self.root)

        # Apply to all widgets
        self.theme_manager.apply_theme_to_widget(self.root, recursive=True)

        # Update the flexible layout theme
        self.layout.refresh_theme()

        # Update menu theming
        try:
            menubar = self.root.nametowidget(self.root["menu"])
            self.theme_manager.apply_menubar_theme(menubar, self.root)
        except (KeyError, tk.TclError):
            pass

        # Update status bar
        self.status_right.config(text=f"Theme: {theme_type.value.title()}")
        self.status_left.config(text=f"Theme switched to {theme_type.value}")

        print(f"✅ Theme switched to {theme_type.value}")

        # Show themed widget report
        self.theme_manager.print_themed_widget_report()

    def update_line_numbers(self):
        """Update line numbers in the editor."""
        content = self.text_editor.get("1.0", "end-1c")
        lines = content.split("\n")
        line_count = len(lines)

        line_numbers_text = "\n".join(str(i) for i in range(1, line_count + 1))

        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.config(state="disabled")

    def update_cursor_position(self):
        """Update cursor position in status bar."""
        cursor_pos = self.text_editor.index(tk.INSERT)
        line, col = cursor_pos.split(".")
        self.editor_status.config(
            text=f"Line {line}, Column {int(col)+1} | Python | UTF-8 | Spaces: 4 | Professional Theme"
        )

    def switch_tab(self, tab_index):
        """Switch to a different tab."""
        self.active_tab = tab_index
        for i, btn in enumerate(self.tab_buttons):
            btn.config(relief="flat" if i == tab_index else "raised")
        self.status_left.config(text=f"Switched to {self.tabs[tab_index]}")

    def close_tab(self):
        """Close the current tab."""
        if len(self.tabs) > 1:
            closed_tab = self.tabs.pop(self.active_tab)
            self.tab_buttons[self.active_tab].destroy()
            self.tab_buttons.pop(self.active_tab)
            self.active_tab = max(0, self.active_tab - 1)
            self.status_left.config(text=f"Closed {closed_tab}")

    # Event handlers
    def on_file_select(self, event):
        """Handle file selection in the file list."""
        selection = self.file_list.curselection()
        if selection:
            file_name = self.file_list.get(selection[0])
            self.status_left.config(text=f"Selected: {file_name.strip()}")

    # Menu command handlers
    def new_file(self):
        self.status_left.config(text="New file created")

    def open_file(self):
        self.status_left.config(text="Open file dialog")

    def save_file(self):
        self.status_left.config(text="File saved")

    def save_as(self):
        self.status_left.config(text="Save as dialog")

    def recent_files(self):
        self.status_left.config(text="Recent files")

    def undo(self):
        try:
            self.text_editor.edit_undo()
            self.status_left.config(text="Undo")
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.text_editor.edit_redo()
            self.status_left.config(text="Redo")
        except tk.TclError:
            pass

    def cut(self):
        self.text_editor.event_generate("<<Cut>>")
        self.status_left.config(text="Cut")

    def copy(self):
        self.text_editor.event_generate("<<Copy>>")
        self.status_left.config(text="Copy")

    def paste(self):
        self.text_editor.event_generate("<<Paste>>")
        self.status_left.config(text="Paste")

    def select_all(self):
        self.text_editor.tag_add("sel", "1.0", "end")
        self.status_left.config(text="Select all")

    def toggle_explorer(self):
        self.status_left.config(text="Toggle explorer")

    def toggle_tools(self):
        self.status_left.config(text="Toggle tools")

    def zoom_in(self):
        self.status_left.config(text="Zoom in")

    def zoom_out(self):
        self.status_left.config(text="Zoom out")

    def reset_zoom(self):
        self.status_left.config(text="Reset zoom")

    def refresh_files(self):
        self.status_left.config(text="Files refreshed")

    def find_replace(self):
        self.status_left.config(text="Find & Replace")

    def code_analysis(self):
        self.status_left.config(text="Running code analysis...")

    def run_tests(self):
        self.status_left.config(text="Running tests...")

    def build_project(self):
        self.status_left.config(text="Building project...")

    def deploy(self):
        self.status_left.config(text="Deploying...")

    def theme_editor(self):
        self.status_left.config(text="Opening theme editor...")

    def show_settings(self):
        self.status_left.config(text="Opening settings...")

    def clipboard_history(self):
        self.status_left.config(text="Clipboard history")

    def reset_theme(self):
        self.switch_theme(ThemeType.LIGHT)

    def show_theme_info(self):
        """Show information about the current theme."""
        current_theme = self.theme_manager.current_theme
        theme_colors = self.theme_manager.get_current_theme()

        info = f"""Professional Theme Information

Current Theme: {current_theme.value.title()}
Available Themes: {', '.join(t.value for t in ThemeType)}

Color Scheme (Matching themes.py):
• Primary Background: {theme_colors.primary_bg}
• Primary Text: {theme_colors.primary_text}
• Panel Background: {theme_colors.panel_bg}
• Panel Header: {theme_colors.panel_header_bg}
• Button Background: {theme_colors.button_bg}
• Accent Color: {theme_colors.accent_bg}

Professional Features:
✅ Flexible layout with detachable panes
✅ Custom control buttons with hover effects
✅ Professional pane headers and separators
✅ Comprehensive widget theming
✅ Menu and window theming
✅ Theme colors matching original themes.py
✅ Central theme manager integration
✅ Conflict prevention system"""

        messagebox.showinfo("Professional Theme Information", info)

    def show_docs(self):
        self.status_left.config(text="Opening documentation...")

    def show_shortcuts(self):
        shortcuts = """Keyboard Shortcuts

File Operations:
• Ctrl+N - New File
• Ctrl+O - Open File
• Ctrl+S - Save File
• Ctrl+Shift+S - Save As

Edit Operations:
• Ctrl+Z - Undo
• Ctrl+Y - Redo
• Ctrl+X - Cut
• Ctrl+C - Copy
• Ctrl+V - Paste
• Ctrl+A - Select All
• Ctrl+H - Find & Replace

View Operations:
• Ctrl++ - Zoom In
• Ctrl+- - Zoom Out
• Ctrl+0 - Reset Zoom

Application:
• Ctrl+Q - Exit"""

        messagebox.showinfo("Keyboard Shortcuts", shortcuts)

    def show_about(self):
        """Show about dialog."""
        about_text = """Professional Enhanced Layout Demo
Central Theme Manager Integration

This demo showcases the FlexibleThreePaneLayout
with the modern central_theme_manager system.

Features:
• Professional pane headers with detach buttons
• Custom control buttons with hover effects
• Theme colors matching original themes.py
• Comprehensive widget theming
• Menu and window theming
• Flexible layout with detachable panes
• Professional IDE-like interface

Built with ThreePaneWindows library
Using Central Theme Manager for consistent styling"""

        messagebox.showinfo("About Professional Enhanced Demo", about_text)

    def run(self):
        """Run the demo application."""
        print("🎯 Starting Professional Enhanced Demo...")
        print("📋 Features:")
        print("   ✅ Flexible layout with professional styling")
        print("   ✅ Central theme manager integration")
        print("   ✅ Professional pane headers and detach buttons")
        print("   ✅ Theme colors matching original themes.py")
        print("   ✅ Custom control buttons with hover effects")
        print("   ✅ Comprehensive widget and menu theming")
        print("\n🎨 Try switching themes using the Themes menu!")
        print("🔧 Try detaching panes to see professional styling!")
        print("💡 Notice the professional control buttons and headers!")

        self.root.mainloop()


def main():
    """Main entry point."""
    try:
        demo = ProfessionalEnhancedDemo()
        demo.run()
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
