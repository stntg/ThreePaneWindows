"""
Example applications demonstrating the use of ThreePaneWindows.
"""

import threading
import time
import tkinter as tk

from .dockable import DockableThreePaneWindow
from .enhanced_dockable import EnhancedDockableThreePaneWindow, PaneConfig
from .fixed import FixedThreePaneLayout


def run_demo_with_timeout(timeout_seconds=5, interactive=False):
    """Run demo with automatic timeout for testing.

    Args:
        timeout_seconds (int): Maximum time to run before closing
        interactive (bool): Whether to run in interactive mode

    Returns:
        bool: True if demo ran successfully, False if timeout or error
    """
    # For non-interactive mode, just run directly without threading
    # to avoid TTK theme issues with threads
    if not interactive:
        try:
            run_demo(interactive=False)
            return True
        except Exception:
            return False

    # For interactive mode, use threading with timeout
    success = False
    error = None

    def run_demo_thread():
        nonlocal success, error
        try:
            run_demo(interactive=interactive, auto_close_delay=timeout_seconds * 1000)
            success = True
        except Exception as e:
            error = e

    thread = threading.Thread(target=run_demo_thread, daemon=True)
    thread.start()
    thread.join(timeout=timeout_seconds + 1)

    if thread.is_alive():
        # Thread is still running, demo might be hanging
        return False

    if error:
        # For testing purposes, don't raise the error, just return False
        return False

    return success


def test_all_demo_components():
    """Test that all demo components can be created without errors.

    Returns:
        dict: Results of component tests
    """
    results = {
        "dockable_window": False,
        "fixed_layout": False,
        "enhanced_window": False,
        "builders": False,
    }

    try:
        # Test basic Tkinter availability
        root = tk.Tk()
        root.withdraw()

        # Test DockableThreePaneWindow creation
        try:

            def dummy_builder(frame):
                tk.Label(frame, text="Test").pack()

            window = DockableThreePaneWindow(
                root,
                side_width=200,
                left_builder=dummy_builder,
                center_builder=dummy_builder,
                right_builder=dummy_builder,
            )
            results["dockable_window"] = True
            window.destroy()
        except Exception:
            pass

        # Test FixedThreePaneLayout creation
        try:
            layout = FixedThreePaneLayout(root, side_width=180)
            results["fixed_layout"] = True
            layout.destroy()
        except Exception:
            pass

        # Test EnhancedDockableThreePaneWindow creation with error handling
        try:
            config = PaneConfig(title="Test", icon="🔧")
            try:
                window = EnhancedDockableThreePaneWindow(
                    root,
                    left_config=config,
                    center_config=config,
                    right_config=config,
                    left_builder=dummy_builder,
                    center_builder=dummy_builder,
                    right_builder=dummy_builder,
                    theme_name="light",  # Use simple theme
                    enable_animations=False,  # Disable animations for testing
                )
                results["enhanced_window"] = True
                window.destroy()
            except (RuntimeError, tk.TclError) as e:
                # If theme issues occur, try without theme
                if "main thread" in str(e) or "theme" in str(e).lower():
                    # Skip enhanced window test if theme issues
                    pass
                else:
                    raise
        except Exception:
            pass

        # Test builder functions
        try:
            frame = tk.Frame(root)
            dummy_builder(frame)
            results["builders"] = True
            frame.destroy()
        except Exception:
            pass

        root.destroy()

    except Exception:
        pass

    return results


def test_basic_demo_components():
    """Test basic demo components without enhanced features.

    Returns:
        dict: Results of basic component tests
    """
    results = {"dockable_window": False, "fixed_layout": False, "builders": False}

    try:
        # Test basic Tkinter availability
        root = tk.Tk()
        root.withdraw()

        # Test DockableThreePaneWindow creation
        try:

            def dummy_builder(frame):
                tk.Label(frame, text="Test").pack()

            window = DockableThreePaneWindow(
                root,
                side_width=200,
                left_builder=dummy_builder,
                center_builder=dummy_builder,
                right_builder=dummy_builder,
            )
            results["dockable_window"] = True
            window.destroy()
        except Exception:
            pass

        # Test FixedThreePaneLayout creation
        try:
            layout = FixedThreePaneLayout(root, side_width=180)
            results["fixed_layout"] = True
            layout.destroy()
        except Exception:
            pass

        # Test builder functions
        try:
            frame = tk.Frame(root)
            dummy_builder(frame)
            results["builders"] = True
            frame.destroy()
        except Exception:
            pass

        root.destroy()

    except Exception:
        pass

    return results


