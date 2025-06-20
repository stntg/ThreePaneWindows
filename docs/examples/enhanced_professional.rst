Enhanced Professional Examples
==============================

The ``EnhancedDockableThreePaneWindow`` provides the most advanced features including professional theming, custom pane configurations, and modern UI elements.

Professional File Manager
--------------------------

Create a professional file manager with theming:

.. code-block:: python

    import tkinter as tk
    from tkinter import ttk
    from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

    def create_professional_file_manager():
        root = tk.Tk()
        root.title("Professional File Manager")
        root.geometry("1200x800")

        def build_sidebar(frame):
            """Build a professional sidebar with navigation."""
            # Quick access section
            quick_frame = tk.LabelFrame(frame, text="Quick Access", 
                                      font=("Segoe UI", 10, "bold"))
            quick_frame.pack(fill=tk.X, padx=8, pady=8)
            
            quick_items = [
                ("🏠 Home", "#4CAF50"),
                ("📄 Documents", "#2196F3"), 
                ("🖼️ Pictures", "#FF9800"),
                ("🎵 Music", "#9C27B0"),
                ("📹 Videos", "#F44336")
            ]
            
            for item, color in quick_items:
                btn = tk.Button(quick_frame, text=item, anchor="w", 
                              bg=color, fg="white", font=("Segoe UI", 9),
                              relief="flat", pady=5)
                btn.pack(fill=tk.X, padx=5, pady=2)
            
            # Folder tree section
            tree_frame = tk.LabelFrame(frame, text="Folders", 
                                     font=("Segoe UI", 10, "bold"))
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
            
            # Professional treeview
            tree = ttk.Treeview(tree_frame, style="Professional.Treeview")
            tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=tree_scroll.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            tree_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
            
            # Sample folder structure
            computer = tree.insert("", "end", text="💻 This PC", open=True)
            
            c_drive = tree.insert(computer, "end", text="💾 Local Disk (C:)", open=True)
            tree.insert(c_drive, "end", text="📁 Program Files")
            tree.insert(c_drive, "end", text="📁 Users")
            tree.insert(c_drive, "end", text="📁 Windows")
            
            documents = tree.insert(computer, "end", text="📄 Documents", open=True)
            tree.insert(documents, "end", text="📁 Projects")
            tree.insert(documents, "end", text="📁 Reports")

        def build_main_view(frame):
            """Build the main file view area."""
            # Toolbar
            toolbar = tk.Frame(frame, bg="#f0f0f0", height=40)
            toolbar.pack(fill=tk.X)
            toolbar.pack_propagate(False)
            
            # Navigation buttons
            nav_frame = tk.Frame(toolbar, bg="#f0f0f0")
            nav_frame.pack(side=tk.LEFT, padx=10, pady=5)
            
            nav_buttons = ["⬅️ Back", "➡️ Forward", "⬆️ Up", "🔄 Refresh"]
            for btn_text in nav_buttons:
                btn = tk.Button(nav_frame, text=btn_text, font=("Segoe UI", 9),
                              relief="flat", bg="#e0e0e0", padx=10)
                btn.pack(side=tk.LEFT, padx=2)
            
            # Address bar
            address_frame = tk.Frame(toolbar, bg="#f0f0f0")
            address_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)
            
            tk.Label(address_frame, text="📍", bg="#f0f0f0").pack(side=tk.LEFT)
            address_entry = tk.Entry(address_frame, font=("Segoe UI", 10))
            address_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            address_entry.insert(0, "C:\\Users\\Documents")
            
            # Search
            search_frame = tk.Frame(toolbar, bg="#f0f0f0")
            search_frame.pack(side=tk.RIGHT, padx=10, pady=5)
            
            tk.Label(search_frame, text="🔍", bg="#f0f0f0").pack(side=tk.LEFT)
            search_entry = tk.Entry(search_frame, width=20, font=("Segoe UI", 10))
            search_entry.pack(side=tk.LEFT, padx=5)
            
            # File list view
            list_frame = tk.Frame(frame)
            list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Professional file list
            columns = ("Name", "Size", "Type", "Modified")
            file_tree = ttk.Treeview(list_frame, columns=columns, show="tree headings",
                                   style="Professional.Treeview")
            
            # Configure columns
            file_tree.column("#0", width=300, minwidth=200)
            file_tree.column("Size", width=100, minwidth=80)
            file_tree.column("Type", width=150, minwidth=100)
            file_tree.column("Modified", width=150, minwidth=120)
            
            file_tree.heading("#0", text="Name", anchor=tk.W)
            file_tree.heading("Size", text="Size", anchor=tk.W)
            file_tree.heading("Type", text="Type", anchor=tk.W)
            file_tree.heading("Modified", text="Date Modified", anchor=tk.W)
            
            # Sample files
            files = [
                ("📁 Projects", "", "Folder", "Today"),
                ("📁 Reports", "", "Folder", "Yesterday"),
                ("📄 document.docx", "2.4 MB", "Word Document", "2 hours ago"),
                ("📊 spreadsheet.xlsx", "1.8 MB", "Excel Workbook", "1 day ago"),
                ("🖼️ image.png", "856 KB", "PNG Image", "3 days ago"),
                ("📝 notes.txt", "12 KB", "Text Document", "1 week ago"),
                ("🐍 script.py", "4.2 KB", "Python File", "2 weeks ago")
            ]
            
            for name, size, file_type, modified in files:
                file_tree.insert("", "end", text=name, values=(size, file_type, modified))
            
            # Scrollbars
            v_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=file_tree.yview)
            h_scroll = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=file_tree.xview)
            file_tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            
            file_tree.grid(row=0, column=0, sticky="nsew")
            v_scroll.grid(row=0, column=1, sticky="ns")
            h_scroll.grid(row=1, column=0, sticky="ew")
            
            list_frame.grid_rowconfigure(0, weight=1)
            list_frame.grid_columnconfigure(0, weight=1)

        def build_properties_panel(frame):
            """Build a detailed properties panel."""
            # File preview section
            preview_frame = tk.LabelFrame(frame, text="Preview", 
                                        font=("Segoe UI", 10, "bold"))
            preview_frame.pack(fill=tk.X, padx=8, pady=8)
            
            # Placeholder for file preview
            preview_canvas = tk.Canvas(preview_frame, height=120, bg="white")
            preview_canvas.pack(fill=tk.X, padx=5, pady=5)
            
            # Add sample preview
            preview_canvas.create_rectangle(10, 10, 110, 110, fill="lightblue", outline="blue")
            preview_canvas.create_text(60, 60, text="📄\nDocument\nPreview", 
                                     font=("Segoe UI", 9), justify=tk.CENTER)
            
            # Properties section
            props_frame = tk.LabelFrame(frame, text="Properties", 
                                      font=("Segoe UI", 10, "bold"))
            props_frame.pack(fill=tk.X, padx=8, pady=8)
            
            properties = [
                ("Name:", "document.docx"),
                ("Type:", "Microsoft Word Document"),
                ("Size:", "2.4 MB (2,457,600 bytes)"),
                ("Location:", "C:\\Users\\Documents"),
                ("Created:", "January 15, 2024 2:30 PM"),
                ("Modified:", "January 20, 2024 4:45 PM"),
                ("Accessed:", "Today 10:15 AM")
            ]
            
            for prop, value in properties:
                prop_frame = tk.Frame(props_frame)
                prop_frame.pack(fill=tk.X, padx=5, pady=3)
                
                tk.Label(prop_frame, text=prop, font=("Segoe UI", 9, "bold"), 
                        width=12, anchor="w").pack(side=tk.LEFT)
                tk.Label(prop_frame, text=value, font=("Segoe UI", 9), 
                        anchor="w", wraplength=150).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Actions section
            actions_frame = tk.LabelFrame(frame, text="Actions", 
                                        font=("Segoe UI", 10, "bold"))
            actions_frame.pack(fill=tk.X, padx=8, pady=8)
            
            actions = [
                ("📂 Open", "#4CAF50"),
                ("✏️ Edit", "#2196F3"),
                ("📋 Copy", "#FF9800"),
                ("🗑️ Delete", "#F44336")
            ]
            
            for action, color in actions:
                btn = tk.Button(actions_frame, text=action, bg=color, fg="white",
                              font=("Segoe UI", 9), relief="flat", pady=3)
                btn.pack(fill=tk.X, padx=5, pady=2)

        # Configure professional panes
        sidebar_config = PaneConfig(
            title="Navigation",
            icon="🗂️",
            default_width=280,
            min_width=200,
            max_width=400,
            detachable=True
        )
        
        main_config = PaneConfig(
            title="Files",
            icon="📄",
            detachable=False
        )
        
        properties_config = PaneConfig(
            title="Properties",
            icon="ℹ️",
            default_width=250,
            min_width=200,
            max_width=350,
            detachable=True
        )

        # Create the enhanced window with professional theme
        file_manager = EnhancedDockableThreePaneWindow(
            root,
            left_config=sidebar_config,
            center_config=main_config,
            right_config=properties_config,
            left_builder=build_sidebar,
            center_builder=build_main_view,
            right_builder=build_properties_panel,
            theme_name="blue"  # Professional blue theme
        )
        file_manager.pack(fill=tk.BOTH, expand=True)

        return root

    if __name__ == "__main__":
        app = create_professional_file_manager()
        app.mainloop()

