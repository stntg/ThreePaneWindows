#!/usr/bin/env python3
"""
Comprehensive test for fixed width features across all three pane window types.

This example demonstrates:
1. Fixed width panes that don't resize
2. Resizable panes (default behavior)
3. Optional menu bar integration
4. Dynamic width changes
5. All three window types: Fixed, Dockable, Enhanced
"""

import tkinter as tk
from tkinter import ttk, messagebox
from threepanewindows import FixedThreePaneLayout, DockableThreePaneWindow, EnhancedDockableThreePaneWindow, PaneConfig
from window_utils import setup_window_geometry


def create_menu_bar(root, window_type=""):
    """Create a sample menu bar."""
    menubar = tk.Menu(root)
    
    # File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="New", command=lambda: messagebox.showinfo("Menu", f"{window_type} - New File"))
    file_menu.add_command(label="Open", command=lambda: messagebox.showinfo("Menu", f"{window_type} - Open File"))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)
    
    # View menu
    view_menu = tk.Menu(menubar, tearoff=0)
    view_menu.add_command(label="Zoom In", command=lambda: messagebox.showinfo("Menu", f"{window_type} - Zoom In"))
    view_menu.add_command(label="Zoom Out", command=lambda: messagebox.showinfo("Menu", f"{window_type} - Zoom Out"))
    menubar.add_cascade(label="View", menu=view_menu)
    
    return menubar


def test_fixed_layout():
    """Test the FixedThreePaneLayout with fixed width features."""
    root = tk.Tk()
    setup_window_geometry(root, "Fixed Layout - Width Control Test", 900, 600)
    
    # Create menu bar
    menu_bar = create_menu_bar(root, "Fixed Layout")
    
    # Create layout with fixed left width, resizable right
    layout = FixedThreePaneLayout(
        root, 
        side_width=150,  # Default width
        left_fixed_width=200,  # Left pane fixed at 200px
        right_fixed_width=None,  # Right pane resizable (uses side_width)
        menu_bar=menu_bar
    )
    
    # Add content to demonstrate the fixed width behavior
    # Left pane content
    left_label = tk.Label(layout.frame_left, text="FIXED WIDTH\n200px", 
                         bg="#3A7CA5", fg="white", font=("Arial", 10, "bold"))
    left_label.pack(pady=10)
    
    width_info = tk.Label(layout.frame_left, 
                         text=f"Fixed: {layout.is_left_fixed()}\nWidth: {layout.get_left_width()}px",
                         bg="#3A7CA5", fg="white", font=("Arial", 8))
    width_info.pack(pady=5)
    
    # Center pane content
    center_frame = tk.Frame(layout.frame_center, bg="white")
    center_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    tk.Label(center_frame, text="CENTER PANE - RESIZABLE", 
             font=("Arial", 12, "bold")).pack(pady=10)
    
    # Control buttons
    control_frame = tk.Frame(center_frame, bg="white")
    control_frame.pack(pady=10)
    
    tk.Button(control_frame, text="Set Left Width to 250px", 
              command=lambda: [layout.set_left_width(250), update_info()]).pack(side=tk.LEFT, padx=5)
    
    tk.Button(control_frame, text="Set Right Width to 180px", 
              command=lambda: [layout.set_right_width(180), update_info()]).pack(side=tk.LEFT, padx=5)
    
    # Info display
    info_label = tk.Label(center_frame, text="", bg="white", font=("Arial", 10))
    info_label.pack(pady=10)
    
    def update_info():
        info_text = f"Left: {'Fixed' if layout.is_left_fixed() else 'Resizable'} ({layout.get_left_width()}px)\n"
        info_text += f"Right: {'Fixed' if layout.is_right_fixed() else 'Resizable'} ({layout.get_right_width()}px)"
        info_label.config(text=info_text)
        
        # Update left pane info
        width_info.config(text=f"Fixed: {layout.is_left_fixed()}\nWidth: {layout.get_left_width()}px")
    
    update_info()
    
    # Right pane content
    right_label = tk.Label(layout.frame_right, text="RESIZABLE\n(Default)", 
                          bg="#F4A261", fg="black", font=("Arial", 10, "bold"))
    right_label.pack(pady=10)
    
    tk.Label(layout.frame_right, text="Try resizing the window\nto see the difference", 
             bg="#F4A261", fg="black", font=("Arial", 8)).pack(pady=5)
    
    root.mainloop()


