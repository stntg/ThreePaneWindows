Status Bar Integration Examples
===============================

This section demonstrates how to integrate status bars and notifications with ThreePaneWindows layouts.

Basic Status Bar
----------------

Add a simple status bar to your application:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import FixedThreePaneLayout

    def create_basic_status_bar_example():
        root = tk.Tk()
        root.title("Basic Status Bar Example")
        root.geometry("800x600")

        # Create layout
        layout = FixedThreePaneLayout(root, side_width=200)
        layout.pack(fill=tk.BOTH, expand=True)

        layout.set_label_texts(
            left="📁 Files",
            center="📝 Editor",
            right="🔧 Tools"
        )

        # Add content to demonstrate status updates
        # Left panel
        file_listbox = tk.Listbox(layout.frame_left, font=("Arial", 10))
        file_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        files = ["document.txt", "image.png", "script.py", "data.csv"]
        for file in files:
            file_listbox.insert(tk.END, file)

        # Center panel
        text_editor = tk.Text(layout.frame_center, wrap=tk.WORD, font=("Arial", 11))
        text_editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        sample_text = "Type here to see status updates..."
        text_editor.insert("1.0", sample_text)

        # Right panel
        tk.Label(layout.frame_right, text="Tools Panel", 
                font=("Arial", 12, "bold")).pack(pady=10)

        # Status bar
        status_bar = tk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W,
                            font=("Arial", 9), bg="#f0f0f0")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Status update functions
        def update_file_status(event):
            selection = file_listbox.curselection()
            if selection:
                filename = files[selection[0]]
                status_bar.config(text=f"Selected: {filename}")

        def update_editor_status(event):
            # Get cursor position
            cursor_pos = text_editor.index(tk.INSERT)
            line, col = cursor_pos.split('.')
            
            # Get text statistics
            content = text_editor.get("1.0", tk.END + "-1c")
            words = len(content.split())
            chars = len(content)
            
            status_bar.config(text=f"Line {line}, Column {int(col)+1} | Words: {words} | Characters: {chars}")

        # Bind events
        file_listbox.bind('<<ListboxSelect>>', update_file_status)
        text_editor.bind('<KeyRelease>', update_editor_status)
        text_editor.bind('<Button-1>', update_editor_status)

        return root

    if __name__ == "__main__":
        app = create_basic_status_bar_example()
        app.mainloop()

Advanced Status Bar with Multiple Sections
-------------------------------------------

Create a status bar with multiple information sections:

