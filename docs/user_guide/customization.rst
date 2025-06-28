Customization Guide
===================

ThreePaneWindows provides extensive customization options to tailor the appearance and behavior to your specific needs.

Overview
--------

Customization options include:

* **Pane Configuration**: Size constraints, behavior, and appearance
* **Visual Styling**: Colors, fonts, borders, and spacing
* **Interaction Behavior**: Drag and drop, resizing, detachment
* **Event Handling**: Custom callbacks and responses
* **Content Management**: Dynamic content loading and updates

Pane Configuration
------------------

Basic Pane Setup
~~~~~~~~~~~~~~~~

Configure individual panes with PaneConfig:

.. code-block:: python

    from threepanewindows import PaneConfig

    # Basic configuration
    config = PaneConfig(
        title="My Panel",              # Panel title
        icon="🔧",                     # Unicode icon
        default_width=250,             # Default width in pixels
        min_width=200,                 # Minimum width constraint
        max_width=400,                 # Maximum width constraint
        detachable=True,               # Allow detachment
        resizable=True,                # Allow resizing
        closable=False                 # Allow closing
    )

Advanced Pane Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Advanced configuration with all options
    advanced_config = PaneConfig(
        title="Advanced Panel",
        icon="⚙️",
        window_icon="icons/advanced.png",  # Icon for detached windows
        default_width=300,
        min_width=250,
        max_width=500,
        fixed_width=None,               # Set to pixel value for fixed width
        detachable=True,
        resizable=True,
        closable=True,
        collapsible=False,              # Allow collapsing (future feature)
        initial_state="normal"          # "normal", "collapsed", "detached"
    )

Size Constraints
~~~~~~~~~~~~~~~~

Control pane sizing behavior:

.. code-block:: python

    # Flexible sizing
    flexible_config = PaneConfig(
        default_width=250,
        min_width=150,      # Can shrink to 150px
        max_width=500,      # Can expand to 500px
        resizable=True
    )

    # Fixed width pane
    fixed_config = PaneConfig(
        fixed_width=200,    # Always 200px wide
        resizable=False     # Cannot be resized
    )

    # Constrained sizing
    constrained_config = PaneConfig(
        default_width=300,
        min_width=300,      # Cannot shrink below default
        max_width=300,      # Cannot expand above default
        resizable=True      # Still shows resize handles
    )

Visual Styling
--------------

