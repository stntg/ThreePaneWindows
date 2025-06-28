Cross-Platform Icon Examples
=============================

This section demonstrates how to use cross-platform icon support in ThreePaneWindows applications.

Basic Icon Usage
----------------

Simple example showing how to add icons to detached windows:

.. code-block:: python

    import tkinter as tk
    from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

    def create_basic_icon_example():
        root = tk.Tk()
        root.title("Basic Icon Example")
        root.geometry("1000x700")

        def build_file_panel(frame):
            tk.Label(frame, text="📁 File Manager", font=("Arial", 12, "bold")).pack(pady=10)
            
            files = ["📄 document.txt", "🖼️ image.png", "🎵 music.mp3"]
            for file in files:
                tk.Button(frame, text=file, anchor="w").pack(fill=tk.X, padx=5, pady=2)

        def build_editor_panel(frame):
            tk.Label(frame, text="📝 Text Editor", font=("Arial", 12, "bold")).pack(pady=10)
            
            text = tk.Text(frame, wrap=tk.WORD, font=("Consolas", 10))
            text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text.insert("1.0", "# Welcome to the Text Editor\n\nThis is a sample document.")

        def build_tools_panel(frame):
            tk.Label(frame, text="🔧 Tools", font=("Arial", 12, "bold")).pack(pady=10)
            
            tools = ["🔍 Find", "🔄 Replace", "📊 Statistics", "⚙️ Settings"]
            for tool in tools:
                tk.Button(frame, text=tool, anchor="w").pack(fill=tk.X, padx=5, pady=2)

        # Configure panels with cross-platform icons
        file_config = PaneConfig(
            title="Files",
            icon="📁",
            window_icon="icons/files.png",  # PNG works on all platforms
            default_width=200,
            detachable=True
        )

        editor_config = PaneConfig(
            title="Editor",
            icon="📝",
            window_icon="icons/editor.png",  # PNG works on all platforms
            detachable=False
        )

        tools_config = PaneConfig(
            title="Tools",
            icon="🔧",
            window_icon="icons/tools.png",  # PNG works on all platforms
            default_width=180,
            detachable=True
        )

        # Create the enhanced window
        window = EnhancedDockableThreePaneWindow(
            root,
            left_config=file_config,
            center_config=editor_config,
            right_config=tools_config,
            left_builder=build_file_panel,
            center_builder=build_editor_panel,
            right_builder=build_tools_panel,
            theme_name="light"
        )
        window.pack(fill=tk.BOTH, expand=True)

        return root

    if __name__ == "__main__":
        app = create_basic_icon_example()
        app.mainloop()

Platform-Specific Icon Selection
---------------------------------

Advanced example showing how to select the best icon for each platform:

.. code-block:: python

    import tkinter as tk
    import platform
    import os
    from threepanewindows import (
        EnhancedDockableThreePaneWindow, 
        PaneConfig,
        get_recommended_icon_formats,
        validate_icon_path
    )

    def create_platform_specific_example():
        root = tk.Tk()
        root.title("Platform-Specific Icons")
        root.geometry("1200x800")

        def get_best_icon(base_name):
            """Get the best icon for the current platform."""
            system = platform.system()
            
            # Define icon paths for different platforms
            icon_candidates = []
            
            if system == "Windows":
                icon_candidates = [
                    f"icons/{base_name}.ico",
                    f"icons/{base_name}.png",
                    f"icons/{base_name}.bmp"
                ]
            elif system == "Darwin":  # macOS
                icon_candidates = [
                    f"icons/{base_name}.png",
                    f"icons/{base_name}.gif",
                    f"icons/{base_name}.bmp"
                ]
            else:  # Linux and others
                icon_candidates = [
                    f"icons/{base_name}.png",
                    f"icons/{base_name}.xbm",
                    f"icons/{base_name}.gif"
                ]
            
            # Find the first existing icon
            for icon_path in icon_candidates:
                if os.path.exists(icon_path):
                    is_valid, message = validate_icon_path(icon_path)
                    if is_valid:
                        return icon_path
            
            return ""  # No icon found

        def build_project_panel(frame):
            tk.Label(frame, text="📁 Project Explorer", font=("Arial", 12, "bold")).pack(pady=10)
            
            # Show current platform info
            system_info = f"Platform: {platform.system()}"
            formats = get_recommended_icon_formats()
            formats_info = f"Recommended: {', '.join(formats)}"
            
            info_frame = tk.LabelFrame(frame, text="Platform Info")
            info_frame.pack(fill=tk.X, padx=5, pady=5)
            
            tk.Label(info_frame, text=system_info, font=("Arial", 9)).pack(anchor="w", padx=5)
            tk.Label(info_frame, text=formats_info, font=("Arial", 9), 
                    wraplength=180).pack(anchor="w", padx=5, pady=(0,5))
            
            # Project tree
            tree_frame = tk.Frame(frame)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            project_items = [
                "📁 src/",
                "  🐍 main.py",
                "  🐍 utils.py",
                "📁 assets/",
                "  🖼️ icon.png",
                "  🖼️ logo.ico",
                "📄 README.md"
            ]
            
            listbox = tk.Listbox(tree_frame, font=("Consolas", 9))
            listbox.pack(fill=tk.BOTH, expand=True)
            
            for item in project_items:
                listbox.insert(tk.END, item)

        def build_code_panel(frame):
            tk.Label(frame, text="📝 Code Editor", font=("Arial", 12, "bold")).pack(pady=10)
            
            # Code editor with syntax highlighting simulation
            code_frame = tk.Frame(frame)
            code_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Line numbers
            line_frame = tk.Frame(code_frame, width=40, bg="lightgray")
            line_frame.pack(side=tk.LEFT, fill=tk.Y)
            line_frame.pack_propagate(False)
            
            line_text = tk.Text(line_frame, width=4, bg="lightgray", fg="gray", 
                              font=("Consolas", 10), state=tk.DISABLED)
            line_text.pack(fill=tk.BOTH, expand=True)
            
            # Code area
            code_text = tk.Text(code_frame, font=("Consolas", 10), wrap=tk.NONE)
            code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Sample code
            sample_code = '''# Cross-Platform Icon Example
import platform
from threepanewindows import PaneConfig, get_recommended_icon_formats

def setup_icons():
    """Setup icons with platform detection."""
    system = platform.system()
    formats = get_recommended_icon_formats()
    
    if system == "Windows":
        icon = "app.ico"  # Best on Windows
    else:
        icon = "app.png"  # Universal fallback
    
    return PaneConfig(window_icon=icon)

config = setup_icons()
print(f"Using icon: {config.window_icon}")
'''
            code_text.insert("1.0", sample_code)
            
            # Add line numbers
            lines = sample_code.count('\n') + 1
            line_numbers = '\n'.join(str(i) for i in range(1, lines + 1))
            line_text.config(state=tk.NORMAL)
            line_text.insert("1.0", line_numbers)
            line_text.config(state=tk.DISABLED)

        def build_output_panel(frame):
            tk.Label(frame, text="📊 Output", font=("Arial", 12, "bold")).pack(pady=10)
            
            # Platform detection results
            results_frame = tk.LabelFrame(frame, text="Icon Detection Results")
            results_frame.pack(fill=tk.X, padx=5, pady=5)
            
            system = platform.system()
            formats = get_recommended_icon_formats()
            
            results = [
                f"Current Platform: {system}",
                f"Recommended Formats: {', '.join(formats)}",
                "",
                "Icon Validation Results:"
            ]
            
            # Test some common icon paths
            test_icons = ["app.ico", "app.png", "icon.gif"]
            for icon in test_icons:
                is_valid, message = validate_icon_path(icon)
                status = "✓" if is_valid else "✗"
                results.append(f"  {status} {icon}: {message}")
            
            output_text = tk.Text(results_frame, height=8, font=("Consolas", 9))
            output_text.pack(fill=tk.X, padx=5, pady=5)
            
            for result in results:
                output_text.insert(tk.END, result + "\n")
            
            output_text.config(state=tk.DISABLED)

        # Configure panels with platform-specific icons
        project_config = PaneConfig(
            title="Project",
            icon="📁",
            window_icon=get_best_icon("project"),
            default_width=250,
            detachable=True
        )

        code_config = PaneConfig(
            title="Code",
            icon="📝",
            window_icon=get_best_icon("code"),
            detachable=False
        )

        output_config = PaneConfig(
            title="Output",
            icon="📊",
            window_icon=get_best_icon("output"),
            default_width=300,
            detachable=True
        )

        # Create the enhanced window
        window = EnhancedDockableThreePaneWindow(
            root,
            left_config=project_config,
            center_config=code_config,
            right_config=output_config,
            left_builder=build_project_panel,
            center_builder=build_code_panel,
            right_builder=build_output_panel,
            theme_name="blue"
        )
        window.pack(fill=tk.BOTH, expand=True)

        return root

    if __name__ == "__main__":
        app = create_platform_specific_example()
        app.mainloop()

