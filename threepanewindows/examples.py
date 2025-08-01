"""
Example applications demonstrating the use of ThreePaneWindows.
"""

import threading
import tkinter as tk

from .dockable import DockableThreePaneWindow
from .enhanced_dockable import EnhancedDockableThreePaneWindow, PaneConfig
from .fixed import FixedThreePaneLayout
from .logging_config import get_logger

# Initialize logger for this module
logger = get_logger(__name__)

# Global theme update coordination
_theme_update_in_progress = False


def _coordinate_theme_update(update_func, *args, **kwargs):
    """
    Coordinate theme updates to prevent cascading updates.

    This function prevents multiple simultaneous theme updates that could
    cause performance issues or visual glitches.

    Args:
        update_func: The theme update function to call.
        *args: Positional arguments to pass to the update function.
        **kwargs: Keyword arguments to pass to the update function.

    Returns:
        The return value of the update function, or None if update is skipped.
    """
    global _theme_update_in_progress

    if _theme_update_in_progress:
        return

    _theme_update_in_progress = True
    try:
        return update_func(*args, **kwargs)
    finally:
        _theme_update_in_progress = False


def run_demo_with_timeout(timeout_seconds: int = 5, interactive: bool = False) -> bool:
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
            logger.warning("Non-interactive demo failed: %s", e)
            return False

    # For interactive mode, use threading with timeout
    success = False
    error = None

    def run_demo_thread() -> None:
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


def test_all_demo_components() -> dict:
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

            def dummy_builder(frame) -> None:
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
        logger.debug("Test environment initialization failed: %s", e)
        # This is expected in headless environments, so we don't raise

    return results


def test_basic_demo_components() -> dict:
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

            def dummy_builder(frame) -> None:
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
        logger.debug("Basic test environment initialization failed: %s", e)
        # This is expected in headless environments, so we don't raise

    return results


def _build_dockable_left_panel(frame) -> None:
    """Build left panel for dockable demo."""
    tk.Label(frame, text="Left Panel Content").pack(pady=10)
    tk.Button(frame, text="Sample Button").pack(pady=5)


def _build_dockable_center_panel(frame) -> None:
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
                logger.debug(
                    "Skipping enhanced demo due to theme/threading issue: %s", e
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
                    logger.debug("Cleanup error (expected): %s", cleanup_error)
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
logger.info("Recommended formats: %s", formats)

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
                logger.error("Theme change error: %s", e)
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
    try:
        import darkdetect

        # Detect system theme for perfect initial setup
        initial_theme = "dark" if darkdetect.isDark() else "light"
    except ImportError:
        # Fallback if darkdetect is not available
        initial_theme = "light"

    from .themes import set_global_theme

    root = tk.Tk()
    root.title("🎨 Enhanced Three-Pane Demo - All Improved Features")
    root.geometry("1400x800")

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

    # Create the enhanced window with all features enabled (including toolbar)
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
        show_toolbar=True,  # Enable toolbar to hold demo controls
        enable_animations=True,
    )
    window.pack(fill="both", expand=True)

    # Ensure window is fully initialized before setting titlebar theme
    root.update_idletasks()
    root.update()

    # Set titlebar theme to match
    set_global_theme(initial_theme, window=root)

    # Create comprehensive theme switcher and demo controls in toolbar
    _create_enhanced_demo_controls(root, window, initial_theme)

    # Show platform and feature information
    _show_enhanced_demo_info(window, initial_theme)

    if auto_close_delay:
        root.after(auto_close_delay, root.destroy)

    if interactive:
        root.mainloop()

    return root, window


def _get_layout_instance(frame):
    """Get layout instance for scrollbar creation."""
    layout = None
    parent = frame
    while parent and layout is None:
        if hasattr(parent, "create_themed_scrollbar"):
            layout = parent
            break
        parent = parent.master
    return layout


def _create_file_explorer_header(frame, panel_name):
    """Create header section for file explorer."""
    from tkinter import ttk

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

    return header_frame