Custom Colors and Appearance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def build_styled_panel(frame):
        """Build a panel with custom styling."""
        
        # Custom frame styling
        styled_frame = tk.Frame(
            frame,
            bg="#f8f9fa",           # Light background
            relief=tk.RAISED,       # Raised border
            borderwidth=2
        )
        styled_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Custom header
        header_frame = tk.Frame(styled_frame, bg="#007bff", height=40)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="📊 Custom Panel",
            bg="#007bff",
            fg="white",
            font=("Arial", 12, "bold")
        )
        header_label.pack(expand=True)
        
        # Content area
        content_frame = tk.Frame(styled_frame, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Custom widgets
        tk.Label(
            content_frame,
            text="Custom Content",
            font=("Arial", 11),
            bg="white"
        ).pack(pady=10)

Custom Separators
~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_custom_separator_window():
        """Create window with custom separator styling."""
        
        window = EnhancedDockableThreePaneWindow(
            root,
            # ... other parameters ...
            separator_width=6,          # Thicker separators
            separator_color="#34495e",  # Custom color
            separator_hover_color="#2c3e50",  # Hover color
            separator_style="raised"    # "flat", "raised", "sunken"
        )
        
        return window

Font Customization
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import tkinter.font as tkfont

    def setup_custom_fonts():
        """Setup custom fonts for the application."""
        
        # Define custom fonts
        header_font = tkfont.Font(
            family="Segoe UI",
            size=12,
            weight="bold"
        )
        
        content_font = tkfont.Font(
            family="Segoe UI",
            size=10,
            weight="normal"
        )
        
        code_font = tkfont.Font(
            family="Consolas",
            size=10,
            weight="normal"
        )
        
        return header_font, content_font, code_font

    def build_font_styled_panel(frame):
        """Build panel with custom fonts."""
        header_font, content_font, code_font = setup_custom_fonts()
        
        # Header with custom font
        tk.Label(
            frame,
            text="Custom Font Header",
            font=header_font
        ).pack(pady=10)
        
        # Content with custom font
        tk.Label(
            frame,
            text="This text uses a custom content font.",
            font=content_font
        ).pack(pady=5)
        
        # Code area with monospace font
        code_text = tk.Text(frame, font=code_font, height=5)
        code_text.pack(fill=tk.X, padx=10, pady=5)
        code_text.insert("1.0", "# Code with custom font\nprint('Hello, World!')")

Interaction Behavior
--------------------

Custom Drag and Drop
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_custom_drag_behavior():
        """Create window with custom drag behavior."""
        
        def on_drag_start(pane_side, event):
            """Called when drag starts."""
            print(f"Drag started on {pane_side} pane")
            # Custom drag start logic
        
        def on_drag_motion(pane_side, event):
            """Called during drag motion."""
            # Custom drag motion logic
            pass
        
        def on_drag_end(pane_side, event):
            """Called when drag ends."""
            print(f"Drag ended on {pane_side} pane")
            # Custom drag end logic
        
        window = EnhancedDockableThreePaneWindow(
            root,
            # ... other parameters ...
            on_drag_start=on_drag_start,
            on_drag_motion=on_drag_motion,
            on_drag_end=on_drag_end,
            drag_threshold=10,          # Pixels before drag starts
            drag_opacity=0.8            # Opacity during drag
        )
        
        return window

Custom Resize Behavior
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_custom_resize_behavior():
        """Create window with custom resize behavior."""
        
        def on_resize_start(pane_side):
            """Called when resize starts."""
            print(f"Resize started on {pane_side}")
        
        def on_resize(pane_side, new_width):
            """Called during resize."""
            print(f"Resizing {pane_side} to {new_width}px")
            
            # Custom resize constraints
            if pane_side == "left" and new_width > 400:
                return 400  # Limit left pane to 400px
            
            return new_width  # Allow resize
        
        def on_resize_end(pane_side, final_width):
            """Called when resize ends."""
            print(f"Resize ended: {pane_side} = {final_width}px")
            
            # Save user preferences
            save_pane_width(pane_side, final_width)
        
        window = EnhancedDockableThreePaneWindow(
            root,
            # ... other parameters ...
            on_resize_start=on_resize_start,
            on_resize=on_resize,
            on_resize_end=on_resize_end,
            resize_cursor="sb_h_double_arrow"  # Custom resize cursor
        )
        
        return window

Event Handling
--------------

Comprehensive Event System
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_event_driven_window():
        """Create window with comprehensive event handling."""
        
        def on_pane_detached(pane_side, detached_window):
            """Handle pane detachment."""
            print(f"Pane {pane_side} detached")
            
            # Customize detached window
            detached_window.title(f"Detached {pane_side.title()} Panel")
            detached_window.geometry("400x500")
            
            # Add custom menu to detached window
            menubar = tk.Menu(detached_window)
            detached_window.config(menu=menubar)
            
            file_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Window", menu=file_menu)
            file_menu.add_command(label="Reattach", 
                                 command=lambda: reattach_pane(pane_side))
        
        def on_pane_reattached(pane_side):
            """Handle pane reattachment."""
            print(f"Pane {pane_side} reattached")
            # Custom reattachment logic
        
        def on_pane_closed(pane_side):
            """Handle pane closing."""
            print(f"Pane {pane_side} closed")
            # Update UI state
            update_menu_state()
        
        def on_theme_changed(old_theme, new_theme):
            """Handle theme changes."""
            print(f"Theme changed from {old_theme} to {new_theme}")
            # Update custom styling
            update_custom_styling(new_theme)
        
        window = EnhancedDockableThreePaneWindow(
            root,
            # ... other parameters ...
            on_detach=on_pane_detached,
            on_reattach=on_pane_reattached,
            on_close=on_pane_closed,
            on_theme_change=on_theme_changed
        )
        
        return window

Custom Context Menus
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def add_custom_context_menus(window):
        """Add custom context menus to panes."""
        
        def create_pane_context_menu(pane_side):
            """Create context menu for a pane."""
            menu = tk.Menu(window, tearoff=0)
            
            # Standard options
            menu.add_command(
                label=f"Detach {pane_side.title()}",
                command=lambda: window.detach_pane(pane_side)
            )
            
            menu.add_separator()
            
            # Custom options
            menu.add_command(
                label="Refresh Content",
                command=lambda: refresh_pane_content(pane_side)
            )
            
            menu.add_command(
                label="Export Content",
                command=lambda: export_pane_content(pane_side)
            )
            
            menu.add_separator()
            
            # Theme submenu
            theme_menu = tk.Menu(menu, tearoff=0)
            menu.add_cascade(label="Theme", menu=theme_menu)
            
            for theme in ["light", "dark", "blue"]:
                theme_menu.add_command(
                    label=theme.title(),
                    command=lambda t=theme: window.set_theme(t)
                )
            
            return menu
        
        # Bind context menus to panes
        for pane_side in ["left", "center", "right"]:
            pane = getattr(window, f"{pane_side}_pane")
            menu = create_pane_context_menu(pane_side)
            
            def show_context_menu(event, m=menu):
                try:
                    m.tk_popup(event.x_root, event.y_root)
                finally:
                    m.grab_release()
            
            pane.bind("<Button-3>", show_context_menu)  # Right-click

Content Management
------------------

Dynamic Content Loading
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_dynamic_content_window():
        """Create window with dynamic content loading."""
        
        # Content registry
        content_registry = {}
        
        def register_content_builder(pane_side, builder_func):
            """Register a content builder for a pane."""
            content_registry[pane_side] = builder_func
        
        def rebuild_pane_content(pane_side):
            """Rebuild content for a specific pane."""
            if pane_side in content_registry:
                pane = getattr(window, f"{pane_side}_pane")
                
                # Clear existing content
                for widget in pane.winfo_children():
                    widget.destroy()
                
                # Rebuild content
                content_registry[pane_side](pane)
                
                # Update display
                pane.update()
        
        def build_dynamic_left_panel(frame):
            """Build left panel with dynamic content."""
            tk.Label(frame, text="📁 Dynamic File List", 
                    font=("Arial", 12, "bold")).pack(pady=10)
            
            # Dynamic file list
            file_frame = tk.Frame(frame)
            file_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # Refresh button
            refresh_btn = tk.Button(
                file_frame,
                text="🔄 Refresh",
                command=lambda: rebuild_pane_content("left")
            )
            refresh_btn.pack(anchor="ne", padx=5, pady=5)
            
            # File list (simulated)
            import random
            files = [f"file_{random.randint(1000, 9999)}.txt" for _ in range(5)]
            
            listbox = tk.Listbox(file_frame)
            listbox.pack(fill=tk.BOTH, expand=True, pady=5)
            
            for file in files:
                listbox.insert(tk.END, f"📄 {file}")
        
        # Register content builders
        register_content_builder("left", build_dynamic_left_panel)
        
        # Create window
        window = EnhancedDockableThreePaneWindow(
            root,
            left_config=PaneConfig(title="Dynamic Content"),
            center_config=PaneConfig(title="Main"),
            right_config=PaneConfig(title="Properties"),
            left_builder=build_dynamic_left_panel,
            center_builder=lambda f: tk.Label(f, text="Main Content").pack(),
            right_builder=lambda f: tk.Label(f, text="Properties").pack()
        )
        
        return window

Content State Management
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class ContentStateManager:
        """Manage content state across pane operations."""
        
        def __init__(self):
            self.state_data = {}
        
        def save_pane_state(self, pane_side, state_data):
            """Save state data for a pane."""
            self.state_data[pane_side] = state_data
        
        def restore_pane_state(self, pane_side):
            """Restore state data for a pane."""
            return self.state_data.get(pane_side, {})
        
        def clear_pane_state(self, pane_side):
            """Clear state data for a pane."""
            if pane_side in self.state_data:
                del self.state_data[pane_side]

    def create_stateful_content_window():
        """Create window with stateful content management."""
        
        state_manager = ContentStateManager()
        
        def build_stateful_panel(frame, pane_side):
            """Build panel that maintains state."""
            
            # Restore previous state
            state = state_manager.restore_pane_state(pane_side)
            
            # Create content with restored state
            tk.Label(frame, text=f"Stateful {pane_side.title()} Panel").pack(pady=10)
            
            # Text widget that maintains content
            text_widget = tk.Text(frame, height=10)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # Restore text content
            if "text_content" in state:
                text_widget.insert("1.0", state["text_content"])
            
            # Save state on changes
            def save_text_state(event=None):
                content = text_widget.get("1.0", tk.END)
                state_manager.save_pane_state(pane_side, {"text_content": content})
            
            text_widget.bind("<KeyRelease>", save_text_state)
            text_widget.bind("<FocusOut>", save_text_state)
        
        # Create builders for each pane
        left_builder = lambda f: build_stateful_panel(f, "left")
        center_builder = lambda f: build_stateful_panel(f, "center")
        right_builder = lambda f: build_stateful_panel(f, "right")
        
        window = EnhancedDockableThreePaneWindow(
            root,
            left_config=PaneConfig(title="Left State"),
            center_config=PaneConfig(title="Center State"),
            right_config=PaneConfig(title="Right State"),
            left_builder=left_builder,
            center_builder=center_builder,
            right_builder=right_builder
        )
        
        return window

Advanced Customization Examples
-------------------------------

Professional IDE Layout
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_professional_ide():
        """Create a professional IDE-style layout."""
        
        # Custom styling
        ide_style = {
            "bg_color": "#1e1e1e",
            "fg_color": "#d4d4d4",
            "accent_color": "#007acc",
            "border_color": "#3c3c3c"
        }
        
        def build_project_explorer(frame):
            # Professional project explorer
            frame.configure(bg=ide_style["bg_color"])
            
            # Toolbar
            toolbar = tk.Frame(frame, bg=ide_style["bg_color"], height=30)
            toolbar.pack(fill=tk.X)
            toolbar.pack_propagate(False)
            
            # Project controls
            controls = ["📁", "🔄", "⚙️"]
            for control in controls:
                btn = tk.Button(
                    toolbar,
                    text=control,
                    bg=ide_style["bg_color"],
                    fg=ide_style["fg_color"],
                    relief=tk.FLAT,
                    width=3
                )
                btn.pack(side=tk.LEFT, padx=2, pady=2)
            
            # File tree
            tree_frame = tk.Frame(frame, bg=ide_style["bg_color"])
            tree_frame.pack(fill=tk.BOTH, expand=True)
            
            # Custom tree widget (simplified)
            tree_text = tk.Text(
                tree_frame,
                bg=ide_style["bg_color"],
                fg=ide_style["fg_color"],
                font=("Consolas", 9),
                relief=tk.FLAT
            )
            tree_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Sample project structure
            project_structure = """📁 MyProject
├── 📁 src
│   ├── 🐍 main.py
│   ├── 🐍 utils.py
│   └── 📁 components
│       ├── 🐍 __init__.py
│       └── 🐍 widgets.py
├── 📁 tests
│   └── 🐍 test_main.py
├── 📄 README.md
└── 📄 requirements.txt"""
            
            tree_text.insert("1.0", project_structure)
            tree_text.config(state=tk.DISABLED)
        
        def build_code_editor(frame):
            # Professional code editor
            frame.configure(bg=ide_style["bg_color"])
            
            # Tab bar
            tab_bar = tk.Frame(frame, bg=ide_style["border_color"], height=35)
            tab_bar.pack(fill=tk.X)
            tab_bar.pack_propagate(False)
            
            # Editor tabs
            tabs = ["main.py", "utils.py", "README.md"]
            for i, tab in enumerate(tabs):
                tab_bg = ide_style["bg_color"] if i == 0 else ide_style["border_color"]
                tab_btn = tk.Button(
                    tab_bar,
                    text=f"📄 {tab}",
                    bg=tab_bg,
                    fg=ide_style["fg_color"],
                    relief=tk.FLAT,
                    anchor="w"
                )
                tab_btn.pack(side=tk.LEFT, fill=tk.Y, padx=1)
            
            # Editor area
            editor_frame = tk.Frame(frame, bg=ide_style["bg_color"])
            editor_frame.pack(fill=tk.BOTH, expand=True)
            
            # Line numbers
            line_frame = tk.Frame(editor_frame, bg=ide_style["border_color"], width=50)
            line_frame.pack(side=tk.LEFT, fill=tk.Y)
            line_frame.pack_propagate(False)
            
            line_text = tk.Text(
                line_frame,
                width=4,
                bg=ide_style["border_color"],
                fg=ide_style["fg_color"],
                font=("Consolas", 10),
                state=tk.DISABLED
            )
            line_text.pack(fill=tk.BOTH, expand=True)
            
            # Code area
            code_text = tk.Text(
                editor_frame,
                bg=ide_style["bg_color"],
                fg=ide_style["fg_color"],
                font=("Consolas", 10),
                insertbackground=ide_style["fg_color"],
                selectbackground=ide_style["accent_color"]
            )
            code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Sample code
            sample_code = '''#!/usr/bin/env python3
"""
Professional IDE Example
"""

import tkinter as tk
from threepanewindows import EnhancedDockableThreePaneWindow

def main():
    """Main application entry point."""
    root = tk.Tk()
    root.title("Professional IDE")
    
    # Create IDE layout
    ide = create_professional_ide()
    
    root.mainloop()

if __name__ == "__main__":
    main()
'''
            code_text.insert("1.0", sample_code)
            
            # Add line numbers
            lines = sample_code.count('\n') + 1
            line_numbers = '\n'.join(str(i) for i in range(1, lines + 1))
            line_text.config(state=tk.NORMAL)
            line_text.insert("1.0", line_numbers)
            line_text.config(state=tk.DISABLED)
        
        def build_output_panel(frame):
            # Professional output panel
            frame.configure(bg=ide_style["bg_color"])
            
            # Output tabs
            tab_frame = tk.Frame(frame, bg=ide_style["border_color"], height=30)
            tab_frame.pack(fill=tk.X)
            tab_frame.pack_propagate(False)
            
            output_tabs = ["Terminal", "Problems", "Output", "Debug"]
            for tab in output_tabs:
                tab_btn = tk.Button(
                    tab_frame,
                    text=tab,
                    bg=ide_style["border_color"],
                    fg=ide_style["fg_color"],
                    relief=tk.FLAT,
                    font=("Arial", 9)
                )
                tab_btn.pack(side=tk.LEFT, padx=2, pady=2)
            
            # Output area
            output_text = tk.Text(
                frame,
                bg=ide_style["bg_color"],
                fg=ide_style["fg_color"],
                font=("Consolas", 9)
            )
            output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Sample output
            output_text.insert("1.0", "$ python main.py\nApplication started successfully.\nListening on port 8000...\n")
        
        # Configure IDE panes
        explorer_config = PaneConfig(
            title="Explorer",
            icon="📁",
            window_icon="icons/explorer.png",
            default_width=250,
            min_width=200,
            max_width=400,
            detachable=True
        )
        
        editor_config = PaneConfig(
            title="Editor",
            icon="📝",
            window_icon="icons/editor.png",
            detachable=False
        )
        
        output_config = PaneConfig(
            title="Output",
            icon="📊",
            window_icon="icons/output.png",
            default_width=300,
            min_width=250,
            detachable=True
        )
        
        # Create IDE window
        ide_window = EnhancedDockableThreePaneWindow(
            root,
            left_config=explorer_config,
            center_config=editor_config,
            right_config=output_config,
            left_builder=build_project_explorer,
            center_builder=build_code_editor,
            right_builder=build_output_panel,
            theme_name="dark",
            enable_animations=True
        )
        
        return ide_window

Best Practices
--------------

**Configuration Management:**
1. Use PaneConfig for consistent pane setup
2. Validate configuration parameters
3. Provide sensible defaults
4. Document configuration options

**Visual Consistency:**
1. Maintain consistent styling across panes
2. Use theme system for color coordination
3. Test appearance on different screen sizes
4. Consider accessibility requirements

**Performance Optimization:**
1. Lazy-load content when possible
2. Cache expensive operations
3. Minimize widget creation/destruction
4. Use efficient event handling

**User Experience:**
1. Provide visual feedback for interactions
2. Implement undo/redo for destructive actions
3. Save and restore user preferences
4. Handle errors gracefully

**Code Organization:**
1. Separate content builders from configuration
2. Use consistent naming conventions
3. Document custom behaviors
4. Provide examples and templates

The customization system provides the flexibility to create professional, tailored applications while maintaining the robustness and reliability of the underlying framework.