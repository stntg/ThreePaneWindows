#!/usr/bin/env python3
"""
Test script specifically for testing the reattach functionality.
"""

import tkinter as tk
from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig
from window_utils import setup_window_geometry

def test_reattach_positioning():
    """Test that panes reattach to the correct positions."""
    
    def build_left(frame):
        tk.Label(frame, text="LEFT PANEL", bg="lightblue", font=("Arial", 12, "bold")).pack(fill="both", expand=True)
        tk.Label(frame, text="This should be on the LEFT side", bg="lightblue").pack(pady=10)
    
    def build_center(frame):
        tk.Label(frame, text="CENTER PANEL", bg="lightgreen", font=("Arial", 12, "bold")).pack(fill="both", expand=True)
        tk.Label(frame, text="This should be in the CENTER", bg="lightgreen").pack(pady=10)
    
    def build_right(frame):
        tk.Label(frame, text="RIGHT PANEL", bg="lightcoral", font=("Arial", 12, "bold")).pack(fill="both", expand=True)
        tk.Label(frame, text="This should be on the RIGHT side", bg="lightcoral").pack(pady=10)
    
    # Create main window with proper sizing
    root = tk.Tk()
    setup_window_geometry(
        root,
        "Reattach Position Test",
        preferred_width=900,
        preferred_height=600,
        min_width=800,
        min_height=500
    )
    
    # Create configurations with clear visual distinctions
    left_config = PaneConfig(
        title="LEFT",
        icon="⬅️",
        default_width=200,
        detachable=True
    )
    
    center_config = PaneConfig(
        title="CENTER",
        icon="🎯",
        detachable=True  # Make center detachable for testing
    )
    
    right_config = PaneConfig(
        title="RIGHT",
        icon="➡️",
        default_width=200,
        detachable=True
    )
    
    # Create enhanced window
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=build_left,
        center_builder=build_center,
        right_builder=build_right,
        theme_name="light"
    )
    window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Add test instructions
    instructions = tk.Text(root, height=6, bg="#f0f0f0")
    instructions.pack(fill=tk.X, padx=10, pady=5)
    
    test_instructions = """REATTACH POSITION TEST:

1. Notice the panel colors: LEFT (blue), CENTER (green), RIGHT (red)
2. Detach the LEFT panel by dragging its header or clicking the detach button
3. Reattach it by closing the detached window or clicking "Reattach"
4. Verify the LEFT panel returns to the LEFT side (not the right side)
5. Repeat with RIGHT panel - it should return to the RIGHT side
6. Test CENTER panel as well

The bug was that LEFT panel was reattaching on the wrong side. This should now be fixed."""
    
    instructions.insert(tk.END, test_instructions)
    instructions.config(state=tk.DISABLED)
    
    # Add programmatic test buttons
    button_frame = tk.Frame(root)
    button_frame.pack(fill=tk.X, padx=10, pady=5)
    
    def test_left_detach_reattach():
        """Test left panel detach/reattach programmatically."""
        if not window.is_pane_detached("left"):
            window._detach_pane("left")
            root.after(2000, lambda: window._reattach_pane("left"))  # Auto-reattach after 2 seconds
        
    def test_right_detach_reattach():
        """Test right panel detach/reattach programmatically."""
        if not window.is_pane_detached("right"):
            window._detach_pane("right")
            root.after(2000, lambda: window._reattach_pane("right"))  # Auto-reattach after 2 seconds
    
    tk.Button(button_frame, text="Test LEFT Panel (Auto)", command=test_left_detach_reattach, 
              bg="lightblue").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Test RIGHT Panel (Auto)", command=test_right_detach_reattach, 
              bg="lightcoral").pack(side=tk.LEFT, padx=5)
    
    # Status label
    status_label = tk.Label(root, text="Ready for testing. Use drag handles or buttons above.", 
                           bg="#e0e0e0", fg="#666666")
    status_label.pack(fill=tk.X, pady=2)
    
    return root

def main():
    """Run the reattach test."""
    print("Testing Enhanced Dockable Reattach Positioning...")
    print("This test verifies that panels reattach to their original positions.")
    
    root = test_reattach_positioning()
    
    print("Test window created!")
    print("Instructions:")
    print("1. Detach panels by dragging headers or using detach buttons")
    print("2. Reattach by closing detached windows or clicking reattach")
    print("3. Verify panels return to correct positions:")
    print("   - LEFT (blue) should return to left side")
    print("   - RIGHT (red) should return to right side")
    print("   - CENTER (green) should return to center")
    
    root.mainloop()

if __name__ == "__main__":
    main()