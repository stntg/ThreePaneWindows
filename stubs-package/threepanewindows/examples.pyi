"""Type stubs for threepanewindows.examples module."""

import tkinter as tk
from typing import Any, Callable, Optional

def build_left_content(frame: tk.Widget) -> None:
    """Build content for the left pane."""
    ...

def build_center_content(frame: tk.Widget) -> None:
    """Build content for the center pane."""
    ...

def build_right_content(frame: tk.Widget) -> None:
    """Build content for the right pane."""
    ...

def create_sample_menu() -> tk.Menu:
    """Create a sample menu bar."""
    ...

def run_fixed_example() -> None:
    """Run the fixed layout example."""
    ...

def run_dockable_example() -> None:
    """Run the dockable layout example."""
    ...

def run_enhanced_example() -> None:
    """Run the enhanced dockable layout example."""
    ...

def run_demo() -> None:
    """Run the interactive demo with all examples."""
    ...