.. code-block:: python

    import tkinter as tk
    from tkinter import ttk
    import time
    import threading
    from threepanewindows import DockableThreePaneWindow

    class AdvancedStatusBar(tk.Frame):
        """Advanced status bar with multiple sections."""
        
        def __init__(self, parent, **kwargs):
            super().__init__(parent, relief=tk.SUNKEN, bd=1, **kwargs)
            
            self.setup_ui()
            self.start_clock()
            
        def setup_ui(self):
            """Set up the status bar sections."""
            # Main status message (left side)
            self.status_label = tk.Label(self, text="Ready", anchor=tk.W, 
                                        font=("Arial", 9))
            self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            # Separator
            separator1 = ttk.Separator(self, orient=tk.VERTICAL)
            separator1.pack(side=tk.RIGHT, fill=tk.Y, padx=2)
            
            # Clock (right side)
            self.clock_label = tk.Label(self, text="", anchor=tk.E, 
                                      font=("Arial", 9), width=20)
            self.clock_label.pack(side=tk.RIGHT, padx=5)
            
            # Separator
            separator2 = ttk.Separator(self, orient=tk.VERTICAL)
            separator2.pack(side=tk.RIGHT, fill=tk.Y, padx=2)
            
            # Progress bar (initially hidden)
            self.progress_var = tk.DoubleVar()
            self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, 
                                              length=100, mode='determinate')
            
            # Progress label
            self.progress_label = tk.Label(self, text="", anchor=tk.E, 
                                         font=("Arial", 9), width=15)
            
            # Separator
            separator3 = ttk.Separator(self, orient=tk.VERTICAL)
            separator3.pack(side=tk.RIGHT, fill=tk.Y, padx=2)
            
            # Connection status
            self.connection_label = tk.Label(self, text="🔴 Offline", anchor=tk.E,
                                           font=("Arial", 9), width=12)
            self.connection_label.pack(side=tk.RIGHT, padx=5)
            
        def set_status(self, message):
            """Set the main status message."""
            self.status_label.config(text=message)
            
        def set_connection_status(self, connected):
            """Set connection status."""
            if connected:
                self.connection_label.config(text="🟢 Online", fg="green")
            else:
                self.connection_label.config(text="🔴 Offline", fg="red")
                
        def show_progress(self, message="Processing..."):
            """Show progress bar with message."""
            self.progress_label.config(text=message)
            self.progress_label.pack(side=tk.RIGHT, padx=5)
            self.progress_bar.pack(side=tk.RIGHT, padx=5)
            self.progress_var.set(0)
            
        def update_progress(self, value, message=None):
            """Update progress bar value (0-100)."""
            self.progress_var.set(value)
            if message:
                self.progress_label.config(text=message)
                
        def hide_progress(self):
            """Hide progress bar."""
            self.progress_bar.pack_forget()
            self.progress_label.pack_forget()
            
        def start_clock(self):
            """Start the clock update thread."""
            def update_clock():
                while True:
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    self.clock_label.config(text=current_time)
                    time.sleep(1)
                    
            clock_thread = threading.Thread(target=update_clock, daemon=True)
            clock_thread.start()

    def create_advanced_status_bar_example():
        """Example with advanced status bar."""
        root = tk.Tk()
        root.title("Advanced Status Bar Example")
        root.geometry("1000x700")

        def build_file_manager(frame):
            """Build file manager panel."""
            tk.Label(frame, text="📁 File Manager", 
                    font=("Arial", 11, "bold")).pack(pady=5)
            
            # File operations
            operations_frame = tk.Frame(frame)
            operations_frame.pack(fill=tk.X, padx=5, pady=5)
            
            tk.Button(operations_frame, text="📂 Open", 
                     command=lambda: simulate_file_operation("Opening file...")).pack(
                         side=tk.LEFT, padx=2)
            tk.Button(operations_frame, text="💾 Save", 
                     command=lambda: simulate_file_operation("Saving file...")).pack(
                         side=tk.LEFT, padx=2)
            tk.Button(operations_frame, text="🔄 Sync", 
                     command=lambda: simulate_sync_operation()).pack(
                         side=tk.LEFT, padx=2)
            
            # File list
            file_tree = ttk.Treeview(frame)
            file_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Sample files
            files = [
                ("📄 document.txt", "2.1 KB"),
                ("🖼️ image.png", "856 KB"),
                ("🐍 script.py", "4.2 KB"),
                ("📊 data.csv", "125 KB")
            ]
            
            for filename, size in files:
                file_tree.insert("", "end", text=filename, values=(size,))
                
            def on_file_select(event):
                selection = file_tree.selection()
                if selection:
                    item = file_tree.item(selection[0])
                    filename = item['text']
                    status_bar.set_status(f"Selected: {filename}")
                    
            file_tree.bind('<<TreeviewSelect>>', on_file_select)

        def build_editor(frame):
            """Build text editor panel."""
            # Editor toolbar
            toolbar = tk.Frame(frame, bg="#f0f0f0", height=35)
            toolbar.pack(fill=tk.X)
            toolbar.pack_propagate(False)
            
            tk.Label(toolbar, text="📝 Text Editor", font=("Arial", 11, "bold"),
                    bg="#f0f0f0").pack(side=tk.LEFT, padx=10, pady=8)
            
            # Word count button
            tk.Button(toolbar, text="📊 Word Count", 
                     command=lambda: show_word_count()).pack(side=tk.RIGHT, padx=10, pady=5)
            
            # Text editor
            global text_editor
            text_editor = tk.Text(frame, wrap=tk.WORD, font=("Arial", 11))
            text_editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            sample_text = '''Welcome to the Advanced Status Bar Example!

This text editor demonstrates various status bar features:

1. Real-time cursor position tracking
2. Word and character count
3. File operation progress
4. Connection status monitoring
5. Live clock display

Try typing, selecting text, or using the file operations to see the status bar in action.

The status bar provides valuable feedback to users about the current state of the application and ongoing operations.'''
            
            text_editor.insert("1.0", sample_text)
            
            def on_text_change(event):
                # Update cursor position and text stats
                cursor_pos = text_editor.index(tk.INSERT)
                line, col = cursor_pos.split('.')
                
                content = text_editor.get("1.0", tk.END + "-1c")
                words = len(content.split())
                chars = len(content)
                
                status_bar.set_status(f"Line {line}, Col {int(col)+1} | Words: {words} | Chars: {chars}")
                
            text_editor.bind('<KeyRelease>', on_text_change)
            text_editor.bind('<Button-1>', on_text_change)
            
            def show_word_count():
                content = text_editor.get("1.0", tk.END + "-1c")
                words = len(content.split())
                chars = len(content)
                lines = content.count('\n') + 1
                
                tk.messagebox.showinfo("Word Count", 
                    f"Lines: {lines}\nWords: {words}\nCharacters: {chars}")

        def build_tools(frame):
            """Build tools panel."""
            tk.Label(frame, text="🔧 Tools", 
                    font=("Arial", 11, "bold")).pack(pady=10)
            
            # Connection controls
            connection_frame = tk.LabelFrame(frame, text="Connection", 
                                           font=("Arial", 10, "bold"))
            connection_frame.pack(fill=tk.X, padx=10, pady=10)
            
            tk.Button(connection_frame, text="🔌 Connect", 
                     command=lambda: toggle_connection(True)).pack(pady=5)
            tk.Button(connection_frame, text="🔌 Disconnect", 
                     command=lambda: toggle_connection(False)).pack(pady=5)
            
            # Processing controls
            process_frame = tk.LabelFrame(frame, text="Processing", 
                                        font=("Arial", 10, "bold"))
            process_frame.pack(fill=tk.X, padx=10, pady=10)
            
            tk.Button(process_frame, text="⚙️ Start Process", 
                     command=lambda: simulate_long_process()).pack(pady=5)
            tk.Button(process_frame, text="📊 Analyze Data", 
                     command=lambda: simulate_analysis()).pack(pady=5)

        # Create dockable window
        window = DockableThreePaneWindow(
            root,
            side_width=250,
            left_builder=build_file_manager,
            center_builder=build_editor,
            right_builder=build_tools
        )
        window.pack(fill=tk.BOTH, expand=True)

        # Create advanced status bar
        status_bar = AdvancedStatusBar(root)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Status bar operation functions
        def simulate_file_operation(message):
            """Simulate a file operation with progress."""
            status_bar.show_progress(message)
            
            def progress_update():
                for i in range(0, 101, 10):
                    status_bar.update_progress(i, f"{message} {i}%")
                    time.sleep(0.1)
                status_bar.hide_progress()
                status_bar.set_status("Operation completed")
                
            threading.Thread(target=progress_update, daemon=True).start()

        def simulate_sync_operation():
            """Simulate a sync operation."""
            status_bar.show_progress("Synchronizing...")
            
            def sync_update():
                steps = ["Connecting...", "Uploading...", "Downloading...", "Finalizing..."]
                for i, step in enumerate(steps):
                    progress = (i + 1) * 25
                    status_bar.update_progress(progress, step)
                    time.sleep(0.5)
                status_bar.hide_progress()
                status_bar.set_status("Sync completed successfully")
                
            threading.Thread(target=sync_update, daemon=True).start()

        def toggle_connection(connected):
            """Toggle connection status."""
            status_bar.set_connection_status(connected)
            if connected:
                status_bar.set_status("Connected to server")
            else:
                status_bar.set_status("Disconnected from server")

        def simulate_long_process():
            """Simulate a long-running process."""
            status_bar.show_progress("Processing data...")
            
            def process_update():
                for i in range(0, 101, 5):
                    status_bar.update_progress(i, f"Processing... {i}%")
                    time.sleep(0.2)
                status_bar.hide_progress()
                status_bar.set_status("Processing completed")
                
            threading.Thread(target=process_update, daemon=True).start()

        def simulate_analysis():
            """Simulate data analysis."""
            status_bar.show_progress("Analyzing...")
            
            def analysis_update():
                phases = ["Parsing data...", "Computing statistics...", "Generating report..."]
                for i, phase in enumerate(phases):
                    for j in range(0, 101, 20):
                        progress = (i * 100 + j) // 3
                        status_bar.update_progress(progress, phase)
                        time.sleep(0.1)
                status_bar.hide_progress()
                status_bar.set_status("Analysis completed")
                
            threading.Thread(target=analysis_update, daemon=True).start()

        # Initialize status
        status_bar.set_status("Application ready")
        status_bar.set_connection_status(False)

        return root

    if __name__ == "__main__":
        app = create_advanced_status_bar_example()
        app.mainloop()