def run_demo(interactive=True, auto_close_delay=None):
    """Run a simple demo of both layout types.

    Args:
        interactive (bool): If True, run in interactive mode with mainloop.
                           If False, create windows but don't start mainloop.
        auto_close_delay (int): If provided, automatically close windows after
                               this many milliseconds (for testing).
    """

    def show_dockable():
        def build_left(frame):
            tk.Label(frame, text="Left Panel Content").pack(pady=10)
            tk.Button(frame, text="Sample Button").pack(pady=5)

        def build_center(frame):
            tk.Label(frame, text="Center Panel Content").pack(pady=10)
            text = tk.Text(frame, height=10)
            text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text.insert(
                tk.END, "This is the center panel.\nYou can detach the side panels!"
            )

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
            right_builder=build_right,
        )
        window.pack(fill=tk.BOTH, expand=True)

        if auto_close_delay:
            root.after(auto_close_delay, root.destroy)

        if interactive:
            root.mainloop()

        return root, window

    def show_fixed_width_dockable():
        """Demo showing dockable window with fixed width panels."""

        def build_left(frame):
            tk.Label(frame, text="Fixed Left Panel", font=("Arial", 10, "bold")).pack(
                pady=10
            )
            tk.Label(frame, text="Width: 180px", font=("Arial", 8)).pack()
            tk.Button(frame, text="Button 1").pack(pady=2)
            tk.Button(frame, text="Button 2").pack(pady=2)

        def build_center(frame):
            tk.Label(
                frame, text="Resizable Center Panel", font=("Arial", 12, "bold")
            ).pack(pady=10)
            text = tk.Text(frame, height=10)
            text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text.insert(
                tk.END,
                """Fixed Width Demo:

- Left panel: Fixed at 180px width
- Right panel: Fixed at 150px width
- Center panel: Resizable

Try detaching the panels - the detached windows should only show reattach buttons,
not detach buttons!

This demonstrates the bug fix for detached panel buttons.""",
            )

        def build_right(frame):
            tk.Label(frame, text="Fixed Right Panel", font=("Arial", 10, "bold")).pack(
                pady=10
            )
            tk.Label(frame, text="Width: 150px", font=("Arial", 8)).pack()
            for i in range(5):
                tk.Label(frame, text=f"Item {i+1}", relief="ridge").pack(
                    fill="x", pady=1, padx=5
                )

        root = tk.Tk()
        root.title("Fixed Width Dockable Demo")
        root.geometry("900x600")

        window = DockableThreePaneWindow(
            root,
            side_width=200,  # Default width
            left_fixed_width=180,  # Fixed left width
            right_fixed_width=150,  # Fixed right width
            left_builder=build_left,
            center_builder=build_center,
            right_builder=build_right,
        )
        window.pack(fill=tk.BOTH, expand=True)

        if auto_close_delay:
            root.after(auto_close_delay, root.destroy)

        if interactive:
            root.mainloop()

        return root, window

    def show_fixed():
        root = tk.Tk()
        root.title("Fixed Three-Pane Demo")
        root.geometry("800x500")

        layout = FixedThreePaneLayout(root, side_width=180)
        layout.pack(fill=tk.BOTH, expand=True)

        layout.set_label_texts(
            left="Navigation", center="Workspace", right="Properties"
        )

        # Add some content
        layout.add_to_left(tk.Button(root, text="Menu Item 1"))
        layout.add_to_left(tk.Button(root, text="Menu Item 2"))

        text_widget = tk.Text(root)
        text_widget.insert(
            tk.END, "This is the fixed layout demo.\nThe panels have fixed positions."
        )
        layout.add_to_center(text_widget)

        layout.add_to_right(tk.Label(root, text="Property 1"))
        layout.add_to_right(tk.Label(root, text="Property 2"))

        if auto_close_delay:
            root.after(auto_close_delay, root.destroy)

        if interactive:
            root.mainloop()

        return root, layout

    def show_enhanced_with_icons():
        """Demo showing enhanced dockable window with all advanced features."""

        # Store reference to window for callbacks - use a container so it can be updated
        window_container = {"window": None}

        # Create theme variable at higher scope so it can be synchronized
        theme_var = tk.StringVar(
            value="light"
        )  # Start with light theme to match default

        def build_file_explorer(frame):
            # Header is handled by the pane configuration, no need for duplicate

            # Create a simple tree-like structure
            files = [
                "📄 main.py",
                "📄 config.py",
                "📁 assets/",
                "  🖼️ icon.png",
                "  🖼️ logo.ico",
                "📁 src/",
                "  📄 __init__.py",
                "  📄 enhanced_dockable.py",
                "  📄 themes.py",
                "📁 tests/",
                "  📄 test_examples.py",
                "  📄 test_enhanced.py",
            ]

            # Create frame for file list and controls
            list_frame = tk.Frame(frame)
            list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            # Add some controls
            controls_frame = tk.Frame(list_frame)
            controls_frame.pack(fill="x", pady=(0, 5))

            tk.Button(controls_frame, text="📁 New Folder", font=("Arial", 8)).pack(
                side="left", padx=2
            )
            tk.Button(controls_frame, text="📄 New File", font=("Arial", 8)).pack(
                side="left", padx=2
            )

            listbox = tk.Listbox(list_frame, font=("Consolas", 9))
            scrollbar = tk.Scrollbar(
                list_frame, orient="vertical", command=listbox.yview
            )
            listbox.configure(yscrollcommand=scrollbar.set)

            listbox.pack(side="left", fill=tk.BOTH, expand=True)
            scrollbar.pack(side="right", fill="y")

            for file in files:
                listbox.insert(tk.END, file)

            # Add selection handler
            def on_file_select(event):
                window_ref = window_container["window"]
                if window_ref and hasattr(window_ref, "update_status"):
                    selection = listbox.curselection()
                    if selection:
                        file_name = listbox.get(selection[0]).strip()
                        window_ref.update_status(f"Selected: {file_name}")

            listbox.bind("<<ListboxSelect>>", on_file_select)

        def build_code_editor(frame):
            # Create toolbar frame
            toolbar_frame = tk.Frame(frame)
            toolbar_frame.pack(fill="x", padx=5, pady=5)

            # Add toolbar buttons
            toolbar_buttons = tk.Frame(toolbar_frame)
            toolbar_buttons.pack(side="right")

            def save_file():
                window_ref = window_container["window"]
                if window_ref and hasattr(window_ref, "update_status"):
                    window_ref.update_status("File saved successfully!")

            def run_code():
                window_ref = window_container["window"]
                if window_ref and hasattr(window_ref, "update_status"):
                    window_ref.update_status("Running code...")

            tk.Button(
                toolbar_buttons, text="💾 Save", command=save_file, font=("Arial", 8)
            ).pack(side="left", padx=2)
            tk.Button(
                toolbar_buttons, text="▶️ Run", command=run_code, font=("Arial", 8)
            ).pack(side="left", padx=2)
            tk.Button(toolbar_buttons, text="🔍 Find", font=("Arial", 8)).pack(
                side="left", padx=2
            )

            # Create text editor with scrollbars
            editor_frame = tk.Frame(frame)
            editor_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            text = tk.Text(editor_frame, font=("Consolas", 10), wrap=tk.NONE)
            v_scrollbar = tk.Scrollbar(
                editor_frame, orient="vertical", command=text.yview
            )
            h_scrollbar = tk.Scrollbar(
                editor_frame, orient="horizontal", command=text.xview
            )
            text.configure(
                yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set
            )

            text.grid(row=0, column=0, sticky="nsew")
            v_scrollbar.grid(row=0, column=1, sticky="ns")
            h_scrollbar.grid(row=1, column=0, sticky="ew")

            editor_frame.grid_rowconfigure(0, weight=1)
            editor_frame.grid_columnconfigure(0, weight=1)

            # Add comprehensive sample code demonstrating features
            sample_code = """# Enhanced Three-Pane Window Demo - Advanced Features
from threepanewindows.enhanced_dockable import (
    EnhancedDockableThreePaneWindow,
    PaneConfig,
    get_recommended_icon_formats
)

# Cross-platform icon support
formats = get_recommended_icon_formats()
print(f"Recommended formats: {formats}")

# Configure panels with advanced options
left_config = PaneConfig(
    title="Explorer",
    icon="📁",
    default_width=250,
    min_width=200,
    max_width=400,
    detachable=True,
    resizable=True
)

center_config = PaneConfig(
    title="Editor",
    icon="📝",
    detachable=False,  # Center typically stays docked
    resizable=True
)

right_config = PaneConfig(
    title="Properties",
    icon="🔧",
    default_width=200,
    min_width=150,
    max_width=300,
    detachable=True,
    resizable=True
)

# Create window with theme and animations
window = EnhancedDockableThreePaneWindow(
    root,
    left_config=left_config,
    center_config=center_config,
    right_config=right_config,
    left_builder=build_left_panel,
    center_builder=build_center_panel,
    right_builder=build_right_panel,
    theme_name="blue",  # Available: light, dark, blue
    enable_animations=True,
    show_status_bar=True,
    show_toolbar=True
)

# Theme switching
window.switch_theme("dark")

# Status bar updates
window.update_status("Ready")

# Panel visibility control
window.show_left_pane()
window.hide_right_pane()
window.toggle_left_pane()

# Advanced features demonstrated in this demo!
"""
            text.insert(tk.END, sample_code)

            # Add text change handler
            def on_text_change(event):
                window_ref = window_container["window"]
                if window_ref and hasattr(window_ref, "update_status"):
                    lines = text.get("1.0", "end-1c").count("\n") + 1
                    chars = len(text.get("1.0", "end-1c"))
                    window_ref.update_status(f"Lines: {lines}, Characters: {chars}")

            text.bind("<KeyRelease>", on_text_change)

        def build_properties(frame):
            # Header is handled by the pane configuration, no need for duplicate

            # Create notebook for organized controls
            try:
                from tkinter import ttk

                notebook = ttk.Notebook(frame)
                notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

                # Theme tab
                theme_frame = ttk.Frame(notebook)
                notebook.add(theme_frame, text="Themes")

                # Features tab
                features_frame = ttk.Frame(notebook)
                notebook.add(features_frame, text="Features")

                # Info tab
                info_frame = ttk.Frame(notebook)
                notebook.add(info_frame, text="Info")

            except ImportError:
                # Fallback if ttk not available
                notebook = frame
                theme_frame = tk.Frame(notebook)
                theme_frame.pack(fill="x", padx=10, pady=5)
                features_frame = tk.Frame(notebook)
                features_frame.pack(fill="x", padx=10, pady=5)
                info_frame = tk.Frame(notebook)
                info_frame.pack(fill="x", padx=10, pady=5)

            # Theme Controls
            tk.Label(
                theme_frame, text="Theme Selection:", font=("Arial", 10, "bold")
            ).pack(anchor="w", pady=(10, 5))

            themes = ["light", "dark", "blue"]

            def change_theme():
                window_ref = window_container["window"]
                if window_ref and hasattr(window_ref, "switch_theme"):
                    new_theme = theme_var.get()
                    try:
                        window_ref.switch_theme(new_theme)
                        # Force UI refresh after theme change
                        window_ref.update_idletasks()
                        if hasattr(window_ref, "update_status"):
                            window_ref.update_status(
                                f"Theme changed to: {new_theme.upper()}"
                            )
                    except Exception as e:
                        if hasattr(window_ref, "update_status"):
                            window_ref.update_status(f"Theme change failed: {str(e)}")

            for theme in themes:
                rb = tk.Radiobutton(
                    theme_frame,
                    text=theme.title(),
                    variable=theme_var,
                    value=theme,
                    command=change_theme,
                    font=("Arial", 9),
                )
                rb.pack(anchor="w", padx=20)

            # Feature Controls (Panel toggles moved to toolbar for accessibility)
            tk.Label(
                features_frame, text="Panel Controls:", font=("Arial", 10, "bold")
            ).pack(anchor="w", pady=(10, 5))

            tk.Label(
                features_frame,
                text="Panel toggle buttons are in the toolbar\nfor better accessibility!",
                font=("Arial", 8),
                fg="gray",
            ).pack(anchor="w", padx=20, pady=2)

            # Animation controls
            tk.Label(
                features_frame, text="Animation Controls:", font=("Arial", 10, "bold")
            ).pack(anchor="w", pady=(10, 5))

            animation_var = tk.BooleanVar(value=True)

            def toggle_animations():
                window_ref = window_container["window"]
                if window_ref and hasattr(window_ref, "enable_animations"):
                    enabled = animation_var.get()
                    window_ref.enable_animations = enabled
                    if hasattr(window_ref, "update_status"):
                        status = "enabled" if enabled else "disabled"
                        window_ref.update_status(f"Animations {status}")

            tk.Checkbutton(
                features_frame,
                text="Enable Animations",
                variable=animation_var,
                command=toggle_animations,
            ).pack(anchor="w", padx=20)

            # Platform and Icon Information
            tk.Label(
                info_frame, text="Platform Information:", font=("Arial", 10, "bold")
            ).pack(anchor="w", pady=(10, 5))

            import platform

            from .enhanced_dockable import get_recommended_icon_formats

            formats = get_recommended_icon_formats()

            info_text = tk.Text(info_frame, height=8, font=("Arial", 9))
            info_text.pack(fill="both", expand=True, padx=20, pady=5)

            info_content = f"""Platform: {platform.system()} {platform.release()}
Python: {platform.python_version()}

Recommended Icon Formats:
{', '.join(formats)}

Enhanced Features Demonstrated:
• Dynamic theme switching
• Panel visibility controls
• Status bar integration
• Toolbar integration
• Animation controls
• Cross-platform icon support
• Resizable panels with constraints
• Detachable panels
• Custom panel configurations
"""
            info_text.insert(tk.END, info_content)
            info_text.config(state="disabled")

        root = tk.Tk()
        root.title("Enhanced Three-Pane Demo - All Features")
        root.geometry("1200x800")

        # Configure panels with comprehensive settings
        left_config = PaneConfig(
            title="File Explorer",
            icon="📁",
            # Note: In a real app, you'd have actual icon files
            # window_icon="icons/explorer.png",  # Uncomment if you have icon files
            default_width=320,  # Increased to ensure detach button is visible
            min_width=250,  # Increased minimum width
            max_width=450,
            detachable=True,
            resizable=True,
            custom_titlebar=True,  # Use custom title bar for detached windows
            custom_titlebar_shadow=True,
        )

        center_config = PaneConfig(
            title="Code Editor",
            icon="📝",
            # window_icon="icons/editor.png",  # Uncomment if you have icon files
            detachable=False,  # Center panel typically not detachable
            resizable=True,
        )

        right_config = PaneConfig(
            title="Properties & Controls",
            icon="🔧",
            # window_icon="icons/properties.ico",  # Uncomment if you have icon files
            default_width=280,  # Increased width
            min_width=220,  # Increased minimum width
            max_width=400,
            detachable=True,
            resizable=True,
            custom_titlebar=True,  # Use custom title bar for detached windows
            custom_titlebar_shadow=True,
        )

        # Create enhanced window with error handling for theme issues
        try:
            window = EnhancedDockableThreePaneWindow(
                root,
                left_config=left_config,
                center_config=center_config,
                right_config=right_config,
                left_builder=build_file_explorer,
                center_builder=build_code_editor,
                right_builder=build_properties,
                theme_name="light",
                enable_animations=True,
                show_status_bar=True,
                show_toolbar=True,
            )

            # Store reference for callbacks
            window_container["window"] = window

            # Update theme variable to match current theme
            current_theme = window.get_theme_name().lower()
            theme_var.set(current_theme)

            # Add panel toggle controls to toolbar for accessibility
            def toggle_left():
                window_ref = window_container["window"]
                if window_ref and hasattr(window_ref, "toggle_left_pane"):
                    window_ref.toggle_left_pane()
                    is_visible = window_ref.is_pane_visible("left")
                    status = "shown" if is_visible else "hidden"
                    window_ref.update_status(f"Left panel {status}")

            def toggle_right():
                window_ref = window_container["window"]
                if window_ref and hasattr(window_ref, "toggle_right_pane"):
                    window_ref.toggle_right_pane()
                    is_visible = window_ref.is_pane_visible("right")
                    status = "shown" if is_visible else "hidden"
                    window_ref.update_status(f"Right panel {status}")

            # Add toggle buttons to toolbar
            window.add_toolbar_button(
                "👁️ Left", toggle_left, "Toggle left panel visibility"
            )
            window.add_toolbar_button(
                "👁️ Right", toggle_right, "Toggle right panel visibility"
            )

            # Demonstrate status bar
            window.update_status(
                "Enhanced demo loaded - Try the theme switcher and panel controls!"
            )

        except (RuntimeError, tk.TclError) as e:
            # If theme fails (e.g., in threading context), try with default theme
            if "main thread" in str(e) or "theme" in str(e).lower():
                window = EnhancedDockableThreePaneWindow(
                    root,
                    left_config=left_config,
                    center_config=center_config,
                    right_config=right_config,
                    left_builder=build_file_explorer,
                    center_builder=build_code_editor,
                    right_builder=build_properties,
                    theme_name="light",  # Fallback to light theme
                    enable_animations=False,  # Disable animations for safety
                    show_status_bar=True,
                    show_toolbar=False,  # Disable toolbar for safety
                )
                window_container["window"] = window
                # Update theme variable for fallback case
                theme_var.set(window.get_theme_name().lower())
                if hasattr(window, "update_status"):
                    window.update_status("Demo loaded with fallback theme")
            else:
                raise

        window.pack(fill=tk.BOTH, expand=True)

        if auto_close_delay:
            root.after(auto_close_delay, root.destroy)

        if interactive:
            root.mainloop()

        return root, window

    # If not interactive, run all demos briefly for testing
    if not interactive:
        demos = []
        try:
            demos.append(show_dockable())
            demos.append(show_fixed_width_dockable())
            demos.append(show_fixed())

            # Try enhanced demo, but skip if it causes theme issues
            try:
                demos.append(show_enhanced_with_icons())
            except (RuntimeError, tk.TclError) as e:
                if "main thread" in str(e) or "theme" in str(e).lower():
                    # Skip enhanced demo if theme issues
                    pass
                else:
                    raise

        except Exception as e:
            # Clean up any created windows
            for demo in demos:
                if demo and len(demo) >= 1 and demo[0]:
                    try:
                        demo[0].destroy()
                    except:
                        pass
            raise e
        return demos

    # Create demo selector for interactive mode
    root = tk.Tk()
    root.title("ThreePaneWindows Demo")
    root.geometry("350x350")

    tk.Label(root, text="Choose a demo:", font=("Arial", 12)).pack(pady=20)

    tk.Button(root, text="Dockable Layout Demo", command=show_dockable, width=30).pack(
        pady=5
    )
    tk.Button(
        root,
        text="Fixed Width Dockable Demo",
        command=show_fixed_width_dockable,
        width=30,
    ).pack(pady=5)
    tk.Button(
        root,
        text="Enhanced Demo - All Features",
        command=show_enhanced_with_icons,
        width=30,
    ).pack(pady=5)
    tk.Button(root, text="Fixed Layout Demo", command=show_fixed, width=30).pack(pady=5)

    if auto_close_delay:
        root.after(auto_close_delay, root.destroy)

    root.mainloop()
    return root


if __name__ == "__main__":
    run_demo()
