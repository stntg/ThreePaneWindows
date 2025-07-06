#!/usr/bin/env python3
"""
Comprehensive example demonstrating cross-platform theming features.

This example showcases:
- Platform-native themes (Windows, macOS, Linux)
- System appearance detection and adaptation
- Cross-platform font handling with fallbacks
- Enhanced theme management and switching
- Real-time theme updates
- Platform-specific color schemes and typography
"""

import os
import platform
import sys
import tkinter as tk
from tkinter import ttk

# Add the package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from threepanewindows.dockable import DockableThreePaneWindow
from threepanewindows.platform import platform_handler
from threepanewindows.themes import ThemeManager, ThemeType


class CrossPlatformThemingDemo:
    """Demo application showcasing cross-platform theming features."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"Cross-Platform Theming Demo - {platform.system()}")
        self.root.geometry("1200x800")

        # Initialize theme manager with system-appropriate default
        initial_theme = (
            ThemeType.NATIVE if self.has_native_themes() else ThemeType.SYSTEM
        )
        self.theme_manager = ThemeManager(theme=initial_theme)

        # Create the UI
        self.create_ui()

        # Apply initial theming
        self.apply_current_theme()

        # Set up periodic theme refresh for system themes
        self.setup_theme_monitoring()

    def has_native_themes(self) -> bool:
        """Check if native themes are available."""
        temp_manager = ThemeManager()
        return temp_manager.is_native_theme_available()

    def create_ui(self):
        """Create the user interface."""
        # Create notebook for different demo sections
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Platform Information Tab
        self.create_platform_tab(notebook)

        # Theme Controls Tab
        self.create_theme_controls_tab(notebook)

        # Widget Showcase Tab
        self.create_widget_showcase_tab(notebook)

        # Three-Pane Demo Tab
        self.create_three_pane_tab(notebook)

    def create_platform_tab(self, notebook):
        """Create platform information tab."""
        platform_frame = ttk.Frame(notebook)
        notebook.add(platform_frame, text="Platform Info")

        # Title
        title_label = ttk.Label(
            platform_frame,
            text=f"{platform.system()} Platform Information",
            font=("default", 16, "bold"),
        )
        title_label.pack(pady=(10, 20))

        # Platform details
        info_frame = ttk.LabelFrame(platform_frame, text="System Details")
        info_frame.pack(fill="x", padx=10, pady=5)

        platform_info = self.theme_manager.get_platform_info()

        # Create a scrollable text widget for platform info
        info_text = tk.Text(info_frame, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(
            info_frame, orient="vertical", command=info_text.yview
        )
        info_text.configure(yscrollcommand=scrollbar.set)

        # Add platform information
        info_content = []
        info_content.append(
            f"Operating System: {platform.system()} {platform.release()}"
        )
        info_content.append(f"Platform: {platform.platform()}")
        info_content.append(f"Architecture: {platform.architecture()[0]}")
        info_content.append(f"Python Version: {platform.python_version()}")
        info_content.append("")
        info_content.append("ThreePaneWindows Theming Capabilities:")
        info_content.append("=" * 40)

        for key, value in platform_info.items():
            formatted_key = key.replace("_", " ").title()
            info_content.append(f"{formatted_key}: {value}")

        # Add font information
        info_content.append("")
        info_content.append("Available System Fonts (first 20):")
        info_content.append("-" * 30)
        try:
            import tkinter.font as tkfont

            fonts = sorted(tkfont.families())[:20]
            for font in fonts:
                info_content.append(f"  • {font}")
        except Exception as e:
            info_content.append(f"Could not retrieve font list: {e}")

        info_text.insert("1.0", "\n".join(info_content))
        info_text.configure(state="disabled")

        info_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Store reference for theming
        self.platform_info_text = info_text

    def create_theme_controls_tab(self, notebook):
        """Create theme controls tab."""
        controls_frame = ttk.Frame(notebook)
        notebook.add(controls_frame, text="Theme Controls")

        # Title
        title_label = ttk.Label(
            controls_frame, text="Theme Management", font=("default", 16, "bold")
        )
        title_label.pack(pady=(10, 20))

        # Available themes section
        themes_frame = ttk.LabelFrame(controls_frame, text="Available Themes")
        themes_frame.pack(fill="x", padx=10, pady=5)

        # Get available themes
        available_themes = self.theme_manager.get_available_themes()

        # Create theme selection buttons in a grid
        button_frame = ttk.Frame(themes_frame)
        button_frame.pack(fill="x", padx=10, pady=10)

        # Organize themes by category
        standard_themes = ["light", "dark", "blue", "green", "purple"]
        system_themes = ["system"]
        native_themes = ["native", "native_light", "native_dark"]

        row = 0

        # Standard themes
        if any(theme in available_themes for theme in standard_themes):
            std_label = ttk.Label(
                button_frame, text="Standard Themes:", font=("default", 10, "bold")
            )
            std_label.grid(row=row, column=0, columnspan=4, sticky="w", pady=(0, 5))
            row += 1

            col = 0
            for theme_name in standard_themes:
                if theme_name in available_themes:
                    btn = ttk.Button(
                        button_frame,
                        text=theme_name.title(),
                        command=lambda t=theme_name: self.switch_theme(t),
                    )
                    btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
                    col += 1
                    if col >= 4:
                        col = 0
                        row += 1
            if col > 0:
                row += 1

        # System themes
        if any(theme in available_themes for theme in system_themes):
            sys_label = ttk.Label(
                button_frame, text="System Themes:", font=("default", 10, "bold")
            )
            sys_label.grid(row=row, column=0, columnspan=4, sticky="w", pady=(10, 5))
            row += 1

            col = 0
            for theme_name in system_themes:
                if theme_name in available_themes:
                    btn = ttk.Button(
                        button_frame,
                        text=theme_name.title(),
                        command=lambda t=theme_name: self.switch_theme(t),
                    )
                    btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
                    col += 1
            if col > 0:
                row += 1

        # Native themes
        if any(theme in available_themes for theme in native_themes):
            native_label = ttk.Label(
                button_frame, text="Native Themes:", font=("default", 10, "bold")
            )
            native_label.grid(row=row, column=0, columnspan=4, sticky="w", pady=(10, 5))
            row += 1

            col = 0
            for theme_name in native_themes:
                if theme_name in available_themes:
                    btn = ttk.Button(
                        button_frame,
                        text=theme_name.replace("_", " ").title(),
                        command=lambda t=theme_name: self.switch_theme(t),
                    )
                    btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
                    col += 1
                    if col >= 4:
                        col = 0
                        row += 1

        # Configure grid weights
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)

        # Control buttons
        control_frame = ttk.Frame(controls_frame)
        control_frame.pack(fill="x", padx=10, pady=10)

        refresh_btn = ttk.Button(
            control_frame,
            text="Refresh System Theme",
            command=self.refresh_system_theme,
        )
        refresh_btn.pack(side="left", padx=(0, 10))

        auto_refresh_var = tk.BooleanVar(value=True)
        auto_refresh_check = ttk.Checkbutton(
            control_frame,
            text="Auto-refresh system themes",
            variable=auto_refresh_var,
            command=lambda: self.toggle_auto_refresh(auto_refresh_var.get()),
        )
        auto_refresh_check.pack(side="left")

        # Current theme display
        self.current_theme_var = tk.StringVar()
        current_theme_label = ttk.Label(
            controls_frame,
            textvariable=self.current_theme_var,
            font=("default", 12, "bold"),
        )
        current_theme_label.pack(pady=10)

        self.update_current_theme_display()

    def create_widget_showcase_tab(self, notebook):
        """Create widget showcase tab."""
        showcase_frame = ttk.Frame(notebook)
        notebook.add(showcase_frame, text="Widget Showcase")

        # Create scrollable frame
        canvas = tk.Canvas(showcase_frame)
        scrollbar = ttk.Scrollbar(
            showcase_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Title
        title_label = ttk.Label(
            scrollable_frame,
            text="Widget Theming Showcase",
            font=("default", 16, "bold"),
        )
        title_label.pack(pady=(10, 20))

        # TTK Widgets section
        ttk_frame = ttk.LabelFrame(scrollable_frame, text="TTK Widgets")
        ttk_frame.pack(fill="x", padx=10, pady=5)

        # Labels
        ttk.Label(ttk_frame, text="Normal Label").pack(anchor="w", padx=5, pady=2)
        ttk.Label(ttk_frame, text="Header Label", style="Header.TLabel").pack(
            anchor="w", padx=5, pady=2
        )

        # Buttons
        button_frame = ttk.Frame(ttk_frame)
        button_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(button_frame, text="Normal Button").pack(side="left", padx=2)
        ttk.Button(button_frame, text="Themed Button", style="Themed.TButton").pack(
            side="left", padx=2
        )

        # Entry and Combobox
        entry_frame = ttk.Frame(ttk_frame)
        entry_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(entry_frame, text="Entry:").pack(side="left")
        entry = ttk.Entry(entry_frame, width=20)
        entry.insert(0, "Sample text")
        entry.pack(side="left", padx=5)

        ttk.Label(entry_frame, text="Combobox:").pack(side="left", padx=(10, 0))
        combo = ttk.Combobox(
            entry_frame, values=["Option 1", "Option 2", "Option 3"], width=15
        )
        combo.set("Option 1")
        combo.pack(side="left", padx=5)

        # Checkbuttons and Radiobuttons
        check_frame = ttk.Frame(ttk_frame)
        check_frame.pack(fill="x", padx=5, pady=5)

        ttk.Checkbutton(check_frame, text="Checkbox 1").pack(side="left")
        ttk.Checkbutton(check_frame, text="Checkbox 2").pack(side="left", padx=10)

        radio_var = tk.StringVar(value="1")
        ttk.Radiobutton(
            check_frame, text="Radio 1", variable=radio_var, value="1"
        ).pack(side="left", padx=(20, 0))
        ttk.Radiobutton(
            check_frame, text="Radio 2", variable=radio_var, value="2"
        ).pack(side="left", padx=5)

        # Progress bar and Scale
        progress_frame = ttk.Frame(ttk_frame)
        progress_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(progress_frame, text="Progress:").pack(side="left")
        progress = ttk.Progressbar(progress_frame, length=200, value=60)
        progress.pack(side="left", padx=5)

        ttk.Label(progress_frame, text="Scale:").pack(side="left", padx=(20, 0))
        scale = ttk.Scale(progress_frame, from_=0, to=100, length=150)
        scale.set(30)
        scale.pack(side="left", padx=5)

        # TK Widgets section
        tk_frame = ttk.LabelFrame(scrollable_frame, text="TK Widgets (Custom Themed)")
        tk_frame.pack(fill="x", padx=10, pady=5)

        # Text widget
        text_frame = ttk.Frame(tk_frame)
        text_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(text_frame, text="Text Widget:").pack(anchor="w")
        text_widget = tk.Text(text_frame, height=4, width=50)
        text_widget.insert(
            "1.0",
            "This is a themed Text widget.\nIt adapts to the current theme colors.\nTry switching themes to see the changes.",
        )
        text_widget.pack(fill="x", pady=2)

        # Listbox
        list_frame = ttk.Frame(tk_frame)
        list_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(list_frame, text="Listbox:").pack(anchor="w")
        listbox_container = ttk.Frame(list_frame)
        listbox_container.pack(fill="x", pady=2)

        listbox = tk.Listbox(listbox_container, height=4)
        list_scrollbar = ttk.Scrollbar(
            listbox_container, orient="vertical", command=listbox.yview
        )
        listbox.configure(yscrollcommand=list_scrollbar.set)

        for i in range(10):
            listbox.insert("end", f"Themed List Item {i+1}")

        listbox.pack(side="left", fill="both", expand=True)
        list_scrollbar.pack(side="right", fill="y")

        # Canvas
        canvas_frame = ttk.Frame(tk_frame)
        canvas_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(canvas_frame, text="Canvas:").pack(anchor="w")
        demo_canvas = tk.Canvas(canvas_frame, height=100, width=300)
        demo_canvas.pack(pady=2)

        # Draw some shapes on canvas
        demo_canvas.create_rectangle(10, 10, 60, 60, fill="blue", outline="darkblue")
        demo_canvas.create_oval(80, 10, 130, 60, fill="red", outline="darkred")
        demo_canvas.create_line(150, 10, 200, 60, fill="green", width=3)
        demo_canvas.create_text(250, 35, text="Themed Canvas", fill="purple")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Store references for theming
        self.showcase_widgets = {
            "text_widget": text_widget,
            "listbox": listbox,
            "demo_canvas": demo_canvas,
        }

    def create_three_pane_tab(self, notebook):
        """Create three-pane demo tab."""
        three_pane_frame = ttk.Frame(notebook)
        notebook.add(three_pane_frame, text="Three-Pane Demo")

        # Instructions
        instructions = ttk.Label(
            three_pane_frame,
            text="This demonstrates how themes are applied to a three-pane layout",
            font=("default", 12),
        )
        instructions.pack(pady=10)

        # Create three-pane layout
        paned_window = ttk.PanedWindow(three_pane_frame, orient="horizontal")
        paned_window.pack(fill="both", expand=True, padx=10, pady=10)

        # Left pane
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)

        left_header = ttk.Label(left_frame, text="Navigation", style="Header.TLabel")
        left_header.pack(pady=5)

        # Tree view for navigation
        tree = ttk.Treeview(left_frame, height=15)
        tree.heading("#0", text="File Explorer")

        # Add some sample items
        folders = tree.insert("", "end", text="Documents", open=True)
        tree.insert(folders, "end", text="file1.txt")
        tree.insert(folders, "end", text="file2.pdf")

        projects = tree.insert("", "end", text="Projects", open=True)
        tree.insert(projects, "end", text="project1")
        tree.insert(projects, "end", text="project2")

        tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Center pane
        center_frame = ttk.Frame(paned_window)
        paned_window.add(center_frame, weight=2)

        center_header = ttk.Label(center_frame, text="Content", style="Header.TLabel")
        center_header.pack(pady=5)

        # Notebook for content
        content_notebook = ttk.Notebook(center_frame)
        content_notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Tab 1
        tab1 = ttk.Frame(content_notebook)
        content_notebook.add(tab1, text="Editor")

        editor_text = tk.Text(tab1, wrap=tk.WORD)
        editor_text.insert(
            "1.0",
            """# Sample Code File

