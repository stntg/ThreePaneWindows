Fixed Width Panes Examples
===========================

This section demonstrates how to create panes with fixed widths that don't resize when the window is resized.

Basic Fixed Width Layout
-------------------------

Create a layout where side panes have fixed widths:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import FixedThreePaneLayout

    def create_basic_fixed_width():
        root = tk.Tk()
        root.title("Basic Fixed Width Example")
        root.geometry("800x500")

        # Create layout with left pane fixed at 200px, right pane resizable
        layout = FixedThreePaneLayout(
            root,
            left_fixed_width=200,    # Left pane stays at 200px
            right_fixed_width=None,  # Right pane resizes normally
            side_width=150           # Default width for right pane
        )
        layout.pack(fill=tk.BOTH, expand=True)

        # Add content to demonstrate fixed vs resizable behavior
        tk.Label(layout.frame_left, text="FIXED WIDTH\n200px",
                bg="#3A7CA5", fg="white", font=("Arial", 12, "bold")).pack(expand=True)

        tk.Label(layout.frame_center, text="CENTER - RESIZABLE\nAdjusts to fill remaining space",
                font=("Arial", 12, "bold")).pack(expand=True)

        tk.Label(layout.frame_right, text="RESIZABLE\nChanges with window",
                bg="#F4A261", font=("Arial", 10, "bold")).pack(expand=True)

        # Instructions
        instructions = tk.Label(root,
            text="💡 Try resizing the window - left pane stays 200px, center adjusts, right resizes normally",
            bg="lightyellow", font=("Arial", 9))
        instructions.pack(fill=tk.X, pady=2)

        return root

    if __name__ == "__main__":
        app = create_basic_fixed_width()
        app.mainloop()

Both Sides Fixed
-----------------

Create a layout where both side panes have fixed widths:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import FixedThreePaneLayout

    def create_both_sides_fixed():
        root = tk.Tk()
        root.title("Both Sides Fixed Width")
        root.geometry("900x600")

        # Both side panes have fixed widths
        layout = FixedThreePaneLayout(
            root,
            left_fixed_width=180,   # Left fixed at 180px
            right_fixed_width=220   # Right fixed at 220px
        )
        layout.pack(fill=tk.BOTH, expand=True)

        layout.set_label_texts(
            left="🗂️ Navigation (180px)",
            center="📝 Content Area (Flexible)",
            right="🔧 Tools (220px)"
        )

        # Left panel - Navigation
        nav_frame = tk.Frame(layout.frame_left, bg="#E8F4FD")
        nav_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(nav_frame, text="Navigation Menu", font=("Arial", 11, "bold"),
                bg="#E8F4FD").pack(pady=10)

        nav_items = ["🏠 Home", "📊 Dashboard", "📁 Projects", "⚙️ Settings", "❓ Help"]
        for item in nav_items:
            btn = tk.Button(nav_frame, text=item, width=18, anchor="w")
            btn.pack(pady=2, padx=10, fill=tk.X)

        # Center panel - Main content
        content_frame = tk.Frame(layout.frame_center)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(content_frame, text="Main Content Area",
                font=("Arial", 14, "bold")).pack(pady=10)

        text_area = tk.Text(content_frame, wrap=tk.WORD, font=("Arial", 11))
        scrollbar = tk.Scrollbar(content_frame, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)

        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        sample_text = '''This is the main content area.

The left navigation panel is fixed at 180 pixels wide.
The right tools panel is fixed at 220 pixels wide.
This center panel expands and contracts to fill the remaining space.

Try resizing the window to see how the layout behaves:
- Left panel: Always 180px
- Right panel: Always 220px
- Center panel: Adjusts to fill remaining width

This is perfect for applications where you need consistent sidebar widths but want the main content to be flexible.'''

        text_area.insert("1.0", sample_text)

        # Right panel - Tools
        tools_frame = tk.Frame(layout.frame_right, bg="#FFF8E1")
        tools_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(tools_frame, text="Tool Panel", font=("Arial", 11, "bold"),
                bg="#FFF8E1").pack(pady=10)

        # Tool sections
        sections = [
            ("Quick Actions", ["🔍 Search", "📋 Copy", "✂️ Cut", "📌 Pin"]),
            ("Format", ["🅱️ Bold", "🅸 Italic", "🅿️ Underline"]),
            ("View", ["🔍 Zoom In", "🔍 Zoom Out", "📏 Fit Width"])
        ]

        for section_name, tools in sections:
            section_frame = tk.LabelFrame(tools_frame, text=section_name,
                                        font=("Arial", 9, "bold"), bg="#FFF8E1")
            section_frame.pack(fill=tk.X, padx=5, pady=5)

            for tool in tools:
                btn = tk.Button(section_frame, text=tool, width=20)
                btn.pack(pady=1, padx=5)

        return root

    if __name__ == "__main__":
        app = create_both_sides_fixed()
        app.mainloop()