def _create_file_tree_with_scrollbars(frame, layout):
    """Create file tree with scrollbars."""
    from tkinter import ttk

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
        for file in files[:2]:  # Add some files to folders
            tree.insert(folder_id, "end", text=f"  {file}")

    for file in files:
        tree.insert("", "end", text=file)

    # Create scrollbars
    if layout:
        v_scrollbar = layout.create_themed_scrollbar(
            tree_frame, orient="vertical", command=tree.yview
        )
        h_scrollbar = layout.create_themed_scrollbar(
            tree_frame, orient="horizontal", command=tree.xview
        )
    else:
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # Layout
    tree.grid(row=0, column=0, sticky="nsew")
    v_scrollbar.grid(row=0, column=1, sticky="ns")
    h_scrollbar.grid(row=1, column=0, sticky="ew")

    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    return tree_frame, tree, v_scrollbar, h_scrollbar


def _create_file_explorer_status(frame):
    """Create status section for file explorer."""
    from tkinter import ttk

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

    return status_frame


def _build_enhanced_file_explorer(frame, panel_name):
    """Build an enhanced file explorer panel with themed widgets."""
    from .themes import get_theme_manager

    layout = _get_layout_instance(frame)
    header_frame = _create_file_explorer_header(frame, panel_name)
    tree_frame, tree, v_scrollbar, h_scrollbar = _create_file_tree_with_scrollbars(
        frame, layout
    )
    status_frame = _create_file_explorer_status(frame)

    # Theme update function with debouncing
    _last_theme_update = [0]  # Use list to allow modification in nested function

    def update_theme(theme_name=None):
        import time

        # Skip if global theme update is in progress (prevents cascading updates)
        if _theme_update_in_progress:
            return

        # Simple debouncing - ignore rapid updates
        current_time = time.time()
        if current_time - _last_theme_update[0] < 0.1:  # 100ms debounce
            return
        _last_theme_update[0] = current_time

        theme_manager = get_theme_manager()
        if theme_name:
            theme_manager.set_theme(theme_name)

        current_theme = theme_manager.get_current_theme()

        # Batch all updates together to minimize layout recalculations
        def _apply_updates():
            # Temporarily disable geometry propagation to prevent jumping
            frame.pack_propagate(False)
            frame.grid_propagate(False)

            try:
                # Update scrollbars
                if hasattr(v_scrollbar, "apply_theme"):
                    v_scrollbar.apply_theme(current_theme.colors)
                    h_scrollbar.apply_theme(current_theme.colors)

                # Update ttk widget styles
                _update_file_explorer_styles(
                    theme_manager,
                    panel_name,
                    [header_frame, tree_frame, status_frame],
                    tree,
                )

                # Force update of pending geometry changes
                frame.update_idletasks()

            finally:
                # Re-enable geometry propagation
                frame.pack_propagate(True)
                frame.grid_propagate(True)

            logger.info("📁 %s updated to theme: %s", panel_name, current_theme.name)

        # Schedule the update to happen after current event processing
        frame.after_idle(_apply_updates)

    frame.update_theme = update_theme


def _update_file_explorer_styles(theme_manager, panel_name, frames, tree):
    """Update styles for file explorer widgets."""
    import tkinter as tk
    from tkinter import ttk

    try:
        style = ttk.Style()
        theme_manager.apply_ttk_theme(style)

        # Only update widgets if they don't already have the correct style
        for widget in frames:
            if hasattr(widget, "winfo_exists") and widget.winfo_exists():
                try:
                    current_style = widget.cget("style")
                    if current_style != "Themed.TFrame":
                        widget.configure(style="Themed.TFrame")
                except (tk.TclError, AttributeError):
                    pass

        # Update treeview style only if needed
        if hasattr(tree, "winfo_exists") and tree.winfo_exists():
            try:
                current_style = tree.cget("style")
                if current_style != "Themed.Treeview":
                    tree.configure(style="Themed.Treeview")
            except (tk.TclError, AttributeError):
                pass

    except Exception as e:
        logger.warning("Error updating ttk styles in %s: %s", panel_name, e)


def _create_code_editor_toolbar(frame, panel_name):
    """Create toolbar for code editor."""
    from tkinter import ttk

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

    for icon in ["💾", "🔍", "▶️"]:
        ttk.Button(button_frame, text=icon, style="Themed.TButton", width=3).pack(
            side="left", padx=1
        )

    return toolbar_frame