Notification System Integration
-------------------------------

Add a notification system to your application:

.. code-block:: python

    import tkinter as tk
    from tkinter import ttk
    import time
    import threading
    from threepanewindows import FixedThreePaneLayout

    class NotificationSystem:
        """A notification system for the application."""
        
        def __init__(self, parent):
            self.parent = parent
            self.notifications = []
            self.notification_frame = None
            
        def show_notification(self, message, notification_type="info", duration=3000):
            """Show a notification message."""
            # Create notification frame if it doesn't exist
            if not self.notification_frame:
                self.notification_frame = tk.Frame(self.parent, bg="#333333")
                self.notification_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
            
            # Create notification
            notification = self.create_notification(message, notification_type)
            self.notifications.append(notification)
            
            # Position notifications
            self.position_notifications()
            
            # Auto-hide after duration
            if duration > 0:
                self.parent.after(duration, lambda: self.hide_notification(notification))
                
        def create_notification(self, message, notification_type):
            """Create a notification widget."""
            # Color scheme based on type
            colors = {
                "info": {"bg": "#2196F3", "fg": "white"},
                "success": {"bg": "#4CAF50", "fg": "white"},
                "warning": {"bg": "#FF9800", "fg": "white"},
                "error": {"bg": "#F44336", "fg": "white"}
            }
            
            color = colors.get(notification_type, colors["info"])
            
            # Create notification frame
            notif_frame = tk.Frame(self.notification_frame, bg=color["bg"], 
                                 relief=tk.RAISED, bd=2)
            notif_frame.pack(fill=tk.X, pady=2)
            
            # Icon based on type
            icons = {
                "info": "ℹ️",
                "success": "✅", 
                "warning": "⚠️",
                "error": "❌"
            }
            
            icon = icons.get(notification_type, icons["info"])
            
            # Notification content
            content_frame = tk.Frame(notif_frame, bg=color["bg"])
            content_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(content_frame, text=icon, bg=color["bg"], fg=color["fg"],
                    font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
            
            tk.Label(content_frame, text=message, bg=color["bg"], fg=color["fg"],
                    font=("Arial", 10), wraplength=250).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Close button
            close_btn = tk.Button(content_frame, text="✕", bg=color["bg"], fg=color["fg"],
                                font=("Arial", 8), relief=tk.FLAT, bd=0,
                                command=lambda: self.hide_notification(notif_frame))
            close_btn.pack(side=tk.RIGHT, padx=5)
            
            return notif_frame
            
        def hide_notification(self, notification):
            """Hide a specific notification."""
            if notification in self.notifications:
                self.notifications.remove(notification)
                notification.destroy()
                self.position_notifications()
                
        def position_notifications(self):
            """Reposition all notifications."""
            for i, notification in enumerate(self.notifications):
                notification.pack_forget()
                notification.pack(fill=tk.X, pady=2)

    def create_notification_example():
        """Example with notification system."""
        root = tk.Tk()
        root.title("Notification System Example")
        root.geometry("900x600")

        # Create layout
        layout = FixedThreePaneLayout(root, side_width=200)
        layout.pack(fill=tk.BOTH, expand=True)

        layout.set_label_texts(
            left="🔔 Notifications",
            center="📝 Main Content",
            right="⚙️ Settings"
        )

        # Create notification system
        notifications = NotificationSystem(root)

        # Left panel - Notification controls
        notif_frame = tk.Frame(layout.frame_left)
        notif_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(notif_frame, text="Notification Types", 
                font=("Arial", 11, "bold")).pack(pady=10)
        
        # Notification buttons
        notif_types = [
            ("ℹ️ Info", "info", "This is an information message"),
            ("✅ Success", "success", "Operation completed successfully!"),
            ("⚠️ Warning", "warning", "This is a warning message"),
            ("❌ Error", "error", "An error has occurred!")
        ]
        
        for label, notif_type, message in notif_types:
            btn = tk.Button(notif_frame, text=label, width=15,
                          command=lambda t=notif_type, m=message: notifications.show_notification(m, t))
            btn.pack(pady=5, fill=tk.X)
        
        # Custom notification
        tk.Label(notif_frame, text="Custom Message:", 
                font=("Arial", 10, "bold")).pack(pady=(20, 5))
        
        custom_entry = tk.Entry(notif_frame, font=("Arial", 10))
        custom_entry.pack(fill=tk.X, pady=5)
        custom_entry.insert(0, "Custom notification message")
        
        def show_custom():
            message = custom_entry.get()
            if message:
                notifications.show_notification(message, "info")
                
        tk.Button(notif_frame, text="Show Custom", 
                 command=show_custom).pack(pady=5, fill=tk.X)

        # Center panel - Main content
        content_frame = tk.Frame(layout.frame_center)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(content_frame, text="Main Application Content", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        text_area = tk.Text(content_frame, wrap=tk.WORD, font=("Arial", 11))
        text_area.pack(fill=tk.BOTH, expand=True)
        
        content_text = '''This example demonstrates a notification system integrated with ThreePaneWindows.

Key Features:
• Multiple notification types (info, success, warning, error)
• Auto-hide functionality with customizable duration
• Manual close buttons
• Proper positioning and stacking
• Non-intrusive overlay design

Try clicking the notification buttons in the left panel to see different types of notifications.

The notification system provides immediate feedback to users about:
- Successful operations
- Warnings and alerts
- Error conditions
- General information

Notifications appear in the top-right corner and automatically disappear after a few seconds, or can be manually closed by clicking the X button.'''
        
        text_area.insert("1.0", content_text)

        # Right panel - Settings
        settings_frame = tk.Frame(layout.frame_right)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(settings_frame, text="Notification Settings", 
                font=("Arial", 11, "bold")).pack(pady=10)
        
        # Duration setting
        tk.Label(settings_frame, text="Duration (ms):", 
                font=("Arial", 10)).pack(anchor="w")
        
        duration_var = tk.IntVar(value=3000)
        duration_scale = tk.Scale(settings_frame, from_=1000, to=10000, 
                                orient=tk.HORIZONTAL, variable=duration_var)
        duration_scale.pack(fill=tk.X, pady=5)
        
        # Enable/disable notifications
        enable_var = tk.BooleanVar(value=True)
        tk.Checkbutton(settings_frame, text="Enable notifications", 
                      variable=enable_var, font=("Arial", 10)).pack(anchor="w", pady=5)
        
        # Sound setting
        sound_var = tk.BooleanVar(value=False)
        tk.Checkbutton(settings_frame, text="Play notification sound", 
                      variable=sound_var, font=("Arial", 10)).pack(anchor="w", pady=5)

        # Status bar with notification count
        status_frame = tk.Frame(root, relief=tk.SUNKEN, bd=1)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        status_label = tk.Label(status_frame, text="Ready", anchor=tk.W, 
                              font=("Arial", 9))
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        notif_count_label = tk.Label(status_frame, text="Notifications: 0", 
                                   anchor=tk.E, font=("Arial", 9))
        notif_count_label.pack(side=tk.RIGHT, padx=5)
        
        # Update notification count
        original_show = notifications.show_notification
        notification_count = [0]
        
        def enhanced_show_notification(message, notif_type="info", duration=3000):
            if enable_var.get():
                notification_count[0] += 1
                notif_count_label.config(text=f"Notifications: {notification_count[0]}")
                original_show(message, notif_type, duration_var.get())
                
        notifications.show_notification = enhanced_show_notification

        return root

    if __name__ == "__main__":
        app = create_notification_example()
        app.mainloop()

Best Practices for Status Integration
-------------------------------------

When integrating status bars and notifications:

1. **Clear Information**: Provide clear, concise status messages
2. **Appropriate Timing**: Show progress for operations longer than 1-2 seconds
3. **Non-Intrusive**: Don't block user interaction unnecessarily
4. **Consistent Placement**: Keep status information in predictable locations
5. **Visual Hierarchy**: Use colors and icons to convey message importance
6. **Accessibility**: Ensure status information is accessible to screen readers

Status Bar Components
---------------------

Common status bar elements:

**Primary Status**
- Current operation or state
- File information
- Cursor position

**Progress Indicators**
- Progress bars for long operations
- Percentage completion
- Time estimates

**System Information**
- Connection status
- Time and date
- Resource usage

**User Feedback**
- Success/error messages
- Warnings and alerts
- Help text

Next Steps
----------

Explore more integration examples:

- :doc:`real_world_applications` - Complete applications with status systems
- :doc:`custom_widgets` - Custom status widgets and indicators
- Advanced notification patterns and user preferences