Icon Validation Example
-----------------------

Example showing how to validate icons before using them:

.. code-block:: python

    import tkinter as tk
    from tkinter import filedialog, messagebox
    from threepanewindows import (
        EnhancedDockableThreePaneWindow, 
        PaneConfig,
        get_recommended_icon_formats,
        validate_icon_path
    )

    def create_icon_validation_example():
        root = tk.Tk()
        root.title("Icon Validation Example")
        root.geometry("1000x600")

        # Store current icon paths
        current_icons = {
            "left": "",
            "center": "",
            "right": ""
        }

        def build_icon_selector(frame):
            tk.Label(frame, text="🖼️ Icon Selector", font=("Arial", 12, "bold")).pack(pady=10)
            
            # Recommended formats info
            formats_frame = tk.LabelFrame(frame, text="Recommended Formats")
            formats_frame.pack(fill=tk.X, padx=5, pady=5)
            
            formats = get_recommended_icon_formats()
            formats_text = ", ".join(formats)
            tk.Label(formats_frame, text=formats_text, font=("Arial", 9), 
                    wraplength=200).pack(padx=5, pady=5)
            
            # Icon selection buttons
            selection_frame = tk.LabelFrame(frame, text="Select Icons")
            selection_frame.pack(fill=tk.X, padx=5, pady=5)
            
            def select_icon(pane_name):
                filetypes = [
                    ("Icon files", "*.ico *.png *.gif *.bmp *.xbm"),
                    ("PNG files", "*.png"),
                    ("ICO files", "*.ico"),
                    ("All files", "*.*")
                ]
                
                filename = filedialog.askopenfilename(
                    title=f"Select icon for {pane_name} pane",
                    filetypes=filetypes
                )
                
                if filename:
                    is_valid, message = validate_icon_path(filename)
                    if is_valid:
                        current_icons[pane_name] = filename
                        update_icon_display()
                        messagebox.showinfo("Success", f"Icon selected: {message}")
                    else:
                        messagebox.showwarning("Validation Failed", message)
            
            for pane in ["left", "center", "right"]:
                btn = tk.Button(selection_frame, text=f"Select {pane.title()} Icon",
                              command=lambda p=pane: select_icon(p))
                btn.pack(fill=tk.X, padx=5, pady=2)
            
            # Current icons display
            global icons_display_frame
            icons_display_frame = tk.LabelFrame(frame, text="Current Icons")
            icons_display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            update_icon_display()

        def update_icon_display():
            # Clear existing widgets
            for widget in icons_display_frame.winfo_children():
                widget.destroy()
            
            for pane, icon_path in current_icons.items():
                pane_frame = tk.Frame(icons_display_frame)
                pane_frame.pack(fill=tk.X, padx=5, pady=2)
                
                tk.Label(pane_frame, text=f"{pane.title()}:", width=8, 
                        anchor="w").pack(side=tk.LEFT)
                
                if icon_path:
                    # Show filename and validation status
                    filename = icon_path.split('/')[-1]
                    is_valid, message = validate_icon_path(icon_path)
                    status = "✓" if is_valid else "✗"
                    
                    tk.Label(pane_frame, text=f"{status} {filename}", 
                            fg="green" if is_valid else "red",
                            font=("Arial", 9)).pack(side=tk.LEFT)
                else:
                    tk.Label(pane_frame, text="No icon selected", 
                            fg="gray", font=("Arial", 9)).pack(side=tk.LEFT)

        def build_preview_panel(frame):
            tk.Label(frame, text="👁️ Preview", font=("Arial", 12, "bold")).pack(pady=10)
            
            preview_text = tk.Text(frame, wrap=tk.WORD, font=("Arial", 10))
            preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            preview_content = """Icon Preview Panel

This panel shows how your selected icons will appear in detached windows.

To test:
1. Select icons using the Icon Selector
2. Detach this panel (drag the header)
3. Observe the icon in the window title bar

The system will automatically:
- Validate icon format compatibility
- Use the best display method for your platform
- Provide fallbacks if the primary method fails
- Continue gracefully if no icon is available

Cross-platform compatibility ensures your application looks professional on all operating systems.
"""
            preview_text.insert("1.0", preview_content)
            preview_text.config(state=tk.DISABLED)

        def build_validation_panel(frame):
            tk.Label(frame, text="✅ Validation", font=("Arial", 12, "bold")).pack(pady=10)
            
            # Validation results
            validation_frame = tk.LabelFrame(frame, text="Validation Results")
            validation_frame.pack(fill=tk.X, padx=5, pady=5)
            
            global validation_text
            validation_text = tk.Text(validation_frame, height=10, font=("Consolas", 9))
            validation_text.pack(fill=tk.X, padx=5, pady=5)
            
            # Test button
            test_btn = tk.Button(frame, text="🔍 Test Current Icons", 
                               command=run_validation_test)
            test_btn.pack(pady=10)
            
            # Initial validation
            run_validation_test()

        def run_validation_test():
            validation_text.delete("1.0", tk.END)
            validation_text.insert(tk.END, "Icon Validation Test Results\n")
            validation_text.insert(tk.END, "=" * 35 + "\n\n")
            
            for pane, icon_path in current_icons.items():
                validation_text.insert(tk.END, f"{pane.title()} Pane:\n")
                
                if icon_path:
                    is_valid, message = validate_icon_path(icon_path)
                    status = "VALID" if is_valid else "INVALID"
                    validation_text.insert(tk.END, f"  Status: {status}\n")
                    validation_text.insert(tk.END, f"  Message: {message}\n")
                    validation_text.insert(tk.END, f"  Path: {icon_path}\n")
                else:
                    validation_text.insert(tk.END, "  Status: NO ICON\n")
                    validation_text.insert(tk.END, "  Message: No icon selected\n")
                
                validation_text.insert(tk.END, "\n")
            
            # Platform info
            formats = get_recommended_icon_formats()
            validation_text.insert(tk.END, f"Platform Recommendations:\n")
            validation_text.insert(tk.END, f"  Formats: {', '.join(formats)}\n")

        # Configure panels
        selector_config = PaneConfig(
            title="Icon Selector",
            icon="🖼️",
            window_icon=current_icons.get("left", ""),
            default_width=250,
            detachable=True
        )

        preview_config = PaneConfig(
            title="Preview",
            icon="👁️",
            window_icon=current_icons.get("center", ""),
            detachable=True
        )

        validation_config = PaneConfig(
            title="Validation",
            icon="✅",
            window_icon=current_icons.get("right", ""),
            default_width=300,
            detachable=True
        )

        # Create the enhanced window
        window = EnhancedDockableThreePaneWindow(
            root,
            left_config=selector_config,
            center_config=preview_config,
            right_config=validation_config,
            left_builder=build_icon_selector,
            center_builder=build_preview_panel,
            right_builder=build_validation_panel,
            theme_name="light"
        )
        window.pack(fill=tk.BOTH, expand=True)

        return root

    if __name__ == "__main__":
        app = create_icon_validation_example()
        app.mainloop()

Key Features Demonstrated
-------------------------

These examples showcase:

**Cross-Platform Compatibility**
  Icons work consistently across Windows, macOS, and Linux with automatic format optimization.

**Icon Validation**
  Built-in validation ensures icons are compatible before use, preventing runtime errors.

**Platform Detection**
  Automatic detection of the best icon formats for the current platform.

**Graceful Fallbacks**
  If an icon can't be loaded, the application continues without errors.

**Professional Integration**
  Icons enhance the professional appearance of detached windows.

Best Practices
--------------

1. **Use PNG for universal compatibility** - Works on all platforms
2. **Provide .ico files for Windows** - Best native support
3. **Validate icons before use** - Prevent runtime issues
4. **Handle missing icons gracefully** - Don't let missing icons break your app
5. **Test on multiple platforms** - Ensure consistent behavior

These examples provide a solid foundation for implementing cross-platform icon support in your ThreePaneWindows applications.