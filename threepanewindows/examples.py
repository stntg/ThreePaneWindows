"""
Example applications demonstrating the use of ThreePaneWindows.
"""

import threading
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
        except Exception as e:
            # Log the specific error for debugging
            print(f"Warning: Non-interactive demo failed: {e}")
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
            # Failed to create dockable window - likely due to missing dependencies
            # or display issues
            results["dockable_window"] = False

        # Test FixedThreePaneLayout creation
        try:
            layout = FixedThreePaneLayout(root, side_width=180)
            results["fixed_layout"] = True
            layout.destroy()
        except Exception:
            # Failed to create fixed layout - likely due to missing dependencies
            # or display issues
            results["fixed_layout"] = False

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
                    # Skip enhanced window test if theme issues - this is expected
                    # in test environments
                    results["enhanced_window"] = False
                else:
                    raise
        except Exception:
            # Failed to create enhanced window - likely due to missing dependencies
            results["enhanced_window"] = False

        # Test builder functions
        try:
            frame = tk.Frame(root)
            dummy_builder(frame)
            results["builders"] = True
            frame.destroy()
        except Exception:
            # Failed to test builder functions - likely due to display issues
            results["builders"] = False

        root.destroy()

    except Exception as e:
        # Failed to initialize test environment - likely no display available
        # Return current results (all False by default) - this is expected in
        # headless environments
        print(f"Debug: Test environment initialization failed: {e}")
        # This is expected in headless environments, so we don't raise

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
            # Failed to create basic dockable window - likely due to missing
            # dependencies or display issues
            results["dockable_window"] = False

        # Test FixedThreePaneLayout creation
        try:
            layout = FixedThreePaneLayout(root, side_width=180)
            results["fixed_layout"] = True
            layout.destroy()
        except Exception:
            # Failed to create basic fixed layout - likely due to missing
            # dependencies or display issues
            results["fixed_layout"] = False

        # Test builder functions
        try:
            frame = tk.Frame(root)
            dummy_builder(frame)
            results["builders"] = True
            frame.destroy()
        except Exception:
            # Failed to test basic builder functions - likely due to display
            # issues
            results["builders"] = False

        root.destroy()

    except Exception as e:
        # Failed to initialize basic test environment - likely no display available
        # Return current results (all False by default) - this is expected in
        # headless environments
        print(f"Debug: Basic test environment initialization failed: {e}")
        # This is expected in headless environments, so we don't raise

    return results


def _build_dockable_left_panel(frame):
    """Build left panel for dockable demo."""
    tk.Label(frame, text="Left Panel Content").pack(pady=10)
    tk.Button(frame, text="Sample Button").pack(pady=5)


def _build_dockable_center_panel(frame):
    """Build center panel for dockable demo."""
    tk.Label(frame, text="Center Panel Content").pack(pady=10)
    text = tk.Text(frame, height=10)
    text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    text.insert(tk.END, "This is the center panel.\nYou can detach the side panels!")


def _build_dockable_right_panel(frame):
    """Build right panel for dockable demo."""
    tk.Label(frame, text="Right Panel Content").pack(pady=10)
    listbox = tk.Listbox(frame)
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    for i in range(10):
        listbox.insert(tk.END, f"Item {i+1}")


def _show_dockable_demo(interactive, auto_close_delay):
    """Show basic dockable demo."""
    root = tk.Tk()
    root.title("Dockable Three-Pane Demo")
    root.geometry("900x600")

    window = DockableThreePaneWindow(
        root,
        side_width=200,
        left_builder=_build_dockable_left_panel,
        center_builder=_build_dockable_center_panel,
        right_builder=_build_dockable_right_panel,
    )
    window.pack(fill=tk.BOTH, expand=True)

    if auto_close_delay:
        root.after(auto_close_delay, root.destroy)

    if interactive:
        root.mainloop()

    return root, window


def _build_fixed_width_left_panel(frame):
    """Build left panel for fixed width demo."""
    tk.Label(frame, text="Fixed Left Panel", font=("Arial", 10, "bold")).pack(pady=10)
    tk.Label(frame, text="Width: 180px", font=("Arial", 8)).pack()
    tk.Button(frame, text="Button 1").pack(pady=2)
    tk.Button(frame, text="Button 2").pack(pady=2)


