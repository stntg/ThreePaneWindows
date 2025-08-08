#!/usr/bin/env python3
"""
Custom Themeable Menubar

This module provides a fully themeable menubar that works on all platforms,
including Windows where the native menubar cannot be themed.
"""

import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import Any, Callable, Dict, List, Optional, Union


@dataclass
class MenuItem:
    """Represents a menu item."""

    label: str
    command: Optional[Callable] = None
    submenu: Optional[List["MenuItem"]] = None
    separator: bool = False
    accelerator: Optional[str] = None
    state: str = "normal"  # normal, disabled, active


class CustomMenubar(tk.Frame):
    """
    Custom menubar that can be fully themed on all platforms.

    This replaces the native tk.Menu menubar with a custom implementation
    using Tkinter widgets that can be fully themed.
    """

    def __init__(self, parent: tk.Tk, **kwargs):
        """
        Initialize the custom menubar.

        Args:
            parent: The parent window
            **kwargs: Additional Frame options
        """
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.menus: Dict[str, List[MenuItem]] = {}
        self.menu_buttons: Dict[str, tk.Label] = {}
        self.active_menu: Optional[tk.Menu] = None
        self.active_button: Optional[tk.Label] = None

        # Configure the menubar frame
        self.configure(relief="flat", bd=0, height=28)
        self.pack_propagate(False)  # Don't shrink to fit contents

        # Bind events for menu dismissal
        self.parent.bind("<Button-1>", self._on_window_click, add="+")
        self.parent.bind("<Key>", self._on_key_press, add="+")

    def add_menu(self, label: str, items: List[MenuItem]) -> None:
        """
        Add a menu to the menubar.

        Args:
            label: The menu label (e.g., "File", "Edit")
            items: List of menu items
        """
        # Store menu items
        self.menus[label] = items

        # Create menu button
        menu_button = tk.Label(
            self,
            text=label,
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2",
            font=("Segoe UI", 9) if tk.TkVersion >= 8.5 else None,
        )
        menu_button.pack(side="left")

        # Store button reference
        self.menu_buttons[label] = menu_button

        # Bind events
        menu_button.bind("<Button-1>", lambda e: self._show_menu(label, menu_button))
        menu_button.bind("<Enter>", lambda e: self._on_menu_enter(label, menu_button))
        menu_button.bind("<Leave>", lambda e: self._on_menu_leave(label, menu_button))

    def _show_menu(self, label: str, button: tk.Label) -> None:
        """Show the dropdown menu for a menu button."""
        try:
            # Hide any active menu
            if self.active_menu:
                self.active_menu.unpost()
                if self.active_button:
                    self._reset_button_appearance(self.active_button)

            # Create dropdown menu with proper theming from start
            dropdown = tk.Menu(self.parent, tearoff=0, relief="flat", borderwidth=0)

            # Add menu items
            items = self.menus.get(label, [])
            self._build_menu_items(dropdown, items)

            # Apply theme to dropdown and all submenus
            self._apply_menu_theme_recursive(dropdown)

            # Show the menu
            x = button.winfo_rootx()
            y = button.winfo_rooty() + button.winfo_height()
            dropdown.post(x, y)

            # Set active menu and button
            self.active_menu = dropdown
            self.active_button = button

            # Highlight the active button
            self._highlight_active_button(button)

        except tk.TclError:
            pass

    def _build_menu_items(self, menu: tk.Menu, items: List[MenuItem]) -> None:
        """Recursively build menu items including submenus."""
        for item in items:
            if item.separator:
                menu.add_separator()
            elif item.submenu:
                # Handle submenus recursively with proper theming
                submenu = tk.Menu(menu, tearoff=0, relief="flat", borderwidth=0)
                self._build_menu_items(submenu, item.submenu)  # Recursive call
                menu.add_cascade(label=item.label, menu=submenu)
            else:
                menu.add_command(
                    label=item.label,
                    command=item.command,
                    accelerator=item.accelerator,
                    state=item.state,
                )

    def _on_menu_enter(self, label: str, button: tk.Label) -> None:
        """Handle mouse enter on menu button."""
        if button != self.active_button:
            # Apply hover effect
            from .central_theme_manager import get_theme_manager

            theme = get_theme_manager().get_current_theme()
            button.configure(bg=theme.menu_hover)

            # If another menu is active, switch to this one
            if self.active_menu and self.active_button:
                self._show_menu(label, button)

    def _on_menu_leave(self, label: str, button: tk.Label) -> None:
        """Handle mouse leave on menu button."""
        if button != self.active_button:
            # Remove hover effect
            from .central_theme_manager import get_theme_manager

            theme = get_theme_manager().get_current_theme()
            button.configure(bg=theme.menu_bg)

    def _highlight_active_button(self, button: tk.Label) -> None:
        """Highlight the active menu button."""
        from .central_theme_manager import get_theme_manager

        theme = get_theme_manager().get_current_theme()
        button.configure(bg=theme.menu_active)

    def _reset_button_appearance(self, button: tk.Label) -> None:
        """Reset button to normal appearance."""
        from .central_theme_manager import get_theme_manager

        theme = get_theme_manager().get_current_theme()
        button.configure(bg=theme.menu_bg)

    def _on_window_click(self, event) -> None:
        """Handle clicks outside the menu to dismiss it."""
        if self.active_menu:
            # Check if click is outside the menubar and menu
            widget = event.widget
            if not self._is_menubar_widget(widget):
                self._dismiss_menu()

    def _on_key_press(self, event) -> None:
        """Handle key presses to dismiss menu."""
        if self.active_menu and event.keysym == "Escape":
            self._dismiss_menu()

    def _dismiss_menu(self) -> None:
        """Dismiss the active menu."""
        if self.active_menu:
            self.active_menu.unpost()
            self.active_menu = None

        if self.active_button:
            self._reset_button_appearance(self.active_button)
            self.active_button = None

    def _is_menubar_widget(self, widget) -> bool:
        """Check if a widget is part of the menubar."""
        current = widget
        while current:
            if current == self:
                return True
            try:
                current = current.master
            except AttributeError:
                break
        return False

    def _apply_menu_theme(self, menu: tk.Menu) -> None:
        """Apply theme to a single dropdown menu."""
        try:
            from .central_theme_manager import get_theme_manager

            theme = get_theme_manager().get_current_theme()

            # Enhanced menu theming with proper border handling
            menu.configure(
                bg=theme.menu_bg,
                fg=theme.menu_text,
                activebackground=theme.menu_hover,
                activeforeground=theme.menu_text,
                selectcolor=theme.accent_bg,
                relief="flat",
                borderwidth=0,  # Remove border completely
                font=("Segoe UI", 9) if tk.TkVersion >= 8.5 else None,
            )

            # Additional platform-specific theming for better appearance
            try:
                # Set additional menu properties for better theming
                menu.configure(
                    disabledforeground=theme.secondary_text,  # Disabled item color
                    tearoff=0,  # Ensure no tearoff
                )

                # Try to set border color to match background (fallback)
                if hasattr(menu, "configure"):
                    try:
                        menu.configure(highlightbackground=theme.menu_bg)
                        menu.configure(highlightcolor=theme.menu_bg)
                    except tk.TclError:
                        pass

            except (tk.TclError, AttributeError):
                pass

        except Exception:
            pass

    def _apply_menu_theme_recursive(self, menu: tk.Menu) -> None:
        """Apply theme to a menu and all its submenus recursively."""
        try:
            # Apply theme to this menu
            self._apply_menu_theme(menu)

            # Get all menu items and find submenus
            last_index = menu.index("end")
            if last_index is not None:
                for i in range(last_index + 1):
                    try:
                        # Check if this item is a cascade (submenu)
                        item_type = menu.type(i)
                        if item_type == "cascade":
                            # Get the submenu and apply theme recursively
                            submenu = menu.nametowidget(menu.entrycget(i, "menu"))
                            if submenu:
                                self._apply_menu_theme_recursive(
                                    submenu
                                )  # Recursive call
                    except (tk.TclError, AttributeError):
                        # Skip items that can't be processed
                        continue

        except Exception as e:
            # Fallback to basic theming if recursive fails
            self._apply_menu_theme(menu)

    def apply_theme(self) -> None:
        """Apply the current theme to the menubar and all menus."""
        try:
            from .central_theme_manager import get_theme_manager

            theme = get_theme_manager().get_current_theme()

            # Theme the menubar frame
            self.configure(bg=theme.menu_bg)

            # Theme all menu buttons
            for label, button in self.menu_buttons.items():
                button.configure(
                    bg=theme.menu_bg,
                    fg=theme.menu_text,
                    activebackground=theme.menu_hover,
                    activeforeground=theme.menu_text,
                )

            # If there's an active menu, re-theme it and all submenus
            if self.active_menu:
                self._apply_menu_theme_recursive(self.active_menu)

        except Exception:
            pass

    def get_menu_height(self) -> int:
        """Get the height of the menubar."""
        return self.winfo_reqheight()

    def force_menu_retheme(self) -> None:
        """Force re-theming of all menus (useful when theme changes while menus are open)."""
        try:
            # If there's an active menu, re-theme it immediately
            if self.active_menu:
                self._apply_menu_theme_recursive(self.active_menu)

            # Also re-theme the menubar itself
            self.apply_theme()

        except Exception:
            pass


