Layout Types
============

ThreePaneWindows provides three main layout types, each designed for different use cases and complexity requirements.

Overview
--------

.. list-table:: Layout Comparison
   :header-rows: 1
   :widths: 25 25 25 25

   * - Feature
     - FixedThreePaneWindow
     - DockableThreePaneWindow
     - EnhancedDockableThreePaneWindow
   * - Complexity
     - Low
     - Medium
     - High
   * - Fixed pane sizes
     - ✓
     - ✗
     - ✗
   * - Resizable panes
     - ✗
     - ✓
     - ✓
   * - Drag & drop
     - ✗
     - ✓
     - ✓
   * - Detachable panes
     - ✗
     - ✓
     - ✓
   * - Professional theming
     - Basic
     - ✓
     - ✓
   * - Cross-platform icons
     - ✗
     - ✗
     - ✓
   * - Status bars
     - ✗
     - ✗
     - ✓
   * - Menu integration
     - Manual
     - Manual
     - Built-in

FixedThreePaneWindow
--------------------

The simplest layout with fixed pane sizes. Perfect for applications that don't need dynamic resizing.

**Use Cases:**
- Simple applications with static layouts
- Prototyping and quick development
- Applications where pane sizes are predetermined

**Basic Usage:**

.. code-block:: python

    import tkinter as tk
    from threepanewindows import FixedThreePaneWindow

    root = tk.Tk()
    root.geometry("1000x600")

    # Create fixed layout
    layout = FixedThreePaneWindow(
        root,
        left_width=200,    # Fixed left pane width
        right_width=250    # Fixed right pane width
    )
    layout.pack(fill=tk.BOTH, expand=True)

    # Access panes directly
    left_pane = layout.left_pane
    center_pane = layout.center_pane
    right_pane = layout.right_pane

**Configuration Options:**

.. code-block:: python

    layout = FixedThreePaneWindow(
        root,
        left_width=200,        # Left pane width in pixels
        right_width=250,       # Right pane width in pixels
        separator_width=3,     # Width of separators
        bg_color="#f0f0f0"     # Background color
    )

**Advantages:**
- Simple and lightweight
- Predictable layout behavior
- Fast rendering
- Minimal resource usage

**Limitations:**
- No user resizing
- No drag and drop
- Basic theming only
- No detachable panes

DockableThreePaneWindow
-----------------------

Advanced layout with resizable and detachable panes. Suitable for most professional applications.

**Use Cases:**
- Professional desktop applications
- IDEs and code editors
- File managers and browsers
- Applications requiring flexible layouts

**Basic Usage:**

.. code-block:: python

    import tkinter as tk
    from threepanewindows import DockableThreePaneWindow

    def build_left_pane(frame):
        tk.Label(frame, text="Navigation").pack(pady=10)
        # Add your widgets here

    def build_center_pane(frame):
        tk.Label(frame, text="Main Content").pack(pady=10)
        # Add your widgets here

    def build_right_pane(frame):
        tk.Label(frame, text="Properties").pack(pady=10)
        # Add your widgets here

    root = tk.Tk()
    root.geometry("1200x800")

    # Create dockable layout
    window = DockableThreePaneWindow(
        root,
        left_builder=build_left_pane,
        center_builder=build_center_pane,
        right_builder=build_right_pane,
        side_width=250,           # Initial side pane width
        min_pane_size=150         # Minimum pane size
    )
    window.pack(fill=tk.BOTH, expand=True)

**Advanced Configuration:**

.. code-block:: python

    window = DockableThreePaneWindow(
        root,
        left_builder=build_left_pane,
        center_builder=build_center_pane,
        right_builder=build_right_pane,
        side_width=250,           # Initial side pane width
        min_pane_size=150,        # Minimum pane size
        separator_width=4,        # Separator thickness
        allow_left_detach=True,   # Allow left pane detachment
        allow_right_detach=True,  # Allow right pane detachment
        theme="dark"              # Apply theme
    )

**Features:**
- Resizable panes with drag handles
- Detachable side panes
- Professional theming support
- Drag and drop reordering
- Customizable separators

**Event Handling:**

.. code-block:: python

    def on_pane_detached(side):
        print(f"{side} pane was detached")

    def on_pane_reattached(side):
        print(f"{side} pane was reattached")

    window = DockableThreePaneWindow(
        root,
        # ... other parameters ...
        on_detach=on_pane_detached,
        on_reattach=on_pane_reattached
    )

EnhancedDockableThreePaneWindow
-------------------------------

The most advanced layout with professional features, cross-platform icon support, and extensive customization options.

**Use Cases:**
- Professional applications requiring maximum flexibility
- Applications with complex UI requirements
- Cross-platform applications needing consistent appearance
- Applications requiring advanced theming and customization

**Basic Usage:**

