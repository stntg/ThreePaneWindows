Advanced Features
=================

ThreePaneWindows provides sophisticated features for building professional applications with complex requirements.

Overview
--------

Advanced features include:

* **Cross-Platform Icon Support**: Multi-format icon handling with automatic optimization
* **Professional Theming System**: Advanced theme management and customization
* **Dynamic Layout Management**: Runtime layout modifications and state management
* **Event-Driven Architecture**: Comprehensive event system for custom behaviors
* **Performance Optimization**: Efficient rendering and resource management
* **Accessibility Support**: Screen reader compatibility and keyboard navigation

Cross-Platform Icon Support
----------------------------

Multi-Format Icon Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~

The enhanced system supports multiple icon formats with automatic platform optimization:

.. code-block:: python

    from threepanewindows import (
        EnhancedDockableThreePaneWindow,
        PaneConfig,
        get_recommended_icon_formats,
        validate_icon_path
    )

    # Check platform-specific recommendations
    formats = get_recommended_icon_formats()
    print(f"Recommended formats: {formats}")
    # Windows: ['.ico', '.png', '.bmp', '.gif']
    # macOS: ['.png', '.gif', '.bmp']
    # Linux: ['.png', '.xbm', '.gif', '.bmp']

    # Validate icon compatibility
    is_valid, message = validate_icon_path("my_icon.png")
    if is_valid:
        print(f"Icon is compatible: {message}")
    else:
        print(f"Icon issue: {message}")

Automatic Icon Resolution
~~~~~~~~~~~~~~~~~~~~~~~~~

The system automatically selects the best icon display method:

.. code-block:: python

    def create_cross_platform_application():
        """Create application with cross-platform icon support."""

        # Configure panes with different icon formats
        configs = {
            "left": PaneConfig(
                title="Files",
                icon="📁",
                window_icon="icons/files.ico",    # Windows .ico
                detachable=True
            ),
            "center": PaneConfig(
                title="Editor",
                icon="📝",
                window_icon="icons/editor.png",   # Universal PNG
                detachable=False
            ),
            "right": PaneConfig(
                title="Tools",
                icon="🔧",
                window_icon="icons/tools.gif",    # Animated GIF
                detachable=True
            )
        }

        # The system will automatically:
        # 1. Check file existence
        # 2. Detect format from extension
        # 3. Use best method for platform (.ico -> iconbitmap, others -> iconphoto)
        # 4. Fallback gracefully if icon fails to load

        window = EnhancedDockableThreePaneWindow(
            root,
            left_config=configs["left"],
            center_config=configs["center"],
            right_config=configs["right"],
            # ... builders ...
        )

        return window

Icon Fallback Strategy
~~~~~~~~~~~~~~~~~~~~~

Implement robust icon fallback for missing files:

.. code-block:: python

    import os
    import platform

    def get_platform_icon(base_name, fallback_icon=""):
        """Get best icon for platform with fallback."""

        system = platform.system()

        # Define search order by platform
        if system == "Windows":
            candidates = [f"{base_name}.ico", f"{base_name}.png", f"{base_name}.bmp"]
        elif system == "Darwin":  # macOS
            candidates = [f"{base_name}.png", f"{base_name}.gif", f"{base_name}.bmp"]
        else:  # Linux
            candidates = [f"{base_name}.png", f"{base_name}.xbm", f"{base_name}.gif"]

        # Find first existing icon
        for icon_path in candidates:
            if os.path.exists(f"icons/{icon_path}"):
                is_valid, _ = validate_icon_path(f"icons/{icon_path}")
                if is_valid:
                    return f"icons/{icon_path}"

        return fallback_icon  # Return fallback or empty string

    # Use with PaneConfig
    config = PaneConfig(
        title="Robust Panel",
        window_icon=get_platform_icon("panel", "")  # Empty string if no icon found
    )

Professional Theming System
---------------------------

