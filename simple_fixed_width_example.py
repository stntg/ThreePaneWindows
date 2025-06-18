#!/usr/bin/env python3
"""
Simple example showing fixed width panes with menu bar support.

This demonstrates the basic usage of the new fixed width features
across all three window types.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from threepanewindows import FixedThreePaneLayout, DockableThreePaneWindow, EnhancedDockableThreePaneWindow, PaneConfig


def create_simple_menu(root):
    """Create a simple menu bar."""
    menubar = tk.Menu(root)
    
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="New", command=lambda: messagebox.showinfo("Menu", "New File"))
    file_menu.add_command(label="Open", command=lambda: messagebox.showinfo("Menu", "Open File"))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)
    
    return menubar


def example_fixed_layout():
    """Example using FixedThreePaneLayout with fixed widths."""
    root = tk.Tk()
    root.title("Fixed Layout - Left Fixed, Right Resizable")
    root.geometry("800x500")
    
    # Create menu
    menu = create_simple_menu(root)
    
    # Create layout with left pane fixed at 200px, right pane resizable
    layout = FixedThreePaneLayout(
        root,
        left_fixed_width=200,    # Left pane fixed at 200px
        right_fixed_width=None,  # Right pane resizable
        menu_bar=menu
    )
    
    # Add content
    tk.Label(layout.frame_left, text="FIXED\n200px", 
             bg="#3A7CA5", fg="white", font=("Arial", 12, "bold")).pack(expand=True)
    
    tk.Label(layout.frame_center, text="CENTER - RESIZABLE", 
             font=("Arial", 14, "bold")).pack(expand=True)
    
    tk.Label(layout.frame_right, text="RESIZABLE\nTry resizing window", 
             bg="#F4A261", font=("Arial", 10)).pack(expand=True)
    
    root.mainloop()


def example_dockable_window():
    """Example using DockableThreePaneWindow with fixed widths."""
    root = tk.Tk()
    root.title("Dockable Window - Both Sides Fixed")
    root.geometry("900x600")
    
    # Create menu
    menu = create_simple_menu(root)
    
    def build_left(frame):
        tk.Label(frame, text="LEFT PANEL\nFixed: 180px", 
                font=("Arial", 10, "bold")).pack(pady=20)
        tk.Label(frame, text="Cannot resize", fg="red").pack()
    
    def build_center(frame):
        tk.Label(frame, text="CENTER PANEL - RESIZABLE", 
                font=("Arial", 12, "bold")).pack(pady=20)
        tk.Label(frame, text="This pane adjusts to fill remaining space").pack()
    
    def build_right(frame):
        tk.Label(frame, text="RIGHT PANEL\nFixed: 150px", 
                font=("Arial", 10, "bold")).pack(pady=20)
        tk.Label(frame, text="Detachable", fg="blue").pack()
    
    # Create dockable window with both sides fixed
    window = DockableThreePaneWindow(
        root,
        left_builder=build_left,
        center_builder=build_center,
        right_builder=build_right,
        left_fixed_width=180,   # Left fixed at 180px
        right_fixed_width=150,  # Right fixed at 150px
        menu_bar=menu
    )
    window.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()


def example_enhanced_window():
    """Example using EnhancedDockableThreePaneWindow with fixed widths."""
    root = tk.Tk()
    root.title("Enhanced Window - Professional Fixed Width Layout")
    root.geometry("1000x650")
    
    # Create menu
    menu = create_simple_menu(root)
    
    def build_sidebar(frame):
        tk.Label(frame, text="📁 SIDEBAR", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Sample list
        listbox = tk.Listbox(frame)
        listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        for i in range(10):
            listbox.insert(tk.END, f"Item {i+1}")
    
    def build_editor(frame):
        tk.Label(frame, text="📝 MAIN EDITOR", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Text area
        text = tk.Text(frame, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert("1.0", "This is the main content area.\n\nThe sidebar is fixed at 220px width.\nThe properties panel is fixed at 180px width.\n\nThis center pane resizes to fill the remaining space.")
    
    def build_properties(frame):
        tk.Label(frame, text="🔧 PROPERTIES", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Properties
        props = [("Name:", "document.txt"), ("Size:", "1.2 KB"), ("Type:", "Text")]
        for prop, value in props:
            prop_frame = tk.Frame(frame)
            prop_frame.pack(fill=tk.X, padx=5, pady=2)
            tk.Label(prop_frame, text=prop, font=("Arial", 9, "bold")).pack(side=tk.LEFT)
            tk.Label(prop_frame, text=value, font=("Arial", 9)).pack(side=tk.RIGHT)
    
    # Configure panes with fixed widths
    left_config = PaneConfig(
        title="Sidebar",
        icon="📁",
        fixed_width=220,  # Fixed at 220px
        detachable=True
    )
    
    center_config = PaneConfig(
        title="Editor",
        icon="📝",
        detachable=False
    )
    
    right_config = PaneConfig(
        title="Properties",
        icon="🔧",
        fixed_width=180,  # Fixed at 180px
        detachable=True
    )
    
    # Create enhanced window
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=build_sidebar,
        center_builder=build_editor,
        right_builder=build_properties,
        menu_bar=menu
    )
    window.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()


def main():
    """Main selector."""
    root = tk.Tk()
    root.title("Fixed Width Examples")
    root.geometry("400x300")
    
    tk.Label(root, text="Fixed Width Pane Examples", 
             font=("Arial", 16, "bold")).pack(pady=20)
    
    tk.Button(root, text="Fixed Layout Example", 
              command=lambda: [root.destroy(), example_fixed_layout()],
              width=25, height=2).pack(pady=5)
    
    tk.Button(root, text="Dockable Window Example", 
              command=lambda: [root.destroy(), example_dockable_window()],
              width=25, height=2).pack(pady=5)
    
    tk.Button(root, text="Enhanced Window Example", 
              command=lambda: [root.destroy(), example_enhanced_window()],
              width=25, height=2).pack(pady=5)
    
    root.mainloop()


if __name__ == "__main__":
    main()