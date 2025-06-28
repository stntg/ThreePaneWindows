Menu Integration Examples
=========================

This section shows how to integrate menus and toolbars with ThreePaneWindows layouts.

Basic Menu Integration
----------------------

Add a menu bar to a three-pane layout:

.. code-block:: python

    import tkinter as tk
    from tkinter import messagebox
    from threepanewindows import FixedThreePaneLayout

    def create_menu_example():
        root = tk.Tk()
        root.title("Three-Pane Window with Menu")
        root.geometry("900x600")

        def create_menu():
            """Create the application menu."""
            menubar = tk.Menu(root)

            # File menu
            file_menu = tk.Menu(menubar, tearoff=0)
            file_menu.add_command(label="New", accelerator="Ctrl+N",
                                command=lambda: messagebox.showinfo("Menu", "New File"))
            file_menu.add_command(label="Open", accelerator="Ctrl+O",
                                command=lambda: messagebox.showinfo("Menu", "Open File"))
            file_menu.add_command(label="Save", accelerator="Ctrl+S",
                                command=lambda: messagebox.showinfo("Menu", "Save File"))
            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=root.quit)
            menubar.add_cascade(label="File", menu=file_menu)

            # Edit menu
            edit_menu = tk.Menu(menubar, tearoff=0)
            edit_menu.add_command(label="Undo", accelerator="Ctrl+Z")
            edit_menu.add_command(label="Redo", accelerator="Ctrl+Y")
            edit_menu.add_separator()
            edit_menu.add_command(label="Cut", accelerator="Ctrl+X")
            edit_menu.add_command(label="Copy", accelerator="Ctrl+C")
            edit_menu.add_command(label="Paste", accelerator="Ctrl+V")
            menubar.add_cascade(label="Edit", menu=edit_menu)

            # View menu
            view_menu = tk.Menu(menubar, tearoff=0)
            view_menu.add_checkbutton(label="Show Left Panel", variable=tk.BooleanVar(value=True))
            view_menu.add_checkbutton(label="Show Right Panel", variable=tk.BooleanVar(value=True))
            view_menu.add_separator()
            view_menu.add_command(label="Zoom In", accelerator="Ctrl++")
            view_menu.add_command(label="Zoom Out", accelerator="Ctrl+-")
            menubar.add_cascade(label="View", menu=view_menu)

            # Help menu
            help_menu = tk.Menu(menubar, tearoff=0)
            help_menu.add_command(label="About",
                                command=lambda: messagebox.showinfo("About", "ThreePaneWindows Example"))
            menubar.add_cascade(label="Help", menu=help_menu)

            return menubar

        # Create the menu
        menu = create_menu()

        # Create layout with menu integration
        layout = FixedThreePaneLayout(root, side_width=200, menu_bar=menu)
        layout.pack(fill=tk.BOTH, expand=True)

        # Add content to demonstrate menu integration
        layout.set_label_texts(
            left="📁 Explorer",
            center="📝 Editor",
            right="🔧 Properties"
        )

        # Left panel content
        tk.Label(layout.frame_left, text="File Explorer",
                font=("Arial", 11, "bold")).pack(pady=10)

        files = ["document.txt", "image.png", "script.py", "data.csv"]
        for file in files:
            tk.Label(layout.frame_left, text=f"📄 {file}", anchor="w").pack(
                fill=tk.X, padx=10, pady=2)

        # Center panel content
        tk.Label(layout.frame_center, text="Text Editor",
                font=("Arial", 12, "bold")).pack(pady=10)

        text_editor = tk.Text(layout.frame_center, wrap=tk.WORD, font=("Consolas", 11))
        text_editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        sample_text = '''# Sample Document

This is a sample document in the text editor.

The menu bar above provides standard application functionality:
- File operations (New, Open, Save)
- Edit operations (Undo, Redo, Cut, Copy, Paste)
- View options (Panel visibility, Zoom)
- Help and About information

Try using the menu items to see how they integrate with the three-pane layout!'''

        text_editor.insert("1.0", sample_text)

        # Right panel content
        tk.Label(layout.frame_right, text="Properties",
                font=("Arial", 11, "bold")).pack(pady=10)

        properties = [
            ("File:", "document.txt"),
            ("Size:", "1.2 KB"),
            ("Lines:", "15"),
            ("Words:", "89"),
            ("Characters:", "456")
        ]

        for prop, value in properties:
            prop_frame = tk.Frame(layout.frame_right)
            prop_frame.pack(fill=tk.X, padx=10, pady=2)

            tk.Label(prop_frame, text=prop, font=("Arial", 9, "bold")).pack(side=tk.LEFT)
            tk.Label(prop_frame, text=value, font=("Arial", 9)).pack(side=tk.RIGHT)

        return root

    if __name__ == "__main__":
        app = create_menu_example()
        app.mainloop()