Advanced Theme Management
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from threepanewindows.themes import ThemeManager, Theme, get_theme_manager

    def create_advanced_theme_system():
        """Create advanced theme management system."""

        theme_manager = get_theme_manager()

        # Create custom corporate theme
        corporate_theme = Theme(
            name="corporate",
            background="#f8f9fa",
            foreground="#212529",
            accent="#007bff",
            border="#dee2e6",
            hover="#e9ecef",
            active="#0056b3",
            text="#495057",
            text_secondary="#6c757d"
        )

        # Register custom theme
        theme_manager.register_theme(corporate_theme)

        # Theme switching with validation
        def switch_theme_safely(theme_name):
            """Switch theme with error handling."""
            try:
                if theme_manager.has_theme(theme_name):
                    theme_manager.apply_theme(window, theme_name)
                    save_theme_preference(theme_name)
                else:
                    print(f"Theme '{theme_name}' not found")
            except Exception as e:
                print(f"Error switching theme: {e}")
                # Fallback to default theme
                theme_manager.apply_theme(window, "light")

        return theme_manager, switch_theme_safely

Runtime Theme Customization
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_runtime_theme_editor():
        """Create runtime theme editor for live customization."""

        def build_theme_editor(frame):
            """Build theme editor panel."""

            tk.Label(frame, text="🎨 Theme Editor",
                    font=("Arial", 12, "bold")).pack(pady=10)

            theme_manager = get_theme_manager()
            current_theme = theme_manager.get_current_theme()

            # Color editors
            color_vars = {}
            color_properties = [
                ("Background", "background"),
                ("Foreground", "foreground"),
                ("Accent", "accent"),
                ("Border", "border")
            ]

            for label, prop in color_properties:
                frame_row = tk.Frame(frame)
                frame_row.pack(fill=tk.X, padx=10, pady=2)

                tk.Label(frame_row, text=f"{label}:", width=12,
                        anchor="w").pack(side=tk.LEFT)

                color_var = tk.StringVar(value=getattr(current_theme, prop))
                color_vars[prop] = color_var

                color_entry = tk.Entry(frame_row, textvariable=color_var, width=10)
                color_entry.pack(side=tk.LEFT, padx=5)

                # Color preview
                color_preview = tk.Label(frame_row, text="  ", width=3,
                                       bg=color_var.get())
                color_preview.pack(side=tk.LEFT, padx=5)

                # Update preview when color changes
                def update_preview(var=color_var, preview=color_preview):
                    try:
                        preview.config(bg=var.get())
                    except tk.TclError:
                        preview.config(bg="white")  # Invalid color

                color_var.trace("w", lambda *args, func=update_preview: func())

            # Apply button
            def apply_custom_theme():
                """Apply custom theme with current colors."""
                try:
                    custom_theme = Theme(
                        name="custom_live",
                        **{prop: var.get() for prop, var in color_vars.items()}
                    )

                    theme_manager.register_theme(custom_theme)
                    theme_manager.apply_theme(window, "custom_live")

                except Exception as e:
                    tk.messagebox.showerror("Theme Error", f"Invalid theme: {e}")

            apply_btn = tk.Button(frame, text="Apply Theme",
                                command=apply_custom_theme)
            apply_btn.pack(pady=10)

        return build_theme_editor

Dynamic Layout Management
-------------------------

