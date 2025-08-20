#!/usr/bin/env python3
"""
Simple test for custom titlebar functionality.
This helps debug custom titlebar issues on WSL and other platforms.
"""

import os
import sys
import tkinter as tk


def create_test_window():
    """Create a simple test window with custom titlebar."""
    print("Creating test window with custom titlebar...")

    # Create root window
    root = tk.Tk()
    root.title("Custom Titlebar Test")
    root.geometry("500x400+200+200")

    try:
        # Remove window decorations
        print("Removing window decorations...")
        root.overrideredirect(True)

        # Create custom titlebar
        print("Creating custom titlebar...")
        titlebar = tk.Frame(root, bg="#2d2d30", height=32, relief="flat")
        titlebar.pack(fill="x", side="top")
        titlebar.pack_propagate(False)

        # Window title
        title_label = tk.Label(
            titlebar,
            text="Custom Titlebar Test - Drag me!",
            bg="#2d2d30",
            fg="white",
            font=("Arial", 10, "bold"),
            anchor="w",
        )
        title_label.pack(side="left", fill="both", expand=True, padx=10, pady=6)

        # Window controls
        controls_frame = tk.Frame(titlebar, bg="#2d2d30")
        controls_frame.pack(side="right", pady=4, padx=4)

        # Minimize button
        min_btn = tk.Button(
            controls_frame,
            text="−",
            command=lambda: root.iconify(),
            bg="#2d2d30",
            fg="white",
            activebackground="#404040",
            activeforeground="white",
            relief="flat",
            width=3,
            height=1,
            font=("Arial", 12, "bold"),
            bd=0,
            highlightthickness=0,
        )
        min_btn.pack(side="left", padx=1)

        # Close button
        close_btn = tk.Button(
            controls_frame,
            text="×",
            command=root.quit,
            bg="#2d2d30",
            fg="white",
            activebackground="#e74c3c",
            activeforeground="white",
            relief="flat",
            width=3,
            height=1,
            font=("Arial", 12, "bold"),
            bd=0,
            highlightthickness=0,
        )
        close_btn.pack(side="left", padx=1)

        # Make window draggable
        def start_drag(event):
            root.x = event.x
            root.y = event.y

        def drag_window(event):
            x = root.winfo_pointerx() - root.x
            y = root.winfo_pointery() - root.y
            root.geometry(f"+{x}+{y}")

        titlebar.bind("<Button-1>", start_drag)
        titlebar.bind("<B1-Motion>", drag_window)
        title_label.bind("<Button-1>", start_drag)
        title_label.bind("<B1-Motion>", drag_window)

        # Add content area
        content_frame = tk.Frame(root, bg="white")
        content_frame.pack(fill="both", expand=True)

        # Add test content
        info_text = tk.Text(content_frame, wrap="word", font=("Arial", 10))
        info_text.pack(fill="both", expand=True, padx=10, pady=10)

        test_info = f"""Custom Titlebar Test

This window tests custom titlebar functionality.

Features to test:
✓ Custom titlebar with dark theme
✓ Window dragging (click and drag the titlebar)
✓ Minimize button (−)
✓ Close button (×)
✓ Emergency exit keys

Environment Information:
- Platform: {sys.platform}
- Python: {sys.version.split()[0]}
- DISPLAY: {os.environ.get('DISPLAY', 'Not set')}
- WSL_DISTRO_NAME: {os.environ.get('WSL_DISTRO_NAME', 'Not set')}

Instructions:
1. Try dragging the window by clicking and dragging the titlebar
2. Test the minimize button (−)
3. Test the close button (×)
4. Try emergency exit keys: Ctrl+Q, Alt+F4, Escape

If the titlebar is missing or not working:
- The window decorations were removed but titlebar creation failed
- Use emergency keys to close: Ctrl+Q, Alt+F4, or Escape
- Check the console for error messages
"""

        info_text.insert("1.0", test_info)
        info_text.configure(state="disabled")

        # Emergency exit keybindings
        root.bind("<Control-q>", lambda e: root.quit())
        root.bind("<Alt-F4>", lambda e: root.quit())
        root.bind("<Escape>", lambda e: root.quit())

        print("✓ Custom titlebar created successfully")
        print("✓ Window dragging enabled")
        print("✓ Emergency exit keys: Ctrl+Q, Alt+F4, Escape")
        print()
        print("Test the following:")
        print("1. Drag the window by the titlebar")
        print("2. Click the minimize button (−)")
        print("3. Click the close button (×)")
        print("4. Use emergency keys if needed")
        print()

        # Start the GUI
        root.mainloop()

        print("✓ Test completed successfully")
        return True

    except Exception as e:
        print(f"✗ Error creating custom titlebar: {e}")
        import traceback

        traceback.print_exc()

        # Try to restore window decorations
        try:
            root.overrideredirect(False)
            root.title("Custom Titlebar Test - ERROR")

            # Show error in window
            error_label = tk.Label(
                root,
                text=f"Custom titlebar failed!\n\nError: {e}\n\nPress Ctrl+Q to quit",
                font=("Arial", 12),
                justify="center",
                fg="red",
            )
            error_label.pack(expand=True)

            root.bind("<Control-q>", lambda e: root.quit())
            root.mainloop()

        except Exception as restore_error:
            print(f"✗ Could not restore window: {restore_error}")

        return False


def main():
    """Main test function."""
    print("=" * 60)
    print("Custom Titlebar Test")
    print("=" * 60)
    print()

    print("This test creates a simple window with a custom titlebar")
    print("to help debug titlebar issues on WSL and other platforms.")
    print()

    try:
        if create_test_window():
            print("✓ Custom titlebar test passed")
            return 0
        else:
            print("✗ Custom titlebar test failed")
            return 1

    except KeyboardInterrupt:
        print("\n✗ Test interrupted by user")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
