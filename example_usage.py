#!/usr/bin/env python3
"""
Example usage of the threepanewindows library.

This script demonstrates how to use both DockableThreePaneWindow and FixedThreePaneLayout.
"""

import tkinter as tk
from threepanewindows import DockableThreePaneWindow, FixedThreePaneLayout, EnhancedDockableThreePaneWindow, PaneConfig
from window_utils import setup_window_geometry


def dockable_example():
    """Example using DockableThreePaneWindow."""
    
    def build_left(frame):
        tk.Label(frame, text="File Explorer", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Simple file list
        files = ["main.py", "utils.py", "config.py", "README.md"]
        for file in files:
            tk.Label(frame, text=f"📄 {file}", anchor="w").pack(fill="x", padx=5, pady=1)
    
    def build_center(frame):
        tk.Label(frame, text="Code Editor", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Text editor
        text = tk.Text(frame, wrap=tk.WORD, font=("Consolas", 10))
        text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sample code
        sample_code = '''def hello_world():
    """A simple hello world function."""
    print("Hello from ThreePaneWindows!")
    return "Success"

if __name__ == "__main__":
    message = hello_world()
    print(f"Result: {message}")'''
        
        text.insert(tk.END, sample_code)
    
    def build_right(frame):
        tk.Label(frame, text="Properties", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Properties
        props = [
            "File: main.py",
            "Size: 1.2 KB",
            "Lines: 25",
            "Modified: Today"
        ]
        
        for prop in props:
            tk.Label(frame, text=prop, anchor="w").pack(fill="x", padx=5, pady=1)
    
    root = tk.Tk()
    root.title("Dockable Three-Pane Example")
    root.geometry("1000x600")
    
    window = DockableThreePaneWindow(
        root,
        side_width=200,
        left_builder=build_left,
        center_builder=build_center,
        right_builder=build_right
    )
    window.pack(fill=tk.BOTH, expand=True)
    
    return root


def fixed_example():
    """Example using FixedThreePaneLayout."""
    
    root = tk.Tk()
    root.title("Fixed Three-Pane Example")
    root.geometry("800x500")
    
    layout = FixedThreePaneLayout(root, side_width=180)
    layout.pack(fill=tk.BOTH, expand=True)
    
    # Set custom labels
    layout.set_label_texts(
        left="🗂️ Navigation",
        center="📝 Workspace", 
        right="🔧 Tools"
    )
    
    # Add navigation items
    nav_items = ["Dashboard", "Projects", "Settings", "Help"]
    for item in nav_items:
        btn = tk.Button(layout.frame_left, text=item, width=15)
        btn.pack(pady=2, padx=5, fill=tk.X)
    
    # Add main content
    text_widget = tk.Text(layout.frame_center, wrap=tk.WORD)
    text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    text_widget.insert(tk.END, "Welcome to the Fixed Three-Pane Layout!\n\n")
    text_widget.insert(tk.END, "This layout has fixed panel sizes. ")
    text_widget.insert(tk.END, "The side panels maintain their width while ")
    text_widget.insert(tk.END, "the center panel adjusts to fill the remaining space.")
    
    # Add tools
    tools = ["🔍 Search", "📊 Analytics", "⚙️ Settings", "💾 Export"]
    for tool in tools:
        btn = tk.Button(layout.frame_right, text=tool, width=12)
        btn.pack(pady=2, padx=5)
    
    return root


def enhanced_example():
    """Example using EnhancedDockableThreePaneWindow."""
    
    def build_left(frame):
        tk.Label(frame, text="📁 Enhanced Explorer", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Professional file list with icons
        files = [
            ("📄 main.py", "Python File"),
            ("📄 utils.py", "Python Module"),
            ("📄 config.json", "Configuration"),
            ("📁 assets/", "Folder"),
            ("📄 README.md", "Documentation")
        ]
        
        for file_name, file_type in files:
            file_frame = tk.Frame(frame, bg=frame.cget('bg'))
            file_frame.pack(fill="x", padx=5, pady=1)
            
            tk.Label(file_frame, text=file_name, anchor="w", bg=frame.cget('bg')).pack(side="left")
            tk.Label(file_frame, text=file_type, anchor="e", fg="gray", bg=frame.cget('bg')).pack(side="right")
    
    def build_center(frame):
        tk.Label(frame, text="✨ Enhanced Editor", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Enhanced text editor with line numbers
        editor_frame = tk.Frame(frame)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Line numbers
        line_frame = tk.Frame(editor_frame, bg="#f0f0f0", width=30)
        line_frame.pack(side="left", fill="y")
        line_frame.pack_propagate(False)
        
        line_numbers = tk.Text(line_frame, width=3, bg="#f0f0f0", fg="gray", 
                              font=("Consolas", 10), state=tk.DISABLED, wrap=tk.NONE)
        line_numbers.pack(fill="both", expand=True)
        
        # Main editor
        text = tk.Text(editor_frame, wrap=tk.WORD, font=("Consolas", 10), 
                      bg="white", fg="black", insertbackground="black")
        text.pack(side="left", fill=tk.BOTH, expand=True)
        
        # Sample code
        sample_code = '''# Enhanced Three-Pane Window Demo
from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

def create_professional_interface():
    """Create a professional interface with theming."""
    
    # Configure panels
    left_config = PaneConfig(
        title="File Explorer",
        icon="📁",
        default_width=250,
        detachable=True
    )
    
    # Create enhanced window
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        theme_name="blue"
    )
    
    return window

# Professional, customizable, beautiful!'''
        
        text.insert(tk.END, sample_code)
        
        # Update line numbers
        lines = sample_code.count('\n') + 1
        line_numbers.config(state=tk.NORMAL)
        line_numbers.insert(tk.END, '\n'.join(str(i) for i in range(1, lines + 1)))
        line_numbers.config(state=tk.DISABLED)
    
    def build_right(frame):
        tk.Label(frame, text="🎨 Enhanced Properties", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Professional properties with sections
        sections = [
            ("Theme", [
                ("Current", "Blue Professional"),
                ("Style", "Modern"),
                ("Animation", "Enabled")
            ]),
            ("Panel", [
                ("Detachable", "Yes"),
                ("Resizable", "Yes"),
                ("Min Width", "200px")
            ]),
            ("Features", [
                ("Drag & Drop", "✓"),
                ("Professional UI", "✓"),
                ("Custom Themes", "✓")
            ])
        ]
        
        for section_name, properties in sections:
            # Section header
            section_frame = tk.LabelFrame(frame, text=section_name, font=("Arial", 9, "bold"))
            section_frame.pack(fill="x", padx=5, pady=5)
            
            # Properties
            for prop_name, prop_value in properties:
                prop_frame = tk.Frame(section_frame)
                prop_frame.pack(fill="x", padx=5, pady=1)
                
                tk.Label(prop_frame, text=f"{prop_name}:", anchor="w").pack(side="left")
                tk.Label(prop_frame, text=prop_value, anchor="e", fg="blue").pack(side="right")
    
    root = tk.Tk()
    setup_window_geometry(
        root,
        "Enhanced Dockable Three-Pane Example",
        preferred_width=1000,
        preferred_height=650,
        min_width=800,
        min_height=500
    )
    
    # Create pane configurations
    left_config = PaneConfig(
        title="File Explorer",
        icon="📁",
        default_width=250,
        min_width=200,
        max_width=400,
        detachable=True
    )
    
    center_config = PaneConfig(
        title="Code Editor",
        icon="📝",
        detachable=False
    )
    
    right_config = PaneConfig(
        title="Properties",
        icon="🎨",
        default_width=200,
        min_width=150,
        max_width=300,
        detachable=True
    )
    
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=build_left,
        center_builder=build_center,
        right_builder=build_right,
        theme_name="blue"
    )
    window.pack(fill=tk.BOTH, expand=True)
    
    return root


def main():
    """Main function to choose which example to run."""
    
    def run_dockable():
        selector.destroy()
        root = dockable_example()
        root.mainloop()
    
    def run_fixed():
        selector.destroy()
        root = fixed_example()
        root.mainloop()
    
    def run_enhanced():
        selector.destroy()
        root = enhanced_example()
        root.mainloop()
    
    # Create selector window with proper sizing
    selector = tk.Tk()
    setup_window_geometry(
        selector,
        "ThreePaneWindows Examples",
        preferred_width=500,
        preferred_height=400,
        min_width=400,
        min_height=300
    )
    
    # Bring window to front and focus
    selector.lift()
    selector.focus_force()
    selector.attributes('-topmost', True)
    selector.after(100, lambda: selector.attributes('-topmost', False))
    
    # Title
    title = tk.Label(selector, text="ThreePaneWindows Examples", font=("Arial", 14, "bold"))
    title.pack(pady=20)
    
    # Description
    desc = tk.Label(selector, text="Choose an example to run:", font=("Arial", 10))
    desc.pack(pady=10)
    
    # Buttons
    btn_frame = tk.Frame(selector)
    btn_frame.pack(pady=20, expand=True)
    
    dockable_btn = tk.Button(
        btn_frame, 
        text="🔗 Dockable Layout", 
        command=run_dockable,
        width=20,
        height=3,
        font=("Arial", 11, "bold"),
        bg="#4CAF50",
        fg="white",
        relief="raised",
        bd=2
    )
    dockable_btn.pack(pady=8, padx=20, fill="x")
    
    fixed_btn = tk.Button(
        btn_frame, 
        text="📐 Fixed Layout", 
        command=run_fixed,
        width=20,
        height=3,
        font=("Arial", 11, "bold"),
        bg="#2196F3",
        fg="white",
        relief="raised",
        bd=2
    )
    fixed_btn.pack(pady=8, padx=20, fill="x")
    
    enhanced_btn = tk.Button(
        btn_frame, 
        text="✨ Enhanced Professional", 
        command=run_enhanced,
        width=20,
        height=3,
        font=("Arial", 11, "bold"),
        bg="#9C27B0",
        fg="white",
        relief="raised",
        bd=2
    )
    enhanced_btn.pack(pady=8, padx=20, fill="x")
    
    selector.mainloop()


if __name__ == "__main__":
    main()