Runtime Layout Modifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_dynamic_layout_manager():
        """Create system for runtime layout modifications."""

        class LayoutManager:
            def __init__(self, window):
                self.window = window
                self.layout_history = []
                self.current_layout = 0

            def save_layout_state(self):
                """Save current layout state."""
                state = {
                    "left_width": self.window.get_pane_width("left"),
                    "right_width": self.window.get_pane_width("right"),
                    "left_detached": self.window.is_pane_detached("left"),
                    "right_detached": self.window.is_pane_detached("right"),
                    "theme": self.window.get_current_theme()
                }

                # Add to history
                self.layout_history.append(state)
                self.current_layout = len(self.layout_history) - 1

                return state

            def restore_layout_state(self, state):
                """Restore layout from state."""
                try:
                    # Restore pane widths
                    self.window.set_pane_width("left", state["left_width"])
                    self.window.set_pane_width("right", state["right_width"])

                    # Restore detachment state
                    if state["left_detached"] and not self.window.is_pane_detached("left"):
                        self.window.detach_pane("left")
                    elif not state["left_detached"] and self.window.is_pane_detached("left"):
                        self.window.reattach_pane("left")

                    if state["right_detached"] and not self.window.is_pane_detached("right"):
                        self.window.detach_pane("right")
                    elif not state["right_detached"] and self.window.is_pane_detached("right"):
                        self.window.reattach_pane("right")

                    # Restore theme
                    self.window.set_theme(state["theme"])

                except Exception as e:
                    print(f"Error restoring layout: {e}")

            def undo_layout_change(self):
                """Undo last layout change."""
                if self.current_layout > 0:
                    self.current_layout -= 1
                    state = self.layout_history[self.current_layout]
                    self.restore_layout_state(state)

            def redo_layout_change(self):
                """Redo layout change."""
                if self.current_layout < len(self.layout_history) - 1:
                    self.current_layout += 1
                    state = self.layout_history[self.current_layout]
                    self.restore_layout_state(state)

        return LayoutManager

Preset Layout Management
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_preset_layout_system():
        """Create preset layout management system."""

        class PresetManager:
            def __init__(self):
                self.presets = {}
                self.load_default_presets()

            def load_default_presets(self):
                """Load default layout presets."""
                self.presets = {
                    "ide": {
                        "name": "IDE Layout",
                        "description": "Three-pane IDE with file explorer, editor, and output",
                        "left_width": 250,
                        "right_width": 300,
                        "left_config": PaneConfig(
                            title="Explorer",
                            icon="📁",
                            detachable=True
                        ),
                        "center_config": PaneConfig(
                            title="Editor",
                            icon="📝",
                            detachable=False
                        ),
                        "right_config": PaneConfig(
                            title="Output",
                            icon="📊",
                            detachable=True
                        ),
                        "theme": "dark"
                    },
                    "browser": {
                        "name": "Browser Layout",
                        "description": "File browser with preview and properties",
                        "left_width": 200,
                        "right_width": 250,
                        "left_config": PaneConfig(
                            title="Folders",
                            icon="📁",
                            detachable=True
                        ),
                        "center_config": PaneConfig(
                            title="Files",
                            icon="📄",
                            detachable=False
                        ),
                        "right_config": PaneConfig(
                            title="Preview",
                            icon="👁️",
                            detachable=True
                        ),
                        "theme": "light"
                    },
                    "dashboard": {
                        "name": "Dashboard Layout",
                        "description": "Information dashboard with multiple panels",
                        "left_width": 300,
                        "right_width": 300,
                        "left_config": PaneConfig(
                            title="Metrics",
                            icon="📊",
                            detachable=True
                        ),
                        "center_config": PaneConfig(
                            title="Main View",
                            icon="📈",
                            detachable=False
                        ),
                        "right_config": PaneConfig(
                            title="Controls",
                            icon="🎛️",
                            detachable=True
                        ),
                        "theme": "blue"
                    }
                }

            def apply_preset(self, window, preset_name):
                """Apply a layout preset to window."""
                if preset_name not in self.presets:
                    raise ValueError(f"Preset '{preset_name}' not found")

                preset = self.presets[preset_name]

                # Apply configuration
                window.configure_panes(
                    left_config=preset["left_config"],
                    center_config=preset["center_config"],
                    right_config=preset["right_config"]
                )

                # Apply sizing
                window.set_pane_width("left", preset["left_width"])
                window.set_pane_width("right", preset["right_width"])

                # Apply theme
                window.set_theme(preset["theme"])

            def save_custom_preset(self, name, description, window):
                """Save current layout as custom preset."""
                preset = {
                    "name": name,
                    "description": description,
                    "left_width": window.get_pane_width("left"),
                    "right_width": window.get_pane_width("right"),
                    "left_config": window.get_pane_config("left"),
                    "center_config": window.get_pane_config("center"),
                    "right_config": window.get_pane_config("right"),
                    "theme": window.get_current_theme()
                }

                self.presets[name] = preset
                self.save_presets_to_file()

            def get_preset_list(self):
                """Get list of available presets."""
                return [(name, preset["name"], preset["description"])
                       for name, preset in self.presets.items()]

        return PresetManager

