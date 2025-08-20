#!/usr/bin/env python3
"""
Custom Titlebar Demo for ThreePaneWindows

This demo shows how to use the new cross-platform custom titlebar system
that replicates CustomTkinter's functionality without requiring the library.

Features demonstrated:
- Cross-platform custom titlebars (Windows, macOS, Linux)
- Theme switching (light/dark)
- Integration with ThreePaneWindows modules
- Platform-specific optimizations
"""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk

# Add the parent directory to the path so we can import threepanewindows
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from threepanewindows.dockable import DockableThreePaneWindow
    from threepanewindows.enhanced_dockable import EnhancedDockableThreePaneWindow
    from threepanewindows.flexible import EnhancedFlexibleLayout
    from threepanewindows.utils import (
        CustomTitleBarManager,
        apply_custom_titlebar_direct,
        get_titlebar_theme,
        platform_handler,
    )
except ImportError as e:
    print(f"Error importing ThreePaneWindows: {e}")
    print("Make sure you're running this from the examples directory")
    sys.exit(1)


class CustomTitlebarDemo:
    """Demo application showing custom titlebar functionality."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Custom Titlebar Demo - ThreePaneWindows")
        self.root.geometry("800x600")

        # Current theme state
        self.is_dark_theme = False
        self.current_titlebar = None

        # Initialize the demo
        self.setup_demo()

    def setup_demo(self):
        """Set up the demo interface."""
        # Create main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title_label = tk.Label(
            main_frame, text="Custom Titlebar Demo", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Platform info
        platform_info = tk.Label(
            main_frame,
            text=f"Platform: {platform_handler.__class__.__name__}",
            font=("Arial", 10),
        )
        platform_info.pack(pady=(0, 10))

        # Control buttons frame
        controls_frame = tk.Frame(main_frame)
        controls_frame.pack(pady=10)

        # Theme toggle button
        self.theme_button = tk.Button(
            controls_frame,
            text="Switch to Dark Theme",
            command=self.toggle_theme,
            font=("Arial", 10),
            padx=20,
            pady=5,
        )
        self.theme_button.pack(side="left", padx=5)

        # Apply titlebar button
        apply_button = tk.Button(
            controls_frame,
            text="Apply Custom Titlebar",
            command=self.apply_custom_titlebar,
            font=("Arial", 10),
            padx=20,
            pady=5,
        )
        apply_button.pack(side="left", padx=5)

        # Remove titlebar button
        remove_button = tk.Button(
            controls_frame,
            text="Remove Custom Titlebar",
            command=self.remove_custom_titlebar,
            font=("Arial", 10),
            padx=20,
            pady=5,
        )
        remove_button.pack(side="left", padx=5)

        # Demo windows frame
        demo_frame = tk.LabelFrame(main_frame, text="Demo Windows", font=("Arial", 12))
        demo_frame.pack(fill="both", expand=True, pady=20)

        # Demo window buttons
        demo_buttons_frame = tk.Frame(demo_frame)
        demo_buttons_frame.pack(pady=10)

        tk.Button(
            demo_buttons_frame,
            text="Dockable Window Demo",
            command=self.show_dockable_demo,
            font=("Arial", 10),
            padx=15,
            pady=5,
        ).pack(side="left", padx=5)

        tk.Button(
            demo_buttons_frame,
            text="Enhanced Dockable Demo",
            command=self.show_enhanced_demo,
            font=("Arial", 10),
            padx=15,
            pady=5,
        ).pack(side="left", padx=5)

        tk.Button(
            demo_buttons_frame,
            text="Flexible Layout Demo",
            command=self.show_flexible_demo,
            font=("Arial", 10),
            padx=15,
            pady=5,
        ).pack(side="left", padx=5)

        # Info text
        info_text = tk.Text(demo_frame, height=10, wrap="word")
        info_text.pack(fill="both", expand=True, padx=10, pady=10)

        info_content = """
Custom Titlebar Features:

