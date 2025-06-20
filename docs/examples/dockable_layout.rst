Dockable Layout Examples
========================

The ``DockableThreePaneWindow`` provides advanced features like draggable panes and detaching capabilities.

Basic Dockable Window
---------------------

Create a window with dockable panes:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import DockableThreePaneWindow

    def create_dockable_example():
        root = tk.Tk()
        root.title("Dockable Three-Pane Window")
        root.geometry("1000x600")

        def build_left_pane(frame):
            """Build the left pane content."""
            tk.Label(frame, text="Navigation Panel", 
                    font=("Arial", 12, "bold")).pack(pady=10)
            
            # Navigation buttons
            nav_items = ["Home", "Projects", "Settings", "Help"]
            for item in nav_items:
                btn = tk.Button(frame, text=f"📂 {item}", width=20)
                btn.pack(pady=3, padx=10, fill=tk.X)

        def build_center_pane(frame):
            """Build the center pane content."""
            tk.Label(frame, text="Main Workspace", 
                    font=("Arial", 14, "bold")).pack(pady=10)
            
            # Main content area
            content_frame = tk.Frame(frame)
            content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            text_area = tk.Text(content_frame, wrap=tk.WORD, font=("Arial", 11))
            scrollbar = tk.Scrollbar(content_frame, orient=tk.VERTICAL, command=text_area.yview)
            text_area.configure(yscrollcommand=scrollbar.set)
            
            text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            sample_content = '''Welcome to the Dockable Three-Pane Window!

This is the main content area. You can:

1. Drag the pane separators to resize
2. Right-click on pane headers to detach them
3. Drag detached panes back to dock them
4. Customize the layout to your needs

Try dragging the left or right pane headers to see the docking system in action!

The dockable system provides a professional, flexible interface that users can customize to their workflow.'''
            
            text_area.insert("1.0", sample_content)

        def build_right_pane(frame):
            """Build the right pane content."""
            tk.Label(frame, text="Properties & Tools", 
                    font=("Arial", 12, "bold")).pack(pady=10)
            
            # Properties section
            props_frame = tk.LabelFrame(frame, text="Properties", font=("Arial", 10, "bold"))
            props_frame.pack(fill=tk.X, padx=10, pady=5)
            
            properties = [
                ("Width:", "1000px"),
                ("Height:", "600px"),
                ("Panes:", "3"),
                ("Dockable:", "Yes")
            ]
            
            for prop, value in properties:
                prop_frame = tk.Frame(props_frame)
                prop_frame.pack(fill=tk.X, padx=5, pady=2)
                tk.Label(prop_frame, text=prop, font=("Arial", 9)).pack(side=tk.LEFT)
                tk.Label(prop_frame, text=value, font=("Arial", 9, "bold")).pack(side=tk.RIGHT)
            
            # Tools section
            tools_frame = tk.LabelFrame(frame, text="Tools", font=("Arial", 10, "bold"))
            tools_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tools = ["🔍 Search", "📊 Statistics", "⚙️ Configure", "💾 Export"]
            for tool in tools:
                tk.Button(tools_frame, text=tool, width=18).pack(pady=2, padx=5)

        # Create the dockable window
        dockable = DockableThreePaneWindow(
            root,
            side_width=200,
            left_builder=build_left_pane,
            center_builder=build_center_pane,
            right_builder=build_right_pane
        )
        dockable.pack(fill=tk.BOTH, expand=True)

        return root

    if __name__ == "__main__":
        app = create_dockable_example()
        app.mainloop()

IDE-Style Layout
----------------

Create an IDE-style interface with dockable panels:

