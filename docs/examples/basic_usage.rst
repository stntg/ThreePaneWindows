Basic Usage Examples
====================

This page shows the most basic ways to use ThreePaneWindows.

Simple Three-Pane Layout
-------------------------

The simplest way to create a three-pane layout:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import FixedThreePaneLayout

    # Create main window
    root = tk.Tk()
    root.title("Basic Three-Pane Example")
    root.geometry("800x600")

    # Create the layout
    layout = FixedThreePaneLayout(root, side_width=200)
    layout.pack(fill=tk.BOTH, expand=True)

    # Add content to left pane
    tk.Label(layout.frame_left, text="Left Panel",
             font=("Arial", 12, "bold")).pack(pady=10)

    for i in range(5):
        tk.Button(layout.frame_left, text=f"Button {i+1}").pack(
            fill=tk.X, padx=5, pady=2)

    # Add content to center pane
    tk.Label(layout.frame_center, text="Main Content",
             font=("Arial", 14, "bold")).pack(pady=10)

    text_area = tk.Text(layout.frame_center, wrap=tk.WORD)
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    text_area.insert("1.0", "This is the main content area.")

    # Add content to right pane
    tk.Label(layout.frame_right, text="Properties",
             font=("Arial", 12, "bold")).pack(pady=10)

    tk.Label(layout.frame_right, text="Setting 1:").pack(anchor="w", padx=5)
    tk.Entry(layout.frame_right).pack(fill=tk.X, padx=5, pady=2)

    tk.Label(layout.frame_right, text="Setting 2:").pack(anchor="w", padx=5)
    tk.Entry(layout.frame_right).pack(fill=tk.X, padx=5, pady=2)

    root.mainloop()

Custom Labels
-------------

You can customize the pane labels:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import FixedThreePaneLayout

    root = tk.Tk()
    root.title("Custom Labels Example")
    root.geometry("900x650")

    layout = FixedThreePaneLayout(root, side_width=180)
    layout.pack(fill=tk.BOTH, expand=True)

    # Set custom labels with icons
    layout.set_label_texts(
        left="🗂️ File Explorer",
        center="📝 Document Editor",
        right="🔧 Tool Panel"
    )

    # Add file explorer content
    files = ["document.txt", "image.png", "script.py", "data.csv"]
    for file in files:
        file_frame = tk.Frame(layout.frame_left)
        file_frame.pack(fill=tk.X, padx=5, pady=1)

        icon = "📄" if file.endswith(('.txt', '.py')) else "🖼️" if file.endswith('.png') else "📊"
        tk.Label(file_frame, text=f"{icon} {file}").pack(side=tk.LEFT)

    # Add editor content
    editor = tk.Text(layout.frame_center, wrap=tk.WORD, font=("Consolas", 11))
    editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    sample_text = '''# Sample Document
This is a sample document in the editor.

You can add any content here:
- Lists
- Code snippets
- Regular text

The layout automatically handles resizing!'''

    editor.insert("1.0", sample_text)

    # Add tool panel content
    tools = ["🔍 Search", "📋 Copy", "✂️ Cut", "📌 Pin", "🔄 Refresh"]
    for tool in tools:
        tk.Button(layout.frame_right, text=tool, width=15).pack(
            pady=3, padx=5, fill=tk.X)

    root.mainloop()

Simple File Manager
-------------------

A basic file manager-style interface:

.. code-block:: python

    import tkinter as tk
    from tkinter import ttk
    from threepanewindows import FixedThreePaneLayout

    def create_file_manager():
        root = tk.Tk()
        root.title("Simple File Manager")
        root.geometry("1000x700")

        layout = FixedThreePaneLayout(root, side_width=220)
        layout.pack(fill=tk.BOTH, expand=True)

        layout.set_label_texts(
            left="📁 Folders",
            center="📄 Files",
            right="ℹ️ Details"
        )

        # Folder tree (left pane)
        folder_tree = ttk.Treeview(layout.frame_left)
        folder_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add sample folders
        documents = folder_tree.insert("", "end", text="📁 Documents", open=True)
        folder_tree.insert(documents, "end", text="📁 Projects")
        folder_tree.insert(documents, "end", text="📁 Reports")

        pictures = folder_tree.insert("", "end", text="📁 Pictures")
        folder_tree.insert(pictures, "end", text="📁 Vacation")
        folder_tree.insert(pictures, "end", text="📁 Screenshots")

        # File list (center pane)
        file_frame = tk.Frame(layout.frame_center)
        file_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        file_listbox = tk.Listbox(file_frame, font=("Arial", 10))
        file_listbox.pack(fill=tk.BOTH, expand=True)

        # Sample files
        files = [
            "📄 report.docx",
            "📊 data.xlsx",
            "🖼️ photo.jpg",
            "📝 notes.txt",
            "🐍 script.py"
        ]

        for file in files:
            file_listbox.insert(tk.END, file)

        # Details panel (right pane)
        details_frame = tk.Frame(layout.frame_right)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(details_frame, text="File Details",
                font=("Arial", 11, "bold")).pack(pady=(0, 10))

        details = [
            ("Name:", "report.docx"),
            ("Size:", "2.4 MB"),
            ("Type:", "Word Document"),
            ("Modified:", "Today, 2:30 PM"),
            ("Created:", "Yesterday")
        ]

        for label, value in details:
            detail_frame = tk.Frame(details_frame)
            detail_frame.pack(fill=tk.X, pady=2)

            tk.Label(detail_frame, text=label, font=("Arial", 9, "bold")).pack(side=tk.LEFT)
            tk.Label(detail_frame, text=value, font=("Arial", 9)).pack(side=tk.RIGHT)

        return root

    if __name__ == "__main__":
        app = create_file_manager()
        app.mainloop()

Key Features Demonstrated
-------------------------

These basic examples show:

1. **Simple Setup**: How to create a three-pane layout with minimal code
2. **Content Addition**: Adding widgets to each pane
3. **Custom Labels**: Setting meaningful labels for each pane
4. **Real-world Layout**: Creating a practical file manager interface
5. **Responsive Design**: How the layout adapts to window resizing

Next Steps
----------

Once you're comfortable with these basics, try:

- :doc:`dockable_layout` - For draggable and detachable panes
- :doc:`enhanced_professional` - For advanced theming and features
- :doc:`fixed_width_panes` - For precise control over pane sizing
