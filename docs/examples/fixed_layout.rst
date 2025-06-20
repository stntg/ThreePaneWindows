Fixed Layout Examples
====================

The ``FixedThreePaneLayout`` provides a simple, stable three-pane interface where panes maintain consistent proportions.

Basic Fixed Layout
------------------

Create a simple fixed three-pane layout:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import FixedThreePaneLayout

    def create_basic_fixed_layout():
        root = tk.Tk()
        root.title("Basic Fixed Layout")
        root.geometry("800x600")

        # Create the fixed layout
        layout = FixedThreePaneLayout(root, side_width=200, sash_width=3)
        layout.pack(fill=tk.BOTH, expand=True)

        # Set custom labels
        layout.set_label_texts(
            left="📁 Files",
            center="📝 Content", 
            right="🔧 Tools"
        )

        # Add content to left pane
        tk.Label(layout.frame_left, text="File Browser", 
                font=("Arial", 12, "bold")).pack(pady=10)
        
        files = ["document.txt", "image.png", "script.py", "data.csv", "notes.md"]
        for file in files:
            file_frame = tk.Frame(layout.frame_left)
            file_frame.pack(fill=tk.X, padx=5, pady=2)
            
            icon = "📄" if file.endswith(('.txt', '.py', '.md')) else "🖼️" if file.endswith('.png') else "📊"
            tk.Label(file_frame, text=f"{icon} {file}").pack(side=tk.LEFT)

        # Add content to center pane
        tk.Label(layout.frame_center, text="Main Content Area", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        text_area = tk.Text(layout.frame_center, wrap=tk.WORD, font=("Arial", 11))
        scrollbar = tk.Scrollbar(layout.frame_center, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        sample_text = '''Welcome to the Fixed Three-Pane Layout!

This layout provides a stable, predictable interface with three distinct areas:

LEFT PANE: File browser and navigation
- Shows files and folders
- Maintains consistent width
- Perfect for navigation elements

CENTER PANE: Main content area  
- Primary workspace
- Expands to fill available space
- Where the main action happens

RIGHT PANE: Tools and properties
- Secondary tools and information
- Consistent width like left pane
- Contextual information and controls

The fixed layout is ideal when you want a stable, predictable interface that doesn't change as users interact with it.'''
        
        text_area.insert("1.0", sample_text)

        # Add content to right pane
        tk.Label(layout.frame_right, text="Tool Panel", 
                font=("Arial", 12, "bold")).pack(pady=10)
        
        # Tool sections
        sections = [
            ("Format", ["Bold", "Italic", "Underline"]),
            ("Insert", ["Image", "Table", "Link"]),
            ("View", ["Zoom In", "Zoom Out", "Full Screen"])
        ]
        
        for section_name, tools in sections:
            section_frame = tk.LabelFrame(layout.frame_right, text=section_name, 
                                        font=("Arial", 10, "bold"))
            section_frame.pack(fill=tk.X, padx=5, pady=5)
            
            for tool in tools:
                btn = tk.Button(section_frame, text=tool, width=12)
                btn.pack(pady=2, padx=5)

        return root

    if __name__ == "__main__":
        app = create_basic_fixed_layout()
        app.mainloop()

Dashboard-Style Layout
----------------------

Create a dashboard-style interface:

.. code-block:: python

    import tkinter as tk
    from tkinter import ttk
    from threepanewindows import FixedThreePaneLayout

    def create_dashboard_layout():
        root = tk.Tk()
        root.title("Dashboard - Fixed Layout")
        root.geometry("1000x700")

        # Create layout with custom sizing
        layout = FixedThreePaneLayout(root, side_width=220, sash_width=2)
        layout.pack(fill=tk.BOTH, expand=True)

        # Set dashboard labels
        layout.set_label_texts(
            left="📊 Navigation",
            center="📈 Dashboard",
            right="📋 Summary"
        )

        # Left panel - Navigation menu
        nav_frame = tk.Frame(layout.frame_left, bg="#2C3E50")
        nav_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(nav_frame, text="📊 DASHBOARD", font=("Arial", 12, "bold"),
                bg="#2C3E50", fg="white").pack(pady=15)
        
        # Navigation items
        nav_items = [
            ("🏠 Overview", "#3498DB"),
            ("📈 Analytics", "#27AE60"),
            ("👥 Users", "#E67E22"),
            ("💰 Revenue", "#9B59B6"),
            ("📊 Reports", "#34495E"),
            ("⚙️ Settings", "#95A5A6")
        ]
        
        for item, color in nav_items:
            btn = tk.Button(nav_frame, text=item, bg=color, fg="white",
                          font=("Arial", 10, "bold"), anchor="w", relief="flat",
                          width=20, pady=8)
            btn.pack(fill=tk.X, padx=10, pady=2)

        # Center panel - Main dashboard
        dashboard_frame = tk.Frame(layout.frame_center, bg="#ECF0F1")
        dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Dashboard header
        header_frame = tk.Frame(dashboard_frame, bg="#3498DB", height=60)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📈 Business Dashboard", 
                font=("Arial", 16, "bold"), bg="#3498DB", fg="white").pack(expand=True)
        
        # Statistics cards
        stats_frame = tk.Frame(dashboard_frame, bg="#ECF0F1")
        stats_frame.pack(fill=tk.X, pady=10)
        
        stats = [
            ("Total Revenue", "$125,430", "#27AE60", "↗️ +12%"),
            ("Active Users", "8,492", "#3498DB", "↗️ +5%"),
            ("Orders Today", "247", "#E67E22", "↗️ +8%"),
            ("Conversion", "3.2%", "#9B59B6", "↘️ -2%")
        ]
        
        for title, value, color, change in stats:
            card = tk.Frame(stats_frame, bg=color, relief="raised", bd=2)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            tk.Label(card, text=title, font=("Arial", 10, "bold"),
                    bg=color, fg="white").pack(pady=5)
            tk.Label(card, text=value, font=("Arial", 18, "bold"),
                    bg=color, fg="white").pack()
            tk.Label(card, text=change, font=("Arial", 9),
                    bg=color, fg="white").pack(pady=5)
        
        # Chart area (simulated)
        chart_frame = tk.LabelFrame(dashboard_frame, text="📊 Sales Trend", 
                                  font=("Arial", 12, "bold"), bg="#ECF0F1")
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Simulated chart
        chart_canvas = tk.Canvas(chart_frame, bg="white", height=200)
        chart_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Draw simple chart
        chart_canvas.create_line(50, 150, 100, 120, 150, 100, 200, 80, 
                               250, 90, 300, 70, 350, 60, fill="#3498DB", width=3)
        chart_canvas.create_text(200, 30, text="📈 Revenue Growth", 
                               font=("Arial", 12, "bold"))

        # Right panel - Summary and alerts
        summary_frame = tk.Frame(layout.frame_right, bg="#F8F9FA")
        summary_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(summary_frame, text="📋 SUMMARY", font=("Arial", 12, "bold"),
                bg="#F8F9FA").pack(pady=10)
        
        # Recent activity
        activity_frame = tk.LabelFrame(summary_frame, text="Recent Activity", 
                                     font=("Arial", 10, "bold"), bg="#F8F9FA")
        activity_frame.pack(fill=tk.X, padx=10, pady=5)
        
        activities = [
            "🔄 Data updated 2 min ago",
            "👤 New user registered",
            "💰 Payment received",
            "📊 Report generated",
            "⚠️ Server alert resolved"
        ]
        
        for activity in activities:
            tk.Label(activity_frame, text=activity, font=("Arial", 9),
                    bg="#F8F9FA", anchor="w").pack(fill=tk.X, padx=5, pady=2)
        
        # Alerts
        alerts_frame = tk.LabelFrame(summary_frame, text="Alerts", 
                                   font=("Arial", 10, "bold"), bg="#F8F9FA")
        alerts_frame.pack(fill=tk.X, padx=10, pady=5)
        
        alerts = [
            ("⚠️ High CPU usage", "#E67E22"),
            ("✅ Backup completed", "#27AE60"),
            ("🔔 5 new messages", "#3498DB")
        ]
        
        for alert, color in alerts:
            alert_frame = tk.Frame(alerts_frame, bg=color)
            alert_frame.pack(fill=tk.X, padx=5, pady=2)
            
            tk.Label(alert_frame, text=alert, font=("Arial", 9),
                    bg=color, fg="white").pack(pady=3)
        
        # Quick stats
        quick_stats_frame = tk.LabelFrame(summary_frame, text="Quick Stats", 
                                        font=("Arial", 10, "bold"), bg="#F8F9FA")
        quick_stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        quick_stats = [
            ("Uptime:", "99.9%"),
            ("Response:", "120ms"),
            ("Storage:", "78% used"),
            ("Memory:", "45% used")
        ]
        
        for stat, value in quick_stats:
            stat_frame = tk.Frame(quick_stats_frame, bg="#F8F9FA")
            stat_frame.pack(fill=tk.X, padx=5, pady=1)
            
            tk.Label(stat_frame, text=stat, font=("Arial", 9),
                    bg="#F8F9FA").pack(side=tk.LEFT)
            tk.Label(stat_frame, text=value, font=("Arial", 9, "bold"),
                    bg="#F8F9FA").pack(side=tk.RIGHT)

        return root

    if __name__ == "__main__":
        app = create_dashboard_layout()
        app.mainloop()

Settings/Preferences Interface
------------------------------

Create a settings interface with fixed layout:

.. code-block:: python

    import tkinter as tk
    from tkinter import ttk
    from threepanewindows import FixedThreePaneLayout

    def create_settings_interface():
        root = tk.Tk()
        root.title("Application Settings")
        root.geometry("900x650")

        # Create settings layout
        layout = FixedThreePaneLayout(root, side_width=180, sash_width=1)
        layout.pack(fill=tk.BOTH, expand=True)

        layout.set_label_texts(
            left="⚙️ Categories",
            center="🔧 Settings",
            right="ℹ️ Help"
        )

        # Left panel - Settings categories
        categories_frame = tk.Frame(layout.frame_left, bg="#F5F5F5")
        categories_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(categories_frame, text="Settings", font=("Arial", 12, "bold"),
                bg="#F5F5F5").pack(pady=10)
        
        # Category buttons
        categories = [
            ("🎨 Appearance", self.show_appearance_settings),
            ("🔔 Notifications", self.show_notification_settings),
            ("🔒 Privacy", self.show_privacy_settings),
            ("🌐 Network", self.show_network_settings),
            ("📁 Files", self.show_file_settings),
            ("🔧 Advanced", self.show_advanced_settings)
        ]
        
        self.category_buttons = []
        for category, command in categories:
            btn = tk.Button(categories_frame, text=category, anchor="w",
                          font=("Arial", 10), width=18, pady=5,
                          command=command, relief="flat", bg="#E8E8E8")
            btn.pack(fill=tk.X, padx=10, pady=2)
            self.category_buttons.append(btn)

        # Center panel - Settings content
        self.settings_frame = tk.Frame(layout.frame_center)
        self.settings_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Right panel - Help and info
        help_frame = tk.Frame(layout.frame_right, bg="#F0F8FF")
        help_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(help_frame, text="Help & Tips", font=("Arial", 12, "bold"),
                bg="#F0F8FF").pack(pady=10)
        
        # Help content
        help_text = tk.Text(help_frame, wrap=tk.WORD, font=("Arial", 9),
                          bg="#F0F8FF", relief="flat", height=10)
        help_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        help_content = '''💡 Settings Help

Click on categories in the left panel to view different settings.

🎨 Appearance: Customize the look and feel of the application.

🔔 Notifications: Control when and how you receive notifications.

🔒 Privacy: Manage your privacy and security settings.

🌐 Network: Configure network and connection settings.

📁 Files: Set default file locations and behaviors.

🔧 Advanced: Advanced configuration options for power users.

Changes are saved automatically when you modify settings.'''
        
        help_text.insert("1.0", help_content)
        help_text.config(state=tk.DISABLED)
        
        # Show default settings
        self.show_appearance_settings()
        
        return root

    def show_appearance_settings(self):
        """Show appearance settings."""
        self.clear_settings_frame()
        self.highlight_category(0)
        
        tk.Label(self.settings_frame, text="🎨 Appearance Settings", 
                font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 20))
        
        # Theme selection
        theme_frame = tk.LabelFrame(self.settings_frame, text="Theme", 
                                  font=("Arial", 11, "bold"))
        theme_frame.pack(fill=tk.X, pady=10)
        
        theme_var = tk.StringVar(value="Light")
        themes = ["Light", "Dark", "Auto"]
        for theme in themes:
            tk.Radiobutton(theme_frame, text=theme, variable=theme_var, 
                         value=theme, font=("Arial", 10)).pack(anchor="w", padx=10, pady=2)
        
        # Font settings
        font_frame = tk.LabelFrame(self.settings_frame, text="Font", 
                                 font=("Arial", 11, "bold"))
        font_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(font_frame, text="Font Family:", font=("Arial", 10)).pack(anchor="w", padx=10, pady=2)
        font_combo = ttk.Combobox(font_frame, values=["Arial", "Helvetica", "Times", "Courier"])
        font_combo.pack(anchor="w", padx=10, pady=2)
        font_combo.set("Arial")
        
        tk.Label(font_frame, text="Font Size:", font=("Arial", 10)).pack(anchor="w", padx=10, pady=2)
        size_scale = tk.Scale(font_frame, from_=8, to=24, orient=tk.HORIZONTAL)
        size_scale.pack(anchor="w", padx=10, pady=2)
        size_scale.set(11)
        
        # Color settings
        color_frame = tk.LabelFrame(self.settings_frame, text="Colors", 
                                  font=("Arial", 11, "bold"))
        color_frame.pack(fill=tk.X, pady=10)
        
        tk.Checkbutton(color_frame, text="Use system colors", 
                      font=("Arial", 10)).pack(anchor="w", padx=10, pady=2)
        tk.Checkbutton(color_frame, text="High contrast mode", 
                      font=("Arial", 10)).pack(anchor="w", padx=10, pady=2)

    def show_notification_settings(self):
        """Show notification settings."""
        self.clear_settings_frame()
        self.highlight_category(1)
        
        tk.Label(self.settings_frame, text="🔔 Notification Settings", 
                font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 20))
        
        # General notifications
        general_frame = tk.LabelFrame(self.settings_frame, text="General", 
                                    font=("Arial", 11, "bold"))
        general_frame.pack(fill=tk.X, pady=10)
        
        tk.Checkbutton(general_frame, text="Enable notifications", 
                      font=("Arial", 10)).pack(anchor="w", padx=10, pady=2)
        tk.Checkbutton(general_frame, text="Show notification badges", 
                      font=("Arial", 10)).pack(anchor="w", padx=10, pady=2)
        tk.Checkbutton(general_frame, text="Play notification sounds", 
                      font=("Arial", 10)).pack(anchor="w", padx=10, pady=2)

    def show_privacy_settings(self):
        """Show privacy settings."""
        self.clear_settings_frame()
        self.highlight_category(2)
        
        tk.Label(self.settings_frame, text="🔒 Privacy Settings", 
                font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 20))
        
        # Privacy options
        privacy_frame = tk.LabelFrame(self.settings_frame, text="Privacy", 
                                    font=("Arial", 11, "bold"))
        privacy_frame.pack(fill=tk.X, pady=10)
        
        tk.Checkbutton(privacy_frame, text="Send usage statistics", 
                      font=("Arial", 10)).pack(anchor="w", padx=10, pady=2)
        tk.Checkbutton(privacy_frame, text="Allow crash reports", 
                      font=("Arial", 10)).pack(anchor="w", padx=10, pady=2)

    def show_network_settings(self):
        """Show network settings."""
        self.clear_settings_frame()
        self.highlight_category(3)
        
        tk.Label(self.settings_frame, text="🌐 Network Settings", 
                font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 20))

    def show_file_settings(self):
        """Show file settings."""
        self.clear_settings_frame()
        self.highlight_category(4)
        
        tk.Label(self.settings_frame, text="📁 File Settings", 
                font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 20))

    def show_advanced_settings(self):
        """Show advanced settings."""
        self.clear_settings_frame()
        self.highlight_category(5)
        
        tk.Label(self.settings_frame, text="🔧 Advanced Settings", 
                font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 20))

    def clear_settings_frame(self):
        """Clear the settings frame."""
        for widget in self.settings_frame.winfo_children():
            widget.destroy()

    def highlight_category(self, index):
        """Highlight the selected category."""
        for i, btn in enumerate(self.category_buttons):
            if i == index:
                btn.config(bg="#D0D0D0", relief="sunken")
            else:
                btn.config(bg="#E8E8E8", relief="flat")

    if __name__ == "__main__":
        app = create_settings_interface()
        app.mainloop()