• Windows: Uses native titlebar with DWM API for dark/light theming
• macOS: Enables system-wide dark titlebar support like CustomTkinter
• Linux: Full custom titlebar with window controls (minimize, maximize, close)

Platform-Specific Optimizations:
• Windows: Leverages Windows DWM API for seamless integration
• macOS: Uses system commands for native appearance
• Linux: Custom implementation with drag-and-drop window movement

Theme Support:
• Light and dark themes
• Platform-appropriate fonts and colors
• Smooth theme transitions
• Integration with ThreePaneWindows theming system

Usage:
1. Click "Apply Custom Titlebar" to enable custom titlebar
2. Use "Switch Theme" to toggle between light and dark themes
3. Try the demo windows to see integration with ThreePaneWindows modules
4. Click "Remove Custom Titlebar" to restore native titlebar
        """

        info_text.insert("1.0", info_content.strip())
        info_text.config(state="disabled")

        # Apply initial theme
        self.apply_theme()

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.is_dark_theme = not self.is_dark_theme
        self.theme_button.config(
            text=(
                "Switch to Light Theme"
                if self.is_dark_theme
                else "Switch to Dark Theme"
            )
        )
        self.apply_theme()

    def apply_theme(self):
        """Apply the current theme to the window."""
        theme = get_titlebar_theme(self.is_dark_theme)

        # Apply theme to main window
        self.root.config(bg=theme["content_bg"])

        # Update titlebar if it exists
        if self.current_titlebar:
            self.current_titlebar.apply_theme(theme)

    def apply_custom_titlebar(self):
        """Apply custom titlebar to the main window."""
        try:
            theme = get_titlebar_theme(self.is_dark_theme)

            # Remove existing titlebar if any
            if self.current_titlebar:
                self.current_titlebar.destroy()

            # Apply new titlebar
            self.current_titlebar = apply_custom_titlebar_direct(
                self.root, theme, "Custom Titlebar Demo - ThreePaneWindows"
            )

            if self.current_titlebar:
                print("Custom titlebar applied successfully!")
            else:
                print("Failed to apply custom titlebar")

        except Exception as e:
            print(f"Error applying custom titlebar: {e}")

    def remove_custom_titlebar(self):
        """Remove custom titlebar and restore native titlebar."""
        try:
            if self.current_titlebar:
                self.current_titlebar.destroy()
                self.current_titlebar = None

                # Restore native titlebar (platform-specific)
                if hasattr(self.root, "overrideredirect"):
                    self.root.overrideredirect(False)

                print("Custom titlebar removed successfully!")
            else:
                print("No custom titlebar to remove")

        except Exception as e:
            print(f"Error removing custom titlebar: {e}")

    def show_dockable_demo(self):
        """Show dockable three-pane window demo with custom titlebar."""
        try:
            demo_window = tk.Toplevel(self.root)
            demo_window.title("Dockable Demo with Custom Titlebar")
            demo_window.geometry("600x400")

            # Apply custom titlebar to demo window
            theme = get_titlebar_theme(self.is_dark_theme)
            titlebar = apply_custom_titlebar_direct(demo_window, theme, "Dockable Demo")

            # Create dockable layout
            def create_left_panel(parent):
                label = tk.Label(parent, text="Left Panel", bg="lightblue")
                label.pack(fill="both", expand=True)

            def create_center_panel(parent):
                label = tk.Label(parent, text="Center Panel", bg="lightgreen")
                label.pack(fill="both", expand=True)

            def create_right_panel(parent):
                label = tk.Label(parent, text="Right Panel", bg="lightcoral")
                label.pack(fill="both", expand=True)

            dockable = DockableThreePaneWindow(
                demo_window,
                left_builder=create_left_panel,
                center_builder=create_center_panel,
                right_builder=create_right_panel,
            )
            dockable.pack(fill="both", expand=True)

        except Exception as e:
            print(f"Error creating dockable demo: {e}")

    def show_enhanced_demo(self):
        """Show enhanced dockable demo with custom titlebar."""
        try:
            demo_window = tk.Toplevel(self.root)
            demo_window.title("Enhanced Dockable Demo with Custom Titlebar")
            demo_window.geometry("700x500")

            # Apply custom titlebar to demo window
            theme = get_titlebar_theme(self.is_dark_theme)
            titlebar = apply_custom_titlebar_direct(
                demo_window, theme, "Enhanced Dockable Demo"
            )

            # Create enhanced dockable layout
            def create_left_panel(parent):
                frame = tk.Frame(parent, bg="#f0f0f0")
                frame.pack(fill="both", expand=True)
                tk.Label(frame, text="Enhanced Left Panel", bg="#f0f0f0").pack(pady=20)
                tk.Button(frame, text="Sample Button").pack(pady=5)

            def create_center_panel(parent):
                frame = tk.Frame(parent, bg="#ffffff")
                frame.pack(fill="both", expand=True)
                tk.Label(frame, text="Enhanced Center Panel", bg="#ffffff").pack(
                    pady=20
                )
                text = tk.Text(frame, height=10)
                text.pack(fill="both", expand=True, padx=10, pady=10)
                text.insert(
                    "1.0", "This is an enhanced dockable window with custom titlebar!"
                )

            def create_right_panel(parent):
                frame = tk.Frame(parent, bg="#f8f8f8")
                frame.pack(fill="both", expand=True)
                tk.Label(frame, text="Enhanced Right Panel", bg="#f8f8f8").pack(pady=20)
                for i in range(3):
                    tk.Checkbutton(frame, text=f"Option {i+1}", bg="#f8f8f8").pack(
                        anchor="w", padx=20
                    )

            # Note: This is a simplified version - in practice you'd use the actual
            # EnhancedDockableThreePaneWindow class with proper configuration
            dockable = DockableThreePaneWindow(
                demo_window,
                left_builder=create_left_panel,
                center_builder=create_center_panel,
                right_builder=create_right_panel,
            )
            dockable.pack(fill="both", expand=True)

        except Exception as e:
            print(f"Error creating enhanced demo: {e}")

    def show_flexible_demo(self):
        """Show flexible layout demo with custom titlebar."""
        try:
            demo_window = tk.Toplevel(self.root)
            demo_window.title("Flexible Layout Demo with Custom Titlebar")
            demo_window.geometry("800x600")

            # Apply custom titlebar to demo window
            theme = get_titlebar_theme(self.is_dark_theme)
            titlebar = apply_custom_titlebar_direct(
                demo_window, theme, "Flexible Layout Demo"
            )

            # Create flexible layout
            main_frame = tk.Frame(demo_window)
            main_frame.pack(fill="both", expand=True)

            # Create a simple flexible layout demonstration
            paned_window = tk.PanedWindow(main_frame, orient="horizontal")
            paned_window.pack(fill="both", expand=True)

            # Left pane
            left_frame = tk.Frame(paned_window, bg="lightblue", width=200)
            tk.Label(left_frame, text="Flexible Left Pane", bg="lightblue").pack(
                pady=20
            )
            paned_window.add(left_frame)

            # Center pane
            center_frame = tk.Frame(paned_window, bg="lightgreen")
            tk.Label(center_frame, text="Flexible Center Pane", bg="lightgreen").pack(
                pady=20
            )
            paned_window.add(center_frame)

            # Right pane
            right_frame = tk.Frame(paned_window, bg="lightcoral", width=200)
            tk.Label(right_frame, text="Flexible Right Pane", bg="lightcoral").pack(
                pady=20
            )
            paned_window.add(right_frame)

        except Exception as e:
            print(f"Error creating flexible demo: {e}")

    def run(self):
        """Run the demo application."""
        print("Starting Custom Titlebar Demo...")
        print(f"Platform: {platform_handler.__class__.__name__}")
        print("Use the buttons to test custom titlebar functionality!")

        self.root.mainloop()


def main():
    """Main entry point for the demo."""
    try:
        demo = CustomTitlebarDemo()
        demo.run()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Error running demo: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