Professional Code Editor
-------------------------

Create a professional code editor with syntax highlighting simulation:

.. code-block:: python

    import tkinter as tk
    from tkinter import ttk, font
    from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

    def create_professional_editor():
        root = tk.Tk()
        root.title("Professional Code Editor")
        root.geometry("1400x900")

        def build_project_panel(frame):
            """Build a professional project panel."""
            # Project selector
            project_frame = tk.Frame(frame, bg="#2d2d2d")
            project_frame.pack(fill=tk.X, padx=5, pady=5)
            
            tk.Label(project_frame, text="📁 Current Project", 
                    font=("Segoe UI", 10, "bold"), bg="#2d2d2d", fg="white").pack(anchor="w")
            
            project_combo = ttk.Combobox(project_frame, values=["ThreePaneWindows", "WebApp", "DataAnalysis"])
            project_combo.pack(fill=tk.X, pady=5)
            project_combo.set("ThreePaneWindows")
            
            # File tree
            tree_frame = tk.Frame(frame)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            file_tree = ttk.Treeview(tree_frame, style="Dark.Treeview")
            tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=file_tree.yview)
            file_tree.configure(yscrollcommand=tree_scroll.set)
            
            file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Project structure
            root_node = file_tree.insert("", "end", text="📁 ThreePaneWindows", open=True)
            
            src = file_tree.insert(root_node, "end", text="📁 threepanewindows", open=True)
            file_tree.insert(src, "end", text="🐍 __init__.py")
            file_tree.insert(src, "end", text="🐍 dockable.py")
            file_tree.insert(src, "end", text="🐍 enhanced_dockable.py")
            file_tree.insert(src, "end", text="🐍 fixed.py")
            file_tree.insert(src, "end", text="🐍 themes.py")
            
            docs = file_tree.insert(root_node, "end", text="📁 docs")
            file_tree.insert(docs, "end", text="📄 README.md")
            file_tree.insert(docs, "end", text="📄 API.md")
            
            tests = file_tree.insert(root_node, "end", text="📁 tests")
            file_tree.insert(tests, "end", text="🐍 test_dockable.py")
            file_tree.insert(tests, "end", text="🐍 test_fixed.py")

        def build_editor_panel(frame):
            """Build the main editor panel."""
            # Tab bar
            tab_frame = tk.Frame(frame, bg="#3c3c3c", height=35)
            tab_frame.pack(fill=tk.X)
            tab_frame.pack_propagate(False)
            
            # Editor tabs
            tabs = ["dockable.py", "enhanced_dockable.py", "themes.py"]
            for i, tab in enumerate(tabs):
                tab_color = "#4d4d4d" if i == 0 else "#3c3c3c"
                tab_btn = tk.Button(tab_frame, text=f"🐍 {tab}", bg=tab_color, fg="white",
                                  font=("Segoe UI", 9), relief="flat", padx=15, pady=5)
                tab_btn.pack(side=tk.LEFT, padx=1)
            
            # Editor area
            editor_frame = tk.Frame(frame)
            editor_frame.pack(fill=tk.BOTH, expand=True)
            
            # Line numbers
            line_frame = tk.Frame(editor_frame, bg="#2d2d2d", width=50)
            line_frame.pack(side=tk.LEFT, fill=tk.Y)
            line_frame.pack_propagate(False)
            
            line_font = font.Font(family="Consolas", size=10)
            line_numbers = tk.Text(line_frame, width=4, bg="#2d2d2d", fg="#858585",
                                 font=line_font, state=tk.DISABLED, wrap=tk.NONE,
                                 relief=tk.FLAT, selectbackground="#2d2d2d")
            line_numbers.pack(fill=tk.BOTH, expand=True, padx=5)
            
            # Main editor
            editor_font = font.Font(family="Consolas", size=11)
            editor = tk.Text(editor_frame, bg="#1e1e1e", fg="#d4d4d4", font=editor_font,
                           insertbackground="white", selectbackground="#264f78",
                           wrap=tk.NONE, relief=tk.FLAT)
            editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Sample code with syntax highlighting simulation
            sample_code = '''"""
Enhanced Dockable Three-Pane Window Module

This module provides professional dockable three-pane windows with theming.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Dict, Any

class EnhancedDockableThreePaneWindow(tk.Frame):
    """Professional dockable three-pane window with theming support."""
    
    def __init__(self, parent: tk.Widget, **kwargs):
        """Initialize the enhanced dockable window.
        
        Args:
            parent: Parent widget
            **kwargs: Additional configuration options
        """
        super().__init__(parent)
        
        self.theme_name = kwargs.get('theme_name', 'blue')
        self.left_config = kwargs.get('left_config')
        self.center_config = kwargs.get('center_config')
        self.right_config = kwargs.get('right_config')
        
        self._setup_ui()
        self._apply_theme()
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Create the main paned window
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Create panes
        self._create_left_pane()
        self._create_center_pane()
        self._create_right_pane()
    
    def _apply_theme(self):
        """Apply the selected theme."""
        if self.theme_name == 'blue':
            self._apply_blue_theme()
        elif self.theme_name == 'dark':
            self._apply_dark_theme()
        else:
            self._apply_default_theme()'''
            
            editor.insert("1.0", sample_code)
            
            # Update line numbers
            lines = sample_code.count('\n') + 1
            line_numbers.config(state=tk.NORMAL)
            line_numbers.insert("1.0", '\n'.join(str(i) for i in range(1, lines + 1)))
            line_numbers.config(state=tk.DISABLED)
            
            # Status bar
            status_frame = tk.Frame(frame, bg="#007acc", height=25)
            status_frame.pack(fill=tk.X, side=tk.BOTTOM)
            status_frame.pack_propagate(False)
            
            tk.Label(status_frame, text="Line 1, Column 1", bg="#007acc", fg="white",
                    font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=10, pady=2)
            tk.Label(status_frame, text="Python", bg="#007acc", fg="white",
                    font=("Segoe UI", 9)).pack(side=tk.RIGHT, padx=10, pady=2)

        def build_tools_panel(frame):
            """Build the tools and output panel."""
            # Tools notebook
            notebook = ttk.Notebook(frame, style="Dark.TNotebook")
            notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Output tab
            output_frame = tk.Frame(notebook, bg="#1e1e1e")
            notebook.add(output_frame, text="🖥️ Output")
            
            output_text = tk.Text(output_frame, bg="#1e1e1e", fg="#d4d4d4",
                                font=("Consolas", 10), height=10)
            output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            output_content = '''Building ThreePaneWindows...
✓ Compiling dockable.py
✓ Compiling enhanced_dockable.py  
✓ Compiling themes.py
✓ Running tests...
✓ All tests passed!

Build completed successfully in 2.3 seconds.'''
            
            output_text.insert("1.0", output_content)
            
            # Problems tab
            problems_frame = tk.Frame(notebook, bg="#1e1e1e")
            notebook.add(problems_frame, text="⚠️ Problems")
            
            problems_tree = ttk.Treeview(problems_frame, columns=("File", "Line", "Message"),
                                       show="tree headings", style="Dark.Treeview")
            problems_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            problems_tree.heading("#0", text="Type")
            problems_tree.heading("File", text="File")
            problems_tree.heading("Line", text="Line")
            problems_tree.heading("Message", text="Message")
            
            # Sample problems
            problems_tree.insert("", "end", text="⚠️ Warning", 
                                values=("dockable.py", "45", "Unused import 'sys'"))
            problems_tree.insert("", "end", text="💡 Info", 
                                values=("themes.py", "12", "Consider using f-strings"))
            
            # Terminal tab
            terminal_frame = tk.Frame(notebook, bg="#000000")
            notebook.add(terminal_frame, text="💻 Terminal")
            
            terminal_text = tk.Text(terminal_frame, bg="#000000", fg="#00ff00",
                                  font=("Consolas", 10))
            terminal_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            terminal_content = '''$ python -m pytest tests/
========================= test session starts =========================
platform win32 -- Python 3.9.0, pytest-6.2.4
collected 15 items

tests/test_dockable.py ........                              [ 53%]
tests/test_enhanced.py .......                               [100%]

========================= 15 passed in 0.42s =========================

$ python setup.py build
running build
running build_py
copying threepanewindows/__init__.py -> build/lib/threepanewindows
copying threepanewindows/dockable.py -> build/lib/threepanewindows
Build completed successfully!

$ '''
            
            terminal_text.insert("1.0", terminal_content)

        # Configure professional panes
        project_config = PaneConfig(
            title="Project Explorer",
            icon="📁",
            default_width=300,
            min_width=250,
            max_width=500,
            detachable=True
        )
        
        editor_config = PaneConfig(
            title="Code Editor",
            icon="📝",
            detachable=False
        )
        
        tools_config = PaneConfig(
            title="Output & Tools",
            icon="🔧",
            default_width=350,
            min_width=300,
            max_width=600,
            detachable=True
        )

        # Create the professional editor
        editor = EnhancedDockableThreePaneWindow(
            root,
            left_config=project_config,
            center_config=editor_config,
            right_config=tools_config,
            left_builder=build_project_panel,
            center_builder=build_editor_panel,
            right_builder=build_tools_panel,
            theme_name="dark"  # Professional dark theme
        )
        editor.pack(fill=tk.BOTH, expand=True)

        return root

    if __name__ == "__main__":
        app = create_professional_editor()
        app.mainloop()

