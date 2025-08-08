"""
Tests for the Custom Menubar component.
"""

import tkinter as tk
from unittest.mock import Mock

import pytest

from threepanewindows.custom_menubar import CustomMenubar, MenuItem


class TestMenuItem:
    """Test cases for MenuItem dataclass."""

    def test_basic_menu_item(self):
        """Test basic MenuItem creation."""
        item = MenuItem(label="File")

        assert item.label == "File"
        assert item.command is None
        assert item.submenu is None
        assert item.separator is False
        assert item.accelerator is None
        assert item.state == "normal"

    def test_menu_item_with_command(self):
        """Test MenuItem with command."""
        mock_command = Mock()
        item = MenuItem(label="Open", command=mock_command)

        assert item.label == "Open"
        assert item.command == mock_command

    def test_menu_item_with_submenu(self):
        """Test MenuItem with submenu."""
        sub_item = MenuItem(label="Sub Item")
        item = MenuItem(label="Parent", submenu=[sub_item])

        assert item.label == "Parent"
        assert len(item.submenu) == 1
        assert item.submenu[0] == sub_item

    def test_separator_menu_item(self):
        """Test separator MenuItem."""
        item = MenuItem(label="", separator=True)

        assert item.separator is True
        assert item.label == ""

    def test_menu_item_with_accelerator(self):
        """Test MenuItem with accelerator."""
        item = MenuItem(label="Save", accelerator="Ctrl+S")

        assert item.label == "Save"
        assert item.accelerator == "Ctrl+S"

    def test_menu_item_with_state(self):
        """Test MenuItem with different states."""
        normal_item = MenuItem(label="Normal", state="normal")
        disabled_item = MenuItem(label="Disabled", state="disabled")
        active_item = MenuItem(label="Active", state="active")

        assert normal_item.state == "normal"
        assert disabled_item.state == "disabled"
        assert active_item.state == "active"

    def test_complex_menu_item(self):
        """Test MenuItem with all parameters."""
        mock_command = Mock()
        item = MenuItem(
            label="Complex Item",
            command=mock_command,
            accelerator="Ctrl+Alt+C",
            state="disabled",
        )

        assert item.label == "Complex Item"
        assert item.command == mock_command
        assert item.accelerator == "Ctrl+Alt+C"
        assert item.state == "disabled"

    def test_nested_submenu(self):
        """Test nested submenu structure."""
        sub_sub_item = MenuItem(label="Deep Item")
        sub_item = MenuItem(label="Sub Item", submenu=[sub_sub_item])
        main_item = MenuItem(label="Main Item", submenu=[sub_item])

        assert len(main_item.submenu) == 1
        assert len(main_item.submenu[0].submenu) == 1
        assert main_item.submenu[0].submenu[0].label == "Deep Item"