def _create_code_editor_text_area(frame, layout):
    """Create text area with scrollbars for code editor."""
    import tkinter as tk
    from tkinter import ttk

    from .themes import get_theme_manager

    editor_frame = ttk.Frame(frame, style="Themed.TFrame")
    editor_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Create text widget with theme styling
    theme_manager = get_theme_manager()
    text_style = theme_manager.get_tk_widget_style("text")
    if "font" in text_style:
        del text_style["font"]
    text = tk.Text(editor_frame, wrap=tk.NONE, **text_style, font=("Consolas", 11))

    # Sample code content
    sample_code = _get_sample_code()
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

    return editor_frame, text, v_scrollbar, h_scrollbar


def _get_sample_code():
    """Get sample code content."""
    return '''# 🎨 Enhanced Three-Pane Window Demo
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


def _create_code_editor_status(frame):
    """Create status bar for code editor."""
    from tkinter import ttk

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

    return status_frame


def _build_enhanced_code_editor(frame, panel_name):
    """Build an enhanced code editor panel with themed widgets."""
    from .themes import get_theme_manager

    layout = _get_layout_instance(frame)
    toolbar_frame = _create_code_editor_toolbar(frame, panel_name)
    editor_frame, text, v_scrollbar, h_scrollbar = _create_code_editor_text_area(
        frame, layout
    )
    status_frame = _create_code_editor_status(frame)

    # Theme update function with debouncing
    _last_theme_update = [0]  # Use list to allow modification in nested function

    def update_theme(theme_name=None):
        import time

        # Simple debouncing - ignore rapid updates
        current_time = time.time()
        if current_time - _last_theme_update[0] < 0.1:  # 100ms debounce
            return
        _last_theme_update[0] = current_time

        theme_manager = get_theme_manager()
        if theme_name:
            theme_manager.set_theme(theme_name)

        current_theme = theme_manager.get_current_theme()

        # Batch all updates together to minimize layout recalculations
        def _apply_updates():
            # Temporarily disable geometry propagation to prevent jumping
            frame.pack_propagate(False)
            frame.grid_propagate(False)

            try:
                # Update text widget only if style has changed
                text_style = theme_manager.get_tk_widget_style("text")
                current_bg = text.cget("bg")
                new_bg = text_style.get("bg", current_bg)

                if current_bg != new_bg:
                    text.configure(**text_style)
                    text.configure(font=("Consolas", 11))

                # Update scrollbars
                if hasattr(v_scrollbar, "apply_theme"):
                    v_scrollbar.apply_theme(current_theme.colors)
                    h_scrollbar.apply_theme(current_theme.colors)

                # Update ttk widget styles
                _update_code_editor_styles(
                    theme_manager,
                    panel_name,
                    [toolbar_frame, editor_frame, status_frame],
                )

                # Force update of pending geometry changes
                frame.update_idletasks()

            finally:
                # Re-enable geometry propagation
                frame.pack_propagate(True)
                frame.grid_propagate(True)

            logger.info("📝 %s updated to theme: %s", panel_name, current_theme.name)

        # Schedule the update to happen after current event processing
        frame.after_idle(_apply_updates)

    frame.update_theme = update_theme


def _update_code_editor_styles(theme_manager, panel_name, frames):
    """Update styles for code editor widgets."""
    import tkinter as tk
    from tkinter import ttk

    try:
        style = ttk.Style()
        theme_manager.apply_ttk_theme(style)

        # Only update widgets if they don't already have the correct style
        for widget in frames:
            if hasattr(widget, "winfo_exists") and widget.winfo_exists():
                try:
                    current_style = widget.cget("style")
                    if current_style != "Themed.TFrame":
                        widget.configure(style="Themed.TFrame")
                except (tk.TclError, AttributeError):
                    pass

    except Exception as e:
        logger.warning("Error updating ttk styles in %s: %s", panel_name, e)


def _build_enhanced_properties(frame, panel_name):
    """Build an enhanced properties panel with themed widgets."""
    # Set up the UI components
    layout = _find_layout_instance(frame)
    header_frame = _create_properties_header(frame, panel_name)
    props_frame, listbox, scrollbar = _create_properties_list(frame, layout)

    # Set up theme update functionality
    _setup_properties_theme_update(
        frame, panel_name, listbox, scrollbar, header_frame, props_frame
    )


def _find_layout_instance(frame):
    """Find the layout instance that can create themed scrollbars."""
    layout = None
    parent = frame
    while parent and layout is None:
        if hasattr(parent, "create_themed_scrollbar"):
            layout = parent
            break
        parent = parent.master
    return layout


def _create_properties_header(frame, panel_name):
    """Create the header section for the properties panel."""
    from tkinter import ttk

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

    return header_frame


def _create_properties_list(frame, layout):
    """Create the properties list with scrollbar."""
    from tkinter import ttk

    from .themes import get_theme_manager

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
    properties = _get_properties_content()
    for prop in properties:
        listbox.insert(tk.END, prop)

    # Create scrollbar
    scrollbar = _create_properties_scrollbar(props_frame, layout, listbox)

    # Layout
    listbox.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    props_frame.grid_rowconfigure(0, weight=1)
    props_frame.grid_columnconfigure(0, weight=1)

    return props_frame, listbox, scrollbar


def _get_properties_content():
    """Get the content for the properties list."""
    return [
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


def _create_properties_scrollbar(props_frame, layout, listbox):
    """Create the scrollbar for the properties list."""
    from tkinter import ttk

    if layout:
        scrollbar = layout.create_themed_scrollbar(
            props_frame, orient="vertical", command=listbox.yview
        )
    else:
        scrollbar = ttk.Scrollbar(props_frame, orient="vertical", command=listbox.yview)

    listbox.configure(yscrollcommand=scrollbar.set)
    return scrollbar


def _setup_properties_theme_update(
    frame, panel_name, listbox, scrollbar, header_frame, props_frame
):
    """Set up the theme update functionality for the properties panel."""
    # Theme update function with debouncing
    _last_theme_update = [0]  # Use list to allow modification in nested function

    def update_theme(theme_name=None):
        import time

        from .themes import get_theme_manager

        # Simple debouncing - ignore rapid updates
        if not _should_update_theme(_last_theme_update):
            return

        theme_manager = get_theme_manager()
        if theme_name:
            theme_manager.set_theme(theme_name)

        current_theme = theme_manager.get_current_theme()

        # Create the update function and schedule it
        update_func = _create_theme_update_function(
            frame,
            panel_name,
            listbox,
            scrollbar,
            header_frame,
            props_frame,
            theme_manager,
            current_theme,
        )
        frame.after_idle(update_func)

    frame.update_theme = update_theme


def _should_update_theme(_last_theme_update):
    """Check if theme should be updated based on debouncing."""
    import time

    current_time = time.time()
    if current_time - _last_theme_update[0] < 0.1:  # 100ms debounce
        return False
    _last_theme_update[0] = current_time
    return True


def _create_theme_update_function(
    frame,
    panel_name,
    listbox,
    scrollbar,
    header_frame,
    props_frame,
    theme_manager,
    current_theme,
):
    """Create the function that applies theme updates."""

    def _apply_updates():
        # Temporarily disable geometry propagation to prevent jumping
        frame.pack_propagate(False)
        frame.grid_propagate(False)

        try:
            _update_listbox_theme(listbox, theme_manager)
            _update_scrollbar_theme(scrollbar, current_theme)
            _update_ttk_widgets_theme(
                theme_manager, panel_name, header_frame, props_frame
            )

            # Force update of pending geometry changes
            frame.update_idletasks()

        finally:
            # Re-enable geometry propagation
            frame.pack_propagate(True)
            frame.grid_propagate(True)

        logger.info("🔧 %s updated to theme: %s", panel_name, current_theme.name)

    return _apply_updates


def _update_listbox_theme(listbox, theme_manager):
    """Update the listbox theme if needed."""
    listbox_style = theme_manager.get_tk_widget_style("listbox")
    current_bg = listbox.cget("bg")
    new_bg = listbox_style.get("bg", current_bg)

    if current_bg != new_bg:
        listbox.configure(**listbox_style)
        listbox.configure(font=("Arial", 9))


def _update_scrollbar_theme(scrollbar, current_theme):
    """Update the scrollbar theme if it supports theming."""
    if hasattr(scrollbar, "apply_theme"):
        scrollbar.apply_theme(current_theme.colors)


def _update_ttk_widgets_theme(theme_manager, panel_name, header_frame, props_frame):
    """Update TTK widgets theme."""
    import tkinter as tk
    from tkinter import ttk

    try:
        style = ttk.Style()
        # Force refresh of themed styles
        theme_manager.apply_ttk_theme(style)

        # Update specific widgets only if needed
        for widget in [header_frame, props_frame]:
            _update_single_ttk_widget(widget)

    except Exception as e:
        logger.warning("Error updating ttk styles in %s: %s", panel_name, e)


def _update_single_ttk_widget(widget):
    """Update a single TTK widget's style if needed."""
    import tkinter as tk

    if hasattr(widget, "winfo_exists") and widget.winfo_exists():
        try:
            current_style = widget.cget("style")
            if current_style != "Themed.TFrame":
                widget.configure(style="Themed.TFrame")
        except (tk.TclError, AttributeError):
            pass


def _create_enhanced_demo_controls(root, window, initial_theme):
    """Create comprehensive demo controls in the toolbar."""
    from .themes import get_theme_manager, set_global_theme

    theme_names = get_theme_manager().list_themes()
    current_theme = [
        initial_theme
    ]  # Use list to allow modification in nested functions
    theme_button = [None]  # Store reference to theme button for updating

    def on_theme_change():
        # Cycle through available themes
        theme_list = list(theme_names.keys())
        current_index = theme_list.index(current_theme[0])
        next_index = (current_index + 1) % len(theme_list)
        selected_theme = theme_list[next_index]
        current_theme[0] = selected_theme

        # Show detached windows info (only if there are any)
        detached_count = len(window.detached_windows)
        if detached_count > 0:
            logger.info("📊 Currently detached: %d panels", detached_count)
            for pane_side in window.detached_windows:
                titlebar_type = (
                    "custom"
                    if getattr(
                        window.detached_windows[pane_side].config,
                        "custom_titlebar",
                        False,
                    )
                    else "regular"
                )
                logger.info(
                    "  🪟 %s panel (detached, %s titlebar)", pane_side, titlebar_type
                )

        # Use coordinated theme switching to prevent cascading updates
        def _do_theme_switch():
            # Use the enhanced theme switching
            window.switch_theme(selected_theme, update_status=True)

            # Update main window titlebar
            set_global_theme(selected_theme, window=root)

            # Update theme button text
            if theme_button[0]:
                theme_button[0].configure(text=f"🎨 Theme: {selected_theme.title()}")

        _coordinate_theme_update(_do_theme_switch)

    # Demo info function
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

    # Add controls to toolbar
    theme_button[0] = window.add_toolbar_button(
        f"🎨 Theme: {current_theme[0].title()}",
        on_theme_change,
        "Click to cycle through themes",
    )
    window.add_toolbar_button(
        "ℹ️ Demo Info", show_demo_info, "Show demo information and test instructions"
    )


def _show_enhanced_demo_info(window, initial_theme):
    """Show comprehensive demo information."""
    from .themes import get_theme_manager

    platform_info = window.get_platform_info()

    logger.info("\n🎨 === Enhanced Three-Pane Demo Started ===")
    logger.info("🖥️  Platform: %s", platform_info["platform"])
    logger.info("📜 Scrollbars: %s", platform_info["scrollbar_type"])
    logger.info("📝 Description: %s", platform_info["scrollbar_description"])
    logger.info("🎨 Initial theme: %s", initial_theme)
    logger.info(
        "🎯 Available themes: %s", list(get_theme_manager().list_themes().keys())
    )
    logger.info("\n✨ NEW FEATURES DEMONSTRATED:")
    logger.info("  ✅ Automatic theme synchronization")
    logger.info("  ✅ Perfect detached window theming")
    logger.info("  ✅ Custom titlebar detached window fix")
    logger.info("  ✅ Platform-specific scrollbar detection")
    logger.info("  ✅ One-call theme switching API")
    logger.info("\n🎯 TEST INSTRUCTIONS:")
    logger.info("  1️⃣  Detach panels using ⧉ buttons")
    logger.info("  2️⃣  Switch themes using dropdown")
    logger.info("  3️⃣  Notice instant theme updates")
    logger.info("  4️⃣  Test custom titlebar panel (right)")
    logger.info("  5️⃣  Try multiple detached panels")
    logger.info("=" * 60)

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
