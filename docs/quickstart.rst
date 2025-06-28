Quick Start Guide
=================

This guide will help you get started with ThreePaneWindows in just a few minutes.

Your First Three-Pane Window
-----------------------------

Let's create a simple three-pane window application:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import FixedThreePaneWindow

    # Create the main window
    root = tk.Tk()
    root.title("My First Three-Pane App")
    root.geometry("1000x600")

    # Create the three-pane layout
    three_pane = FixedThreePaneWindow(root)
    three_pane.pack(fill=tk.BOTH, expand=True)

    # Add content to each pane
    # Left pane - Navigation
    nav_frame = tk.Frame(three_pane.left_pane, bg="lightblue")
    nav_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    tk.Label(nav_frame, text="Navigation", font=("Arial", 12, "bold"), bg="lightblue").pack(pady=10)
    for i in range(5):
        tk.Button(nav_frame, text=f"Item {i+1}").pack(fill=tk.X, padx=10, pady=2)

    # Center pane - Main content
    content_frame = tk.Frame(three_pane.center_pane, bg="white")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    tk.Label(content_frame, text="Main Content Area", font=("Arial", 14, "bold")).pack(pady=20)
    text_widget = tk.Text(content_frame, wrap=tk.WORD)
    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    text_widget.insert("1.0", "This is the main content area where you can add your primary application content.")

    # Right pane - Properties/Tools
    tools_frame = tk.Frame(three_pane.right_pane, bg="lightgray")
    tools_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    tk.Label(tools_frame, text="Properties", font=("Arial", 12, "bold"), bg="lightgray").pack(pady=10)
    tk.Label(tools_frame, text="Width:", bg="lightgray").pack(anchor="w", padx=10)
    tk.Entry(tools_frame).pack(fill=tk.X, padx=10, pady=2)
    tk.Label(tools_frame, text="Height:", bg="lightgray").pack(anchor="w", padx=10)
    tk.Entry(tools_frame).pack(fill=tk.X, padx=10, pady=2)

    # Start the application
    root.mainloop()

Understanding the Layout
------------------------

The ``FixedThreePaneWindow`` creates three distinct areas:

* **Left Pane** (``left_pane``): Typically used for navigation, file trees, or tool palettes
* **Center Pane** (``center_pane``): The main content area of your application
* **Right Pane** (``right_pane``): Usually for properties, settings, or additional tools

Each pane is a standard Tkinter Frame, so you can add any widgets you need.

Customizing Pane Sizes
-----------------------

You can control the initial sizes of the panes:

.. code-block:: python

    three_pane = FixedThreePaneWindow(
        root,
        left_width=200,    # Left pane width in pixels
        right_width=250,   # Right pane width in pixels
        min_pane_size=100  # Minimum size for any pane
    )

Adding a Dockable Layout
------------------------

For more advanced applications, try the dockable layout:

.. code-block:: python

    from threepanewindows import DockableThreePaneWindow

    root = tk.Tk()
    root.title("Dockable Three-Pane App")
    root.geometry("1200x800")

    # Create dockable layout
    dockable = DockableThreePaneWindow(root)
    dockable.pack(fill=tk.BOTH, expand=True)

    # Add content (same as before)
    # ... your content code here ...

    root.mainloop()

The dockable layout allows users to:

* Drag panes to reorder them
* Detach panes into separate windows
* Resize panes by dragging separators

Applying Themes
---------------

ThreePaneWindows comes with built-in themes:

.. code-block:: python

    from threepanewindows import FixedThreePaneWindow
    from threepanewindows.themes import apply_theme

    root = tk.Tk()
    three_pane = FixedThreePaneWindow(root)
    three_pane.pack(fill=tk.BOTH, expand=True)

    # Apply dark theme
    apply_theme(three_pane, "dark")

    # Or light theme
    # apply_theme(three_pane, "light")

Available themes:

* ``"light"`` - Clean, modern light theme
* ``"dark"`` - Professional dark theme
* ``"system"`` - Follows system theme preferences

Enhanced Professional Layout with Icons
----------------------------------------

For more advanced applications, use the enhanced layout with cross-platform icon support:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

    def build_sidebar(frame):
        tk.Label(frame, text="📁 File Explorer", font=("Arial", 12, "bold")).pack(pady=10)
        for item in ["📄 Documents", "🖼️ Images", "🎵 Music"]:
            tk.Button(frame, text=item, anchor="w").pack(fill=tk.X, padx=5, pady=2)

    def build_editor(frame):
        tk.Label(frame, text="📝 Text Editor", font=("Arial", 12, "bold")).pack(pady=10)
        text = tk.Text(frame, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def build_properties(frame):
        tk.Label(frame, text="🔧 Properties", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(frame, text="Font Size:").pack(anchor="w", padx=10)
        tk.Scale(frame, from_=8, to=24, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10)

    root = tk.Tk()
    root.title("Professional Editor")
    root.geometry("1200x800")

    # Configure panels with cross-platform icons
    left_config = PaneConfig(
        title="Explorer",
        icon="📁",
        window_icon="icons/explorer.png",  # Cross-platform PNG icon
        default_width=250,
        detachable=True
    )

    center_config = PaneConfig(
        title="Editor",
        icon="📝",
        window_icon="icons/editor.png",    # Cross-platform PNG icon
        detachable=False
    )

    right_config = PaneConfig(
        title="Properties",
        icon="🔧",
        window_icon="icons/properties.ico", # Windows .ico with fallback
        default_width=200,
        detachable=True
    )

    # Create enhanced window
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=build_sidebar,
        center_builder=build_editor,
        right_builder=build_properties,
        theme_name="blue"  # Professional blue theme
    )
    window.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

This enhanced layout provides:

* **Cross-platform icon support** for detached windows
* **Professional theming** with multiple built-in themes
* **Drag & drop interface** for intuitive panel management
* **Advanced customization** with PaneConfig

Next Steps
----------

Now that you have a basic three-pane window running:

1. **Explore the Examples**: Check out the :doc:`examples/index` for more complex use cases
2. **Read the User Guide**: Learn about advanced features in :doc:`user_guide/index`
3. **API Reference**: Dive deep into the :doc:`api/index` for complete documentation
4. **Customize**: Create your own themes and layouts

Common Patterns
---------------

Here are some common patterns you'll use:

**Adding a Status Bar**

.. code-block:: python

    # Add to the bottom of your main window
    status_bar = tk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

**Creating Resizable Panes**

.. code-block:: python

    # Use PanedWindow for user-resizable sections
    paned = tk.PanedWindow(three_pane.center_pane, orient=tk.VERTICAL)
    paned.pack(fill=tk.BOTH, expand=True)
    
    top_frame = tk.Frame(paned)
    bottom_frame = tk.Frame(paned)
    
    paned.add(top_frame)
    paned.add(bottom_frame)

**Adding Menus**

.. code-block:: python

    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New")
    file_menu.add_command(label="Open")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

That's it! You now have a solid foundation for building professional three-pane applications with ThreePaneWindows.