def hello_world():
    print("Hello, World!")
    return "Success"

class ThemeDemo:
    def __init__(self):
        self.theme = "native"

    def apply_theme(self):
        print(f"Applying {self.theme} theme")

if __name__ == "__main__":
    demo = ThemeDemo()
    demo.apply_theme()
    hello_world()
""",
        )
        editor_text.pack(fill="both", expand=True)

        # Tab 2
        tab2 = ttk.Frame(content_notebook)
        content_notebook.add(tab2, text="Preview")

        preview_label = ttk.Label(tab2, text="Preview content would go here")
        preview_label.pack(expand=True)

        # Right pane
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=1)

        right_header = ttk.Label(right_frame, text="Properties", style="Header.TLabel")
        right_header.pack(pady=5)

        # Properties list
        props_frame = ttk.Frame(right_frame)
        props_frame.pack(fill="both", expand=True, padx=5, pady=5)

        properties = [
            ("Name", "sample_file.py"),
            ("Size", "1.2 KB"),
            ("Modified", "2024-01-15"),
            ("Type", "Python File"),
            ("Encoding", "UTF-8"),
            ("Lines", "23"),
        ]

        for prop, value in properties:
            prop_frame = ttk.Frame(props_frame)
            prop_frame.pack(fill="x", pady=2)

            ttk.Label(prop_frame, text=f"{prop}:", font=("default", 9, "bold")).pack(
                side="left"
            )
            ttk.Label(prop_frame, text=value).pack(side="right")

        # Store references for theming
        self.three_pane_widgets = {
            "editor_text": editor_text,
            "tree": tree,
        }

    def switch_theme(self, theme_name):
        """Switch to a different theme."""
        try:
            success = self.theme_manager.set_theme(theme_name, window=self.root)
            if success:
                self.apply_current_theme()
                self.update_current_theme_display()
                print(f"✓ Switched to theme: {theme_name}")
            else:
                print(f"✗ Failed to switch to theme: {theme_name}")
        except Exception as e:
            print(f"✗ Error switching theme: {e}")

    def refresh_system_theme(self):
        """Refresh system theme to match current OS settings."""
        try:
            success = self.theme_manager.refresh_system_theme()
            if success:
                self.apply_current_theme()
                self.update_current_theme_display()
                print("✓ System theme refreshed")
            else:
                print("✗ Failed to refresh system theme")
        except Exception as e:
            print(f"✗ Error refreshing system theme: {e}")

    def toggle_auto_refresh(self, enabled):
        """Toggle automatic theme refresh."""
        if enabled:
            print("✓ Auto-refresh enabled")
        else:
            print("✗ Auto-refresh disabled")

    def apply_current_theme(self):
        """Apply the current theme to all widgets."""
        try:
            # Use the comprehensive theme application method
            self.theme_manager.apply_theme_to_window(self.root)

            print("✓ Theme applied successfully")

        except Exception as e:
            print(f"✗ Error applying theme: {e}")
            # Fallback to manual application
            try:
                # Apply ttk theme
                style = ttk.Style()
                self.theme_manager.apply_ttk_theme(style)

                # Get current theme
                current_theme = self.theme_manager.get_current_theme()

                # Update root window background
                self.root.configure(bg=current_theme.colors.primary_bg)

                # Apply theme to custom TK widgets
                if hasattr(self, "platform_info_text"):
                    text_style = self.theme_manager.get_tk_widget_style("text")
                    self.platform_info_text.configure(**text_style)

                if hasattr(self, "showcase_widgets"):
                    text_style = self.theme_manager.get_tk_widget_style("text")
                    listbox_style = self.theme_manager.get_tk_widget_style("listbox")
                    canvas_style = self.theme_manager.get_tk_widget_style("canvas")

                    self.showcase_widgets["text_widget"].configure(**text_style)
                    self.showcase_widgets["listbox"].configure(**listbox_style)
                    self.showcase_widgets["demo_canvas"].configure(**canvas_style)

                if hasattr(self, "three_pane_widgets"):
                    text_style = self.theme_manager.get_tk_widget_style("text")
                    self.three_pane_widgets["editor_text"].configure(**text_style)

                print("✓ Theme applied via fallback method")

            except Exception as fallback_error:
                print(f"✗ Fallback theme application also failed: {fallback_error}")

    def update_current_theme_display(self):
        """Update the current theme display."""
        current_theme = self.theme_manager.get_current_theme()
        self.current_theme_var.set(f"Current Theme: {current_theme.name}")

    def setup_theme_monitoring(self):
        """Set up periodic theme monitoring for system themes."""

        def check_system_theme():
            current_theme = self.theme_manager.get_current_theme()
            if current_theme.name.lower() in ["system", "native"]:
                # Check if system theme has changed
                try:
                    self.theme_manager.refresh_system_theme()
                    self.apply_current_theme()
                except Exception:
                    pass

            # Schedule next check in 5 seconds
            self.root.after(5000, check_system_theme)

        # Start monitoring
        self.root.after(5000, check_system_theme)

    def run(self):
        """Run the demo application."""
        print(f"Cross-Platform Theming Demo - {platform.system()}")
        print("=" * 50)
        print("This demo showcases the enhanced theming system with:")
        print("• Platform-native themes")
        print("• System appearance detection")
        print("• Cross-platform font handling")
        print("• Real-time theme updates")
        print("")
        print("Try switching between different themes to see the native integration!")
        print("")

        self.root.mainloop()


if __name__ == "__main__":
    try:
        demo = CrossPlatformThemingDemo()
        demo.run()
    except Exception as e:
        print(f"Error running demo: {e}")
        import traceback

        traceback.print_exc()