def _build_fixed_width_center_panel(frame):
    """Build center panel for fixed width demo."""
    tk.Label(frame, text="Resizable Center Panel", font=("Arial", 12, "bold")).pack(
        pady=10
    )
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


def _build_fixed_width_right_panel(frame):
    """Build right panel for fixed width demo."""
    tk.Label(frame, text="Fixed Right Panel", font=("Arial", 10, "bold")).pack(pady=10)
    tk.Label(frame, text="Width: 150px", font=("Arial", 8)).pack()
    for i in range(5):
        tk.Label(frame, text=f"Item {i+1}", relief="ridge").pack(
            fill="x", pady=1, padx=5
        )


def _show_fixed_width_dockable_demo(interactive, auto_close_delay):
    """Show fixed width dockable demo."""
    root = tk.Tk()
    root.title("Fixed Width Dockable Demo")
    root.geometry("900x600")

    window = DockableThreePaneWindow(
        root,
        side_width=200,
        left_fixed_width=180,
        right_fixed_width=150,
        left_builder=_build_fixed_width_left_panel,
        center_builder=_build_fixed_width_center_panel,
        right_builder=_build_fixed_width_right_panel,
    )
    window.pack(fill=tk.BOTH, expand=True)

    if auto_close_delay:
        root.after(auto_close_delay, root.destroy)

    if interactive:
        root.mainloop()

    return root, window


def _show_fixed_layout_demo(interactive, auto_close_delay):
    """Show fixed layout demo."""
    root = tk.Tk()
    root.title("Fixed Three-Pane Demo")
    root.geometry("800x500")

    layout = FixedThreePaneLayout(root, side_width=180)
    layout.pack(fill=tk.BOTH, expand=True)

    layout.set_label_texts(left="Navigation", center="Workspace", right="Properties")

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


def _run_non_interactive_demos():
    """Run all demos briefly for testing."""
    demos = []
    try:
        demos.append(_show_dockable_demo(False, None))
        demos.append(_show_fixed_width_dockable_demo(False, None))
        demos.append(_show_fixed_layout_demo(False, None))

        # Try enhanced demo, but skip if it causes theme issues
        try:
            demos.append(show_enhanced_with_icons(interactive=False))
        except (RuntimeError, tk.TclError) as e:
            if "main thread" in str(e) or "theme" in str(e).lower():
                # Skip enhanced demo if theme issues - this is expected in
                # non-interactive environments
                print(
                    f"Debug: Skipping enhanced demo due to theme/threading issue: {e}"
                )
            else:
                raise

    except Exception as e:
        # Clean up any created windows
        for demo in demos:
            if demo and len(demo) >= 1 and demo[0]:
                try:
                    demo[0].destroy()
                except Exception as cleanup_error:
                    # Ignore cleanup errors - window may already be destroyed
                    print(f"Debug: Cleanup error (expected): {cleanup_error}")
        raise e
    return demos


def _create_demo_selector(auto_close_delay):
    """Create demo selector window."""
    root = tk.Tk()
    root.title("ThreePaneWindows Demo")
    root.geometry("350x350")

    tk.Label(root, text="Choose a demo:", font=("Arial", 12)).pack(pady=20)

    # Create demo functions that capture the current parameters
    def show_dockable():
        return _show_dockable_demo(True, auto_close_delay)

    def show_fixed_width_dockable():
        return _show_fixed_width_dockable_demo(True, auto_close_delay)

    def show_fixed():
        return _show_fixed_layout_demo(True, auto_close_delay)

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


def _create_file_explorer_builder(window_container):
    """Create file explorer builder function."""

    def build_file_explorer(frame):
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

        list_frame = tk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        controls_frame = tk.Frame(list_frame)
        controls_frame.pack(fill="x", pady=(0, 5))

        tk.Button(controls_frame, text="📁 New Folder", font=("Arial", 8)).pack(
            side="left", padx=2
        )
        tk.Button(controls_frame, text="📄 New File", font=("Arial", 8)).pack(
            side="left", padx=2
        )

        listbox = tk.Listbox(list_frame, font=("Consolas", 9))
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)

        listbox.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")

        for file in files:
            listbox.insert(tk.END, file)

        def on_file_select(event):
            window_ref = window_container["window"]
            if window_ref and hasattr(window_ref, "update_status"):
                selection = listbox.curselection()
                if selection:
                    file_name = listbox.get(selection[0]).strip()
                    window_ref.update_status(f"Selected: {file_name}")

        listbox.bind("<<ListboxSelect>>", on_file_select)

    return build_file_explorer