Dockable Window with Fixed Widths
----------------------------------

Use fixed widths with the dockable window system:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import DockableThreePaneWindow

    def create_dockable_fixed_width():
        root = tk.Tk()
        root.title("Dockable Window - Fixed Width Panels")
        root.geometry("1000x650")

        def build_sidebar(frame):
            """Build a fixed-width sidebar."""
            tk.Label(frame, text="📁 SIDEBAR", font=("Arial", 12, "bold")).pack(pady=10)
            tk.Label(frame, text="Fixed: 200px", fg="red", font=("Arial", 9)).pack()

            # File tree simulation
            files = [
                "📁 Documents",
                "  📄 report.docx",
                "  📄 notes.txt",
                "📁 Images",
                "  🖼️ photo1.jpg",
                "  🖼️ photo2.png",
                "📁 Projects",
                "  📁 WebApp",
                "  📁 MobileApp"
            ]

            listbox = tk.Listbox(frame, font=("Arial", 9))
            listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            for file in files:
                listbox.insert(tk.END, file)

        def build_main_area(frame):
            """Build the main resizable area."""
            tk.Label(frame, text="📝 MAIN AREA", font=("Arial", 14, "bold")).pack(pady=10)
            tk.Label(frame, text="Resizable - Fills remaining space",
                    fg="green", font=("Arial", 10)).pack()

            # Main content
            content_frame = tk.Frame(frame)
            content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Simulated document editor
            editor = tk.Text(content_frame, wrap=tk.WORD, font=("Arial", 11))
            editor.pack(fill=tk.BOTH, expand=True)

            editor_content = '''# Document Editor

This is the main content area that resizes to fill the available space.

## Fixed Width Benefits:

1. **Consistent Layout**: Sidebars maintain their size
2. **Predictable Interface**: Users know where to find tools
3. **Professional Look**: Clean, organized appearance
4. **Flexible Content**: Main area adapts to window size

## How It Works:

- Left sidebar: Fixed at 200px (cannot be resized)
- Right panel: Fixed at 180px (cannot be resized)
- Center area: Expands/contracts to fill remaining width

This creates a professional, predictable interface while maintaining flexibility where it matters most - in the main content area.'''

            editor.insert("1.0", editor_content)

        def build_properties(frame):
            """Build a fixed-width properties panel."""
            tk.Label(frame, text="🔧 PROPERTIES", font=("Arial", 12, "bold")).pack(pady=10)
            tk.Label(frame, text="Fixed: 180px", fg="red", font=("Arial", 9)).pack()

            # Properties sections
            sections = [
                ("Document", [
                    ("Name:", "document.txt"),
                    ("Size:", "2.4 KB"),
                    ("Lines:", "45"),
                    ("Words:", "312")
                ]),
                ("Format", [
                    ("Font:", "Arial"),
                    ("Size:", "11pt"),
                    ("Style:", "Normal"),
                    ("Color:", "Black")
                ]),
                ("Layout", [
                    ("Width:", "Auto"),
                    ("Height:", "Auto"),
                    ("Margin:", "1 inch"),
                    ("Spacing:", "Single")
                ])
            ]

            for section_name, properties in sections:
                section_frame = tk.LabelFrame(frame, text=section_name,
                                            font=("Arial", 9, "bold"))
                section_frame.pack(fill=tk.X, padx=5, pady=5)

                for prop, value in properties:
                    prop_frame = tk.Frame(section_frame)
                    prop_frame.pack(fill=tk.X, padx=3, pady=1)

                    tk.Label(prop_frame, text=prop, font=("Arial", 8),
                            width=8, anchor="w").pack(side=tk.LEFT)
                    tk.Label(prop_frame, text=value, font=("Arial", 8, "bold"),
                            anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Create dockable window with fixed widths
        dockable = DockableThreePaneWindow(
            root,
            left_builder=build_sidebar,
            center_builder=build_main_area,
            right_builder=build_properties,
            left_fixed_width=200,   # Left panel fixed at 200px
            right_fixed_width=180   # Right panel fixed at 180px
        )
        dockable.pack(fill=tk.BOTH, expand=True)

        # Instructions
        instructions = tk.Label(root,
            text="💡 Panels are detachable but maintain their fixed widths even when detached!",
            bg="lightblue", font=("Arial", 9))
        instructions.pack(fill=tk.X, pady=2)

        return root

    if __name__ == "__main__":
        app = create_dockable_fixed_width()
        app.mainloop()

Enhanced Window with Fixed Widths
----------------------------------

Use fixed widths with the enhanced professional window:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

    def create_enhanced_fixed_width():
        root = tk.Tk()
        root.title("Enhanced Window - Professional Fixed Width Layout")
        root.geometry("1200x700")

        def build_navigation(frame):
            """Build a professional navigation panel."""
            # Header
            header = tk.Frame(frame, bg="#2C3E50", height=40)
            header.pack(fill=tk.X)
            header.pack_propagate(False)

            tk.Label(header, text="🧭 Navigation", font=("Segoe UI", 11, "bold"),
                    bg="#2C3E50", fg="white").pack(pady=10)

            # Navigation sections
            sections = [
                ("📊 Dashboard", ["Overview", "Analytics", "Reports"]),
                ("📁 Projects", ["Active", "Completed", "Archived"]),
                ("👥 Team", ["Members", "Roles", "Permissions"]),
                ("⚙️ Settings", ["General", "Security", "Integrations"])
            ]

            for section_name, items in sections:
                # Section header
                section_btn = tk.Button(frame, text=section_name, font=("Segoe UI", 10, "bold"),
                                      bg="#34495E", fg="white", anchor="w", relief="flat")
                section_btn.pack(fill=tk.X, padx=5, pady=2)

                # Section items
                for item in items:
                    item_btn = tk.Button(frame, text=f"  • {item}", font=("Segoe UI", 9),
                                       bg="#ECF0F1", anchor="w", relief="flat")
                    item_btn.pack(fill=tk.X, padx=15, pady=1)

        def build_workspace(frame):
            """Build the main workspace area."""
            # Workspace header
            header = tk.Frame(frame, bg="#3498DB", height=50)
            header.pack(fill=tk.X)
            header.pack_propagate(False)

            title_frame = tk.Frame(header, bg="#3498DB")
            title_frame.pack(expand=True, fill=tk.BOTH)

            tk.Label(title_frame, text="📝 Main Workspace", font=("Segoe UI", 14, "bold"),
                    bg="#3498DB", fg="white").pack(pady=15)

            # Content area
            content_frame = tk.Frame(frame, bg="white")
            content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Dashboard-style content
            stats_frame = tk.Frame(content_frame, bg="white")
            stats_frame.pack(fill=tk.X, pady=10)

            # Statistics cards
            stats = [
                ("📈 Revenue", "$125,430", "#27AE60"),
                ("👥 Users", "8,492", "#3498DB"),
                ("📊 Orders", "1,247", "#E67E22"),
                ("⭐ Rating", "4.8/5", "#9B59B6")
            ]

            for i, (title, value, color) in enumerate(stats):
                card = tk.Frame(stats_frame, bg=color, relief="raised", bd=2)
                card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

                tk.Label(card, text=title, font=("Segoe UI", 10, "bold"),
                        bg=color, fg="white").pack(pady=5)
                tk.Label(card, text=value, font=("Segoe UI", 16, "bold"),
                        bg=color, fg="white").pack(pady=5)

            # Main content area
            main_content = tk.Frame(content_frame, bg="#F8F9FA", relief="sunken", bd=1)
            main_content.pack(fill=tk.BOTH, expand=True, pady=10)

            tk.Label(main_content, text="📋 Recent Activity", font=("Segoe UI", 12, "bold"),
                    bg="#F8F9FA").pack(pady=10)

            # Activity list
            activities = [
                "🔄 Project 'WebApp' updated 2 minutes ago",
                "👤 New user registered 5 minutes ago",
                "📊 Monthly report generated 15 minutes ago",
                "💰 Payment received from Client ABC 1 hour ago",
                "📧 Email campaign sent to 1,500 subscribers 2 hours ago"
            ]

            for activity in activities:
                activity_frame = tk.Frame(main_content, bg="white", relief="flat", bd=1)
                activity_frame.pack(fill=tk.X, padx=10, pady=2)

                tk.Label(activity_frame, text=activity, font=("Segoe UI", 9),
                        bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=5)

        def build_inspector(frame):
            """Build a professional inspector panel."""
            # Header
            header = tk.Frame(frame, bg="#8E44AD", height=40)
            header.pack(fill=tk.X)
            header.pack_propagate(False)

            tk.Label(header, text="🔍 Inspector", font=("Segoe UI", 11, "bold"),
                    bg="#8E44AD", fg="white").pack(pady=10)

            # Inspector sections
            sections = [
                ("📋 Details", [
                    ("ID:", "PRJ-2024-001"),
                    ("Status:", "Active"),
                    ("Priority:", "High"),
                    ("Due Date:", "Jan 30, 2024")
                ]),
                ("👤 Assignment", [
                    ("Owner:", "John Smith"),
                    ("Team:", "Development"),
                    ("Reviewer:", "Jane Doe"),
                    ("Progress:", "75%")
                ]),
                ("📊 Metrics", [
                    ("Budget:", "$15,000"),
                    ("Spent:", "$11,250"),
                    ("Hours:", "120/160"),
                    ("Efficiency:", "94%")
                ]),
                ("🏷️ Tags", [
                    ("Category:", "Web Development"),
                    ("Technology:", "React, Node.js"),
                    ("Client:", "TechCorp Inc"),
                    ("Version:", "2.1.0")
                ])
            ]

            for section_name, properties in sections:
                section_frame = tk.LabelFrame(frame, text=section_name,
                                            font=("Segoe UI", 9, "bold"),
                                            bg="#F8F9FA", fg="#2C3E50")
                section_frame.pack(fill=tk.X, padx=8, pady=5)

                for prop, value in properties:
                    prop_frame = tk.Frame(section_frame, bg="#F8F9FA")
                    prop_frame.pack(fill=tk.X, padx=5, pady=2)

                    tk.Label(prop_frame, text=prop, font=("Segoe UI", 8, "bold"),
                            bg="#F8F9FA", width=10, anchor="w").pack(side=tk.LEFT)
                    tk.Label(prop_frame, text=value, font=("Segoe UI", 8),
                            bg="#F8F9FA", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Configure panes with fixed widths
        nav_config = PaneConfig(
            title="Navigation",
            icon="🧭",
            fixed_width=250,  # Fixed at 250px
            detachable=True
        )

        workspace_config = PaneConfig(
            title="Workspace",
            icon="📝",
            detachable=False
        )

        inspector_config = PaneConfig(
            title="Inspector",
            icon="🔍",
            fixed_width=280,  # Fixed at 280px
            detachable=True
        )

        # Create enhanced window with fixed widths
        enhanced = EnhancedDockableThreePaneWindow(
            root,
            left_config=nav_config,
            center_config=workspace_config,
            right_config=inspector_config,
            left_builder=build_navigation,
            center_builder=build_workspace,
            right_builder=build_inspector,
            theme_name="blue"
        )
        enhanced.pack(fill=tk.BOTH, expand=True)

        # Status bar
        status = tk.Label(root, text="💡 Navigation: 250px fixed | Workspace: flexible | Inspector: 280px fixed",
                         bg="#BDC3C7", font=("Segoe UI", 9), anchor="w")
        status.pack(fill=tk.X)

        return root

    if __name__ == "__main__":
        app = create_enhanced_fixed_width()
        app.mainloop()

When to Use Fixed Width Panes
------------------------------

Fixed width panes are ideal for:

1. **Navigation Panels**: Keep navigation consistent and predictable
2. **Tool Palettes**: Maintain tool accessibility at a fixed size
3. **Property Inspectors**: Ensure property panels don't get too narrow
4. **Status Panels**: Keep status information at a readable width
5. **Professional Applications**: Create polished, consistent interfaces

Benefits of Fixed Width Panes
------------------------------

- **Consistency**: Interface elements stay in predictable locations
- **Professional Appearance**: Clean, organized layout
- **User Experience**: Users know where to find tools and information
- **Content Protection**: Prevents important panels from becoming too narrow
- **Responsive Design**: Main content area adapts while sidebars stay stable

Configuration Options
---------------------

Fixed width configuration options:

.. code-block:: python

    # For FixedThreePaneLayout
    layout = FixedThreePaneLayout(
        root,
        left_fixed_width=200,    # Left pane fixed at 200px
        right_fixed_width=None   # Right pane resizes normally
    )

    # For DockableThreePaneWindow
    dockable = DockableThreePaneWindow(
        root,
        left_fixed_width=180,    # Left pane fixed
        right_fixed_width=220    # Right pane fixed
    )

    # For EnhancedDockableThreePaneWindow
    config = PaneConfig(
        title="Panel",
        fixed_width=250          # Panel fixed at 250px
    )

Next Steps
----------

Learn more about advanced features:

- :doc:`enhanced_professional` - Professional theming and styling
- :doc:`menu_integration` - Adding menus and toolbars
- :doc:`real_world_applications` - Complete application examples
