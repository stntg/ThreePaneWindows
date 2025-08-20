#!/usr/bin/env python3
"""
Complete Integration Demo - ThreePaneWindows with Custom Titlebar

This demo showcases the complete integration of the custom titlebar system
with all ThreePaneWindows modules, demonstrating how it replicates CustomTkinter's
functionality without requiring the library.

Features:
- Automatic custom titlebar integration
- Cross-platform compatibility (Windows, macOS, Linux)
- Theme synchronization
- All ThreePaneWindows module types
- Professional appearance matching CustomTkinter
"""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from threepanewindows.dockable import DockableThreePaneWindow
    from threepanewindows.enhanced_dockable import EnhancedDockableThreePaneWindow
    from threepanewindows.flexible import (
        EnhancedFlexibleLayout,
        FlexContainer,
        FlexPaneConfig,
    )
    from threepanewindows.themes import ThemeType
    from threepanewindows.utils import get_titlebar_theme, platform_handler
except ImportError as e:
    print(f"Error importing ThreePaneWindows: {e}")
    sys.exit(1)


class CompleteIntegrationDemo:
    """Complete demo showing all ThreePaneWindows modules with custom titlebars."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ThreePaneWindows - Complete Integration Demo")
        self.root.geometry("900x700")

        # Current theme
        self.current_theme = "light"

        # Demo windows
        self.demo_windows = {}

        self.setup_main_window()

    def setup_main_window(self):
        """Set up the main demo window."""
        # Apply custom titlebar to main window
        theme = get_titlebar_theme(self.current_theme == "dark")

        try:
            from threepanewindows.utils import apply_custom_titlebar_direct

            titlebar = apply_custom_titlebar_direct(
                self.root, theme, "ThreePaneWindows - Complete Integration Demo"
            )
            if titlebar:
                self.root._custom_titlebar = titlebar
                print("✓ Custom titlebar applied to main window")
        except Exception as e:
            print(f"Note: Custom titlebar not applied to main window: {e}")

        # Main container
        main_frame = tk.Frame(self.root, bg=theme.get("content_bg", "#ffffff"))
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        header_frame = tk.Frame(main_frame, bg=theme.get("content_bg", "#ffffff"))
        header_frame.pack(fill="x", pady=(0, 20))

        title_label = tk.Label(
            header_frame,
            text="ThreePaneWindows Complete Integration Demo",
            font=("Arial", 18, "bold"),
            bg=theme.get("content_bg", "#ffffff"),
            fg=theme.get("fg", "#000000"),
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Custom Titlebar System - No CustomTkinter Required",
            font=("Arial", 12),
            bg=theme.get("content_bg", "#ffffff"),
            fg=theme.get("fg", "#000000"),
        )
        subtitle_label.pack(pady=(5, 0))

        # Platform info
        platform_info = tk.Label(
            header_frame,
            text=f"Platform: {platform_handler.__class__.__name__} | "
            f"Dark Mode: {platform_handler.is_dark_mode()}",
            font=("Arial", 10),
            bg=theme.get("content_bg", "#ffffff"),
            fg=theme.get("fg", "#000000"),
        )
        platform_info.pack(pady=(10, 0))

        # Controls
        controls_frame = tk.Frame(main_frame, bg=theme.get("content_bg", "#ffffff"))
        controls_frame.pack(fill="x", pady=(0, 20))

        # Theme control
        theme_frame = tk.LabelFrame(
            controls_frame, text="Theme Control", font=("Arial", 10)
        )
        theme_frame.pack(fill="x", pady=(0, 10))

        theme_buttons_frame = tk.Frame(theme_frame)
        theme_buttons_frame.pack(pady=10)

        for theme_name in ["light", "dark", "blue"]:
            btn = tk.Button(
                theme_buttons_frame,
                text=f"{theme_name.title()} Theme",
                command=lambda t=theme_name: self.switch_theme(t),
                font=("Arial", 10),
                padx=15,
                pady=5,
            )
            btn.pack(side="left", padx=5)

        # Demo windows
        demo_frame = tk.LabelFrame(
            controls_frame, text="Demo Windows", font=("Arial", 10)
        )
        demo_frame.pack(fill="x", pady=(0, 10))

        demo_buttons_frame = tk.Frame(demo_frame)
        demo_buttons_frame.pack(pady=10)

        demos = [
            ("Basic Dockable", self.show_basic_dockable),
            ("Enhanced Dockable", self.show_enhanced_dockable),
            ("Flexible Layout", self.show_flexible_layout),
            ("Multi-Window Demo", self.show_multi_window_demo),
        ]

        for demo_name, demo_func in demos:
            btn = tk.Button(
                demo_buttons_frame,
                text=demo_name,
                command=demo_func,
                font=("Arial", 10),
                padx=15,
                pady=5,
            )
            btn.pack(side="left", padx=5)

        # Features info
        features_frame = tk.LabelFrame(
            main_frame, text="Custom Titlebar Features", font=("Arial", 12)
        )
        features_frame.pack(fill="both", expand=True)

        features_text = tk.Text(features_frame, wrap="word", font=("Arial", 10))
        features_text.pack(fill="both", expand=True, padx=10, pady=10)

        features_content = """