def _create_code_editor_builder(window_container):
    """Create code editor builder function."""

    def build_code_editor(frame):
        toolbar_frame = tk.Frame(frame)
        toolbar_frame.pack(fill="x", padx=5, pady=5)

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

        editor_frame = tk.Frame(frame)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        text = tk.Text(editor_frame, font=("Consolas", 10), wrap=tk.NONE)
        v_scrollbar = tk.Scrollbar(editor_frame, orient="vertical", command=text.yview)
        h_scrollbar = tk.Scrollbar(
            editor_frame, orient="horizontal", command=text.xview
        )
        text.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        text.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        editor_frame.grid_rowconfigure(0, weight=1)
        editor_frame.grid_columnconfigure(0, weight=1)

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

        def on_text_change(event):
            window_ref = window_container["window"]
            if window_ref and hasattr(window_ref, "update_status"):
                lines = text.get("1.0", "end-1c").count("\n") + 1
                chars = len(text.get("1.0", "end-1c"))
                window_ref.update_status(f"Lines: {lines}, Characters: {chars}")

        text.bind("<KeyRelease>", on_text_change)

    return build_code_editor


def _create_properties_builder(window_container, theme_var):
    """Create properties panel builder function."""

    def build_properties(frame):
        # Create notebook for organized controls
        try:
            from tkinter import ttk

            notebook = ttk.Notebook(frame)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            theme_frame = ttk.Frame(notebook)
            notebook.add(theme_frame, text="Themes")
            features_frame = ttk.Frame(notebook)
            notebook.add(features_frame, text="Features")
            info_frame = ttk.Frame(notebook)
            notebook.add(info_frame, text="Info")
        except ImportError:
            notebook = frame
            theme_frame = tk.Frame(notebook)
            theme_frame.pack(fill="x", padx=10, pady=5)
            features_frame = tk.Frame(notebook)
            features_frame.pack(fill="x", padx=10, pady=5)
            info_frame = tk.Frame(notebook)
            info_frame.pack(fill="x", padx=10, pady=5)

        _setup_theme_controls(theme_frame, window_container, theme_var)
        _setup_feature_controls(features_frame, window_container)
        _setup_info_panel(info_frame)

    return build_properties


def _setup_theme_controls(theme_frame, window_container, theme_var):
    """Setup theme control widgets."""
    tk.Label(theme_frame, text="Theme Selection:", font=("Arial", 10, "bold")).pack(
        anchor="w", pady=(10, 5)
    )

    themes = ["light", "dark", "blue"]

    def change_theme():
        window_ref = window_container["window"]
        if window_ref and hasattr(window_ref, "switch_theme"):
            new_theme = theme_var.get()
            try:
                window_ref.switch_theme(new_theme)
                if hasattr(window_ref, "update_status"):
                    window_ref.update_status(f"Theme: {new_theme.upper()}")
            except Exception as e:
                print(f"Theme change error: {e}")
                if hasattr(window_ref, "update_status"):
                    window_ref.update_status(f"Theme change failed: {str(e)}")

    # Create radio buttons with explicit event handling
    radio_buttons = []

    def make_radio_command(theme_name):
        def radio_clicked():
            theme_var.set(theme_name)
            change_theme()

        return radio_clicked

    for i, theme in enumerate(themes):
        rb = tk.Radiobutton(
            theme_frame,
            text=f"{theme.title()} Theme",
            variable=theme_var,
            value=theme,
            command=make_radio_command(theme),
            font=("Arial", 10),
            bg="white",
            activebackground="lightblue",
            selectcolor="green",
        )
        rb.pack(anchor="w", padx=20, pady=5, fill="x")
        radio_buttons.append(rb)

    # Store radio buttons in window container
    window_container["theme_radios"] = radio_buttons

    # Enable theme changes immediately (remove initialization delay)
    window_container["theme_init_complete"] = True


def _setup_feature_controls(features_frame, window_container):
    """Setup feature control widgets."""
    tk.Label(features_frame, text="Panel Controls:", font=("Arial", 10, "bold")).pack(
        anchor="w", pady=(10, 5)
    )
    tk.Label(
        features_frame,
        text="Panel toggle buttons are in the toolbar\nfor better accessibility!",
        font=("Arial", 8),
        fg="gray",
    ).pack(anchor="w", padx=20, pady=2)

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


