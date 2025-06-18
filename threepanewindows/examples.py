"""
Example applications demonstrating the use of ThreePaneWindows.
"""

import tkinter as tk
from .dockable import DockableThreePaneWindow
from .fixed import FixedThreePaneLayout


def run_demo():
    """Run a simple demo of both layout types."""
    
    def show_dockable():
        def build_left(frame):
            tk.Label(frame, text="Left Panel Content").pack(pady=10)
            tk.Button(frame, text="Sample Button").pack(pady=5)
        
        def build_center(frame):
            tk.Label(frame, text="Center Panel Content").pack(pady=10)
            text = tk.Text(frame, height=10)
            text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text.insert(tk.END, "This is the center panel.\nYou can detach the side panels!")
        
        def build_right(frame):
            tk.Label(frame, text="Right Panel Content").pack(pady=10)
            listbox = tk.Listbox(frame)
            listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            for i in range(10):
                listbox.insert(tk.END, f"Item {i+1}")
        
        root = tk.Tk()
        root.title("Dockable Three-Pane Demo")
        root.geometry("900x600")
        
        window = DockableThreePaneWindow(
            root,
            side_width=200,
            left_builder=build_left,
            center_builder=build_center,
            right_builder=build_right
        )
        window.pack(fill=tk.BOTH, expand=True)
        root.mainloop()
    
    def show_fixed():
        root = tk.Tk()
        root.title("Fixed Three-Pane Demo")
        root.geometry("800x500")
        
        layout = FixedThreePaneLayout(root, side_width=180)
        layout.pack(fill=tk.BOTH, expand=True)
        
        layout.set_label_texts(left="Navigation", center="Workspace", right="Properties")
        
        # Add some content
        layout.add_to_left(tk.Button(root, text="Menu Item 1"))
        layout.add_to_left(tk.Button(root, text="Menu Item 2"))
        
        text_widget = tk.Text(root)
        text_widget.insert(tk.END, "This is the fixed layout demo.\nThe panels have fixed positions.")
        layout.add_to_center(text_widget)
        
        layout.add_to_right(tk.Label(root, text="Property 1"))
        layout.add_to_right(tk.Label(root, text="Property 2"))
        
        root.mainloop()
    
    # Create demo selector
    root = tk.Tk()
    root.title("ThreePaneWindows Demo")
    root.geometry("300x200")
    
    tk.Label(root, text="Choose a demo:", font=("Arial", 12)).pack(pady=20)
    
    tk.Button(root, text="Dockable Layout Demo", command=show_dockable, width=20).pack(pady=10)
    tk.Button(root, text="Fixed Layout Demo", command=show_fixed, width=20).pack(pady=10)
    
    root.mainloop()


if __name__ == "__main__":
    run_demo()