Toolbar Integration
-------------------

Add toolbars to enhance the interface:

.. code-block:: python

    import tkinter as tk
    from tkinter import ttk
    from threepanewindows import DockableThreePaneWindow

    def create_toolbar_example():
        root = tk.Tk()
        root.title("Three-Pane Window with Toolbar")
        root.geometry("1000x700")

        def create_menu_and_toolbar():
            """Create menu and toolbar."""
            # Menu bar
            menubar = tk.Menu(root)

            file_menu = tk.Menu(menubar, tearoff=0)
            file_menu.add_command(label="New Project")
            file_menu.add_command(label="Open Project")
            file_menu.add_command(label="Save Project")
            menubar.add_cascade(label="File", menu=file_menu)

            edit_menu = tk.Menu(menubar, tearoff=0)
            edit_menu.add_command(label="Undo")
            edit_menu.add_command(label="Redo")
            menubar.add_cascade(label="Edit", menu=edit_menu)

            # Toolbar frame
            toolbar = tk.Frame(root, bg="#f0f0f0", height=40, relief=tk.RAISED, bd=1)
            toolbar.pack(fill=tk.X)
            toolbar.pack_propagate(False)

            # Toolbar buttons
            toolbar_buttons = [
                ("📄 New", "#4CAF50"),
                ("📂 Open", "#2196F3"),
                ("💾 Save", "#FF9800"),
                ("|", None),  # Separator
                ("↶ Undo", "#9E9E9E"),
                ("↷ Redo", "#9E9E9E"),
                ("|", None),  # Separator
                ("▶️ Run", "#4CAF50"),
                ("⏹️ Stop", "#F44336"),
                ("🔧 Debug", "#FF9800")
            ]

            for btn_text, color in toolbar_buttons:
                if btn_text == "|":  # Separator
                    separator = tk.Frame(toolbar, width=2, bg="#d0d0d0")
                    separator.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
                else:
                    btn = tk.Button(toolbar, text=btn_text, bg=color, fg="white",
                                  font=("Arial", 9), relief="flat", padx=10, pady=5)
                    btn.pack(side=tk.LEFT, padx=2, pady=5)

            # Status info on right side of toolbar
            status_frame = tk.Frame(toolbar, bg="#f0f0f0")
            status_frame.pack(side=tk.RIGHT, padx=10, pady=5)

            tk.Label(status_frame, text="Ready", bg="#f0f0f0",
                    font=("Arial", 9)).pack(side=tk.RIGHT)

            return menubar

        def build_project_tree(frame):
            """Build project tree panel."""
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

            tree.insert(project, "end", text="📄 README.md")

        def build_code_editor(frame):
            """Build code editor panel."""
            # Editor toolbar
            editor_toolbar = tk.Frame(frame, bg="#e0e0e0", height=30)
            editor_toolbar.pack(fill=tk.X)
            editor_toolbar.pack_propagate(False)

            # File tabs
            tabs = ["main.py", "utils.py", "config.py"]
            for i, tab in enumerate(tabs):
                tab_color = "#ffffff" if i == 0 else "#e0e0e0"
                tab_btn = tk.Button(editor_toolbar, text=tab, bg=tab_color,
                                  font=("Arial", 9), relief="flat", padx=15)
                tab_btn.pack(side=tk.LEFT, padx=1, pady=2)

            # Editor area
            editor_frame = tk.Frame(frame)
            editor_frame.pack(fill=tk.BOTH, expand=True)

            # Line numbers
            line_frame = tk.Frame(editor_frame, bg="#f8f8f8", width=40)
            line_frame.pack(side=tk.LEFT, fill=tk.Y)
            line_frame.pack_propagate(False)

            line_numbers = tk.Text(line_frame, width=4, bg="#f8f8f8", fg="#666",
                                 font=("Consolas", 10), state=tk.DISABLED, wrap=tk.NONE)
            line_numbers.pack(fill=tk.BOTH, expand=True)

            # Code editor
            code_editor = tk.Text(editor_frame, wrap=tk.NONE, font=("Consolas", 11),
                                bg="white", fg="black", insertbackground="black")
            code_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Sample code
            sample_code = '''#!/usr/bin/env python3
"""
Main application module.
"""

import tkinter as tk
from threepanewindows import DockableThreePaneWindow

def create_application():
    """Create the main application window."""
    root = tk.Tk()
    root.title("My Application")
    root.geometry("1000x600")

    # Create three-pane layout
    layout = DockableThreePaneWindow(root)
    layout.pack(fill=tk.BOTH, expand=True)

    return root

def main():
    """Main entry point."""
    app = create_application()
    app.mainloop()

if __name__ == "__main__":
    main()'''

            code_editor.insert("1.0", sample_code)

            # Update line numbers
            lines = sample_code.count('\n') + 1
            line_numbers.config(state=tk.NORMAL)
            line_numbers.insert("1.0", '\n'.join(str(i) for i in range(1, lines + 1)))
            line_numbers.config(state=tk.DISABLED)

        def build_output_panel(frame):
            """Build output panel."""
            # Output toolbar
            output_toolbar = tk.Frame(frame, bg="#2d2d2d", height=30)
            output_toolbar.pack(fill=tk.X)
            output_toolbar.pack_propagate(False)

            tk.Label(output_toolbar, text="🖥️ Output", font=("Arial", 10, "bold"),
                    bg="#2d2d2d", fg="white").pack(side=tk.LEFT, padx=10, pady=5)

            # Clear button
            clear_btn = tk.Button(output_toolbar, text="🗑️ Clear", bg="#666", fg="white",
                                font=("Arial", 8), relief="flat", padx=8)
            clear_btn.pack(side=tk.RIGHT, padx=10, pady=5)

            # Output area
            output = tk.Text(frame, bg="black", fg="lime", font=("Consolas", 10))
            output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            output_text = '''Python 3.9.0 (default, Oct  9 2020, 15:07:54)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> print("Hello from ThreePaneWindows!")
Hello from ThreePaneWindows!
>>> import threepanewindows
>>> print("Library loaded successfully!")
Library loaded successfully!
>>> '''

            output.insert("1.0", output_text)

        # Create menu and toolbar
        menu = create_menu_and_toolbar()

        # Create dockable layout
        dockable = DockableThreePaneWindow(
            root,
            side_width=250,
            left_builder=build_project_tree,
            center_builder=build_code_editor,
            right_builder=build_output_panel,
            menu_bar=menu
        )
        dockable.pack(fill=tk.BOTH, expand=True)

        # Status bar
        status_bar = tk.Label(root, text="Ready | Line 1, Column 1 | Python",
                            relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 9))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        return root

    if __name__ == "__main__":
        app = create_toolbar_example()
        app.mainloop()