def _setup_info_panel(info_frame):
    """Setup information panel."""
    tk.Label(info_frame, text="Platform Information:", font=("Arial", 10, "bold")).pack(
        anchor="w", pady=(10, 5)
    )

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


def _create_pane_configs():
    """Create pane configuration objects."""
    left_config = PaneConfig(
        title="File Explorer",
        icon="📁",
        default_width=320,
        min_width=250,
        max_width=450,
        detachable=True,
        resizable=True,
        custom_titlebar=True,
        custom_titlebar_shadow=True,
    )
    center_config = PaneConfig(
        title="Code Editor",
        icon="📝",
        detachable=False,
        resizable=True,
    )
    right_config = PaneConfig(
        title="Properties & Controls",
        icon="🔧",
        default_width=280,
        min_width=220,
        max_width=400,
        detachable=True,
        resizable=True,
        custom_titlebar=True,
        custom_titlebar_shadow=True,
    )
    return left_config, center_config, right_config


def _create_enhanced_window(root, configs, builders, window_container, theme_var):
    """Create enhanced window with error handling."""
    left_config, center_config, right_config = configs
    build_file_explorer, build_code_editor, build_properties = builders

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
        window_container["window"] = window
        # Set the theme variable to match the window's current theme
        current_theme = window.get_theme_name().lower()
        theme_var.set(current_theme)
        _setup_toolbar_controls(window, window_container)
        window.update_status(
            "Enhanced demo loaded - Try the theme switcher and panel controls!"
        )

        return window
    except (RuntimeError, tk.TclError) as e:
        if "main thread" in str(e) or "theme" in str(e).lower():
            return _create_fallback_window(
                root, configs, builders, window_container, theme_var
            )
        raise


def _create_fallback_window(root, configs, builders, window_container, theme_var):
    """Create fallback window with reduced features."""
    left_config, center_config, right_config = configs
    build_file_explorer, build_code_editor, build_properties = builders

    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=build_file_explorer,
        center_builder=build_code_editor,
        right_builder=build_properties,
        theme_name="light",
        enable_animations=False,
        show_status_bar=True,
        show_toolbar=False,
    )
    window_container["window"] = window
    # Set the theme variable to match the window's current theme
    current_theme = window.get_theme_name().lower()
    theme_var.set(current_theme)
    if hasattr(window, "update_status"):
        window.update_status("Demo loaded with fallback theme")

    return window


def _setup_toolbar_controls(window, window_container):
    """Setup toolbar control buttons."""

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

    window.add_toolbar_button("👁️ Left", toggle_left, "Toggle left panel visibility")
    window.add_toolbar_button("👁️ Right", toggle_right, "Toggle right panel visibility")


def show_enhanced_with_icons(interactive=True, auto_close_delay=None):
    """
    🎨 Enhanced Three-Pane Demo - Showcasing All Improved Features!

    This demo demonstrates:
    ✅ Automatic theme synchronization (no more double-clicking!)
    ✅ Perfect detached window theming (both regular and custom titlebar)
    ✅ Automatic platform detection (Windows/macOS/Linux scrollbars)
    ✅ Professional UI with animations and status updates
    ✅ Mixed detached window scenarios
    """
    import darkdetect

    from .themes import set_global_theme

    root = tk.Tk()
    root.title("🎨 Enhanced Three-Pane Demo - All Improved Features")
    root.geometry("1400x800")

    # Detect system theme for perfect initial setup
    initial_theme = "dark" if darkdetect.isDark() else "light"

    # Create enhanced pane configurations showcasing different features
    left_config = PaneConfig(
        title="📁 File Explorer",
        icon="📁",
        default_width=280,
        min_width=200,
        detachable=True,
        # Regular titlebar for comparison
        custom_titlebar=False,
    )

    center_config = PaneConfig(
        title="📝 Code Editor",
        icon="📝",
        detachable=True,
        # Center panel detachable for testing
        custom_titlebar=False,
    )

    right_config = PaneConfig(
        title="🔧 Properties",
        icon="🔧",
        default_width=300,
        min_width=250,
        detachable=True,
        # Custom titlebar to showcase the fix!
        custom_titlebar=True,
        custom_titlebar_shadow=True,
    )

    # Create the enhanced window with all features enabled
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=lambda frame: _build_enhanced_file_explorer(
            frame, "File Explorer"
        ),
        center_builder=lambda frame: _build_enhanced_code_editor(frame, "Code Editor"),
        right_builder=lambda frame: _build_enhanced_properties(frame, "Properties"),
        theme_name=initial_theme,
        show_status_bar=True,
        enable_animations=True,
    )
    window.pack(fill="both", expand=True)

    # Ensure window is fully initialized before setting titlebar theme
    root.update_idletasks()
    root.update()

    # Set titlebar theme to match
    set_global_theme(initial_theme, window=root)

    # Create comprehensive theme switcher and demo controls
    _create_enhanced_demo_controls(root, window, initial_theme)

    # Show platform and feature information
    _show_enhanced_demo_info(window, initial_theme)

    if auto_close_delay:
        root.after(auto_close_delay, root.destroy)

    if interactive:
        root.mainloop()

    return root, window


