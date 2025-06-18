#!/usr/bin/env python3
"""
Test script for the enhanced dockable three-pane window.
"""

import tkinter as tk
from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig, get_theme_manager

def test_enhanced_features():
    """Test the enhanced features."""
    
    def build_simple_left(frame):
        tk.Label(frame, text="Left Panel Content", bg=frame.cget('bg')).pack(pady=20)
        tk.Button(frame, text="Test Button").pack(pady=5)
    
    def build_simple_center(frame):
        tk.Label(frame, text="Center Panel Content", bg=frame.cget('bg')).pack(pady=20)
        text = tk.Text(frame, height=10)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert(tk.END, "This is the enhanced three-pane window!\n\n")
        text.insert(tk.END, "Features:\n")
        text.insert(tk.END, "• Professional theming\n")
        text.insert(tk.END, "• Drag-and-drop detaching\n")
        text.insert(tk.END, "• Customizable panels\n")
        text.insert(tk.END, "• Beautiful UI\n")
    
    def build_simple_right(frame):
        tk.Label(frame, text="Right Panel Content", bg=frame.cget('bg')).pack(pady=20)
        
        # Theme switcher
        tk.Label(frame, text="Theme:", bg=frame.cget('bg')).pack()
        
        def change_theme(theme_name):
            window.set_theme(theme_name)
        
        themes = ["light", "dark", "blue"]
        for theme in themes:
            btn = tk.Button(frame, text=theme.title(), 
                          command=lambda t=theme: change_theme(t))
            btn.pack(pady=2)
    
    # Create main window
    root = tk.Tk()
    root.title("Enhanced Three-Pane Window Test")
    root.geometry("900x600")
    
    # Create configurations
    left_config = PaneConfig(
        title="Test Left",
        icon="🔍",
        default_width=200,
        detachable=True
    )
    
    center_config = PaneConfig(
        title="Test Center",
        icon="📝",
        detachable=False
    )
    
    right_config = PaneConfig(
        title="Test Right",
        icon="⚙️",
        default_width=180,
        detachable=True
    )
    
    # Create enhanced window
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=build_simple_left,
        center_builder=build_simple_center,
        right_builder=build_simple_right,
        theme_name="light"
    )
    window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Add instructions
    instructions = tk.Label(
        root,
        text="Instructions: Drag panel headers to detach • Use theme buttons to change appearance",
        bg="#f0f0f0",
        fg="#666666",
        font=("Arial", 9)
    )
    instructions.pack(side=tk.BOTTOM, fill=tk.X, pady=2)
    
    return root

def main():
    """Run the test."""
    print("Testing Enhanced Dockable Three-Pane Window...")
    
    # Test theme manager
    theme_manager = get_theme_manager()
    print(f"Current theme: {theme_manager.get_current_theme().name}")
    
    # Test theme switching
    themes = ["light", "dark", "blue"]
    for theme in themes:
        success = theme_manager.set_theme(theme)
        print(f"Theme '{theme}': {'✓' if success else '✗'}")
    
    # Reset to light theme
    theme_manager.set_theme("light")
    
    # Create and run test window
    root = test_enhanced_features()
    
    print("Test window created successfully!")
    print("Try the following:")
    print("1. Drag panel headers to detach panels")
    print("2. Use theme buttons to change appearance")
    print("3. Resize panels by dragging separators")
    print("4. Close detached windows to reattach")
    
    root.mainloop()

if __name__ == "__main__":
    main()