.. code-block:: python

    import tkinter as tk
    from tkinter import ttk
    from threepanewindows import DockableThreePaneWindow

    def create_ide_example():
        root = tk.Tk()
        root.title("IDE-Style Dockable Layout")
        root.geometry("1200x800")

        def build_project_explorer(frame):
            """Build a project explorer panel."""
            tk.Label(frame, text="📁 Project Explorer", 
                    font=("Arial", 11, "bold")).pack(pady=5)
            
            # Project tree
            tree = ttk.Treeview(frame)
            tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Sample project structure
            project = tree.insert("", "end", text="📁 MyProject", open=True)
            src = tree.insert(project, "end", text="📁 src", open=True)
            tree.insert(src, "end", text="📄 main.py")
            tree.insert(src, "end", text="📄 utils.py")
            tree.insert(src, "end", text="📄 config.py")
            
            tests = tree.insert(project, "end", text="📁 tests")
            tree.insert(tests, "end", text="📄 test_main.py")
            tree.insert(tests, "end", text="📄 test_utils.py")
            
            tree.insert(project, "end", text="📄 README.md")
            tree.insert(project, "end", text="📄 requirements.txt")

        def build_code_editor(frame):
            """Build a code editor panel."""
            # Editor header
            header = tk.Frame(frame, bg="#f0f0f0", height=30)
            header.pack(fill=tk.X)
            header.pack_propagate(False)
            
            tk.Label(header, text="📝 main.py", font=("Arial", 10, "bold"), 
                    bg="#f0f0f0").pack(side=tk.LEFT, padx=10, pady=5)
            
            # Editor area
            editor_frame = tk.Frame(frame)
            editor_frame.pack(fill=tk.BOTH, expand=True)
            
            # Line numbers
            line_frame = tk.Frame(editor_frame, bg="#f8f8f8", width=40)
            line_frame.pack(side=tk.LEFT, fill=tk.Y)
            line_frame.pack_propagate(False)
            
            line_text = tk.Text(line_frame, width=4, bg="#f8f8f8", fg="#666", 
                               font=("Consolas", 10), state=tk.DISABLED, wrap=tk.NONE)
            line_text.pack(fill=tk.BOTH, expand=True)
            
            # Main editor
            editor = tk.Text(editor_frame, wrap=tk.NONE, font=("Consolas", 11),
                           bg="white", fg="black", insertbackground="black")
            editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Sample code
            sample_code = '''#!/usr/bin/env python3
"""
Main application module.
"""

import tkinter as tk
from threepanewindows import DockableThreePaneWindow

def main():
    """Main application entry point."""
    root = tk.Tk()
    root.title("My Application")
    root.geometry("1000x600")
    
    # Create the main interface
    app = DockableThreePaneWindow(root)
    app.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()

if __name__ == "__main__":
    main()'''
            
            editor.insert("1.0", sample_code)
            
            # Update line numbers
            lines = sample_code.count('\n') + 1
            line_text.config(state=tk.NORMAL)
            line_text.insert("1.0", '\n'.join(str(i) for i in range(1, lines + 1)))
            line_text.config(state=tk.DISABLED)

        def build_output_panel(frame):
            """Build an output/console panel."""
            tk.Label(frame, text="🖥️ Output Console", 
                    font=("Arial", 11, "bold")).pack(pady=5)
            
            # Console output
            console = tk.Text(frame, bg="black", fg="lime", font=("Consolas", 10),
                            height=8, wrap=tk.WORD)
            console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            console_output = '''Python 3.9.0 (default, Oct  9 2020, 15:07:54)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> print("Hello, World!")
Hello, World!
>>> import threepanewindows
>>> print("ThreePaneWindows loaded successfully!")
ThreePaneWindows loaded successfully!
>>> '''
            
            console.insert("1.0", console_output)

        # Create the IDE layout
        ide = DockableThreePaneWindow(
            root,
            side_width=250,
            left_builder=build_project_explorer,
            center_builder=build_code_editor,
            right_builder=build_output_panel
        )
        ide.pack(fill=tk.BOTH, expand=True)

        return root

    if __name__ == "__main__":
        app = create_ide_example()
        app.mainloop()

Advanced Docking Features
-------------------------