Context Menus
-------------

Add context menus to panes:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import FixedThreePaneLayout

    def create_context_menu_example():
        root = tk.Tk()
        root.title("Three-Pane Window with Context Menus")
        root.geometry("800x600")

        def create_file_context_menu(widget):
            """Create context menu for file operations."""
            context_menu = tk.Menu(root, tearoff=0)
            context_menu.add_command(label="📂 Open",
                                   command=lambda: print("Open file"))
            context_menu.add_command(label="✏️ Edit",
                                   command=lambda: print("Edit file"))
            context_menu.add_separator()
            context_menu.add_command(label="📋 Copy",
                                   command=lambda: print("Copy file"))
            context_menu.add_command(label="✂️ Cut",
                                   command=lambda: print("Cut file"))
            context_menu.add_command(label="📌 Paste",
                                   command=lambda: print("Paste file"))
            context_menu.add_separator()
            context_menu.add_command(label="🗑️ Delete",
                                   command=lambda: print("Delete file"))
            context_menu.add_command(label="🏷️ Rename",
                                   command=lambda: print("Rename file"))

            def show_context_menu(event):
                try:
                    context_menu.tk_popup(event.x_root, event.y_root)
                finally:
                    context_menu.grab_release()

            widget.bind("<Button-3>", show_context_menu)  # Right-click
            return context_menu

        def create_editor_context_menu(widget):
            """Create context menu for editor operations."""
            context_menu = tk.Menu(root, tearoff=0)
            context_menu.add_command(label="↶ Undo",
                                   command=lambda: widget.event_generate("<<Undo>>"))
            context_menu.add_command(label="↷ Redo",
                                   command=lambda: widget.event_generate("<<Redo>>"))
            context_menu.add_separator()
            context_menu.add_command(label="✂️ Cut",
                                   command=lambda: widget.event_generate("<<Cut>>"))
            context_menu.add_command(label="📋 Copy",
                                   command=lambda: widget.event_generate("<<Copy>>"))
            context_menu.add_command(label="📌 Paste",
                                   command=lambda: widget.event_generate("<<Paste>>"))
            context_menu.add_separator()
            context_menu.add_command(label="🔍 Find",
                                   command=lambda: print("Find"))
            context_menu.add_command(label="🔄 Replace",
                                   command=lambda: print("Replace"))

            def show_context_menu(event):
                try:
                    context_menu.tk_popup(event.x_root, event.y_root)
                finally:
                    context_menu.grab_release()

            widget.bind("<Button-3>", show_context_menu)
            return context_menu

        # Create layout
        layout = FixedThreePaneLayout(root, side_width=200)
        layout.pack(fill=tk.BOTH, expand=True)

        layout.set_label_texts(
            left="📁 Files (Right-click for menu)",
            center="📝 Editor (Right-click for menu)",
            right="🔧 Properties"
        )

        # Left panel with file context menu
        file_listbox = tk.Listbox(layout.frame_left, font=("Arial", 10))
        file_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        files = ["📄 document.txt", "🖼️ image.png", "🐍 script.py", "📊 data.csv"]
        for file in files:
            file_listbox.insert(tk.END, file)

        # Add context menu to file list
        create_file_context_menu(file_listbox)

        # Center panel with editor context menu
        text_editor = tk.Text(layout.frame_center, wrap=tk.WORD, font=("Arial", 11))
        text_editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        editor_text = '''Right-click anywhere in this text editor to see the context menu.

The context menu provides common editing operations:
- Undo/Redo
- Cut/Copy/Paste
- Find/Replace

Try selecting some text and right-clicking to see the options.

Context menus provide quick access to frequently used commands without cluttering the interface with buttons.'''

        text_editor.insert("1.0", editor_text)

        # Add context menu to editor
        create_editor_context_menu(text_editor)

        # Right panel
        tk.Label(layout.frame_right, text="Properties Panel",
                font=("Arial", 11, "bold")).pack(pady=10)

        tk.Label(layout.frame_right, text="Context menus provide:\n\n"
                                         "• Quick access to commands\n"
                                         "• Context-sensitive options\n"
                                         "• Reduced interface clutter\n"
                                         "• Improved user experience",
                justify=tk.LEFT, anchor="w").pack(padx=10, pady=10)

        return root

    if __name__ == "__main__":
        app = create_context_menu_example()
        app.mainloop()