def _build_enhanced_file_explorer(frame, panel_name):
    """Build an enhanced file explorer panel with themed widgets."""
    from tkinter import ttk

    from .themes import get_theme_manager

    # Get layout instance for scrollbar creation
    layout = None
    parent = frame
    while parent and layout is None:
        if hasattr(parent, "create_themed_scrollbar"):
            layout = parent
            break
        parent = parent.master

    # Header
    header_frame = ttk.Frame(frame, style="Themed.TFrame")
    header_frame.pack(fill="x", padx=10, pady=(10, 5))

    ttk.Label(
        header_frame,
        text=f"📁 {panel_name}",
        style="Themed.TLabel",
        font=("Arial", 12, "bold"),
    ).pack(side="left")

    ttk.Button(header_frame, text="🔄", style="Themed.TButton", width=3).pack(
        side="right", padx=(5, 0)
    )

    # File tree with themed scrollbars
    tree_frame = ttk.Frame(frame, style="Themed.TFrame")
    tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Create treeview
    tree = ttk.Treeview(tree_frame, style="Themed.Treeview")
    tree.heading("#0", text="Files & Folders", anchor="w")

    # Add sample items
    folders = ["📁 src", "📁 docs", "📁 tests", "📁 examples"]
    files = ["📄 README.md", "📄 setup.py", "📄 requirements.txt"]

    for folder in folders:
        folder_id = tree.insert("", "end", text=folder, open=True)
        for i, file in enumerate(files[:2]):  # Add some files to folders
            tree.insert(folder_id, "end", text=f"  {file}")

    for file in files:
        tree.insert("", "end", text=file)

    # Create scrollbars using automatic platform detection
    if layout:
        v_scrollbar = layout.create_themed_scrollbar(
            tree_frame, orient="vertical", command=tree.yview
        )
        h_scrollbar = layout.create_themed_scrollbar(
            tree_frame, orient="horizontal", command=tree.xview
        )
    else:
        # Fallback
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # Layout
    tree.grid(row=0, column=0, sticky="nsew")
    v_scrollbar.grid(row=0, column=1, sticky="ns")
    h_scrollbar.grid(row=1, column=0, sticky="ew")

    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    # Status info
    status_frame = ttk.Frame(frame, style="Themed.TFrame")
    status_frame.pack(fill="x", padx=10, pady=(5, 10))

    ttk.Label(
        status_frame, text="📊 12 items", style="Themed.TLabel", font=("Arial", 8)
    ).pack(side="left")
    ttk.Label(
        status_frame,
        text="🎨 Theme updates automatically!",
        style="Themed.TLabel",
        font=("Arial", 8),
    ).pack(side="right")

    # Theme update function
    def update_theme(theme_name=None):
        theme_manager = get_theme_manager()
        if theme_name:
            theme_manager.set_theme(theme_name)

        current_theme = theme_manager.get_current_theme()

        # Update scrollbars
        if hasattr(v_scrollbar, "apply_theme"):
            v_scrollbar.apply_theme(current_theme.colors)
            h_scrollbar.apply_theme(current_theme.colors)

        print(f"📁 {panel_name} updated to theme: {current_theme.name}")

    frame.update_theme = update_theme