@pytest.mark.gui
class TestCustomMenubar:
    """Test cases for CustomMenubar class."""

    def test_menubar_initialization(self, root):
        """Test CustomMenubar initialization."""
        menubar = CustomMenubar(root)

        assert isinstance(menubar, tk.Frame)
        assert menubar.parent == root
        assert menubar.winfo_parent() == str(root)

    def test_menubar_with_kwargs(self, root):
        """Test CustomMenubar with Frame kwargs."""
        menubar = CustomMenubar(root, bg="#ffffff", relief="raised")

        assert isinstance(menubar, tk.Frame)

    def test_add_simple_menu(self, root):
        """Test adding a simple menu."""
        menubar = CustomMenubar(root)

        items = [MenuItem(label="New"), MenuItem(label="Open"), MenuItem(label="Save")]

        menubar.add_menu("File", items)

        # Menu should be added
        assert "File" in menubar.menus
        assert len(menubar.menus["File"]) == 3

    def test_add_menu_with_commands(self, root):
        """Test adding menu with commands."""
        menubar = CustomMenubar(root)

        new_command = Mock()
        open_command = Mock()

        items = [
            MenuItem(label="New", command=new_command),
            MenuItem(label="Open", command=open_command),
        ]

        menubar.add_menu("File", items)

        # Commands should be stored
        assert menubar.menus["File"][0].command == new_command
        assert menubar.menus["File"][1].command == open_command

    def test_add_menu_with_separators(self, root):
        """Test adding menu with separators."""
        menubar = CustomMenubar(root)

        items = [
            MenuItem(label="New"),
            MenuItem(label="", separator=True),
            MenuItem(label="Exit"),
        ]

        menubar.add_menu("File", items)

        # Separator should be included
        assert menubar.menus["File"][1].separator is True

    def test_add_menu_with_accelerators(self, root):
        """Test adding menu with accelerators."""
        menubar = CustomMenubar(root)

        items = [
            MenuItem(label="New", accelerator="Ctrl+N"),
            MenuItem(label="Save", accelerator="Ctrl+S"),
        ]

        menubar.add_menu("File", items)

        # Accelerators should be stored
        assert menubar.menus["File"][0].accelerator == "Ctrl+N"
        assert menubar.menus["File"][1].accelerator == "Ctrl+S"

    def test_add_multiple_menus(self, root):
        """Test adding multiple menus."""
        menubar = CustomMenubar(root)

        file_items = [MenuItem(label="New"), MenuItem(label="Open")]
        edit_items = [MenuItem(label="Cut"), MenuItem(label="Copy")]

        menubar.add_menu("File", file_items)
        menubar.add_menu("Edit", edit_items)

        assert "File" in menubar.menus
        assert "Edit" in menubar.menus
        assert len(menubar.menus) == 2

    def test_remove_menu(self, root):
        """Test removing a menu."""
        menubar = CustomMenubar(root)

        items = [MenuItem(label="New")]
        menubar.add_menu("File", items)

        # Menu should exist
        assert "File" in menubar.menus

        # Remove menu
        result = menubar.remove_menu("File")

        assert result is True
        assert "File" not in menubar.menus

    def test_remove_nonexistent_menu(self, root):
        """Test removing non-existent menu."""
        menubar = CustomMenubar(root)

        result = menubar.remove_menu("NonExistent")
        assert result is False

    def test_update_menu(self, root):
        """Test updating an existing menu."""
        menubar = CustomMenubar(root)

        # Add initial menu
        initial_items = [MenuItem(label="Old Item")]
        menubar.add_menu("File", initial_items)

        # Update menu
        new_items = [MenuItem(label="New Item"), MenuItem(label="Another Item")]
        result = menubar.update_menu("File", new_items)

        assert result is True
        assert len(menubar.menus["File"]) == 2
        assert menubar.menus["File"][0].label == "New Item"

    def test_update_nonexistent_menu(self, root):
        """Test updating non-existent menu."""
        menubar = CustomMenubar(root)

        items = [MenuItem(label="Item")]
        result = menubar.update_menu("NonExistent", items)

        assert result is False

    def test_get_menu_names(self, root):
        """Test getting menu names."""
        menubar = CustomMenubar(root)

        # Initially empty
        names = menubar.get_menu_names()
        assert len(names) == 0

        # Add menus
        menubar.add_menu("File", [MenuItem(label="New")])
        menubar.add_menu("Edit", [MenuItem(label="Cut")])

        names = menubar.get_menu_names()
        assert len(names) == 2
        assert "File" in names
        assert "Edit" in names

    def test_clear_all_menus(self, root):
        """Test clearing all menus."""
        menubar = CustomMenubar(root)

        # Add multiple menus
        menubar.add_menu("File", [MenuItem(label="New")])
        menubar.add_menu("Edit", [MenuItem(label="Cut")])
        menubar.add_menu("View", [MenuItem(label="Zoom")])

        assert len(menubar.menus) == 3

        # Clear all
        menubar.clear_all_menus()

        assert len(menubar.menus) == 0

    def test_set_menu_state(self, root):
        """Test setting menu state."""
        menubar = CustomMenubar(root)

        items = [MenuItem(label="New")]
        menubar.add_menu("File", items)

        # Should not raise exception
        result = menubar.set_menu_state("File", "disabled")
        # Result depends on implementation

    def test_set_menu_state_nonexistent(self, root):
        """Test setting state of non-existent menu."""
        menubar = CustomMenubar(root)

        result = menubar.set_menu_state("NonExistent", "disabled")
        assert result is False

    def test_set_item_state(self, root):
        """Test setting item state."""
        menubar = CustomMenubar(root)

        items = [MenuItem(label="New"), MenuItem(label="Open")]
        menubar.add_menu("File", items)

        # Should not raise exception
        result = menubar.set_item_state("File", "New", "disabled")
        # Result depends on implementation

    def test_set_item_state_nonexistent_menu(self, root):
        """Test setting item state for non-existent menu."""
        menubar = CustomMenubar(root)

        result = menubar.set_item_state("NonExistent", "Item", "disabled")
        assert result is False

    def test_set_item_state_nonexistent_item(self, root):
        """Test setting item state for non-existent item."""
        menubar = CustomMenubar(root)

        items = [MenuItem(label="New")]
        menubar.add_menu("File", items)

        result = menubar.set_item_state("File", "NonExistent", "disabled")
        assert result is False

    def test_apply_theme(self, root):
        """Test applying theme to menubar."""
        menubar = CustomMenubar(root)

        theme_colors = {
            "menu_bg": "#ffffff",
            "menu_fg": "#000000",
            "menu_active_bg": "#0078d4",
            "menu_active_fg": "#ffffff",
        }

        # Should not raise exception
        menubar.apply_theme(theme_colors)

    def test_bind_accelerators(self, root):
        """Test binding accelerators."""
        menubar = CustomMenubar(root)

        items = [
            MenuItem(label="New", accelerator="Ctrl+N"),
            MenuItem(label="Save", accelerator="Ctrl+S"),
        ]
        menubar.add_menu("File", items)

        # Should not raise exception
        menubar.bind_accelerators()

    def test_unbind_accelerators(self, root):
        """Test unbinding accelerators."""
        menubar = CustomMenubar(root)

        items = [MenuItem(label="New", accelerator="Ctrl+N")]
        menubar.add_menu("File", items)

        menubar.bind_accelerators()

        # Should not raise exception
        menubar.unbind_accelerators()

    def test_menu_click_handling(self, root):
        """Test menu click handling."""
        menubar = CustomMenubar(root)

        items = [MenuItem(label="New")]
        menubar.add_menu("File", items)

        # Should not raise exception
        menubar.on_menu_click("File")

    def test_menu_enter_handling(self, root):
        """Test menu enter handling."""
        menubar = CustomMenubar(root)

        items = [MenuItem(label="New")]
        menubar.add_menu("File", items)

        # Should not raise exception
        menubar.on_menu_enter("File")

    def test_menu_leave_handling(self, root):
        """Test menu leave handling."""
        menubar = CustomMenubar(root)

        items = [MenuItem(label="New")]
        menubar.add_menu("File", items)

        # Should not raise exception
        menubar.on_menu_leave("File")

    def test_show_dropdown(self, root):
        """Test showing dropdown menu."""
        menubar = CustomMenubar(root)

        items = [MenuItem(label="New"), MenuItem(label="Open")]
        menubar.add_menu("File", items)

        root.update_idletasks()

        # Should not raise exception
        menubar.show_dropdown("File")

    def test_hide_dropdown(self, root):
        """Test hiding dropdown menu."""
        menubar = CustomMenubar(root)

        items = [MenuItem(label="New")]
        menubar.add_menu("File", items)

        # Should not raise exception
        menubar.hide_dropdown()

    def test_menubar_with_submenu(self, root):
        """Test menubar with submenu items."""
        menubar = CustomMenubar(root)

        sub_items = [MenuItem(label="Recent File 1"), MenuItem(label="Recent File 2")]

        items = [
            MenuItem(label="New"),
            MenuItem(label="Recent", submenu=sub_items),
            MenuItem(label="Exit"),
        ]

        menubar.add_menu("File", items)

        # Submenu should be stored
        assert menubar.menus["File"][1].submenu is not None
        assert len(menubar.menus["File"][1].submenu) == 2

    def test_menubar_command_execution(self, root):
        """Test that menu commands can be executed."""
        menubar = CustomMenubar(root)

        command_executed = False

        def test_command():
            nonlocal command_executed
            command_executed = True

        items = [MenuItem(label="Test", command=test_command)]
        menubar.add_menu("Test", items)

        # Execute command directly
        menubar.menus["Test"][0].command()

        assert command_executed

    def test_menubar_layout_management(self, root):
        """Test menubar with different layout managers."""
        menubar = CustomMenubar(root)

        # Test pack
        menubar.pack(fill="x")
        root.update_idletasks()

        menubar.pack_forget()

        # Test grid
        menubar.grid(row=0, column=0, sticky="ew")
        root.update_idletasks()

    def test_menubar_destruction(self, root):
        """Test menubar destruction."""
        menubar = CustomMenubar(root)

        items = [MenuItem(label="Test")]
        menubar.add_menu("Test", items)

        root.update_idletasks()

        # Should not raise exception
        menubar.destroy()

    def test_menubar_with_many_menus(self, root):
        """Test menubar with many menus."""
        menubar = CustomMenubar(root)

        menu_names = ["File", "Edit", "View", "Insert", "Format", "Tools", "Help"]

        for name in menu_names:
            items = [MenuItem(label=f"{name} Item 1"), MenuItem(label=f"{name} Item 2")]
            menubar.add_menu(name, items)

        assert len(menubar.menus) == len(menu_names)

        names = menubar.get_menu_names()
        for name in menu_names:
            assert name in names

    def test_menubar_state_management(self, root):
        """Test menubar state management."""
        menubar = CustomMenubar(root)

        items = [
            MenuItem(label="Always Enabled", state="normal"),
            MenuItem(label="Sometimes Disabled", state="disabled"),
            MenuItem(label="Context Sensitive", state="normal"),
        ]

        menubar.add_menu("Test", items)

        # Test state changes
        menubar.set_item_state("Test", "Context Sensitive", "disabled")
        menubar.set_item_state("Test", "Sometimes Disabled", "normal")

    def test_menubar_error_handling(self, root):
        """Test menubar error handling."""
        menubar = CustomMenubar(root)

        # Test with None items
        try:
            menubar.add_menu("Test", None)
        except Exception:
            pass  # Should handle gracefully

        # Test with empty menu name
        try:
            menubar.add_menu("", [MenuItem(label="Test")])
        except Exception:
            pass  # Should handle gracefully

    def test_menubar_memory_management(self, root):
        """Test menubar memory management."""
        menubars = []

        # Create multiple menubars
        for i in range(5):
            menubar = CustomMenubar(root)
            items = [MenuItem(label=f"Item {j}") for j in range(10)]
            menubar.add_menu(f"Menu{i}", items)
            menubars.append(menubar)

        root.update_idletasks()

        # Clear all menubars
        for menubar in menubars:
            menubar.clear_all_menus()
            menubar.destroy()

    def test_menubar_integration_with_window(self, root):
        """Test menubar integration with main window."""
        menubar = CustomMenubar(root)

        # Pack at top of window
        menubar.pack(side="top", fill="x")

        # Add some menus
        file_items = [
            MenuItem(label="New"),
            MenuItem(label="Open"),
            MenuItem(label="Save"),
        ]
        edit_items = [
            MenuItem(label="Cut"),
            MenuItem(label="Copy"),
            MenuItem(label="Paste"),
        ]

        menubar.add_menu("File", file_items)
        menubar.add_menu("Edit", edit_items)

        # Add other widgets below
        content_frame = tk.Frame(root)
        content_frame.pack(fill="both", expand=True)

        tk.Label(content_frame, text="Main Content Area").pack()

        root.update_idletasks()