When to Use Fixed Layout
------------------------

The fixed layout is ideal for:

1. **Stable Interfaces**: When you want consistent, predictable layouts
2. **Simple Applications**: Straightforward interfaces without complex docking
3. **Dashboard Applications**: Information display with clear sections
4. **Settings/Preferences**: Configuration interfaces with categories
5. **Beginner-Friendly**: Easy to understand and implement

Key Features of Fixed Layout
----------------------------

- **Simplicity**: Easy to set up and use
- **Stability**: Layout doesn't change unexpectedly
- **Predictability**: Users always know where to find things
- **Performance**: Lightweight with minimal overhead
- **Customizable**: Adjustable pane sizes and appearance

Configuration Options
---------------------

.. code-block:: python

    layout = FixedThreePaneLayout(
        parent,
        side_width=200,        # Width of side panes
        sash_width=3,          # Width of separators
        menu_bar=menubar       # Optional menu integration
    )

    # Customize labels
    layout.set_label_texts(
        left="Left Panel",
        center="Main Content",
        right="Right Panel"
    )

Next Steps
----------

Explore more advanced layouts:

- :doc:`dockable_layout` - For draggable and detachable panes
- :doc:`enhanced_professional` - For advanced theming and features
- :doc:`fixed_width_panes` - For precise width control