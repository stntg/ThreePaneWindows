#!/usr/bin/env python3
"""
Demonstration of platform-specific functionality in ThreePaneWindows.

This example shows how the platform separation allows for:
1. Platform-specific icon format recommendations
2. Platform-specific icon handling
3. Platform-specific titlebar customization
4. Automatic platform detection and handling
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

# Add the threepanewindows package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "."))

from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig, ThemeManager
from threepanewindows.platform import platform_handler


def create_left_content(parent):
    """Create content for the left pane."""
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    ttk.Label(frame, text="Platform Information", font=("Arial", 14, "bold")).pack(
        pady=5
    )

    # Platform information
    platform_info = platform_handler.__class__.__name__
    ttk.Label(frame, text=f"Handler: {platform_info}").pack(anchor="w", pady=2)

    icon_formats = platform_handler.get_recommended_icon_formats()
    ttk.Label(frame, text=f"Icon formats: {', '.join(icon_formats)}").pack(
        anchor="w", pady=2
    )

    # Test icon validation
    ttk.Label(frame, text="Icon Validation Tests:", font=("Arial", 10, "bold")).pack(
        anchor="w", pady=(10, 5)
    )

    test_files = ["test.ico", "test.png", "test.gif", "test.xbm", "test.unknown"]
    for test_file in test_files:
        valid, message = platform_handler.validate_icon_path(test_file)
        status = "✓" if valid else "✗"
        ttk.Label(frame, text=f"{status} {test_file}").pack(anchor="w", pady=1)

    return frame


def create_center_content(parent):
    """Create content for the center pane."""
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    ttk.Label(frame, text="Platform Demo", font=("Arial", 14, "bold")).pack(pady=5)

    # Add theme switching controls
    ttk.Label(frame, text="Theme Controls:", font=("Arial", 10, "bold")).pack(
        anchor="w", pady=(10, 5)
    )

    theme_var = tk.StringVar(value="light")
    themes = ["light", "dark", "blue", "green", "purple"]

    # Store references that will be set by main function
    theme_var._window_ref = None
    theme_var._theme_manager_ref = None

    def change_theme():
        theme_name = theme_var.get()
        window = theme_var._window_ref
        theme_manager = theme_var._theme_manager_ref

        if window and theme_manager:
            # Get the root window
            root = window.winfo_toplevel()
            success = theme_manager.set_theme(theme_name, window=root)
            print(f"Theme changed to {theme_name}: {success}")

            # Apply platform-specific titlebar customization
            platform_handler.apply_custom_titlebar(
                root, theme_manager.get_current_theme().colors
            )

            # Refresh the UI to apply the new theme
            if hasattr(window, "refresh_ui"):
                window.refresh_ui()
            else:
                # Fallback: force update
                window.update_idletasks()
        else:
            print(f"Warning: Cannot change theme - missing references")

    theme_frame = ttk.Frame(frame)
    theme_frame.pack(anchor="w", pady=5)

    for theme in themes:
        ttk.Radiobutton(
            theme_frame,
            text=theme.title(),
            variable=theme_var,
            value=theme,
            command=change_theme,
        ).pack(side="left", padx=5)

    # Store the theme_var for later reference setting
    frame._theme_var = theme_var

    # Instructions
    ttk.Label(frame, text="Instructions:", font=("Arial", 10, "bold")).pack(
        anchor="w", pady=(20, 5)
    )
    instructions = [
        "• Try different themes to see platform-specific changes",
        "• Drag pane headers to detach them into separate windows",
        "• Notice platform-specific icon format recommendations",
        "• Platform separation provides better maintainability",
    ]

    for instruction in instructions:
        ttk.Label(frame, text=instruction).pack(anchor="w", pady=1)

    return frame


def create_right_content(parent):
    """Create content for the right pane."""
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    ttk.Label(frame, text="Platform Features", font=("Arial", 14, "bold")).pack(pady=5)

    # Show platform-specific capabilities
    if hasattr(platform_handler, "get_desktop_environment"):
        desktop = platform_handler.get_desktop_environment()
        ttk.Label(frame, text=f"Desktop: {desktop}").pack(anchor="w", pady=2)

    if hasattr(platform_handler, "supports_transparency"):
        transparency = platform_handler.supports_transparency()
        ttk.Label(frame, text=f"Transparency: {transparency}").pack(anchor="w", pady=2)

    # Platform-specific features
    ttk.Label(frame, text="Features:", font=("Arial", 10, "bold")).pack(
        anchor="w", pady=(10, 5)
    )

    if platform_handler.__class__.__name__ == "WindowsPlatformHandler":
        features = [
            "• Native titlebar color customization",
            "• ICO format optimization",
            "• DWM API integration",
        ]
    elif platform_handler.__class__.__name__ == "MacOSPlatformHandler":
        features = [
            "• Custom titlebar with macOS controls",
            "• PNG format optimization",
            "• Draggable titlebar",
        ]
    else:  # Linux
        features = [
            "• Desktop environment detection",
            "• Transparency support detection",
            "• Window manager integration",
        ]

    for feature in features:
        ttk.Label(frame, text=feature).pack(anchor="w", pady=1)

    return frame


def main():
    """Run the platform demonstration."""
    print("ThreePaneWindows Platform Separation Demo")
    print("=" * 50)
    print(f"Detected platform handler: {platform_handler.__class__.__name__}")
    print(
        f"Recommended icon formats: {platform_handler.get_recommended_icon_formats()}"
    )
    print()

    # Create main window
    root = tk.Tk()
    root.title("Platform Separation Demo - ThreePaneWindows")
    root.geometry("1000x700")

    # Create theme manager
    theme_manager = ThemeManager()

    # Configure panes with platform-specific settings
    left_config = PaneConfig(
        title="Platform Info",
        icon="📊",  # Using emoji as icon for demo
        detachable=True,
        resizable=True,
        min_width=200,
        max_width=400,
        default_width=250,
    )

    center_config = PaneConfig(
        title="Main Content", icon="📄", detachable=True, resizable=True, min_width=300
    )

    right_config = PaneConfig(
        title="Tools",
        icon="🔧",
        detachable=True,
        resizable=True,
        min_width=200,
        max_width=350,
        default_width=250,
    )

    # Create the three-pane window with builders
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=create_left_content,
        center_builder=create_center_content,
        right_builder=create_right_content,
        theme_name="light",
    )
    window.pack(fill="both", expand=True)

    # Set up theme change references
    # Find the center content frame and set the references
    def find_theme_var(widget):
        """Recursively find the theme_var in the widget hierarchy."""
        if hasattr(widget, "_theme_var"):
            return widget._theme_var
        for child in widget.winfo_children():
            result = find_theme_var(child)
            if result:
                return result
        return None

    # Wait for the window to be fully created, then set references
    def setup_theme_references():
        theme_var = find_theme_var(window)
        if theme_var:
            theme_var._window_ref = window
            theme_var._theme_manager_ref = window.theme_manager
            print("Theme change references set up successfully")
        else:
            print("Warning: Could not find theme_var to set up references")

    # Schedule the setup after the window is fully created
    root.after(100, setup_theme_references)

    print("Demo window created. Try switching themes and detaching panes!")
    print("Close the window to exit.")

    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()