Event-Driven Architecture
-------------------------

Comprehensive Event System
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_event_driven_application():
        """Create application with comprehensive event handling."""

        class EventManager:
            def __init__(self):
                self.listeners = {}

            def register_listener(self, event_type, callback):
                """Register event listener."""
                if event_type not in self.listeners:
                    self.listeners[event_type] = []
                self.listeners[event_type].append(callback)

            def emit_event(self, event_type, **kwargs):
                """Emit event to all listeners."""
                if event_type in self.listeners:
                    for callback in self.listeners[event_type]:
                        try:
                            callback(**kwargs)
                        except Exception as e:
                            print(f"Error in event listener: {e}")

        event_manager = EventManager()

        # Register event listeners
        def on_pane_detached(pane_side, detached_window):
            """Handle pane detachment."""
            event_manager.emit_event("pane_detached",
                                   pane_side=pane_side,
                                   window=detached_window)

        def on_pane_resized(pane_side, new_width):
            """Handle pane resize."""
            event_manager.emit_event("pane_resized",
                                   pane_side=pane_side,
                                   width=new_width)

        def on_theme_changed(old_theme, new_theme):
            """Handle theme change."""
            event_manager.emit_event("theme_changed",
                                   old_theme=old_theme,
                                   new_theme=new_theme)

        # Application-specific event handlers
        def log_pane_events(**kwargs):
            """Log pane events for debugging."""
            print(f"Pane event: {kwargs}")

        def save_layout_on_change(**kwargs):
            """Auto-save layout on changes."""
            # Save current layout to preferences
            pass

        def update_status_bar(**kwargs):
            """Update status bar with event info."""
            # Update application status
            pass

        # Register listeners
        event_manager.register_listener("pane_detached", log_pane_events)
        event_manager.register_listener("pane_resized", save_layout_on_change)
        event_manager.register_listener("theme_changed", update_status_bar)

        # Create window with event handlers
        window = EnhancedDockableThreePaneWindow(
            root,
            # ... configuration ...
            on_detach=on_pane_detached,
            on_resize=on_pane_resized,
            on_theme_change=on_theme_changed
        )

        return window, event_manager

Custom Event Types
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_custom_event_system():
        """Create system with custom event types."""

        # Define custom event types
        class EventTypes:
            CONTENT_LOADED = "content_loaded"
            USER_ACTION = "user_action"
            DATA_UPDATED = "data_updated"
            ERROR_OCCURRED = "error_occurred"
            PERFORMANCE_METRIC = "performance_metric"

        def build_event_aware_panel(frame, event_manager):
            """Build panel that emits custom events."""

            def load_content():
                """Load content and emit event."""
                # Simulate content loading
                import time
                start_time = time.time()

                # Load content...
                time.sleep(0.1)  # Simulate work

                load_time = time.time() - start_time

                # Emit events
                event_manager.emit_event(EventTypes.CONTENT_LOADED,
                                       panel="file_panel",
                                       load_time=load_time)

                event_manager.emit_event(EventTypes.PERFORMANCE_METRIC,
                                       metric="load_time",
                                       value=load_time)

            def handle_user_action(action):
                """Handle user action and emit event."""
                event_manager.emit_event(EventTypes.USER_ACTION,
                                       action=action,
                                       timestamp=time.time())

            # UI elements
            tk.Label(frame, text="Event-Aware Panel").pack(pady=10)

            load_btn = tk.Button(frame, text="Load Content",
                               command=load_content)
            load_btn.pack(pady=5)

            action_btn = tk.Button(frame, text="User Action",
                                 command=lambda: handle_user_action("button_click"))
            action_btn.pack(pady=5)

        return build_event_aware_panel