def _build_enhanced_code_editor(frame, panel_name):
    """Build an enhanced code editor panel with themed widgets."""
    from tkinter import ttk

    from .themes import get_theme_manager

    # Get layout instance
    layout = None
    parent = frame
    while parent and layout is None:
        if hasattr(parent, "create_themed_scrollbar"):
            layout = parent
            break
        parent = parent.master

    # Toolbar
    toolbar_frame = ttk.Frame(frame, style="Themed.TFrame")
    toolbar_frame.pack(fill="x", padx=10, pady=(10, 5))

    ttk.Label(
        toolbar_frame,
        text=f"📝 {panel_name}",
        style="Themed.TLabel",
        font=("Arial", 12, "bold"),
    ).pack(side="left")

    # Editor buttons
    button_frame = ttk.Frame(toolbar_frame, style="Themed.TFrame")
    button_frame.pack(side="right")

    ttk.Button(button_frame, text="💾", style="Themed.TButton", width=3).pack(
        side="left", padx=1
    )
    ttk.Button(button_frame, text="🔍", style="Themed.TButton", width=3).pack(
        side="left", padx=1
    )
    ttk.Button(button_frame, text="▶️", style="Themed.TButton", width=3).pack(
        side="left", padx=1
    )

    # Editor area
    editor_frame = ttk.Frame(frame, style="Themed.TFrame")
    editor_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Create text widget with theme styling
    theme_manager = get_theme_manager()
    text_style = theme_manager.get_tk_widget_style("text")
    # Remove font from style to avoid conflict
    if "font" in text_style:
        del text_style["font"]
    text = tk.Text(editor_frame, wrap=tk.NONE, **text_style, font=("Consolas", 11))

    # Sample code content
    sample_code = '''# 🎨 Enhanced Three-Pane Window Demo
"""
This demo showcases all the improved features:

✅ Automatic theme synchronization
✅ Perfect detached window theming
✅ Platform-specific scrollbars
✅ Custom titlebar support
✅ Mixed detached scenarios
"""

import tkinter as tk
from threepanewindows.enhanced_dockable import EnhancedDockableThreePaneWindow

def main():
    """Create an enhanced three-pane application."""
    root = tk.Tk()
    root.title("My Enhanced App")

    # The new simplified API!
    layout = EnhancedDockableThreePaneWindow(
        root,
        left_config=PaneConfig(title="Files", detachable=True),
        center_config=PaneConfig(title="Editor", detachable=True),
        right_config=PaneConfig(title="Props", detachable=True, custom_titlebar=True),
        left_builder=build_files,
        center_builder=build_editor,
        right_builder=build_properties,
        theme_name="dark"  # Automatic platform detection!
    )
    layout.pack(fill="both", expand=True)

    # One-line theme switching - everything updates automatically!
    def switch_theme(theme_name):
        layout.switch_theme(theme_name)  # That's it! 🎉

    root.mainloop()

if __name__ == "__main__":
    main()

# 🚀 Try detaching panels and switching themes!
# Notice how detached windows update perfectly now.
'''

    text.insert("1.0", sample_code)

    # Create scrollbars
    if layout:
        v_scrollbar = layout.create_themed_scrollbar(
            editor_frame, orient="vertical", command=text.yview
        )
        h_scrollbar = layout.create_themed_scrollbar(
            editor_frame, orient="horizontal", command=text.xview
        )
    else:
        v_scrollbar = ttk.Scrollbar(editor_frame, orient="vertical", command=text.yview)
        h_scrollbar = ttk.Scrollbar(
            editor_frame, orient="horizontal", command=text.xview
        )

    text.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # Layout
    text.grid(row=0, column=0, sticky="nsew")
    v_scrollbar.grid(row=0, column=1, sticky="ns")
    h_scrollbar.grid(row=1, column=0, sticky="ew")

    editor_frame.grid_rowconfigure(0, weight=1)
    editor_frame.grid_columnconfigure(0, weight=1)

    # Status bar
    status_frame = ttk.Frame(frame, style="Themed.TFrame")
    status_frame.pack(fill="x", padx=10, pady=(5, 10))

    ttk.Label(
        status_frame, text="📍 Line 1, Col 1", style="Themed.TLabel", font=("Arial", 8)
    ).pack(side="left")
    ttk.Label(
        status_frame,
        text="🎯 Detach me and switch themes!",
        style="Themed.TLabel",
        font=("Arial", 8),
    ).pack(side="right")

    # Theme update function
    def update_theme(theme_name=None):
        theme_manager = get_theme_manager()
        if theme_name:
            theme_manager.set_theme(theme_name)

        current_theme = theme_manager.get_current_theme()

        # Update text widget
        text_style = theme_manager.get_tk_widget_style("text")
        text.configure(**text_style)
        text.configure(font=("Consolas", 11))

        # Update scrollbars
        if hasattr(v_scrollbar, "apply_theme"):
            v_scrollbar.apply_theme(current_theme.colors)
            h_scrollbar.apply_theme(current_theme.colors)

        print(f"📝 {panel_name} updated to theme: {current_theme.name}")

    frame.update_theme = update_theme


