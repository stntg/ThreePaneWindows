Custom Widgets Examples
=======================

This section demonstrates how to create custom widgets and specialized content for ThreePaneWindows panels.

Custom File Browser Widget
---------------------------

Create a custom file browser with advanced features:

.. code-block:: python

    import tkinter as tk
    from tkinter import ttk
    import os
    from threepanewindows import FixedThreePaneLayout

    class CustomFileBrowser(tk.Frame):
        """A custom file browser widget with advanced features."""
        
        def __init__(self, parent, **kwargs):
            super().__init__(parent, **kwargs)
            
            self.current_path = os.getcwd()
            self.file_filters = ["All Files (*.*)", "Python Files (*.py)", "Text Files (*.txt)"]
            self.current_filter = self.file_filters[0]
            
            self.setup_ui()
            self.load_directory(self.current_path)
            
        def setup_ui(self):
            """Set up the file browser interface."""
            # Toolbar
            toolbar = tk.Frame(self, bg="#f0f0f0", height=35)
            toolbar.pack(fill=tk.X)
            toolbar.pack_propagate(False)
            
            # Navigation buttons
            tk.Button(toolbar, text="⬆️", command=self.go_up, 
                     font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)
            tk.Button(toolbar, text="🏠", command=self.go_home,
                     font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)
            tk.Button(toolbar, text="🔄", command=self.refresh,
                     font=("Arial", 10)).pack(side=tk.LEFT, padx=2, pady=2)
            
            # Path display
            self.path_var = tk.StringVar(value=self.current_path)
            path_entry = tk.Entry(toolbar, textvariable=self.path_var, font=("Arial", 9))
            path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)
            path_entry.bind('<Return>', self.navigate_to_path)
            
            # Filter dropdown
            filter_combo = ttk.Combobox(toolbar, values=self.file_filters, 
                                      width=15, font=("Arial", 9))
            filter_combo.pack(side=tk.RIGHT, padx=2, pady=2)
            filter_combo.set(self.current_filter)
            filter_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
            
            # File tree
            tree_frame = tk.Frame(self)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Configure treeview with columns
            self.file_tree = ttk.Treeview(tree_frame, columns=("Size", "Modified"), 
                                        show="tree headings")
            
            # Configure columns
            self.file_tree.column("#0", width=200, minwidth=150)
            self.file_tree.column("Size", width=80, minwidth=60)
            self.file_tree.column("Modified", width=120, minwidth=100)
            
            self.file_tree.heading("#0", text="Name", anchor=tk.W)
            self.file_tree.heading("Size", text="Size", anchor=tk.W)
            self.file_tree.heading("Modified", text="Modified", anchor=tk.W)
            
            # Scrollbars
            v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
            h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.file_tree.xview)
            self.file_tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            
            self.file_tree.grid(row=0, column=0, sticky="nsew")
            v_scroll.grid(row=0, column=1, sticky="ns")
            h_scroll.grid(row=1, column=0, sticky="ew")
            
            tree_frame.grid_rowconfigure(0, weight=1)
            tree_frame.grid_columnconfigure(0, weight=1)
            
            # Bind events
            self.file_tree.bind('<Double-1>', self.on_double_click)
            self.file_tree.bind('<Button-3>', self.show_context_menu)
            
        def load_directory(self, path):
            """Load directory contents."""
            try:
                # Clear existing items
                for item in self.file_tree.get_children():
                    self.file_tree.delete(item)
                
                # Load directories first
                items = []
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    if os.path.isdir(item_path):
                        items.append((f"📁 {item}", item_path, "Folder", ""))
                    elif self.matches_filter(item):
                        size = self.format_size(os.path.getsize(item_path))
                        modified = self.format_date(os.path.getmtime(item_path))
                        icon = self.get_file_icon(item)
                        items.append((f"{icon} {item}", item_path, size, modified))
                
                # Sort items (folders first, then files)
                items.sort(key=lambda x: (not x[2] == "Folder", x[0].lower()))
                
                # Add items to tree
                for name, path, size, modified in items:
                    self.file_tree.insert("", "end", text=name, 
                                        values=(size, modified), tags=(path,))
                
                self.current_path = path
                self.path_var.set(path)
                
            except PermissionError:
                tk.messagebox.showerror("Error", "Permission denied")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not load directory: {str(e)}")
                
        def matches_filter(self, filename):
            """Check if file matches current filter."""
            if self.current_filter == "All Files (*.*)":
                return True
            elif self.current_filter == "Python Files (*.py)":
                return filename.endswith('.py')
            elif self.current_filter == "Text Files (*.txt)":
                return filename.endswith('.txt')
            return True
            
        def get_file_icon(self, filename):
            """Get appropriate icon for file type."""
            ext = os.path.splitext(filename)[1].lower()
            icons = {
                '.py': '🐍', '.txt': '📄', '.md': '📝', '.json': '📋',
                '.png': '🖼️', '.jpg': '🖼️', '.jpeg': '🖼️', '.gif': '🖼️',
                '.pdf': '📕', '.doc': '📘', '.docx': '📘',
                '.zip': '📦', '.rar': '📦', '.7z': '📦'
            }
            return icons.get(ext, '📄')
            
        def format_size(self, size):
            """Format file size in human readable format."""
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} TB"
            
        def format_date(self, timestamp):
            """Format modification date."""
            import datetime
            dt = datetime.datetime.fromtimestamp(timestamp)
            return dt.strftime("%Y-%m-%d %H:%M")
            
        # Navigation methods
        def go_up(self):
            """Navigate to parent directory."""
            parent = os.path.dirname(self.current_path)
            if parent != self.current_path:
                self.load_directory(parent)
                
        def go_home(self):
            """Navigate to home directory."""
            home = os.path.expanduser("~")
            self.load_directory(home)
            
        def refresh(self):
            """Refresh current directory."""
            self.load_directory(self.current_path)
            
        def navigate_to_path(self, event):
            """Navigate to path entered in path bar."""
            path = self.path_var.get()
            if os.path.isdir(path):
                self.load_directory(path)
            else:
                self.path_var.set(self.current_path)
                
        def on_filter_change(self, event):
            """Handle filter change."""
            self.current_filter = event.widget.get()
            self.refresh()
            
        def on_double_click(self, event):
            """Handle double-click on item."""
            selection = self.file_tree.selection()
            if selection:
                item = selection[0]
                path = self.file_tree.item(item, "tags")[0]
                if os.path.isdir(path):
                    self.load_directory(path)
                else:
                    # File selected - could trigger callback
                    if hasattr(self, 'on_file_selected'):
                        self.on_file_selected(path)
                        
        def show_context_menu(self, event):
            """Show context menu."""
            # Implementation for context menu
            pass

    def create_custom_browser_example():
        """Example using custom file browser."""
        root = tk.Tk()
        root.title("Custom File Browser Example")
        root.geometry("1000x600")

        layout = FixedThreePaneLayout(root, side_width=300)
        layout.pack(fill=tk.BOTH, expand=True)

        layout.set_label_texts(
            left="📁 Custom File Browser",
            center="📝 File Content",
            right="ℹ️ File Info"
        )

        # Add custom file browser to left pane
        file_browser = CustomFileBrowser(layout.frame_left)
        file_browser.pack(fill=tk.BOTH, expand=True)

        # File content display
        content_text = tk.Text(layout.frame_center, wrap=tk.WORD, font=("Consolas", 11))
        content_scroll = tk.Scrollbar(layout.frame_center, orient=tk.VERTICAL, 
                                    command=content_text.yview)
        content_text.configure(yscrollcommand=content_scroll.set)
        
        content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        content_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        # File info display
        info_frame = tk.Frame(layout.frame_right)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(info_frame, text="File Information", 
                font=("Arial", 12, "bold")).pack(pady=10)
        
        info_text = tk.Text(info_frame, wrap=tk.WORD, font=("Arial", 10), height=15)
        info_text.pack(fill=tk.BOTH, expand=True)

        # Connect file browser to content display
        def on_file_selected(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    content_text.delete(1.0, tk.END)
                    content_text.insert(1.0, content)
                    
                # Update file info
                stat = os.stat(file_path)
                info = f"""File: {os.path.basename(file_path)}
Path: {file_path}
Size: {file_browser.format_size(stat.st_size)}
Modified: {file_browser.format_date(stat.st_mtime)}
Type: {os.path.splitext(file_path)[1] or 'No extension'}
Permissions: {oct(stat.st_mode)[-3:]}"""
                
                info_text.delete(1.0, tk.END)
                info_text.insert(1.0, info)
                
            except Exception as e:
                content_text.delete(1.0, tk.END)
                content_text.insert(1.0, f"Could not read file: {str(e)}")

        file_browser.on_file_selected = on_file_selected

        return root

    if __name__ == "__main__":
        app = create_custom_browser_example()
        app.mainloop()

Custom Code Editor Widget
--------------------------

Create a custom code editor with syntax highlighting:

.. code-block:: python

    import tkinter as tk
    from tkinter import font
    import re
    from threepanewindows import DockableThreePaneWindow

    class CustomCodeEditor(tk.Frame):
        """A custom code editor with basic syntax highlighting."""
        
        def __init__(self, parent, **kwargs):
            super().__init__(parent, **kwargs)
            
            self.setup_ui()
            self.setup_syntax_highlighting()
            
        def setup_ui(self):
            """Set up the editor interface."""
            # Editor toolbar
            toolbar = tk.Frame(self, bg="#2d2d2d", height=30)
            toolbar.pack(fill=tk.X)
            toolbar.pack_propagate(False)
            
            # File info
            self.file_label = tk.Label(toolbar, text="untitled.py", 
                                     font=("Arial", 10, "bold"), 
                                     bg="#2d2d2d", fg="white")
            self.file_label.pack(side=tk.LEFT, padx=10, pady=5)
            
            # Language selector
            self.lang_var = tk.StringVar(value="Python")
            lang_combo = tk.OptionMenu(toolbar, self.lang_var, "Python", "JavaScript", "HTML", "CSS")
            lang_combo.config(bg="#2d2d2d", fg="white", font=("Arial", 9))
            lang_combo.pack(side=tk.RIGHT, padx=10, pady=2)
            
            # Editor frame
            editor_frame = tk.Frame(self)
            editor_frame.pack(fill=tk.BOTH, expand=True)
            
            # Line numbers
            self.line_frame = tk.Frame(editor_frame, bg="#2d2d2d", width=50)
            self.line_frame.pack(side=tk.LEFT, fill=tk.Y)
            self.line_frame.pack_propagate(False)
            
            self.line_numbers = tk.Text(self.line_frame, width=4, bg="#2d2d2d", fg="#858585",
                                      font=("Consolas", 11), state=tk.DISABLED, wrap=tk.NONE,
                                      relief=tk.FLAT, selectbackground="#2d2d2d")
            self.line_numbers.pack(fill=tk.BOTH, expand=True, padx=5)
            
            # Main editor
            self.editor = tk.Text(editor_frame, bg="#1e1e1e", fg="#d4d4d4", 
                                font=("Consolas", 11), insertbackground="white",
                                selectbackground="#264f78", wrap=tk.NONE, undo=True)
            
            # Scrollbars
            v_scroll = tk.Scrollbar(editor_frame, orient=tk.VERTICAL, command=self.sync_scroll)
            h_scroll = tk.Scrollbar(editor_frame, orient=tk.HORIZONTAL, command=self.editor.xview)
            
            self.editor.configure(yscrollcommand=self.on_scroll, xscrollcommand=h_scroll.set)
            
            self.editor.grid(row=0, column=1, sticky="nsew")
            v_scroll.grid(row=0, column=2, sticky="ns")
            h_scroll.grid(row=1, column=1, sticky="ew")
            
            editor_frame.grid_rowconfigure(0, weight=1)
            editor_frame.grid_columnconfigure(1, weight=1)
            
            # Bind events
            self.editor.bind('<KeyRelease>', self.on_text_change)
            self.editor.bind('<Button-1>', self.on_text_change)
            
        def setup_syntax_highlighting(self):
            """Set up syntax highlighting tags."""
            # Python syntax highlighting
            self.editor.tag_configure("keyword", foreground="#569cd6")
            self.editor.tag_configure("string", foreground="#ce9178")
            self.editor.tag_configure("comment", foreground="#6a9955")
            self.editor.tag_configure("number", foreground="#b5cea8")
            self.editor.tag_configure("function", foreground="#dcdcaa")
            self.editor.tag_configure("class", foreground="#4ec9b0")
            
            # Python keywords
            self.python_keywords = [
                'def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try', 'except',
                'finally', 'with', 'as', 'import', 'from', 'return', 'yield', 'lambda',
                'and', 'or', 'not', 'in', 'is', 'True', 'False', 'None', 'pass', 'break',
                'continue', 'global', 'nonlocal', 'assert', 'del', 'raise'
            ]
            
        def highlight_syntax(self):
            """Apply syntax highlighting."""
            content = self.editor.get(1.0, tk.END)
            
            # Clear existing tags
            for tag in ["keyword", "string", "comment", "number", "function", "class"]:
                self.editor.tag_remove(tag, 1.0, tk.END)
            
            # Highlight keywords
            for keyword in self.python_keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                for match in re.finditer(pattern, content):
                    start = f"1.0+{match.start()}c"
                    end = f"1.0+{match.end()}c"
                    self.editor.tag_add("keyword", start, end)
            
            # Highlight strings
            string_patterns = [r'"[^"]*"', r"'[^']*'", r'""".*?"""', r"'''.*?'''"]
            for pattern in string_patterns:
                for match in re.finditer(pattern, content, re.DOTALL):
                    start = f"1.0+{match.start()}c"
                    end = f"1.0+{match.end()}c"
                    self.editor.tag_add("string", start, end)
            
            # Highlight comments
            for match in re.finditer(r'#.*$', content, re.MULTILINE):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.editor.tag_add("comment", start, end)
            
            # Highlight numbers
            for match in re.finditer(r'\b\d+\.?\d*\b', content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.editor.tag_add("number", start, end)
            
            # Highlight function definitions
            for match in re.finditer(r'def\s+(\w+)', content):
                start = f"1.0+{match.start(1)}c"
                end = f"1.0+{match.end(1)}c"
                self.editor.tag_add("function", start, end)
            
            # Highlight class definitions
            for match in re.finditer(r'class\s+(\w+)', content):
                start = f"1.0+{match.start(1)}c"
                end = f"1.0+{match.end(1)}c"
                self.editor.tag_add("class", start, end)
                
        def update_line_numbers(self):
            """Update line numbers display."""
            content = self.editor.get(1.0, tk.END)
            lines = content.count('\n')
            
            self.line_numbers.config(state=tk.NORMAL)
            self.line_numbers.delete(1.0, tk.END)
            
            line_numbers_text = '\n'.join(str(i) for i in range(1, lines + 1))
            self.line_numbers.insert(1.0, line_numbers_text)
            
            self.line_numbers.config(state=tk.DISABLED)
            
        def on_text_change(self, event=None):
            """Handle text changes."""
            self.update_line_numbers()
            self.highlight_syntax()
            
        def sync_scroll(self, *args):
            """Synchronize scrolling between editor and line numbers."""
            self.editor.yview(*args)
            self.line_numbers.yview(*args)
            
        def on_scroll(self, *args):
            """Handle scroll events."""
            self.line_numbers.yview_moveto(args[0])
            return args
            
        def set_content(self, content):
            """Set editor content."""
            self.editor.delete(1.0, tk.END)
            self.editor.insert(1.0, content)
            self.on_text_change()
            
        def get_content(self):
            """Get editor content."""
            return self.editor.get(1.0, tk.END + '-1c')

    def create_custom_editor_example():
        """Example using custom code editor."""
        root = tk.Tk()
        root.title("Custom Code Editor Example")
        root.geometry("1200x800")

        def build_file_panel(frame):
            """Build file management panel."""
            tk.Label(frame, text="📁 Project Files", 
                    font=("Arial", 11, "bold")).pack(pady=5)
            
            # Sample file list
            files = ["main.py", "utils.py", "config.py", "test.py", "README.md"]
            
            file_listbox = tk.Listbox(frame, font=("Arial", 10))
            file_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            for file in files:
                file_listbox.insert(tk.END, f"🐍 {file}")
                
            def on_file_select(event):
                selection = file_listbox.curselection()
                if selection:
                    filename = files[selection[0]]
                    editor.file_label.config(text=filename)
                    
                    # Load sample content based on file
                    if filename == "main.py":
                        content = '''#!/usr/bin/env python3
"""
Main application module.
"""

import tkinter as tk
from threepanewindows import DockableThreePaneWindow

class Application:
    """Main application class."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My Application")
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Create three-pane layout
        self.window = DockableThreePaneWindow(self.root)
        self.window.pack(fill=tk.BOTH, expand=True)
        
        # Add content to panes
        self.build_navigation()
        self.build_main_content()
        self.build_tools()
    
    def build_navigation(self):
        """Build navigation panel."""
        pass  # Implementation here
    
    def build_main_content(self):
        """Build main content area."""
        pass  # Implementation here
    
    def build_tools(self):
        """Build tools panel."""
        pass  # Implementation here
    
    def run(self):
        """Run the application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()'''
                        editor.set_content(content)
                        
            file_listbox.bind('<<ListboxSelect>>', on_file_select)

        def build_editor_panel(frame):
            """Build the main editor panel."""
            nonlocal editor
            editor = CustomCodeEditor(frame)
            editor.pack(fill=tk.BOTH, expand=True)
            
            # Set initial content
            initial_content = '''# Welcome to the Custom Code Editor!

def hello_world():
    """A simple hello world function."""
    message = "Hello from ThreePaneWindows!"
    print(message)
    return True

class CustomWidget:
    """Example of a custom widget class."""
    
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the widget interface."""
        # Widget implementation here
        pass

# Main execution
if __name__ == "__main__":
    result = hello_world()
    print(f"Function returned: {result}")'''
            
            editor.set_content(initial_content)

        def build_output_panel(frame):
            """Build output/console panel."""
            tk.Label(frame, text="🖥️ Output Console", 
                    font=("Arial", 11, "bold")).pack(pady=5)
            
            console = tk.Text(frame, bg="black", fg="lime", font=("Consolas", 10))
            console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            console_output = '''Python 3.9.0 (default, Oct  9 2020, 15:07:54)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exec(open('main.py').read())
Hello from ThreePaneWindows!
Function returned: True
>>> '''
            
            console.insert(1.0, console_output)

        editor = None  # Will be set in build_editor_panel

        # Create dockable window
        window = DockableThreePaneWindow(
            root,
            side_width=200,
            left_builder=build_file_panel,
            center_builder=build_editor_panel,
            right_builder=build_output_panel
        )
        window.pack(fill=tk.BOTH, expand=True)

        return root

    if __name__ == "__main__":
        app = create_custom_editor_example()
        app.mainloop()

Best Practices for Custom Widgets
----------------------------------

When creating custom widgets for ThreePaneWindows:

1. **Inherit from tk.Frame**: Make your widgets frame-based for easy integration
2. **Responsive Design**: Ensure widgets adapt to pane resizing
3. **Event Handling**: Properly handle user interactions and callbacks
4. **Consistent Styling**: Match the overall application theme
5. **Performance**: Optimize for smooth operation, especially with large data
6. **Accessibility**: Consider keyboard navigation and screen readers
7. **Documentation**: Provide clear APIs and usage examples

Widget Integration Patterns
----------------------------

Common patterns for integrating custom widgets:

**Data Binding**
- Connect widgets to share data and state
- Use callbacks and events for communication
- Implement observer patterns for updates

**Theme Consistency**
- Apply consistent colors and fonts
- Respect system theme preferences
- Provide theme customization options

**Performance Optimization**
- Use virtual scrolling for large lists
- Implement lazy loading for heavy content
- Cache frequently accessed data

Next Steps
----------

Explore more advanced customization:

- :doc:`real_world_applications` - Complete applications with custom widgets
- :doc:`theming_examples` - Styling custom widgets with themes
- Advanced widget libraries and integrations