🎯 CUSTOM TITLEBAR FEATURES (Replicating CustomTkinter without the dependency):

✅ CROSS-PLATFORM COMPATIBILITY:
   • Windows: Native DWM API integration for seamless dark/light titlebar theming
   • macOS: System-wide dark mode support using NSRequiresAquaSystemAppearance
   • Linux: Full custom titlebar with window controls (minimize, maximize, close)

✅ AUTOMATIC INTEGRATION:
   • Works automatically with all ThreePaneWindows modules
   • No code changes required - just use your existing ThreePaneWindows code
   • Seamless theme synchronization across all windows

✅ PLATFORM-SPECIFIC OPTIMIZATIONS:
   • Windows: Uses ctypes.windll.dwmapi for native titlebar coloring
   • macOS: Leverages system commands for native appearance
   • Linux: Custom implementation with drag-and-drop window movement

✅ THEME SYNCHRONIZATION:
   • Automatically matches ThreePaneWindows themes
   • Smooth transitions between light/dark/custom themes
   • Real-time updates when themes change

✅ PROFESSIONAL APPEARANCE:
   • Matches CustomTkinter's visual quality
   • Platform-appropriate fonts and styling
   • Consistent behavior across all operating systems

✅ NO EXTERNAL DEPENDENCIES:
   • Pure Python implementation using only standard libraries
   • No need for CustomTkinter or other external packages
   • Lightweight and efficient

🚀 USAGE:
   Simply use any ThreePaneWindows module as normal - custom titlebars are applied automatically!

   Example:
   ```python
   root = tk.Tk()
   window = EnhancedDockableThreePaneWindow(root, theme_name="dark")
   # Custom titlebar automatically applied with dark theme!
   ```

🔧 TECHNICAL IMPLEMENTATION:
   • Windows: DwmSetWindowAttribute API for native titlebar theming
   • macOS: defaults write -g NSRequiresAquaSystemAppearance -bool No
   • Linux: overrideredirect(True) with custom window controls