Performance Optimization
------------------------

Efficient Rendering
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_performance_optimized_window():
        """Create window with performance optimizations."""

        class PerformanceManager:
            def __init__(self):
                self.render_queue = []
                self.render_scheduled = False
                self.frame_rate = 60  # Target FPS
                self.frame_time = 1000 // self.frame_rate  # ms per frame

            def schedule_render(self, callback):
                """Schedule render operation."""
                self.render_queue.append(callback)

                if not self.render_scheduled:
                    self.render_scheduled = True
                    root.after(self.frame_time, self.process_render_queue)

            def process_render_queue(self):
                """Process queued render operations."""
                start_time = time.time()
                max_time = self.frame_time / 1000  # Convert to seconds

                while self.render_queue and (time.time() - start_time) < max_time:
                    callback = self.render_queue.pop(0)
                    try:
                        callback()
                    except Exception as e:
                        print(f"Render error: {e}")

                # Schedule next frame if queue not empty
                if self.render_queue:
                    root.after(self.frame_time, self.process_render_queue)
                else:
                    self.render_scheduled = False

        perf_manager = PerformanceManager()

        def build_optimized_panel(frame):
            """Build panel with performance optimizations."""

            # Lazy loading
            content_loaded = False
            content_widgets = []

            def load_content_lazy():
                """Load content only when needed."""
                nonlocal content_loaded, content_widgets

                if content_loaded:
                    return

                def create_widgets():
                    # Create expensive widgets
                    for i in range(100):
                        widget = tk.Label(frame, text=f"Item {i}")
                        content_widgets.append(widget)

                        # Yield control periodically
                        if i % 10 == 0:
                            perf_manager.schedule_render(lambda: None)

                perf_manager.schedule_render(create_widgets)
                content_loaded = True

            # Trigger loading on first visibility
            def on_visibility_change(event):
                if event.widget == frame and event.state == "visibility":
                    load_content_lazy()

            frame.bind("<Visibility>", on_visibility_change)

        return build_optimized_panel, perf_manager

Resource Management
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_resource_managed_application():
        """Create application with efficient resource management."""

        class ResourceManager:
            def __init__(self):
                self.image_cache = {}
                self.font_cache = {}
                self.max_cache_size = 100

            def get_image(self, path):
                """Get image with caching."""
                if path in self.image_cache:
                    return self.image_cache[path]

                try:
                    image = tk.PhotoImage(file=path)

                    # Manage cache size
                    if len(self.image_cache) >= self.max_cache_size:
                        # Remove oldest entry
                        oldest_key = next(iter(self.image_cache))
                        del self.image_cache[oldest_key]

                    self.image_cache[path] = image
                    return image

                except Exception as e:
                    print(f"Error loading image {path}: {e}")
                    return None

            def get_font(self, family, size, weight="normal"):
                """Get font with caching."""
                key = (family, size, weight)

                if key in self.font_cache:
                    return self.font_cache[key]

                try:
                    font = tkfont.Font(family=family, size=size, weight=weight)
                    self.font_cache[key] = font
                    return font

                except Exception as e:
                    print(f"Error creating font: {e}")
                    return None

            def cleanup_resources(self):
                """Clean up unused resources."""
                # Clear caches
                self.image_cache.clear()
                self.font_cache.clear()

        return ResourceManager

Accessibility Support
---------------------