Best Practices for Menu Integration
-----------------------------------

1. **Consistent Menu Structure**: Follow standard menu conventions
2. **Keyboard Shortcuts**: Provide accelerator keys for common actions
3. **Context Sensitivity**: Enable/disable menu items based on current state
4. **Logical Grouping**: Group related menu items together
5. **Clear Labels**: Use descriptive, action-oriented menu labels

Menu Integration Features
-------------------------

ThreePaneWindows supports:

- **Menu Bar Integration**: Pass menu to layout constructors
- **Toolbar Support**: Add toolbars above or below the layout
- **Context Menus**: Right-click menus for pane-specific actions
- **Status Bar**: Information display at the bottom
- **Keyboard Shortcuts**: Full keyboard navigation support

Configuration Example
---------------------

Complete menu integration setup:

.. code-block:: python

    # Create menu
    menubar = create_application_menu()

    # Create layout with menu
    layout = FixedThreePaneLayout(
        root,
        menu_bar=menubar,  # Integrate menu
        side_width=200
    )

    # Add toolbar
    toolbar = create_toolbar(root)
    toolbar.pack(fill=tk.X)

    # Add layout
    layout.pack(fill=tk.BOTH, expand=True)

    # Add status bar
    status_bar = create_status_bar(root)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

Next Steps
----------

Explore more integration examples:

- :doc:`status_bar_integration` - Adding status bars and notifications
- :doc:`custom_widgets` - Creating custom panel content
- :doc:`real_world_applications` - Complete application examples