Demonstrate advanced docking capabilities:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import DockableThreePaneWindow

    def create_advanced_docking():
        root = tk.Tk()
        root.title("Advanced Docking Features")
        root.geometry("1100x700")

        def build_toolbox(frame):
            """Build a detachable toolbox."""
            tk.Label(frame, text="🧰 Toolbox", 
                    font=("Arial", 12, "bold")).pack(pady=10)
            
            # Tool categories
            categories = [
                ("Drawing", ["✏️ Pencil", "🖌️ Brush", "📐 Line", "⭕ Circle"]),
                ("Selection", ["👆 Select", "🔲 Rectangle", "⚪ Ellipse"]),
                ("Transform", ["🔄 Rotate", "📏 Scale", "↔️ Move"])
            ]
            
            for category, tools in categories:
                cat_frame = tk.LabelFrame(frame, text=category, font=("Arial", 10, "bold"))
                cat_frame.pack(fill=tk.X, padx=5, pady=5)
                
                for tool in tools:
                    tk.Button(cat_frame, text=tool, width=15).pack(pady=1, padx=5)

        def build_canvas_area(frame):
            """Build the main canvas area."""
            tk.Label(frame, text="🎨 Canvas", 
                    font=("Arial", 14, "bold")).pack(pady=10)
            
            # Canvas with scrollbars
            canvas_frame = tk.Frame(frame)
            canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            canvas = tk.Canvas(canvas_frame, bg="white", scrollregion=(0, 0, 1000, 1000))
            
            h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
            v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
            
            canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
            
            canvas.grid(row=0, column=0, sticky="nsew")
            h_scroll.grid(row=1, column=0, sticky="ew")
            v_scroll.grid(row=0, column=1, sticky="ns")
            
            canvas_frame.grid_rowconfigure(0, weight=1)
            canvas_frame.grid_columnconfigure(0, weight=1)
            
            # Add some sample shapes
            canvas.create_rectangle(50, 50, 150, 100, fill="lightblue", outline="blue")
            canvas.create_oval(200, 50, 300, 150, fill="lightcoral", outline="red")
            canvas.create_line(50, 200, 300, 250, fill="green", width=3)

        def build_properties(frame):
            """Build a properties panel."""
            tk.Label(frame, text="⚙️ Properties", 
                    font=("Arial", 12, "bold")).pack(pady=10)
            
            # Object properties
            obj_frame = tk.LabelFrame(frame, text="Selected Object", font=("Arial", 10, "bold"))
            obj_frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Property controls
            props = [
                ("X Position:", "50"),
                ("Y Position:", "50"),
                ("Width:", "100"),
                ("Height:", "50")
            ]
            
            for prop, value in props:
                prop_frame = tk.Frame(obj_frame)
                prop_frame.pack(fill=tk.X, padx=5, pady=2)
                
                tk.Label(prop_frame, text=prop, width=12, anchor="w").pack(side=tk.LEFT)
                entry = tk.Entry(prop_frame, width=10)
                entry.pack(side=tk.RIGHT)
                entry.insert(0, value)
            
            # Style properties
            style_frame = tk.LabelFrame(frame, text="Style", font=("Arial", 10, "bold"))
            style_frame.pack(fill=tk.X, padx=5, pady=5)
            
            tk.Label(style_frame, text="Fill Color:").pack(anchor="w", padx=5)
            color_frame = tk.Frame(style_frame)
            color_frame.pack(fill=tk.X, padx=5, pady=2)
            
            colors = ["red", "blue", "green", "yellow", "purple"]
            for color in colors:
                btn = tk.Button(color_frame, bg=color, width=3, height=1)
                btn.pack(side=tk.LEFT, padx=1)

        # Create the advanced docking window
        docking = DockableThreePaneWindow(
            root,
            side_width=180,
            left_builder=build_toolbox,
            center_builder=build_canvas_area,
            right_builder=build_properties
        )
        docking.pack(fill=tk.BOTH, expand=True)

        # Add instructions
        instructions = tk.Label(root, 
            text="💡 Try right-clicking on pane headers to detach them, then drag them back to dock!",
            bg="lightyellow", font=("Arial", 9))
        instructions.pack(fill=tk.X, pady=2)

        return root

    if __name__ == "__main__":
        app = create_advanced_docking()
        app.mainloop()

Key Docking Features
--------------------

The dockable layout provides:

1. **Drag-and-Drop**: Drag pane headers to reorder or detach
2. **Detachable Panes**: Right-click headers to detach into separate windows
3. **Re-docking**: Drag detached windows back to dock them
4. **Flexible Layout**: Users can customize the interface to their needs
5. **Professional Feel**: Smooth animations and visual feedback

Best Practices
--------------

When using dockable layouts:

- **Provide Clear Headers**: Use descriptive titles and icons
- **Logical Grouping**: Group related functionality in the same pane
- **Responsive Content**: Ensure content adapts to pane resizing
- **Save Layout State**: Consider saving user's preferred layout
- **Keyboard Shortcuts**: Provide shortcuts for common docking operations

Next Steps
----------

Explore more advanced features:

- :doc:`enhanced_professional` - Professional theming and advanced features
- :doc:`menu_integration` - Adding menus and toolbars
- :doc:`real_world_applications` - Complete application examples