class ThemedMenubarMixin:
    """
    Mixin class to add custom themeable menubar functionality to windows.

    This can be used by any ThreePaneWindows module to replace the native
    menubar with a fully themeable custom menubar.
    """

    def create_custom_menubar(self) -> CustomMenubar:
        """
        Create a custom themeable menubar.

        Returns:
            CustomMenubar instance
        """
        # Remove any existing native menubar
        if hasattr(self, "root"):
            self.root.config(menu=None)

        # Create custom menubar
        custom_menubar = CustomMenubar(self.root)
        custom_menubar.pack(fill="x", side="top")

        return custom_menubar

    def add_standard_menus(self, menubar: CustomMenubar) -> None:
        """
        Add standard menus (File, Edit, View, etc.) to the custom menubar.

        Args:
            menubar: The custom menubar to add menus to
        """
        # File menu
        file_items = [
            MenuItem("New", command=lambda: self._menu_action("New")),
            MenuItem("Open", command=lambda: self._menu_action("Open")),
            MenuItem("Save", command=lambda: self._menu_action("Save")),
            MenuItem("Save As...", command=lambda: self._menu_action("Save As")),
            MenuItem("", separator=True),
            MenuItem(
                "Recent Files",
                submenu=[
                    MenuItem(
                        "File 1.txt", command=lambda: self._menu_action("Recent 1")
                    ),
                    MenuItem(
                        "File 2.txt", command=lambda: self._menu_action("Recent 2")
                    ),
                    MenuItem(
                        "File 3.txt", command=lambda: self._menu_action("Recent 3")
                    ),
                ],
            ),
            MenuItem("", separator=True),
            MenuItem("Exit", command=self.root.quit if hasattr(self, "root") else None),
        ]
        menubar.add_menu("File", file_items)

        # Edit menu
        edit_items = [
            MenuItem(
                "Undo", command=lambda: self._menu_action("Undo"), accelerator="Ctrl+Z"
            ),
            MenuItem(
                "Redo", command=lambda: self._menu_action("Redo"), accelerator="Ctrl+Y"
            ),
            MenuItem("", separator=True),
            MenuItem(
                "Cut", command=lambda: self._menu_action("Cut"), accelerator="Ctrl+X"
            ),
            MenuItem(
                "Copy", command=lambda: self._menu_action("Copy"), accelerator="Ctrl+C"
            ),
            MenuItem(
                "Paste",
                command=lambda: self._menu_action("Paste"),
                accelerator="Ctrl+V",
            ),
            MenuItem("", separator=True),
            MenuItem(
                "Select All",
                command=lambda: self._menu_action("Select All"),
                accelerator="Ctrl+A",
            ),
            MenuItem(
                "Find", command=lambda: self._menu_action("Find"), accelerator="Ctrl+F"
            ),
        ]
        menubar.add_menu("Edit", edit_items)

        # View menu
        view_items = [
            MenuItem(
                "Zoom In",
                command=lambda: self._menu_action("Zoom In"),
                accelerator="Ctrl++",
            ),
            MenuItem(
                "Zoom Out",
                command=lambda: self._menu_action("Zoom Out"),
                accelerator="Ctrl+-",
            ),
            MenuItem(
                "Reset Zoom",
                command=lambda: self._menu_action("Reset Zoom"),
                accelerator="Ctrl+0",
            ),
            MenuItem("", separator=True),
            MenuItem(
                "Full Screen",
                command=lambda: self._menu_action("Full Screen"),
                accelerator="F11",
            ),
        ]
        menubar.add_menu("View", view_items)

        # Themes menu (if theme switching is supported)
        if hasattr(self, "apply_theme"):
            from .central_theme_manager import get_theme_manager

            theme_manager = get_theme_manager()
            theme_items = []

            for theme_name in theme_manager.get_theme_names():
                theme_items.append(
                    MenuItem(
                        f"{theme_name.title()} Theme",
                        command=lambda t=theme_name: self.apply_theme(t),
                    )
                )

            menubar.add_menu("Themes", theme_items)

        # Help menu
        help_items = [
            MenuItem("About", command=lambda: self._menu_action("About")),
            MenuItem(
                "Documentation", command=lambda: self._menu_action("Documentation")
            ),
            MenuItem(
                "Keyboard Shortcuts", command=lambda: self._menu_action("Shortcuts")
            ),
        ]
        menubar.add_menu("Help", help_items)

    def _menu_action(self, action: str) -> None:
        """
        Handle menu actions.

        Args:
            action: The menu action name
        """
        print(f"Menu action: {action}")

        # Update status if available
        if hasattr(self, "status_label"):
            self.status_label.config(text=f"✅ {action} action triggered")


# Convenience functions for easy integration
def create_themed_menubar(parent: tk.Tk) -> CustomMenubar:
    """
    Create a themed menubar for a window.

    Args:
        parent: The parent window

    Returns:
        CustomMenubar instance
    """
    return CustomMenubar(parent)


def replace_native_menubar(window: tk.Tk) -> CustomMenubar:
    """
    Replace the native menubar with a custom themed menubar.

    Args:
        window: The window to modify

    Returns:
        CustomMenubar instance
    """
    # Remove native menubar
    window.config(menu=None)

    # Create and return custom menubar
    custom_menubar = CustomMenubar(window)
    custom_menubar.pack(fill="x", side="top")

    return custom_menubar
