#!/usr/bin/env python3
"""
Quick verification script for fixed width features.
"""

import tkinter as tk
from threepanewindows import FixedThreePaneLayout, DockableThreePaneWindow, EnhancedDockableThreePaneWindow, PaneConfig

def test_fixed_layout():
    """Test FixedThreePaneLayout with fixed width."""
    print("Testing FixedThreePaneLayout...")
    
    root = tk.Tk()
    root.withdraw()  # Hide window for testing
    
    # Create menu
    menu = tk.Menu(root)
    file_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=file_menu)
    
    # Test with fixed left, resizable right
    layout = FixedThreePaneLayout(
        root,
        left_fixed_width=200,
        right_fixed_width=None,
        menu_bar=menu
    )
    
    # Test methods
    assert layout.is_left_fixed() == True
    assert layout.is_right_fixed() == False
    assert layout.get_left_width() == 200
    
    # Test dynamic changes
    layout.set_right_width(150)
    assert layout.is_right_fixed() == True
    assert layout.get_right_width() == 150
    
    root.destroy()
    print("✓ FixedThreePaneLayout tests passed")

def test_dockable_window():
    """Test DockableThreePaneWindow with fixed width."""
    print("Testing DockableThreePaneWindow...")
    
    root = tk.Tk()
    root.withdraw()  # Hide window for testing
    
    def dummy_builder(frame):
        tk.Label(frame, text="Test").pack()
    
    # Create menu
    menu = tk.Menu(root)
    
    # Test with both sides fixed
    window = DockableThreePaneWindow(
        root,
        left_builder=dummy_builder,
        center_builder=dummy_builder,
        right_builder=dummy_builder,
        left_fixed_width=180,
        right_fixed_width=150,
        menu_bar=menu
    )
    
    # Test methods
    assert window.is_left_fixed() == True
    assert window.is_right_fixed() == True
    
    # Test dynamic changes
    window.clear_left_fixed_width()
    assert window.is_left_fixed() == False
    
    window.set_right_fixed_width(200)
    assert window.is_right_fixed() == True
    
    root.destroy()
    print("✓ DockableThreePaneWindow tests passed")

def test_enhanced_window():
    """Test EnhancedDockableThreePaneWindow with fixed width."""
    print("Testing EnhancedDockableThreePaneWindow...")
    
    root = tk.Tk()
    root.withdraw()  # Hide window for testing
    
    def dummy_builder(frame):
        tk.Label(frame, text="Test").pack()
    
    # Create menu
    menu = tk.Menu(root)
    
    # Configure with fixed widths
    left_config = PaneConfig(
        title="Left",
        fixed_width=250
    )
    
    center_config = PaneConfig(
        title="Center"
    )
    
    right_config = PaneConfig(
        title="Right",
        fixed_width=200
    )
    
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=dummy_builder,
        center_builder=dummy_builder,
        right_builder=dummy_builder,
        menu_bar=menu
    )
    
    # Test methods
    assert window.is_pane_fixed_width("left") == True
    assert window.is_pane_fixed_width("right") == True
    assert window.is_pane_fixed_width("center") == False
    assert window.get_pane_width("left") == 250
    assert window.get_pane_width("right") == 200
    
    # Test dynamic changes
    window.clear_pane_fixed_width("left")
    assert window.is_pane_fixed_width("left") == False
    
    window.set_pane_fixed_width("right", 180)
    assert window.get_pane_width("right") == 180
    
    root.destroy()
    print("✓ EnhancedDockableThreePaneWindow tests passed")

def main():
    """Run all tests."""
    print("Verifying fixed width features...")
    print()
    
    try:
        test_fixed_layout()
        test_dockable_window()
        test_enhanced_window()
        
        print()
        print("🎉 All tests passed! Fixed width features are working correctly.")
        print()
        print("Features verified:")
        print("• Fixed width pane configuration")
        print("• Menu bar integration")
        print("• Dynamic width control")
        print("• Mixed fixed/resizable configurations")
        print("• All three window types support")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()