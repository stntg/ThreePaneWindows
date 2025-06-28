Troubleshooting Guide
====================

This guide helps you diagnose and resolve common issues when using ThreePaneWindows.

Common Issues and Solutions
---------------------------

Installation and Import Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem: ImportError when importing ThreePaneWindows**

.. code-block:: python

    ImportError: No module named 'threepanewindows'

**Solutions:**

1. **Verify Installation:**

   .. code-block:: bash

       pip list | grep threepanewindows

2. **Reinstall the Package:**

   .. code-block:: bash

       pip uninstall threepanewindows
       pip install threepanewindows

3. **Check Python Environment:**

   .. code-block:: bash

       python -c "import sys; print(sys.path)"

4. **Virtual Environment Issues:**

   .. code-block:: bash

       # Activate your virtual environment first
       source venv/bin/activate  # Linux/macOS
       # or
       venv\Scripts\activate     # Windows

       pip install threepanewindows

**Problem: Tkinter not available**

.. code-block:: python

    ImportError: No module named 'tkinter'

**Solutions:**

1. **Ubuntu/Debian:**

   .. code-block:: bash

       sudo apt-get install python3-tk

2. **CentOS/RHEL:**

   .. code-block:: bash

       sudo yum install tkinter
       # or
       sudo dnf install python3-tkinter

3. **macOS with Homebrew:**

   .. code-block:: bash

       brew install python-tk

4. **Windows:**

   Tkinter should be included with Python. If missing, reinstall Python from python.org.

Window Creation Issues
~~~~~~~~~~~~~~~~~~~~~

**Problem: Window not appearing or appearing blank**

**Diagnostic Steps:**

.. code-block:: python

    import tkinter as tk
    from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

    # Test basic Tkinter functionality
    root = tk.Tk()
    root.title("Test Window")
    root.geometry("400x300")

    # Test basic label
    test_label = tk.Label(root, text="If you see this, Tkinter works")
    test_label.pack(pady=20)

    root.mainloop()

**Solutions:**

1. **Check Display Environment (Linux):**

   .. code-block:: bash

       echo $DISPLAY
       xhost +local:

2. **Verify Window Manager:**

   .. code-block:: python

       import tkinter as tk
       root = tk.Tk()
       print(f"Window manager: {root.wm_name()}")
       print(f"Screen size: {root.winfo_screenwidth()}x{root.winfo_screenheight()}")

3. **Test Minimal Example:**

   .. code-block:: python

       import tkinter as tk
       from threepanewindows import FixedThreePaneWindow

       root = tk.Tk()
       root.geometry("800x600")

       # Use simplest layout first
       layout = FixedThreePaneWindow(root)
       layout.pack(fill=tk.BOTH, expand=True)

       # Add simple content
       tk.Label(layout.left_pane, text="Left").pack()
       tk.Label(layout.center_pane, text="Center").pack()
       tk.Label(layout.right_pane, text="Right").pack()

       root.mainloop()

Icon-Related Issues
~~~~~~~~~~~~~~~~~~

**Problem: Icons not displaying in detached windows**

**Diagnostic Code:**

.. code-block:: python

    from threepanewindows import get_recommended_icon_formats, validate_icon_path
    import os

    # Check recommended formats for your platform
    formats = get_recommended_icon_formats()
    print(f"Recommended formats: {formats}")

    # Test icon validation
    test_icons = ["test.ico", "test.png", "test.gif"]
    for icon in test_icons:
        if os.path.exists(icon):
            is_valid, message = validate_icon_path(icon)
            print(f"{icon}: {'✓' if is_valid else '✗'} {message}")
        else:
            print(f"{icon}: File not found")

**Solutions:**

1. **Use PNG for Universal Compatibility:**

   .. code-block:: python

       config = PaneConfig(
           title="My Panel",
           window_icon="icons/panel.png"  # PNG works everywhere
       )

2. **Provide Multiple Format Options:**

   .. code-block:: python

       import platform
       import os

       def get_best_icon():
           system = platform.system()
           candidates = []

           if system == "Windows":
               candidates = ["app.ico", "app.png", "app.bmp"]
           elif system == "Darwin":  # macOS
               candidates = ["app.png", "app.gif"]
           else:  # Linux
               candidates = ["app.png", "app.xbm"]

           for icon in candidates:
               if os.path.exists(f"icons/{icon}"):
                   return f"icons/{icon}"

           return ""  # No icon found

       config = PaneConfig(window_icon=get_best_icon())