This system provides all the benefits of CustomTkinter's titlebar system while being:
   ✓ More lightweight (no external dependencies)
   ✓ More integrated (works seamlessly with existing code)
   ✓ More maintainable (pure Python, actively maintained)
   ✓ More flexible (platform-specific optimizations)
        """

        features_text.insert("1.0", features_content.strip())
        features_text.config(state="disabled")

        # Store references for theme updates
        self.main_frame = main_frame
        self.features_text = features_text

    def switch_theme(self, theme_name):
        """Switch to a different theme."""
        self.current_theme = theme_name
        print(f"Switching to {theme_name} theme...")

        # Update main window titlebar
        if hasattr(self.root, "_custom_titlebar") and self.root._custom_titlebar:
            theme = get_titlebar_theme(theme_name == "dark")
            self.root._custom_titlebar.apply_theme(theme)

            # Update main window background
            self.main_frame.config(bg=theme.get("content_bg", "#ffffff"))

        # Update all demo windows
        for window_name, window in self.demo_windows.items():
            if window and hasattr(window, "set_theme"):
                try:
                    window.set_theme(theme_name)
                    print(f"✓ Updated theme for {window_name}")
                except Exception as e:
                    print(f"! Failed to update theme for {window_name}: {e}")

        print(f"✓ Theme switched to {theme_name}")

    def show_basic_dockable(self):
        """Show basic dockable window demo."""
        if (
            "basic_dockable" in self.demo_windows
            and self.demo_windows["basic_dockable"]
        ):
            self.demo_windows["basic_dockable"].lift()
            return

        demo_window = tk.Toplevel(self.root)
        demo_window.title("Basic Dockable Demo")
        demo_window.geometry("700x500")

        def create_left_panel(parent):
            frame = tk.Frame(parent, bg="#e8f4fd")
            frame.pack(fill="both", expand=True)
            tk.Label(
                frame, text="Left Panel", bg="#e8f4fd", font=("Arial", 12, "bold")
            ).pack(pady=20)
            tk.Label(frame, text="• File Explorer", bg="#e8f4fd").pack(
                anchor="w", padx=20
            )
            tk.Label(frame, text="• Project Tree", bg="#e8f4fd").pack(
                anchor="w", padx=20
            )
            tk.Label(frame, text="• Bookmarks", bg="#e8f4fd").pack(anchor="w", padx=20)

        def create_center_panel(parent):
            frame = tk.Frame(parent, bg="#ffffff")
            frame.pack(fill="both", expand=True)
            tk.Label(
                frame,
                text="Main Content Area",
                bg="#ffffff",
                font=("Arial", 12, "bold"),
            ).pack(pady=20)
            text = tk.Text(frame, wrap="word")
            text.pack(fill="both", expand=True, padx=10, pady=10)
            text.insert(
                "1.0",
                "This is the main content area of the basic dockable window.\n\n"
                "Features:\n"
                "• Drag panels to detach them\n"
                "• Custom titlebar automatically applied\n"
                "• Cross-platform compatibility\n"
                "• Theme synchronization",
            )

        def create_right_panel(parent):
            frame = tk.Frame(parent, bg="#f0f8f0")
            frame.pack(fill="both", expand=True)
            tk.Label(
                frame, text="Right Panel", bg="#f0f8f0", font=("Arial", 12, "bold")
            ).pack(pady=20)
            tk.Label(frame, text="• Properties", bg="#f0f8f0").pack(anchor="w", padx=20)
            tk.Label(frame, text="• Tools", bg="#f0f8f0").pack(anchor="w", padx=20)
            tk.Label(frame, text="• Settings", bg="#f0f8f0").pack(anchor="w", padx=20)

        dockable = DockableThreePaneWindow(
            demo_window,
            left_builder=create_left_panel,
            center_builder=create_center_panel,
            right_builder=create_right_panel,
        )
        dockable.pack(fill="both", expand=True)

        self.demo_windows["basic_dockable"] = demo_window

        def on_close():
            self.demo_windows["basic_dockable"] = None
            demo_window.destroy()

        demo_window.protocol("WM_DELETE_WINDOW", on_close)
        print("✓ Basic dockable window created with custom titlebar")

    def show_enhanced_dockable(self):
        """Show enhanced dockable window demo."""
        if (
            "enhanced_dockable" in self.demo_windows
            and self.demo_windows["enhanced_dockable"]
        ):
            self.demo_windows["enhanced_dockable"].lift()
            return

        demo_window = tk.Toplevel(self.root)
        demo_window.title("Enhanced Dockable Demo")
        demo_window.geometry("800x600")

        def create_left_panel(parent):
            frame = tk.Frame(parent)
            frame.pack(fill="both", expand=True)
            tk.Label(
                frame, text="Enhanced Left Panel", font=("Arial", 12, "bold")
            ).pack(pady=10)

            # Add some interactive elements
            tk.Button(
                frame, text="Action 1", command=lambda: print("Action 1 clicked")
            ).pack(pady=5)
            tk.Button(
                frame, text="Action 2", command=lambda: print("Action 2 clicked")
            ).pack(pady=5)

            # Listbox
            listbox = tk.Listbox(frame)
            listbox.pack(fill="both", expand=True, padx=10, pady=10)
            for i in range(10):
                listbox.insert(tk.END, f"Item {i+1}")

        def create_center_panel(parent):
            frame = tk.Frame(parent)
            frame.pack(fill="both", expand=True)
            tk.Label(
                frame, text="Enhanced Main Content", font=("Arial", 12, "bold")
            ).pack(pady=10)

            # Notebook widget
            notebook = ttk.Notebook(frame)
            notebook.pack(fill="both", expand=True, padx=10, pady=10)

            for i in range(3):
                tab_frame = tk.Frame(notebook)
                notebook.add(tab_frame, text=f"Tab {i+1}")
                tk.Label(tab_frame, text=f"Content for Tab {i+1}").pack(pady=20)

        def create_right_panel(parent):
            frame = tk.Frame(parent)
            frame.pack(fill="both", expand=True)
            tk.Label(
                frame, text="Enhanced Right Panel", font=("Arial", 12, "bold")
            ).pack(pady=10)

            # Some controls
            for i in range(5):
                tk.Checkbutton(frame, text=f"Option {i+1}").pack(
                    anchor="w", padx=20, pady=2
                )

        enhanced = EnhancedDockableThreePaneWindow(
            demo_window,
            left_builder=create_left_panel,
            center_builder=create_center_panel,
            right_builder=create_right_panel,
            theme_name=self.current_theme,
            show_status_bar=True,
            show_toolbar=True,
        )
        enhanced.pack(fill="both", expand=True)

        self.demo_windows["enhanced_dockable"] = enhanced

        def on_close():
            self.demo_windows["enhanced_dockable"] = None
            demo_window.destroy()

        demo_window.protocol("WM_DELETE_WINDOW", on_close)
        print("✓ Enhanced dockable window created with custom titlebar and theming")

    def show_flexible_layout(self):
        """Show flexible layout demo."""
        if (
            "flexible_layout" in self.demo_windows
            and self.demo_windows["flexible_layout"]
        ):
            self.demo_windows["flexible_layout"].lift()
            return

        demo_window = tk.Toplevel(self.root)
        demo_window.title("Flexible Layout Demo")
        demo_window.geometry("750x550")

        # Create flexible layout configuration
        def create_sidebar_content(parent):
            frame = tk.Frame(parent, bg="#f0f0f0")
            frame.pack(fill="both", expand=True)
            tk.Label(
                frame, text="Sidebar", bg="#f0f0f0", font=("Arial", 12, "bold")
            ).pack(pady=10)
            for i in range(5):
                tk.Button(frame, text=f"Menu {i+1}").pack(fill="x", padx=10, pady=2)

        def create_main_content(parent):
            frame = tk.Frame(parent, bg="#ffffff")
            frame.pack(fill="both", expand=True)
            tk.Label(
                frame, text="Main Content", bg="#ffffff", font=("Arial", 12, "bold")
            ).pack(pady=10)
            text = tk.Text(frame)
            text.pack(fill="both", expand=True, padx=10, pady=10)
            text.insert(
                "1.0",
                "Flexible layout with custom titlebar!\n\n"
                "This demonstrates the flexible layout system with:\n"
                "• Custom titlebar integration\n"
                "• Theme synchronization\n"
                "• Cross-platform compatibility",
            )

        def create_properties_content(parent):
            frame = tk.Frame(parent, bg="#f8f8f8")
            frame.pack(fill="both", expand=True)
            tk.Label(
                frame, text="Properties", bg="#f8f8f8", font=("Arial", 12, "bold")
            ).pack(pady=10)
            for prop in ["Width: 200px", "Height: 150px", "Color: Blue", "Font: Arial"]:
                tk.Label(frame, text=prop, bg="#f8f8f8").pack(
                    anchor="w", padx=10, pady=2
                )

        # Create container configuration
        sidebar_pane = FlexPaneConfig(
            name="sidebar",
            title="Sidebar",
            content_builder=create_sidebar_content,
            default_width=200,
            min_width=150,
            max_width=300,
        )

        main_pane = FlexPaneConfig(
            name="main",
            title="Main Content",
            content_builder=create_main_content,
            default_width=400,
        )

        properties_pane = FlexPaneConfig(
            name="properties",
            title="Properties",
            content_builder=create_properties_content,
            default_width=200,
            min_width=150,
        )

        root_container = FlexContainer(
            direction="horizontal", children=[sidebar_pane, main_pane, properties_pane]
        )

        flexible = EnhancedFlexibleLayout(
            demo_window, root_container, theme_name=self.current_theme
        )
        flexible.pack(fill="both", expand=True)

        self.demo_windows["flexible_layout"] = demo_window

        def on_close():
            self.demo_windows["flexible_layout"] = None
            demo_window.destroy()

        demo_window.protocol("WM_DELETE_WINDOW", on_close)
        print("✓ Flexible layout window created with custom titlebar")

    def show_multi_window_demo(self):
        """Show multiple windows with synchronized themes."""
        print("Creating multi-window demo...")

        # Create multiple windows of different types
        windows = []

        # Window 1: Basic dockable
        window1 = tk.Toplevel(self.root)
        window1.title("Multi-Demo: Basic")
        window1.geometry("400x300+100+100")

        def simple_content(parent):
            tk.Label(parent, text="Basic Dockable\nWindow 1", font=("Arial", 12)).pack(
                expand=True
            )

        dockable1 = DockableThreePaneWindow(
            window1,
            left_builder=simple_content,
            center_builder=simple_content,
            right_builder=simple_content,
        )
        dockable1.pack(fill="both", expand=True)
        windows.append(("Basic 1", window1))

        # Window 2: Enhanced dockable
        window2 = tk.Toplevel(self.root)
        window2.title("Multi-Demo: Enhanced")
        window2.geometry("500x400+550+100")

        enhanced2 = EnhancedDockableThreePaneWindow(
            window2,
            left_builder=simple_content,
            center_builder=simple_content,
            right_builder=simple_content,
            theme_name=self.current_theme,
        )
        enhanced2.pack(fill="both", expand=True)
        windows.append(("Enhanced 2", enhanced2))

        # Window 3: Another enhanced with different theme initially
        window3 = tk.Toplevel(self.root)
        window3.title("Multi-Demo: Themed")
        window3.geometry("450x350+300+300")

        enhanced3 = EnhancedDockableThreePaneWindow(
            window3,
            left_builder=simple_content,
            center_builder=simple_content,
            right_builder=simple_content,
            theme_name="blue",
        )
        enhanced3.pack(fill="both", expand=True)
        windows.append(("Themed 3", enhanced3))

        # Store references
        self.demo_windows["multi_window"] = windows

        def close_all():
            for name, window in windows:
                try:
                    window.destroy()
                except:
                    pass
            if "multi_window" in self.demo_windows:
                del self.demo_windows["multi_window"]

        # Set up close handlers
        for name, window in windows:
            if hasattr(window, "protocol"):
                window.protocol("WM_DELETE_WINDOW", close_all)

        print("✓ Multi-window demo created - all windows have custom titlebars")
        messagebox.showinfo(
            "Multi-Window Demo",
            "Created 3 demo windows with custom titlebars!\n\n"
            "• All windows automatically have custom titlebars\n"
            "• Try switching themes to see synchronization\n"
            "• Each window type demonstrates different features",
        )

    def run(self):
        """Run the complete integration demo."""
        print("=" * 60)
        print("ThreePaneWindows Complete Integration Demo")
        print("=" * 60)
        print(f"Platform: {platform_handler.__class__.__name__}")
        print(f"Dark Mode Detected: {platform_handler.is_dark_mode()}")
        print("Custom titlebar system active - no CustomTkinter required!")
        print("=" * 60)

        self.root.mainloop()


def main():
    """Main entry point."""
    try:
        demo = CompleteIntegrationDemo()
        demo.run()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Error running demo: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
