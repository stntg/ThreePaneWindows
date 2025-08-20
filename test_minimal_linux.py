#!/usr/bin/env python3
"""
Minimal test for Linux demo components
"""

import os
import sys
import tkinter as tk

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def test_basic_layout():
    """Test basic flexible layout without all the complexity."""
    try:
        from threepanewindows.central_theme_manager import get_theme_manager
        from threepanewindows.flexible import (
            EnhancedFlexibleLayout,
            FlexContainer,
            FlexPaneConfig,
            LayoutDirection,
        )

        root = tk.Tk()
        root.title("Minimal Linux Test")
        root.geometry("800x600")

        # Simple pane builder
        def build_simple_content(parent):
            label = tk.Label(parent, text="Test Content", font=("Arial", 12))
            label.pack(expand=True)

        # Create simple pane config
        pane_config = FlexPaneConfig(
            name="test_pane",
            title="Test Pane",
            weight=1.0,
            min_size=200,
            builder=build_simple_content,
        )

        # Create simple container
        container = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        # Create layout
        layout = EnhancedFlexibleLayout(
            root,
            container,
            theme_name="light",
        )
        layout.pack(fill="both", expand=True)

        print("Layout created successfully")

        # Run for a short time to test
        root.after(2000, root.quit)  # Close after 2 seconds
        root.mainloop()

        return True

    except Exception as e:
        print(f"Error in basic layout test: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_theme_manager():
    """Test theme manager functionality."""
    try:
        from threepanewindows.central_theme_manager import (
            ThemeType,
            get_theme_manager,
            set_global_theme,
        )

        theme_manager = get_theme_manager()
        print(f"Current theme: {theme_manager.current_theme}")

        # Test theme switching
        set_global_theme(ThemeType.DARK)
        theme = theme_manager.get_current_theme()
        print(f"Dark theme colors: bg={theme.primary_bg}, fg={theme.primary_text}")

        return True

    except Exception as e:
        print(f"Error in theme manager test: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    print("Testing Linux demo components...")

    # Test theme manager first
    if not test_theme_manager():
        print("Theme manager test failed")
        return 1

    print("Theme manager test passed")

    # Test basic layout
    if not test_basic_layout():
        print("Basic layout test failed")
        return 1

    print("Basic layout test passed")
    print("All tests completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
