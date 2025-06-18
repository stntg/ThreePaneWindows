#!/usr/bin/env python3
"""
Simple test script to run both examples independently.
"""

import tkinter as tk
from threepanewindows import DockableThreePaneWindow, FixedThreePaneLayout


def run_dockable_test():
    """Run dockable example for testing."""
    print("Starting Dockable Layout test...")
    
    def build_left(frame):
        tk.Label(frame, text="File Explorer", font=("Arial", 10, "bold")).pack(pady=5)
        files = ["main.py", "utils.py", "config.py", "README.md"]
        for file in files:
            tk.Label(frame, text=f"📄 {file}", anchor="w").pack(fill="x", padx=5, pady=1)
    
    def build_center(frame):
        tk.Label(frame, text="Code Editor", font=("Arial", 10, "bold")).pack(pady=5)
        text = tk.Text(frame, wrap=tk.WORD, font=("Consolas", 10))
        text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text.insert(tk.END, "# Sample Python Code\nprint('Hello from Dockable Layout!')")
    
    def build_right(frame):
        tk.Label(frame, text="Properties", font=("Arial", 10, "bold")).pack(pady=5)
        props = ["File: main.py", "Size: 1.2 KB", "Lines: 25", "Modified: Today"]
        for prop in props:
            tk.Label(frame, text=prop, anchor="w").pack(fill="x", padx=5, pady=1)
    
    root = tk.Tk()
    root.title("Dockable Three-Pane Test")
    root.geometry("900x600")
    
    window = DockableThreePaneWindow(
        root,
        side_width=200,
        left_builder=build_left,
        center_builder=build_center,
        right_builder=build_right
    )
    window.pack(fill=tk.BOTH, expand=True)
    
    # Add close button
    close_btn = tk.Button(root, text="Close Test", command=root.destroy, 
                         bg="red", fg="white", font=("Arial", 10, "bold"))
    close_btn.pack(side=tk.BOTTOM, pady=5)
    
    print("✓ Dockable layout window opened")
    root.mainloop()


def run_fixed_test():
    """Run fixed example for testing."""
    print("Starting Fixed Layout test...")
    
    root = tk.Tk()
    root.title("Fixed Three-Pane Test")
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
    text_widget.insert(tk.END, "This is a test of the fixed layout functionality.")
    
    # Add tools
    tools = ["🔍 Search", "📊 Analytics", "⚙️ Settings", "💾 Export"]
    for tool in tools:
        btn = tk.Button(layout.frame_right, text=tool, width=12)
        btn.pack(pady=2, padx=5)
    
    # Add close button
    close_btn = tk.Button(root, text="Close Test", command=root.destroy,
                         bg="red", fg="white", font=("Arial", 10, "bold"))
    close_btn.pack(side=tk.BOTTOM, pady=5)
    
    print("✓ Fixed layout window opened")
    root.mainloop()


def main():
    """Main function to choose which test to run."""
    print("ThreePaneWindows - Individual Example Tests")
    print("=" * 45)
    print("1. Test Dockable Layout")
    print("2. Test Fixed Layout")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                run_dockable_test()
            elif choice == "2":
                run_fixed_test()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()