Key Professional Features
-------------------------

The enhanced professional examples demonstrate:

1. **Professional Theming**: Dark and light themes with consistent styling
2. **Advanced Pane Configuration**: Detailed control over pane behavior
3. **Modern UI Elements**: Professional-looking widgets and layouts
4. **Detachable Panels**: Drag-and-drop panel management
5. **Responsive Design**: Adaptive layouts that work at different sizes
6. **Rich Content**: Complex, real-world interface elements

Theme Options
-------------

Available professional themes:

- **Blue Theme**: Professional blue color scheme
- **Dark Theme**: Modern dark interface
- **Light Theme**: Clean, bright interface
- **Custom Themes**: Create your own color schemes

Best Practices for Professional Applications
--------------------------------------------

1. **Consistent Theming**: Use the same theme throughout your application
2. **Logical Panel Organization**: Group related functionality together
3. **Professional Typography**: Use system fonts like Segoe UI or San Francisco
4. **Appropriate Icons**: Use consistent, meaningful icons
5. **Responsive Layouts**: Ensure your interface works at different sizes
6. **User Customization**: Allow users to customize their workspace

Next Steps
----------

Explore more advanced topics:

- :doc:`theming_examples` - Custom theme creation
- :doc:`real_world_applications` - Complete application examples
- :doc:`custom_widgets` - Creating custom panel content