Screen Reader Compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_accessible_application():
        """Create application with accessibility support."""

        def build_accessible_panel(frame):
            """Build panel with accessibility features."""

            # Proper labeling
            header = tk.Label(frame, text="Accessible Panel")
            header.pack(pady=10)

            # Associate labels with controls
            name_label = tk.Label(frame, text="Name:")
            name_label.pack(anchor="w", padx=10)

            name_entry = tk.Entry(frame)
            name_entry.pack(fill=tk.X, padx=10, pady=2)

            # Set accessibility properties
            name_entry.configure(name="name_input")  # For screen readers

            # Keyboard navigation
            def on_key_press(event):
                """Handle keyboard navigation."""
                if event.keysym == "Tab":
                    # Custom tab handling if needed
                    pass
                elif event.keysym == "Return":
                    # Handle enter key
                    pass

            frame.bind("<KeyPress>", on_key_press)

            # Focus management
            def set_initial_focus():
                """Set initial focus for accessibility."""
                name_entry.focus_set()

            frame.after(100, set_initial_focus)

            # Status announcements
            status_var = tk.StringVar()
            status_label = tk.Label(frame, textvariable=status_var)
            status_label.pack(pady=5)

            def announce_status(message):
                """Announce status for screen readers."""
                status_var.set(message)
                # Force screen reader update
                frame.update_idletasks()

            return announce_status

        return build_accessible_panel

Keyboard Navigation
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def add_keyboard_navigation(window):
        """Add comprehensive keyboard navigation."""

        def handle_global_keys(event):
            """Handle global keyboard shortcuts."""

            # Ctrl+1, Ctrl+2, Ctrl+3 - Focus panes
            if event.state & 0x4:  # Ctrl key
                if event.keysym == "1":
                    window.focus_pane("left")
                    return "break"
                elif event.keysym == "2":
                    window.focus_pane("center")
                    return "break"
                elif event.keysym == "3":
                    window.focus_pane("right")
                    return "break"

                # Ctrl+D - Detach current pane
                elif event.keysym == "d":
                    current_pane = window.get_focused_pane()
                    if current_pane and window.can_detach_pane(current_pane):
                        window.detach_pane(current_pane)
                    return "break"

                # Ctrl+R - Reattach pane
                elif event.keysym == "r":
                    for pane in ["left", "right"]:
                        if window.is_pane_detached(pane):
                            window.reattach_pane(pane)
                            break
                    return "break"

                # Ctrl+T - Cycle themes
                elif event.keysym == "t":
                    themes = ["light", "dark", "blue"]
                    current = window.get_current_theme()
                    current_index = themes.index(current) if current in themes else 0
                    next_theme = themes[(current_index + 1) % len(themes)]
                    window.set_theme(next_theme)
                    return "break"

        # Bind to root window
        window.bind_all("<KeyPress>", handle_global_keys)

        # Add focus indicators
        def add_focus_indicators():
            """Add visual focus indicators."""
            for pane_name in ["left", "center", "right"]:
                pane = getattr(window, f"{pane_name}_pane")

                def on_focus_in(event, p=pane):
                    p.configure(relief=tk.SOLID, borderwidth=2)

                def on_focus_out(event, p=pane):
                    p.configure(relief=tk.FLAT, borderwidth=0)

                pane.bind("<FocusIn>", on_focus_in)
                pane.bind("<FocusOut>", on_focus_out)

        add_focus_indicators()

Best Practices
--------------

**Performance:**
1. Use lazy loading for expensive content
2. Implement efficient caching strategies
3. Monitor and optimize render performance
4. Profile memory usage regularly

**Accessibility:**
1. Provide keyboard alternatives for all mouse actions
2. Use proper labeling for screen readers
3. Implement logical tab order
4. Test with accessibility tools

**Cross-Platform:**
1. Test advanced features on all target platforms
2. Handle platform-specific limitations gracefully
3. Use platform-appropriate conventions
4. Provide fallbacks for unsupported features

**Architecture:**
1. Use event-driven design for loose coupling
2. Implement proper error handling
3. Provide comprehensive logging
4. Design for extensibility

**User Experience:**
1. Provide visual feedback for all operations
2. Implement undo/redo for complex operations
3. Save and restore user preferences
4. Handle edge cases gracefully

These advanced features provide the foundation for building sophisticated, professional applications that meet the highest standards of usability, performance, and accessibility.
