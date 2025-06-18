#!/usr/bin/env python3
"""
Quick verification script for panel positioning logic.
"""

import tkinter as tk
from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig
from window_utils import setup_window_geometry

def quick_test():
    """Quick test of positioning logic."""
    
    def build_simple(frame, text, color):
        label = tk.Label(frame, text=text, bg=color, font=("Arial", 14, "bold"))
        label.pack(fill="both", expand=True)
    
    root = tk.Tk()
    setup_window_geometry(
        root,
        "Quick Position Test",
        preferred_width=800,
        preferred_height=400,
        min_width=600,
        min_height=300
    )
    
    # Simple configs
    left_config = PaneConfig(title="LEFT", icon="L", default_width=150, detachable=True)
    center_config = PaneConfig(title="CENTER", icon="C", detachable=False)
    right_config = PaneConfig(title="RIGHT", icon="R", default_width=150, detachable=True)
    
    # Create window
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=lambda f: build_simple(f, "LEFT\nPANEL", "#ffcccc"),
        center_builder=lambda f: build_simple(f, "CENTER\nPANEL", "#ccffcc"),
        right_builder=lambda f: build_simple(f, "RIGHT\nPANEL", "#ccccff"),
        theme_name="light"
    )
    window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Test buttons
    test_frame = tk.Frame(root)
    test_frame.pack(fill=tk.X, pady=5)
    
    def test_sequence():
        """Run automated test sequence."""
        print("Starting automated test...")
        
        # Test left panel
        print("1. Detaching left panel...")
        window._detach_pane("left")
        
        root.after(1500, lambda: [
            print("2. Reattaching left panel..."),
            window._reattach_pane("left")
        ])
        
        # Test right panel
        root.after(3000, lambda: [
            print("3. Detaching right panel..."),
            window._detach_pane("right")
        ])
        
        root.after(4500, lambda: [
            print("4. Reattaching right panel..."),
            window._reattach_pane("right"),
            print("Test complete! Check that panels are in correct positions.")
        ])
    
    tk.Button(test_frame, text="Run Automated Test", command=test_sequence, 
              bg="lightgreen").pack(side=tk.LEFT, padx=5)
    
    tk.Label(test_frame, text="Expected: LEFT(red) | CENTER(green) | RIGHT(blue)", 
             font=("Arial", 10)).pack(side=tk.RIGHT, padx=5)
    
    return root

if __name__ == "__main__":
    print("Quick positioning verification...")
    root = quick_test()
    root.mainloop()