def _build_enhanced_properties(frame, panel_name):
    """Build an enhanced properties panel with themed widgets."""
    from tkinter import ttk

    from .themes import get_theme_manager

    # Get layout instance
    layout = None
    parent = frame
    while parent and layout is None:
        if hasattr(parent, "create_themed_scrollbar"):
            layout = parent
            break
        parent = parent.master

    # Header with custom titlebar indicator
    header_frame = ttk.Frame(frame, style="Themed.TFrame")
    header_frame.pack(fill="x", padx=10, pady=(10, 5))

    ttk.Label(
        header_frame,
        text=f"🔧 {panel_name}",
        style="Themed.TLabel",
        font=("Arial", 12, "bold"),
    ).pack(side="left")
    ttk.Label(
        header_frame,
        text="🪟 Custom Titlebar",
        style="Themed.TLabel",
        font=("Arial", 8),
    ).pack(side="right")

    # Properties list with scrollbar
    props_frame = ttk.Frame(frame, style="Themed.TFrame")
    props_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Create listbox with theme styling
    theme_manager = get_theme_manager()
    listbox_style = theme_manager.get_tk_widget_style("listbox")
    # Remove font from style to avoid conflict
    if "font" in listbox_style:
        del listbox_style["font"]
    listbox = tk.Listbox(props_frame, **listbox_style, font=("Arial", 9))

    # Add property items
    properties = [
        "🎨 Theme System",
        "  ✅ Automatic synchronization",
        "  ✅ Detached window support",
        "  ✅ Platform detection",
        "",
        "🪟 Window Features",
        "  ✅ Custom titlebars",
        "  ✅ Drag & drop detaching",
        "  ✅ Professional animations",
        "",
        "🔧 Technical Details",
        "  📊 Platform: Windows",
        "  🎯 Scrollbars: Custom (better theming)",
        "  🚀 Performance: Optimized",
        "",
        "🎯 Test Instructions",
        "  1️⃣ Detach this panel (⧉ button)",
        "  2️⃣ Switch themes using dropdown",
        "  3️⃣ Notice perfect theme updates!",
        "  4️⃣ Try multiple detached panels",
        "",
        "✨ This panel uses custom titlebar",
        "🔄 Theme updates work perfectly now!",
    ]

    for prop in properties:
        listbox.insert(tk.END, prop)

    # Create scrollbar
    if layout:
        scrollbar = layout.create_themed_scrollbar(
            props_frame, orient="vertical", command=listbox.yview
        )
    else:
        scrollbar = ttk.Scrollbar(props_frame, orient="vertical", command=listbox.yview)

    listbox.configure(yscrollcommand=scrollbar.set)

    # Layout
    listbox.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    props_frame.grid_rowconfigure(0, weight=1)
    props_frame.grid_columnconfigure(0, weight=1)

    # Theme update function
    def update_theme(theme_name=None):
        theme_manager = get_theme_manager()
        if theme_name:
            theme_manager.set_theme(theme_name)

        current_theme = theme_manager.get_current_theme()

        # Update listbox
        listbox_style = theme_manager.get_tk_widget_style("listbox")
        listbox.configure(**listbox_style)
        listbox.configure(font=("Arial", 9))

        # Update scrollbar
        if hasattr(scrollbar, "apply_theme"):
            scrollbar.apply_theme(current_theme.colors)

        print(f"🔧 {panel_name} updated to theme: {current_theme.name}")

    frame.update_theme = update_theme