.. code-block:: python

    import tkinter as tk
    from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

    def build_explorer(frame):
        tk.Label(frame, text="📁 File Explorer", font=("Arial", 12, "bold")).pack(pady=10)
        # Add your widgets here

    def build_editor(frame):
        tk.Label(frame, text="📝 Code Editor", font=("Arial", 12, "bold")).pack(pady=10)
        # Add your widgets here

    def build_properties(frame):
        tk.Label(frame, text="🔧 Properties", font=("Arial", 12, "bold")).pack(pady=10)
        # Add your widgets here

    root = tk.Tk()
    root.geometry("1400x900")

    # Configure panes with advanced options
    left_config = PaneConfig(
        title="Explorer",
        icon="📁",
        window_icon="icons/explorer.png",  # Cross-platform icon
        default_width=280,
        min_width=200,
        max_width=400,
        detachable=True,
        resizable=True
    )

    center_config = PaneConfig(
        title="Editor",
        icon="📝",
        window_icon="icons/editor.png",
        detachable=False  # Center pane typically not detachable
    )

    right_config = PaneConfig(
        title="Properties",
        icon="🔧",
        window_icon="icons/properties.ico",
        default_width=250,
        min_width=180,
        max_width=350,
        detachable=True,
        closable=True  # Allow closing this pane
    )

    # Create enhanced window
    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=build_explorer,
        center_builder=build_editor,
        right_builder=build_properties,
        theme_name="blue",           # Professional blue theme
        enable_animations=True,      # Smooth animations
        show_pane_headers=True       # Show pane titles and icons
    )
    window.pack(fill=tk.BOTH, expand=True)

**PaneConfig Options:**

.. code-block:: python

    config = PaneConfig(
        title="Panel Title",           # Display title
        icon="🔧",                     # Unicode icon for header
        window_icon="icons/panel.png", # File icon for detached windows
        default_width=250,             # Default width in pixels
        min_width=200,                 # Minimum width constraint
        max_width=400,                 # Maximum width constraint
        detachable=True,               # Can be detached
        closable=False,                # Can be closed
        resizable=True,                # Can be resized
        fixed_width=None               # Fixed width (overrides resizable)
    )

**Advanced Features:**

Cross-Platform Icon Support:

.. code-block:: python

    from threepanewindows import get_recommended_icon_formats, validate_icon_path

    # Check recommended formats
    formats = get_recommended_icon_formats()
    print(f"Recommended: {formats}")

    # Validate icon before use
    is_valid, message = validate_icon_path("my_icon.png")
    if is_valid:
        config = PaneConfig(window_icon="my_icon.png")

Professional Theming:

.. code-block:: python

    # Available themes: "light", "dark", "blue"
    window = EnhancedDockableThreePaneWindow(
        root,
        # ... other parameters ...
        theme_name="dark",
        enable_animations=True
    )

Event Callbacks:

.. code-block:: python

    def on_pane_detached(pane_side, detached_window):
        print(f"Pane {pane_side} detached")
        # Customize detached window
        detached_window.title(f"Detached {pane_side.title()} Panel")

    def on_pane_closed(pane_side):
        print(f"Pane {pane_side} closed")

    window = EnhancedDockableThreePaneWindow(
        root,
        # ... other parameters ...
        on_detach=on_pane_detached,
        on_close=on_pane_closed
    )

Choosing the Right Layout
-------------------------

**Use FixedThreePaneWindow when:**
- Building simple applications
- Pane sizes are predetermined
- Performance is critical
- You need minimal complexity

**Use DockableThreePaneWindow when:**
- Users need to resize panes
- Detachable panes are required
- You want professional theming
- Drag and drop is important

**Use EnhancedDockableThreePaneWindow when:**
- Building professional applications
- Cross-platform compatibility is important
- Advanced theming is required
- You need maximum customization
- Icon support is needed

Migration Path
--------------

You can easily migrate between layout types:

**From Fixed to Dockable:**

.. code-block:: python

    # Before (Fixed)
    layout = FixedThreePaneWindow(root, left_width=200, right_width=250)

    # After (Dockable)
    def build_left(frame): pass
    def build_center(frame): pass
    def build_right(frame): pass

    window = DockableThreePaneWindow(
        root,
        left_builder=build_left,
        center_builder=build_center,
        right_builder=build_right,
        side_width=200
    )

**From Dockable to Enhanced:**

.. code-block:: python

    # Before (Dockable)
    window = DockableThreePaneWindow(
        root,
        left_builder=build_left,
        center_builder=build_center,
        right_builder=build_right
    )

    # After (Enhanced)
    left_config = PaneConfig(title="Left", detachable=True)
    center_config = PaneConfig(title="Center", detachable=False)
    right_config = PaneConfig(title="Right", detachable=True)

    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=left_config,
        center_config=center_config,
        right_config=right_config,
        left_builder=build_left,
        center_builder=build_center,
        right_builder=build_right
    )

Best Practices
--------------

**Layout Selection:**
1. Start with the simplest layout that meets your needs
2. Upgrade to more complex layouts as requirements grow
3. Consider your target audience's technical level

**Performance:**
1. Use FixedThreePaneWindow for maximum performance
2. Disable animations if performance is critical
3. Minimize the number of widgets in detachable panes

**User Experience:**
1. Provide clear visual feedback for interactive elements
2. Use consistent theming throughout your application
3. Test detachable panes thoroughly
4. Provide keyboard shortcuts for common actions

**Cross-Platform:**
1. Test on all target platforms
2. Use PNG icons for universal compatibility
3. Validate icon paths before use
4. Handle missing resources gracefully
