#!/usr/bin/env python3
"""
Enhanced example showcasing the professional dockable three-pane window.

This example demonstrates the new features:
- Professional theming system
- Drag-and-drop detaching
- Customizable pane configurations
- Beautiful, modern UI
"""

import tkinter as tk
from tkinter import ttk, messagebox
from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig, ThemeType, set_global_theme
from window_utils import setup_window_geometry, print_window_info


def create_enhanced_example():
    """Create an enhanced professional example."""
    
    def build_file_explorer(frame):
        """Build a professional file explorer."""
        # Create a treeview for file structure
        tree_frame = tk.Frame(frame, bg=frame.cget('bg'))
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # Scrollable treeview
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        file_tree = ttk.Treeview(tree_scroll, yscrollcommand=tree_scroll.set, style="Themed.Treeview")
        file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.config(command=file_tree.yview)
        
        # Configure columns
        file_tree['columns'] = ("Size", "Modified")
        file_tree.column("#0", width=200, minwidth=150)
        file_tree.column("Size", width=80, minwidth=50)
        file_tree.column("Modified", width=120, minwidth=100)
        
        file_tree.heading("#0", text="Name", anchor=tk.W)
        file_tree.heading("Size", text="Size", anchor=tk.W)
        file_tree.heading("Modified", text="Modified", anchor=tk.W)
        
        # Sample file structure
        projects = file_tree.insert("", "end", text="📁 Projects", open=True)
        
        python_proj = file_tree.insert(projects, "end", text="📁 Python Projects", open=True)
        file_tree.insert(python_proj, "end", text="📄 main.py", values=("2.1 KB", "Today"))
        file_tree.insert(python_proj, "end", text="📄 utils.py", values=("1.5 KB", "Yesterday"))
        file_tree.insert(python_proj, "end", text="📄 config.json", values=("0.8 KB", "2 days ago"))
        
        web_proj = file_tree.insert(projects, "end", text="📁 Web Projects", open=False)
        file_tree.insert(web_proj, "end", text="📄 index.html", values=("3.2 KB", "Last week"))
        file_tree.insert(web_proj, "end", text="📄 style.css", values=("2.7 KB", "Last week"))
        file_tree.insert(web_proj, "end", text="📄 script.js", values=("4.1 KB", "Last week"))
        
        docs = file_tree.insert("", "end", text="📁 Documents", open=False)
        file_tree.insert(docs, "end", text="📄 README.md", values=("1.2 KB", "Today"))
        file_tree.insert(docs, "end", text="📄 LICENSE", values=("1.1 KB", "Last month"))
        
        # Context menu
        def show_context_menu(event):
            try:
                item = file_tree.selection()[0]
                context_menu = tk.Menu(frame, tearoff=0)
                context_menu.add_command(label="Open", command=lambda: None)
                context_menu.add_command(label="Rename", command=lambda: None)
                context_menu.add_separator()
                context_menu.add_command(label="Delete", command=lambda: None)
                context_menu.tk_popup(event.x_root, event.y_root)
            except IndexError:
                pass
        
        file_tree.bind("<Button-3>", show_context_menu)  # Right click
    
    def build_code_editor(frame):
        """Build a professional code editor."""
        # Create notebook for tabs
        notebook = ttk.Notebook(frame, style="Themed.TNotebook")
        notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # Tab 1 - Python file
        python_frame = ttk.Frame(notebook, style="Themed.TFrame")
        notebook.add(python_frame, text="📄 main.py")
        
        # Line numbers frame
        line_frame = tk.Frame(python_frame, bg="#f0f0f0", width=40)
        line_frame.pack(side=tk.LEFT, fill=tk.Y)
        line_frame.pack_propagate(False)
        
        # Line numbers
        line_numbers = tk.Text(
            line_frame,
            width=4,
            padx=3,
            pady=5,
            border=0,
            highlightthickness=0,
            takefocus=0,
            bg="#f0f0f0",
            fg="#666666",
            font=("Consolas", 10),
            state=tk.DISABLED,
            wrap=tk.NONE
        )
        line_numbers.pack(fill=tk.BOTH, expand=True)
        
        # Code editor
        code_text = tk.Text(
            python_frame,
            wrap=tk.NONE,
            font=("Consolas", 10),
            bg="#ffffff",
            fg="#000000",
            insertbackground="#000000",
            selectbackground="#316AC5",
            selectforeground="#ffffff",
            padx=5,
            pady=5,
            undo=True,
            maxundo=50
        )
        code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(python_frame, orient=tk.VERTICAL, command=code_text.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        code_text.config(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=code_text.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        code_text.config(xscrollcommand=h_scrollbar.set)
        
        # Sample code with syntax highlighting colors
        sample_code = '''#!/usr/bin/env python3
"""
Professional Three-Pane Window Example
A demonstration of the enhanced dockable interface.
"""

import tkinter as tk
from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Professional IDE")
        self.root.geometry("1200x800")
        
        # Configure the main window
        self.setup_interface()
    
    def setup_interface(self):
        """Setup the main interface."""
        # Create pane configurations
        left_config = PaneConfig(
            title="Explorer",
            icon="📁",
            default_width=250,
            min_width=200,
            max_width=400
        )
        
        right_config = PaneConfig(
            title="Properties",
            icon="🔧",
            default_width=200,
            min_width=150,
            max_width=300
        )
        
        # Create the enhanced window
        self.main_window = EnhancedDockableThreePaneWindow(
            self.root,
            left_config=left_config,
            right_config=right_config,
            theme_name="blue"
        )
        self.main_window.pack(fill=tk.BOTH, expand=True)
    
    def run(self):
        """Run the application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()
'''
        
        code_text.insert(tk.END, sample_code)
        
        # Update line numbers
        def update_line_numbers():
            line_numbers.config(state=tk.NORMAL)
            line_numbers.delete(1.0, tk.END)
            
            line_count = int(code_text.index('end-1c').split('.')[0])
            line_number_string = "\n".join(str(i) for i in range(1, line_count + 1))
            line_numbers.insert(1.0, line_number_string)
            line_numbers.config(state=tk.DISABLED)
        
        code_text.bind('<KeyRelease>', lambda e: update_line_numbers())
        update_line_numbers()
        
        # Tab 2 - JSON file
        json_frame = ttk.Frame(notebook, style="Themed.TFrame")
        notebook.add(json_frame, text="📄 config.json")
        
        json_text = tk.Text(
            json_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#ffffff",
            fg="#000000",
            padx=5,
            pady=5
        )
        json_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        json_content = '''{
    "application": {
        "name": "Enhanced Three-Pane Window",
        "version": "2.0.0",
        "theme": "professional"
    },
    "window": {
        "width": 1200,
        "height": 800,
        "resizable": true
    },
    "panels": {
        "left": {
            "title": "File Explorer",
            "icon": "📁",
            "default_width": 250,
            "detachable": true
        },
        "right": {
            "title": "Properties",
            "icon": "🔧",
            "default_width": 200,
            "detachable": true
        }
    }
}'''
        json_text.insert(tk.END, json_content)
    
    def build_properties_panel(frame):
        """Build a professional properties panel."""
        # Create a scrollable frame
        canvas = tk.Canvas(frame, bg=frame.cget('bg'))
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Themed.TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        scrollbar.pack(side="right", fill="y")
        
        # Properties sections
        sections = [
            ("📄 File Properties", [
                ("Name", "main.py"),
                ("Size", "2.1 KB"),
                ("Type", "Python File"),
                ("Modified", "Today 14:32"),
                ("Created", "Yesterday 09:15"),
                ("Encoding", "UTF-8")
            ]),
            ("🔧 Editor Settings", [
                ("Font", "Consolas 10pt"),
                ("Tab Size", "4 spaces"),
                ("Line Endings", "LF"),
                ("Syntax", "Python 3.x"),
                ("Auto Save", "Enabled")
            ]),
            ("📊 Statistics", [
                ("Lines", "45"),
                ("Characters", "1,247"),
                ("Words", "189"),
                ("Functions", "3"),
                ("Classes", "1")
            ]),
            ("🎨 Appearance", [
                ("Theme", "Light Professional"),
                ("Color Scheme", "Default"),
                ("Font Smoothing", "Enabled"),
                ("Line Numbers", "Visible")
            ])
        ]
        
        for section_title, properties in sections:
            # Section header
            section_frame = ttk.LabelFrame(scrollable_frame, text=section_title, style="Themed.TLabelframe")
            section_frame.pack(fill="x", padx=5, pady=5)
            
            # Properties
            for prop_name, prop_value in properties:
                prop_frame = ttk.Frame(section_frame, style="Themed.TFrame")
                prop_frame.pack(fill="x", padx=10, pady=2)
                
                name_label = ttk.Label(prop_frame, text=f"{prop_name}:", style="Themed.TLabel")
                name_label.pack(side="left")
                
                value_label = ttk.Label(prop_frame, text=prop_value, style="Themed.TLabel", foreground="#666666")
                value_label.pack(side="right")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    # Create main window with proper sizing
    root = tk.Tk()
    setup_window_geometry(
        root, 
        "Enhanced Professional Three-Pane Window",
        preferred_width=1000,  # Reduced from 1400
        preferred_height=650,  # Reduced from 900
        min_width=800,
        min_height=500
    )
    
    # Configure window properties
    root.configure(bg="#f0f0f0")
    
    # Create pane configurations
    left_config = PaneConfig(
        title="File Explorer",
        icon="📁",
        default_width=280,
        min_width=200,
        max_width=400,
        detachable=True
    )
    
    center_config = PaneConfig(
        title="Code Editor",
        icon="📝",
        detachable=False  # Keep center pane attached
    )
    
    right_config = PaneConfig(
        title="Properties",
        icon="🔧",
        default_width=250,
        min_width=200,
        max_width=350,
        detachable=True
    )
    
    # Create the enhanced dockable window
    enhanced_window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=build_file_explorer,
        center_builder=build_code_editor,
        right_builder=build_properties_panel,
        theme_name="blue",  # Start with blue theme
        enable_animations=True
    )
    enhanced_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Create menu bar for theme switching
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # Theme menu
    theme_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Themes", menu=theme_menu)
    
    def change_theme(theme_name):
        enhanced_window.set_theme(theme_name)
        messagebox.showinfo("Theme Changed", f"Theme changed to: {theme_name.title()}")
    
    theme_menu.add_command(label="🌞 Light", command=lambda: change_theme("light"))
    theme_menu.add_command(label="🌙 Dark", command=lambda: change_theme("dark"))
    theme_menu.add_command(label="💙 Blue Professional", command=lambda: change_theme("blue"))
    
    # Help menu
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    
    def show_help():
        help_text = """Enhanced Three-Pane Window Features:

🎨 Professional Theming:
• Multiple built-in themes (Light, Dark, Blue Professional)
• Consistent color schemes and typography
• Professional visual styling

🔗 Advanced Docking:
• Drag panel headers to detach
• Professional detached windows
• Smooth reattaching
• Visual feedback during operations

⚙️ Customization:
• Configurable panel properties
• Adjustable sizes and constraints
• Optional panel titles and icons
• Resizable panels with constraints

🖱️ User Experience:
• Intuitive drag-and-drop interface
• Professional context menus
• Smooth animations and transitions
• Responsive design

Try dragging the panel headers to detach them!"""
        
        messagebox.showinfo("Help - Enhanced Three-Pane Window", help_text)
    
    help_menu.add_command(label="About Features", command=show_help)
    
    # Status bar
    status_frame = tk.Frame(root, bg="#e0e0e0", height=25)
    status_frame.pack(side=tk.BOTTOM, fill=tk.X)
    status_frame.pack_propagate(False)
    
    status_label = tk.Label(
        status_frame,
        text="Ready • Enhanced Three-Pane Window • Drag panel headers to detach",
        bg="#e0e0e0",
        fg="#666666",
        font=("Segoe UI", 9),
        anchor="w"
    )
    status_label.pack(side=tk.LEFT, padx=10, pady=3)
    
    theme_label = tk.Label(
        status_frame,
        text="Theme: Blue Professional",
        bg="#e0e0e0",
        fg="#666666",
        font=("Segoe UI", 9)
    )
    theme_label.pack(side=tk.RIGHT, padx=10, pady=3)
    
    return root


def main():
    """Main function to run the enhanced example."""
    root = create_enhanced_example()
    
    # Window is already properly sized and positioned in create_enhanced_example()
    root.update_idletasks()
    
    # Debug: Print window information
    print("Window Information:")
    print_window_info(root)
    
    # Show welcome message
    root.after(1000, lambda: messagebox.showinfo(
        "Welcome!",
        "Welcome to the Enhanced Three-Pane Window!\n\n" +
        "✨ Try dragging the panel headers to detach them\n" +
        "🎨 Use the Themes menu to change appearance\n" +
        "📱 Panels are fully resizable and customizable\n\n" +
        "Enjoy the professional interface!"
    ))
    
    root.mainloop()


if __name__ == "__main__":
    main()