def _create_enhanced_demo_controls(root, window, initial_theme):
    """Create comprehensive demo controls."""
    from tkinter import ttk

    from .themes import get_theme_manager, set_global_theme

    # Main controls frame
    controls_frame = ttk.Frame(root, style="Themed.TFrame")
    controls_frame.place(x=10, y=10)

    # Theme switcher
    theme_label = ttk.Label(
        controls_frame,
        text="🎨 Theme:",
        style="Themed.TLabel",
        font=("Arial", 10, "bold"),
    )
    theme_label.pack(side="left", padx=(0, 5))

    theme_names = get_theme_manager().list_themes()
    theme_var = tk.StringVar(value=initial_theme)

    def on_theme_change(*_):
        selected = theme_var.get()
        print(f"\n🎨 === Switching to {selected} theme ===")

        # Show detached windows info
        detached_count = len(window.detached_windows)
        print(f"📊 Currently detached: {detached_count} panels")
        for pane_side in window.detached_windows:
            titlebar_type = (
                "custom"
                if getattr(
                    window.detached_windows[pane_side].config, "custom_titlebar", False
                )
                else "regular"
            )
            print(f"  🪟 {pane_side} panel (detached, {titlebar_type} titlebar)")

        # Use the enhanced theme switching
        window.switch_theme(selected, update_status=True)

        # Update main window titlebar
        set_global_theme(selected, window=root)

        print(f"✅ Theme switch to {selected} complete!\n")

    theme_menu = ttk.OptionMenu(
        controls_frame,
        theme_var,
        initial_theme,
        *theme_names.keys(),
        command=lambda _: on_theme_change(),
    )
    theme_menu.configure(style="Themed.TMenubutton")
    theme_menu.pack(side="left", padx=(0, 10))

    # Demo info button
    def show_demo_info():
        info_text = """🎨 Enhanced Three-Pane Demo Features:

✅ FIXED: Theme synchronization (no more double-clicking!)
✅ FIXED: Detached window theming (all panels update)
✅ FIXED: Custom titlebar detached windows (content persists)
✅ NEW: Automatic platform detection (optimal scrollbars)
✅ NEW: One-call theme switching API

🎯 Test Instructions:
1. Detach panels using ⧉ buttons
2. Switch themes - notice instant updates
3. Try custom titlebar panel (right panel)
4. Mix regular and custom titlebar detached windows

🚀 The system now handles all complexity automatically!"""

        import tkinter.messagebox as msgbox

        msgbox.showinfo("🎨 Enhanced Demo Info", info_text)

    info_btn = ttk.Button(
        controls_frame,
        text="ℹ️ Demo Info",
        style="Themed.TButton",
        command=show_demo_info,
    )
    info_btn.pack(side="left")


def _show_enhanced_demo_info(window, initial_theme):
    """Show comprehensive demo information."""
    from .themes import get_theme_manager

    platform_info = window.get_platform_info()

    print("\n🎨 === Enhanced Three-Pane Demo Started ===")
    print(f"🖥️  Platform: {platform_info['platform']}")
    print(f"📜 Scrollbars: {platform_info['scrollbar_type']}")
    print(f"📝 Description: {platform_info['scrollbar_description']}")
    print(f"🎨 Initial theme: {initial_theme}")
    print(f"🎯 Available themes: {list(get_theme_manager().list_themes().keys())}")
    print("\n✨ NEW FEATURES DEMONSTRATED:")
    print("  ✅ Automatic theme synchronization")
    print("  ✅ Perfect detached window theming")
    print("  ✅ Custom titlebar detached window fix")
    print("  ✅ Platform-specific scrollbar detection")
    print("  ✅ One-call theme switching API")
    print("\n🎯 TEST INSTRUCTIONS:")
    print("  1️⃣  Detach panels using ⧉ buttons")
    print("  2️⃣  Switch themes using dropdown")
    print("  3️⃣  Notice instant theme updates")
    print("  4️⃣  Test custom titlebar panel (right)")
    print("  5️⃣  Try multiple detached panels")
    print("=" * 60)

    # Update status bar
    window.update_status(
        f"🎨 Enhanced demo ready! Platform: {platform_info['platform']} | "
        f"Scrollbars: {platform_info['scrollbar_type']} | Theme: {initial_theme}"
    )


def run_demo(interactive=True, auto_close_delay=None):
    """Run a simple demo of both layout types.

    Args:
        interactive (bool): If True, run in interactive mode with mainloop.
                           If False, create windows but don't start mainloop.
        auto_close_delay (int): If provided, automatically close windows after
                               this many milliseconds (for testing).
    """
    if not interactive:
        return _run_non_interactive_demos()
    else:
        return _create_demo_selector(auto_close_delay)


if __name__ == "__main__":
    run_demo()
