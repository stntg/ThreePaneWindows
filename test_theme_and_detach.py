#!/usr/bin/env python3
"""
Test theme updates and detach functionality.
"""

import os
import sys
import tkinter as tk

# Add the threepanewindows package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "."))

from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig


def main():
    """Test theme updates and detach functionality."""
    print("Testing Theme Updates and Detach Functionality")
    print("=" * 50)

    root = tk.Tk()
    root.title("Theme & Detach Test")
    root.geometry("1000x700")

    # Create info label
    info_label = tk.Label(
        root,
        text="✅ Detach buttons (⧉) should be visible | ✅ Icons should not be duplicated | ✅ Theme changes should update all widgets",
        bg="lightblue",
        font=("Arial", 10, "bold"),
        wraplength=900,
    )
    info_label.pack(fill="x", pady=5)

    # Create window with enhanced builders (these have proper theme update functions)
    from threepanewindows.examples import (
        _build_enhanced_code_editor,
        _build_enhanced_file_explorer,
        _build_enhanced_properties,
    )

    window = EnhancedDockableThreePaneWindow(
        root,
        left_config=PaneConfig(
            title="📁 File Explorer", icon="📁", detachable=True, default_width=280
        ),
        center_config=PaneConfig(title="📝 Code Editor", icon="📝", detachable=True),
        right_config=PaneConfig(
            title="🔧 Properties",
            icon="🔧",
            detachable=True,
            custom_titlebar=True,
            default_width=300,
        ),
        left_builder=lambda frame: _build_enhanced_file_explorer(
            frame, "File Explorer"
        ),
        center_builder=lambda frame: _build_enhanced_code_editor(frame, "Code Editor"),
        right_builder=lambda frame: _build_enhanced_properties(frame, "Properties"),
        theme_name="light",
        show_status_bar=True,
    )
    window.pack(fill="both", expand=True)

    # Create theme switching controls
    controls_frame = tk.Frame(root, bg="lightgray")
    controls_frame.pack(fill="x", pady=5)

    tk.Label(
        controls_frame,
        text="Test Theme Switching:",
        bg="lightgray",
        font=("Arial", 10, "bold"),
    ).pack(side="left", padx=10)

    themes = ["light", "dark", "blue", "green", "purple"]
    for theme in themes:
        tk.Button(
            controls_frame,
            text=theme.title(),
            command=lambda t=theme: window.set_theme(t),
            width=8,
        ).pack(side="left", padx=2)

    # Create test instructions
    instructions_frame = tk.Frame(root, bg="lightyellow")
    instructions_frame.pack(fill="x", pady=5)

    instructions = [
        "1. ✅ Check that detach buttons (⧉) are visible in all pane headers",
        "2. ✅ Verify icons are not duplicated (should show '📁 File Explorer', not '📁 📁 File Explorer')",
        "3. ✅ Click theme buttons above to test theme switching - all widgets should update",
        "4. ✅ Detach panels using ⧉ buttons and test theme switching on detached windows",
        "5. ✅ Right panel uses custom titlebar when detached",
    ]

    for instruction in instructions:
        tk.Label(
            instructions_frame,
            text=instruction,
            bg="lightyellow",
            font=("Arial", 9),
            anchor="w",
        ).pack(fill="x", padx=10, pady=1)

    print("\nTest window created. Checklist:")
    print("✅ Detach buttons (⧉) visible in pane headers")
    print("✅ Icons not duplicated in titles")
    print("✅ Theme switching updates all widgets")
    print("✅ Detached windows support theme switching")
    print("✅ Icon file support works for both text and image icons")

    root.mainloop()


if __name__ == "__main__":
    main()