3. **Check File Permissions:**

   .. code-block:: bash

       ls -la icons/
       chmod 644 icons/*.png

4. **Test Icon Loading Manually:**

   .. code-block:: python

       import tkinter as tk

       root = tk.Tk()

       try:
           # Test PNG loading
           photo = tk.PhotoImage(file="icons/test.png")
           root.iconphoto(True, photo)
           print("PNG icon loaded successfully")
       except Exception as e:
           print(f"PNG icon failed: {e}")

       try:
           # Test ICO loading (Windows)
           root.iconbitmap("icons/test.ico")
           print("ICO icon loaded successfully")
       except Exception as e:
           print(f"ICO icon failed: {e}")

Theme-Related Issues
~~~~~~~~~~~~~~~~~~~

**Problem: Themes not applying correctly**

**Diagnostic Code:**

.. code-block:: python

    from threepanewindows import get_theme_manager, ThemeType

    # Check theme manager
    theme_manager = get_theme_manager()
    print(f"Available themes: {theme_manager.get_available_themes()}")

    # Test theme application
    try:
        theme_manager.apply_theme(window, ThemeType.DARK)
        print("Theme applied successfully")
    except Exception as e:
        print(f"Theme application failed: {e}")

**Solutions:**

1. **Verify Theme Names:**

   .. code-block:: python

       # Use exact theme names
       valid_themes = ["light", "dark", "blue"]
       theme_name = "light"  # Make sure this matches exactly

       window = EnhancedDockableThreePaneWindow(
           root,
           # ... other parameters ...
           theme_name=theme_name
       )

2. **Apply Theme After Window Creation:**

   .. code-block:: python

       # Create window first
       window = EnhancedDockableThreePaneWindow(root, ...)
       window.pack(fill=tk.BOTH, expand=True)

       # Apply theme after packing
       theme_manager = get_theme_manager()
       theme_manager.apply_theme(window, "dark")

3. **Check for Theme Conflicts:**

   .. code-block:: python

       # Avoid conflicting theme settings
       window = EnhancedDockableThreePaneWindow(
           root,
           # ... other parameters ...
           theme_name="dark"  # Don't set additional theme properties
       )

Performance Issues
~~~~~~~~~~~~~~~~~

**Problem: Slow window creation or sluggish performance**

**Diagnostic Code:**

.. code-block:: python

    import time
    import psutil
    import os

    def measure_performance():
        """Measure window creation performance."""

        # Measure memory before
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss

        # Measure time
        start_time = time.time()

        # Create window
        root = tk.Tk()
        window = EnhancedDockableThreePaneWindow(
            root,
            # ... configuration ...
        )
        window.pack(fill=tk.BOTH, expand=True)

        creation_time = time.time() - start_time
        memory_after = process.memory_info().rss
        memory_used = memory_after - memory_before

        print(f"Window creation time: {creation_time:.3f} seconds")
        print(f"Memory used: {memory_used / 1024 / 1024:.2f} MB")

        return root

**Solutions:**

1. **Use Lazy Loading:**

   .. code-block:: python

       def build_lazy_panel(frame):
           """Build panel with lazy content loading."""

           # Create placeholder
           placeholder = tk.Label(frame, text="Loading...")
           placeholder.pack(expand=True)

           def load_content():
               # Remove placeholder
               placeholder.destroy()

               # Load actual content
               # ... expensive operations ...

           # Load content after a delay
           frame.after(100, load_content)

2. **Optimize Content Builders:**

   .. code-block:: python

       def build_optimized_panel(frame):
           """Build panel with optimized content."""

           # Use efficient widgets
           # Avoid creating too many widgets at once
           # Use virtual scrolling for large lists

           # Example: Virtual listbox for large datasets
           class VirtualListbox:
               def __init__(self, parent, data):
                   self.data = data
                   self.visible_items = 20
                   self.listbox = tk.Listbox(parent, height=self.visible_items)
                   self.update_display()

               def update_display(self, start_index=0):
                   self.listbox.delete(0, tk.END)
                   end_index = min(start_index + self.visible_items, len(self.data))
                   for i in range(start_index, end_index):
                       self.listbox.insert(tk.END, self.data[i])

3. **Disable Animations for Better Performance:**

   .. code-block:: python

       window = EnhancedDockableThreePaneWindow(
           root,
           # ... other parameters ...
           enable_animations=False  # Disable for better performance
       )

Pane Detachment Issues
~~~~~~~~~~~~~~~~~~~~~

**Problem: Panes not detaching or reattaching properly**

**Diagnostic Code:**

.. code-block:: python

    def test_detachment():
        """Test pane detachment functionality."""

        def build_test_panel(frame):
            label = tk.Label(frame, text="Test Panel")
            label.pack(expand=True)
            return label

        window = EnhancedDockableThreePaneWindow(
            root,
            left_config=PaneConfig(title="Left", detachable=True),
            center_config=PaneConfig(title="Center", detachable=False),
            right_config=PaneConfig(title="Right", detachable=True),
            left_builder=build_test_panel,
            center_builder=build_test_panel,
            right_builder=build_test_panel
        )

        # Test detachment programmatically
        def test_detach():
            try:
                window.detach_pane("left")
                print("Left pane detached successfully")
            except Exception as e:
                print(f"Detachment failed: {e}")

        # Test after window is displayed
        root.after(1000, test_detach)

**Solutions:**

1. **Check Detachable Configuration:**

   .. code-block:: python

       # Ensure pane is configured as detachable
       config = PaneConfig(
           title="My Panel",
           detachable=True  # Must be True for detachment
       )

2. **Verify Window State:**

   .. code-block:: python

       # Check if window is properly initialized
       if hasattr(window, 'left_pane') and window.left_pane.winfo_exists():
           window.detach_pane("left")
       else:
           print("Window not properly initialized")

3. **Handle Detachment Events:**

   .. code-block:: python

       def on_detach(pane_side, detached_window):
           """Handle detachment events."""
           print(f"Pane {pane_side} detached")

           # Ensure detached window is properly configured
           detached_window.title(f"Detached {pane_side.title()}")
           detached_window.geometry("400x500")

       window = EnhancedDockableThreePaneWindow(
           root,
           # ... other parameters ...
           on_detach=on_detach
       )

Platform-Specific Issues
~~~~~~~~~~~~~~~~~~~~~~~

**Windows-Specific Issues:**

1. **DPI Scaling Problems:**

   .. code-block:: python

       import tkinter as tk

       # Enable DPI awareness
       try:
           from ctypes import windll
           windll.shcore.SetProcessDpiAwareness(1)
       except:
           pass

       root = tk.Tk()
       # Continue with window creation...

2. **Icon Format Issues:**

   .. code-block:: python

       # Use .ico files on Windows for best results
       config = PaneConfig(
           title="Windows Panel",
           window_icon="icons/panel.ico"  # .ico preferred on Windows
       )

**macOS-Specific Issues:**

1. **Menu Bar Integration:**

   .. code-block:: python

       import platform

       if platform.system() == "Darwin":
           # macOS-specific menu setup
           root.createcommand('tk::mac::ShowPreferences', show_preferences)
           root.createcommand('tk::mac::Quit', root.quit)

2. **Icon Compatibility:**

   .. code-block:: python

       # Use PNG on macOS
       config = PaneConfig(
           title="macOS Panel",
           window_icon="icons/panel.png"  # PNG preferred on macOS
       )

**Linux-Specific Issues:**

1. **Window Manager Compatibility:**

   .. code-block:: bash

       # Test with different window managers
       echo $XDG_CURRENT_DESKTOP

       # Some window managers may have issues with detached windows

2. **Icon Theme Integration:**

   .. code-block:: python

       # Use system icon theme when possible
       import os

       def get_system_icon(icon_name):
           """Get icon from system theme."""
           icon_dirs = [
               "/usr/share/icons/hicolor/48x48/apps",
               "/usr/share/pixmaps",
               os.path.expanduser("~/.local/share/icons")
           ]

           for icon_dir in icon_dirs:
               icon_path = os.path.join(icon_dir, f"{icon_name}.png")
               if os.path.exists(icon_path):
                   return icon_path

           return ""

Debugging Tools and Techniques
------------------------------

Enable Debug Logging
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import logging

    # Enable debug logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # ThreePaneWindows will output debug information
    logger = logging.getLogger('threepanewindows')
    logger.setLevel(logging.DEBUG)

Widget Inspection
~~~~~~~~~~~~~~~~

.. code-block:: python

    def inspect_widget_hierarchy(widget, level=0):
        """Inspect widget hierarchy for debugging."""
        indent = "  " * level
        widget_info = f"{indent}{widget.__class__.__name__}"

        if hasattr(widget, 'winfo_name'):
            widget_info += f" (name: {widget.winfo_name()})"

        if hasattr(widget, 'cget'):
            try:
                bg = widget.cget('bg')
                widget_info += f" (bg: {bg})"
            except:
                pass

        print(widget_info)

        # Recursively inspect children
        try:
            for child in widget.winfo_children():
                inspect_widget_hierarchy(child, level + 1)
        except:
            pass

    # Use with your window
    inspect_widget_hierarchy(root)

Event Monitoring
~~~~~~~~~~~~~~~

.. code-block:: python

    def monitor_events(widget):
        """Monitor events for debugging."""

        events_to_monitor = [
            '<Button-1>', '<Button-3>', '<Double-Button-1>',
            '<KeyPress>', '<KeyRelease>',
            '<FocusIn>', '<FocusOut>',
            '<Configure>', '<Map>', '<Unmap>',
            '<Visibility>', '<Destroy>'
        ]

        def event_handler(event):
            print(f"Event: {event.type} on {event.widget.__class__.__name__}")
            if hasattr(event, 'keysym'):
                print(f"  Key: {event.keysym}")
            if hasattr(event, 'x') and hasattr(event, 'y'):
                print(f"  Position: ({event.x}, {event.y})")

        for event in events_to_monitor:
            widget.bind(event, event_handler, add=True)

Memory Debugging
~~~~~~~~~~~~~~~

.. code-block:: python

    import gc
    import tracemalloc

    def start_memory_debugging():
        """Start memory debugging."""
        tracemalloc.start()

        def print_memory_stats():
            """Print current memory statistics."""
            current, peak = tracemalloc.get_traced_memory()
            print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
            print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")

            # Print top memory consumers
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')

            print("Top 5 memory consumers:")
            for stat in top_stats[:5]:
                print(f"  {stat}")

        return print_memory_stats

    # Use in your application
    memory_debug = start_memory_debugging()

    # Call periodically
    root.after(5000, memory_debug)  # Every 5 seconds

Getting Help
-----------

When to Seek Help
~~~~~~~~~~~~~~~~

Seek help when you encounter:

1. **Reproducible bugs** that persist after trying the solutions above
2. **Performance issues** that significantly impact user experience
3. **Platform-specific problems** that don't have documented solutions
4. **Integration issues** with other libraries or frameworks

How to Report Issues
~~~~~~~~~~~~~~~~~~~

When reporting issues, include:

1. **System Information:**

   .. code-block:: python

       import platform
       import sys
       import threepanewindows

       print(f"Python: {sys.version}")
       print(f"Platform: {platform.platform()}")
       print(f"ThreePaneWindows: {threepanewindows.__version__}")

2. **Minimal Reproducible Example:**

   .. code-block:: python

       import tkinter as tk
       from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

       # Minimal example that demonstrates the issue
       root = tk.Tk()

       def build_panel(frame):
           tk.Label(frame, text="Test").pack()

       window = EnhancedDockableThreePaneWindow(
           root,
           left_config=PaneConfig(title="Test"),
           center_config=PaneConfig(title="Test"),
           right_config=PaneConfig(title="Test"),
           left_builder=build_panel,
           center_builder=build_panel,
           right_builder=build_panel
       )
       window.pack(fill=tk.BOTH, expand=True)

       root.mainloop()

3. **Error Messages:** Include complete error messages and stack traces

4. **Expected vs. Actual Behavior:** Clearly describe what you expected to happen and what actually happened

Resources for Help
~~~~~~~~~~~~~~~~~

- **Documentation:** Check the complete documentation at the project repository
- **Examples:** Review the examples in the `examples/` directory
- **Issue Tracker:** Search existing issues and create new ones if needed
- **Community Forums:** Participate in Python GUI development communities

This troubleshooting guide should help you resolve most common issues. If you encounter problems not covered here, don't hesitate to seek help from the community or create an issue report.