def test_dockable_window():
    """Test the DockableThreePaneWindow with fixed width features."""
    root = tk.Tk()
    setup_window_geometry(root, "Dockable Window - Width Control Test", 900, 600)
    
    # Create menu bar
    menu_bar = create_menu_bar(root, "Dockable")
    
    def build_left_pane(frame):
        tk.Label(frame, text="LEFT PANE", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(frame, text="Fixed Width: 180px", font=("Arial", 10)).pack(pady=5)
        tk.Label(frame, text="Cannot be resized", font=("Arial", 8), fg="red").pack(pady=5)
    
    def build_center_pane(frame):
        tk.Label(frame, text="CENTER PANE - RESIZABLE", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Control buttons
        control_frame = tk.Frame(frame)
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="Set Left to 220px", 
                  command=lambda: window.set_left_fixed_width(220)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Set Right to 160px", 
                  command=lambda: window.set_right_fixed_width(160)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Make Left Resizable", 
                  command=lambda: window.clear_left_fixed_width()).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Make Right Resizable", 
                  command=lambda: window.clear_right_fixed_width()).pack(side=tk.LEFT, padx=5)
        
        # Info display
        info_frame = tk.Frame(frame)
        info_frame.pack(pady=10)
        
        info_label = tk.Label(info_frame, text="", font=("Arial", 10))
        info_label.pack()
        
        def update_info():
            info_text = f"Left: {'Fixed' if window.is_left_fixed() else 'Resizable'}\n"
            info_text += f"Right: {'Fixed' if window.is_right_fixed() else 'Resizable'}"
            info_label.config(text=info_text)
            root.after(1000, update_info)  # Update every second
        
        update_info()
    
    def build_right_pane(frame):
        tk.Label(frame, text="RIGHT PANE", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(frame, text="Resizable (Default)", font=("Arial", 10)).pack(pady=5)
        tk.Label(frame, text="Can be detached", font=("Arial", 8), fg="blue").pack(pady=5)
    
    # Create dockable window with mixed fixed/resizable panes
    window = DockableThreePaneWindow(
        root,
        left_builder=build_left_pane,
        center_builder=build_center_pane,
        right_builder=build_right_pane,
        left_fixed_width=180,  # Fixed left pane
        right_fixed_width=None,  # Resizable right pane
        menu_bar=menu_bar
    )
    window.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()


def test_enhanced_window():
    """Test the EnhancedDockableThreePaneWindow with fixed width features."""
    root = tk.Tk()
    setup_window_geometry(root, "Enhanced Window - Width Control Test", 1000, 650)
    
    # Create menu bar
    menu_bar = create_menu_bar(root, "Enhanced")
    
    def build_left_pane(frame):
        tk.Label(frame, text="📁 FILE EXPLORER", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(frame, text="Fixed Width: 250px", font=("Arial", 10)).pack(pady=5)
        
        # Sample file tree
        tree = ttk.Treeview(frame, height=8)
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add sample items
        root_item = tree.insert("", "end", text="📁 Project")
        tree.insert(root_item, "end", text="📄 main.py")
        tree.insert(root_item, "end", text="📄 utils.py")
        tree.insert(root_item, "end", text="📁 tests")
    
    def build_center_pane(frame):
        tk.Label(frame, text="📝 MAIN EDITOR", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Text editor
        text_frame = tk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Sample content
        text_widget.insert("1.0", """# Fixed Width Pane Demo

This enhanced three-pane window demonstrates:

1. Left pane: Fixed at 250px width
2. Right pane: Fixed at 200px width  
3. Center pane: Resizable (takes remaining space)

Try resizing the window to see how the fixed panes
maintain their width while the center pane adjusts.

You can also detach the side panes and they will
remember their fixed width settings when reattached.
""")
        
        # Control panel
        control_frame = tk.Frame(frame, bg="lightgray")
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(control_frame, text="Width Controls:", font=("Arial", 10, "bold"), 
                bg="lightgray").pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Left: 300px", 
                  command=lambda: window.set_pane_fixed_width("left", 300)).pack(side=tk.LEFT, padx=2)
        
        tk.Button(control_frame, text="Right: 150px", 
                  command=lambda: window.set_pane_fixed_width("right", 150)).pack(side=tk.LEFT, padx=2)
        
        tk.Button(control_frame, text="Make Left Resizable", 
                  command=lambda: window.clear_pane_fixed_width("left")).pack(side=tk.LEFT, padx=2)
        
        tk.Button(control_frame, text="Make Right Resizable", 
                  command=lambda: window.clear_pane_fixed_width("right")).pack(side=tk.LEFT, padx=2)
    
    def build_right_pane(frame):
        tk.Label(frame, text="🔧 PROPERTIES", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(frame, text="Fixed Width: 200px", font=("Arial", 10)).pack(pady=5)
        
        # Properties list
        props_frame = tk.Frame(frame)
        props_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        properties = [
            ("File:", "main.py"),
            ("Size:", "2.1 KB"),
            ("Modified:", "Today"),
            ("Type:", "Python"),
            ("Lines:", "87")
        ]
        
        for prop, value in properties:
            prop_frame = tk.Frame(props_frame)
            prop_frame.pack(fill=tk.X, pady=2)
            tk.Label(prop_frame, text=prop, font=("Arial", 9, "bold")).pack(side=tk.LEFT)
            tk.Label(prop_frame, text=value, font=("Arial", 9)).pack(side=tk.RIGHT)
    
    # Create enhanced window with fixed width configurations
    left_config = PaneConfig(
        title="File Explorer",
        icon="📁",
        fixed_width=250,  # Fixed at 250px
        detachable=True
    )
    
    center_config = PaneConfig(
        title="Editor",
        icon="📝",
        detachable=False  # Center pane typically not detachable
    )
    
    right_config = PaneConfig(
        title="Properties",
        icon="🔧",
        fixed_width=200,  # Fixed at 200px
        detachable=True
    )
    
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=build_left_pane,
        center_builder=build_center_pane,
        right_builder=build_right_pane,
        menu_bar=menu_bar,
        theme_name="light"
    )
    window.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()


def main():
    """Main function to choose which test to run."""
    root = tk.Tk()
    setup_window_geometry(root, "Fixed Width Features - Test Selector", 500, 400)
    
    tk.Label(root, text="Fixed Width Features Test", 
             font=("Arial", 16, "bold")).pack(pady=20)
    
    tk.Label(root, text="Choose a test to run:", 
             font=("Arial", 12)).pack(pady=10)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    
    tk.Button(button_frame, text="Fixed Layout Test", 
              command=lambda: [root.destroy(), test_fixed_layout()],
              width=20, height=2).pack(pady=5)
    
    tk.Button(button_frame, text="Dockable Window Test", 
              command=lambda: [root.destroy(), test_dockable_window()],
              width=20, height=2).pack(pady=5)
    
    tk.Button(button_frame, text="Enhanced Window Test", 
              command=lambda: [root.destroy(), test_enhanced_window()],
              width=20, height=2).pack(pady=5)
    
    tk.Button(button_frame, text="Exit", 
              command=root.destroy,
              width=20, height=1).pack(pady=10)
    
    # Instructions
    instructions = tk.Text(root, height=8, width=60, wrap=tk.WORD)
    instructions.pack(pady=10, padx=20)
    
    instructions.insert("1.0", """FEATURES DEMONSTRATED:

• Fixed Width Panes: Left/right panes can be set to fixed widths that don't change when the window is resized.

• Resizable Panes: Default behavior allows panes to resize proportionally.

• Menu Bar Integration: All window types support optional menu bars.

• Dynamic Width Control: Change pane widths at runtime.

• Mixed Configurations: Some panes fixed, others resizable in the same window.

• Detachment Support: Enhanced and dockable windows maintain width settings when panes are detached/reattached.""")
    
    instructions.config(state=tk.DISABLED)
    
    root.mainloop()


if __name__ == "__main__":
    main()