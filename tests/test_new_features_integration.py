"""
Integration tests for new v1.3.0 features.

These tests verify that all new components work together correctly.
"""

import tkinter as tk
from unittest.mock import Mock, patch

import pytest

from threepanewindows import (
    EnhancedFlexibleLayout,
    FlexContainer,
    FlexPaneConfig,
    LayoutDirection,
)
from threepanewindows.central_theme_manager import ThemeType, get_theme_manager
from threepanewindows.custom_menubar import CustomMenubar, MenuItem
from threepanewindows.custom_scrollbar import ThemedScrollbar
from threepanewindows.logging_config import enable_console_logging, get_logger


@pytest.mark.gui
@pytest.mark.integration
class TestFlexibleLayoutIntegration:
    """Integration tests for flexible layout system."""

    def test_flexible_layout_with_central_theme_manager(self, root):
        """Test flexible layout integration with central theme manager."""
        # Set up theme manager
        theme_manager = get_theme_manager()
        theme_manager.set_theme(ThemeType.DARK)

        # Create flexible layout
        def build_pane(frame):
            tk.Label(frame, text="Themed Pane").pack()

        pane_config = FlexPaneConfig(
            name="themed_pane", title="Themed Pane", builder=build_pane
        )

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config, theme_name="dark")
        root.update_idletasks()

        # Should not raise exception and pane should exist
        pane = layout.get_pane("themed_pane")
        assert pane is not None

        # Reset theme
        theme_manager.set_theme(ThemeType.LIGHT)

    def test_flexible_layout_with_custom_scrollbar(self, root):
        """Test flexible layout with custom scrollbar."""

        def build_scrollable_pane(frame):
            text = tk.Text(frame)
            scrollbar = ThemedScrollbar(frame, command=text.yview)

            text.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            text.configure(yscrollcommand=scrollbar.set)

            # Add content
            text.insert("1.0", "Line\n" * 50)

        pane_config = FlexPaneConfig(
            name="scrollable", title="Scrollable Pane", builder=build_scrollable_pane
        )

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)
        root.update_idletasks()

        pane = layout.get_pane("scrollable")
        assert pane is not None

    def test_flexible_layout_with_custom_menubar(self, root):
        """Test flexible layout with custom menubar."""
        # Create custom menubar
        menubar = CustomMenubar(root)
        menubar.pack(side="top", fill="x")

        file_items = [
            MenuItem("New", command=lambda: None),
            MenuItem("Open", command=lambda: None),
        ]
        menubar.add_menu("File", file_items)

        # Create flexible layout below menubar
        def build_content(frame):
            tk.Label(frame, text="Content with menubar").pack()

        pane_config = FlexPaneConfig(
            name="content", title="Content", builder=build_content
        )

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)
        layout.pack(fill="both", expand=True)

        root.update_idletasks()

        # Both components should exist
        assert len(menubar.get_menu_names()) == 1
        assert layout.get_pane("content") is not None

    def test_complex_ide_layout_integration(self, root):
        """Test complex IDE-style layout with all new components."""
        # Set up logging
        enable_console_logging()
        logger = get_logger("test_ide_integration")

        # Set up theme
        theme_manager = get_theme_manager()
        theme_manager.set_theme(ThemeType.BLUE)

        # Create menubar
        menubar = CustomMenubar(root)
        menubar.pack(side="top", fill="x")

        file_items = [
            MenuItem("New", accelerator="Ctrl+N"),
            MenuItem("Open", accelerator="Ctrl+O"),
            MenuItem("", separator=True),
            MenuItem("Exit", command=root.quit),
        ]
        menubar.add_menu("File", file_items)

        # Builder functions
        def build_explorer(frame):
            logger.info("Building file explorer")
            tk.Label(frame, text="📁 File Explorer").pack(pady=5)

            listbox = tk.Listbox(frame)
            scrollbar = ThemedScrollbar(frame, command=listbox.yview)

            listbox.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            listbox.configure(yscrollcommand=scrollbar.set)

            # Add some files
            for i in range(20):
                listbox.insert("end", f"file_{i}.py")

        def build_editor(frame):
            logger.info("Building code editor")
            tk.Label(frame, text="📝 Code Editor").pack(pady=5)

            text = tk.Text(frame, wrap="word")
            v_scrollbar = ThemedScrollbar(frame, orient="vertical", command=text.yview)
            h_scrollbar = ThemedScrollbar(
                frame, orient="horizontal", command=text.xview
            )

            text.grid(row=0, column=0, sticky="nsew")
            v_scrollbar.grid(row=0, column=1, sticky="ns")
            h_scrollbar.grid(row=1, column=0, sticky="ew")

            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

            text.configure(
                yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set
            )

            # Add some code
            text.insert("1.0", "# Welcome to the IDE\nprint('Hello, World!')\n" * 20)

        def build_properties(frame):
            logger.info("Building properties panel")
            tk.Label(frame, text="🔧 Properties").pack(pady=5)

            for prop in ["Width: 800", "Height: 600", "Theme: Blue"]:
                tk.Label(frame, text=prop, anchor="w").pack(fill="x", padx=5)

        def build_console(frame):
            logger.info("Building console")
            tk.Label(frame, text="💻 Console").pack(pady=5)

            console = tk.Text(frame, height=8, bg="black", fg="green")
            console_scrollbar = ThemedScrollbar(frame, command=console.yview)

            console.pack(side="left", fill="both", expand=True)
            console_scrollbar.pack(side="right", fill="y")

            console.configure(yscrollcommand=console_scrollbar.set)
            console.insert("1.0", ">>> Python Console Ready\n")

        # Configure layout
        explorer_config = FlexPaneConfig(
            name="explorer",
            title="File Explorer",
            weight=0.2,
            min_size=200,
            max_size=400,
            builder=build_explorer,
            icon="📁",
        )

        editor_config = FlexPaneConfig(
            name="editor",
            title="Code Editor",
            weight=0.7,
            min_size=400,
            builder=build_editor,
            icon="📝",
        )

        console_config = FlexPaneConfig(
            name="console",
            title="Console",
            weight=0.3,
            min_size=100,
            builder=build_console,
            icon="💻",
        )

        properties_config = FlexPaneConfig(
            name="properties",
            title="Properties",
            weight=0.2,
            min_size=150,
            max_size=300,
            builder=build_properties,
            icon="🔧",
        )

        # Create nested layout
        editor_section = FlexContainer(
            direction=LayoutDirection.VERTICAL,
            children=[editor_config, console_config],
            weight=0.6,
        )

        main_layout = FlexContainer(
            direction=LayoutDirection.HORIZONTAL,
            children=[explorer_config, editor_section, properties_config],
        )

        # Create layout
        layout = EnhancedFlexibleLayout(root, main_layout, theme_name="blue")
        layout.pack(fill="both", expand=True)

        root.update_idletasks()

        # Verify all components exist
        assert len(menubar.get_menu_names()) == 1
        assert layout.get_pane("explorer") is not None
        assert layout.get_pane("editor") is not None
        assert layout.get_pane("console") is not None
        assert layout.get_pane("properties") is not None

        logger.info("IDE layout integration test completed successfully")

        # Reset theme
        theme_manager.set_theme(ThemeType.LIGHT)

    def test_theme_switching_with_all_components(self, root):
        """Test theme switching affects all components."""
        theme_manager = get_theme_manager()

        # Create menubar
        menubar = CustomMenubar(root)
        menubar.pack(side="top", fill="x")
        menubar.add_menu("Test", [MenuItem("Item")])

        # Create flexible layout with scrollbar
        def build_scrollable(frame):
            text = tk.Text(frame)
            scrollbar = ThemedScrollbar(frame, command=text.yview)

            text.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            text.configure(yscrollcommand=scrollbar.set)
            text.insert("1.0", "Test content")

        pane_config = FlexPaneConfig(
            name="test_pane", title="Test Pane", builder=build_scrollable
        )

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config, theme_name="light")
        layout.pack(fill="both", expand=True)

        root.update_idletasks()

        # Switch themes
        for theme in [ThemeType.DARK, ThemeType.BLUE, ThemeType.GREEN]:
            theme_manager.set_theme(theme)
            layout.apply_theme(theme.value)

            # Apply theme to menubar
            colors = theme_manager.current_colors
            menubar.apply_theme(
                {
                    "menu_bg": colors.menu_bg,
                    "menu_fg": colors.menu_fg,
                    "menu_active_bg": colors.menu_active_bg,
                    "menu_active_fg": colors.menu_active_fg,
                }
            )

            root.update_idletasks()

        # Reset
        theme_manager.set_theme(ThemeType.LIGHT)

    def test_logging_integration_across_components(self, root):
        """Test logging integration across all components."""
        enable_console_logging()

        # Get loggers for different components
        flexible_logger = get_logger("threepanewindows.flexible")
        theme_logger = get_logger("threepanewindows.central_theme_manager")
        scrollbar_logger = get_logger("threepanewindows.custom_scrollbar")
        menubar_logger = get_logger("threepanewindows.custom_menubar")

        # Create components and log their creation
        flexible_logger.info("Creating flexible layout")

        def build_logged_pane(frame):
            flexible_logger.info("Building pane content")
            tk.Label(frame, text="Logged Pane").pack()

        pane_config = FlexPaneConfig(
            name="logged_pane", title="Logged Pane", builder=build_logged_pane
        )

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)

        theme_logger.info("Applying theme to layout")
        theme_manager = get_theme_manager()
        theme_manager.set_theme(ThemeType.DARK)

        scrollbar_logger.info("Creating themed scrollbar")
        scrollbar = ThemedScrollbar(root)

        menubar_logger.info("Creating custom menubar")
        menubar = CustomMenubar(root)
        menubar.add_menu("Test", [MenuItem("Test Item")])

        root.update_idletasks()

        # All components should be created successfully
        assert layout.get_pane("logged_pane") is not None
        assert isinstance(scrollbar, ThemedScrollbar)
        assert len(menubar.get_menu_names()) == 1

        # Reset
        theme_manager.set_theme(ThemeType.LIGHT)


@pytest.mark.gui
@pytest.mark.integration
class TestBackwardCompatibilityIntegration:
    """Test that new features don't break existing functionality."""

    def test_existing_layouts_with_central_theme_manager(self, root):
        """Test existing layouts work with central theme manager."""
        from threepanewindows import (
            DockableThreePaneWindow,
            EnhancedDockableThreePaneWindow,
            FixedThreePaneWindow,
            PaneConfig,
        )

        theme_manager = get_theme_manager()
        theme_manager.set_theme(ThemeType.BLUE)

        # Test FixedThreePaneWindow
        fixed_window = FixedThreePaneWindow(root, side_width=200)
        fixed_window.pack(fill="both", expand=True)
        root.update_idletasks()

        fixed_window.destroy()

        # Test DockableThreePaneWindow
        def build_simple(frame):
            tk.Label(frame, text="Simple").pack()

        dockable_window = DockableThreePaneWindow(
            root,
            left_builder=build_simple,
            center_builder=build_simple,
            right_builder=build_simple,
        )
        dockable_window.pack(fill="both", expand=True)
        root.update_idletasks()

        dockable_window.destroy()

        # Test EnhancedDockableThreePaneWindow
        left_config = PaneConfig(title="Left", default_width=200)
        center_config = PaneConfig(title="Center", detachable=False)
        right_config = PaneConfig(title="Right", default_width=200)

        enhanced_window = EnhancedDockableThreePaneWindow(
            root,
            left_config=left_config,
            center_config=center_config,
            right_config=right_config,
            left_builder=build_simple,
            center_builder=build_simple,
            right_builder=build_simple,
            theme_name="blue",
        )
        enhanced_window.pack(fill="both", expand=True)
        root.update_idletasks()

        enhanced_window.destroy()

        # Reset theme
        theme_manager.set_theme(ThemeType.LIGHT)

    def test_existing_theme_manager_compatibility(self, root):
        """Test existing theme manager still works alongside central theme manager."""
        from threepanewindows import ThemeManager
        from threepanewindows import get_theme_manager as get_old_theme_manager

        # Old theme manager should still work
        old_theme_manager = get_old_theme_manager()
        assert isinstance(old_theme_manager, ThemeManager)

        # Central theme manager should also work
        central_theme_manager = get_theme_manager()

        # Both should be able to set themes
        old_theme_manager.set_theme("dark")
        central_theme_manager.set_theme(ThemeType.LIGHT)

    def test_import_compatibility(self):
        """Test that all imports still work."""
        # Test that all existing imports still work
        # Test that new imports work
        from threepanewindows import FixedThreePaneLayout  # Legacy alias
        from threepanewindows import (
            DockableThreePaneWindow,
            EnhancedDockableThreePaneWindow,
            EnhancedFlexibleLayout,
            FixedThreePaneWindow,
            FlexContainer,
            FlexPaneConfig,
            LayoutDirection,
            PaneConfig,
            ThemeManager,
        )
        from threepanewindows import ThemeType as OldThemeType
        from threepanewindows import (
            add_file_logging,
            disable_logging,
            enable_console_logging,
            get_recommended_icon_formats,
        )
        from threepanewindows import get_theme_manager as get_old_theme_manager
        from threepanewindows import set_global_theme, validate_icon_path

        # Test central theme manager imports
        from threepanewindows.central_theme_manager import (
            CentralThemeManager,
            ThemeColors,
            ThemeType,
            get_theme_manager,
        )

        # Test custom component imports
        from threepanewindows.custom_menubar import CustomMenubar, MenuItem
        from threepanewindows.custom_scrollbar import ThemedScrollbar

    def test_version_information(self):
        """Test version information is correct."""
        import threepanewindows

        assert hasattr(threepanewindows, "__version__")
        assert hasattr(threepanewindows, "__version_info__")
        assert hasattr(threepanewindows, "FULL_VERSION")

        # Version should be 1.3.0
        assert threepanewindows.__version__ == "1.3.0"
        assert threepanewindows.__version_info__ == (1, 3, 0)

    def test_all_exports_available(self):
        """Test that all expected exports are available."""
        import threepanewindows

        expected_exports = [
            # Version info
            "__version__",
            "__version_info__",
            "FULL_VERSION",
            # Main window classes
            "FixedThreePaneWindow",
            "FixedThreePaneLayout",
            "DockableThreePaneWindow",
            "EnhancedDockableThreePaneWindow",
            "EnhancedFlexibleLayout",
            # Configuration classes
            "PaneConfig",
            "FlexPaneConfig",
            "FlexContainer",
            "LayoutDirection",
            # Icon utilities
            "get_recommended_icon_formats",
            "validate_icon_path",
            # Theming systems
            "ThemeManager",
            "get_theme_manager",
            "set_global_theme",
            "ThemeType",
            # Logging system
            "enable_console_logging",
            "disable_logging",
            "add_file_logging",
        ]

        for export in expected_exports:
            assert hasattr(threepanewindows, export), f"Missing export: {export}"

        # Check __all__ contains expected items
        assert hasattr(threepanewindows, "__all__")
        for export in expected_exports:
            assert export in threepanewindows.__all__, f"Export {export} not in __all__"


@pytest.mark.integration
class TestPerformanceIntegration:
    """Test performance aspects of new features."""

    def test_theme_manager_singleton_performance(self):
        """Test theme manager singleton performance."""
        import time

        # Multiple calls should be fast (singleton pattern)
        start_time = time.time()

        for _ in range(1000):
            theme_manager = get_theme_manager()

        end_time = time.time()

        # Should be very fast (< 0.1 seconds for 1000 calls)
        assert (end_time - start_time) < 0.1

    def test_logger_creation_performance(self):
        """Test logger creation performance."""
        import time

        enable_console_logging()

        start_time = time.time()

        # Create many loggers
        loggers = []
        for i in range(100):
            logger = get_logger(f"performance_test_{i}")
            loggers.append(logger)

        end_time = time.time()

        # Should be reasonably fast
        assert (end_time - start_time) < 1.0

    def test_flexible_layout_creation_performance(self, root):
        """Test flexible layout creation performance."""
        import time

        def simple_builder(frame):
            tk.Label(frame, text="Test").pack()

        # Create multiple pane configs
        pane_configs = []
        for i in range(10):
            config = FlexPaneConfig(
                name=f"pane_{i}", title=f"Pane {i}", builder=simple_builder
            )
            pane_configs.append(config)

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=pane_configs
        )

        start_time = time.time()

        layout = EnhancedFlexibleLayout(root, layout_config)
        root.update_idletasks()

        end_time = time.time()

        # Should create layout reasonably quickly
        assert (end_time - start_time) < 2.0

        # All panes should exist
        for i in range(10):
            assert layout.get_pane(f"pane_{i}") is not None

    @pytest.mark.gui
    def test_memory_usage_stability(self, root):
        """Test memory usage doesn't grow excessively."""
        import gc

        # Force garbage collection
        gc.collect()

        # Create and destroy components multiple times
        for iteration in range(10):
            # Create flexible layout
            pane_config = FlexPaneConfig(
                name=f"test_{iteration}",
                title=f"Test {iteration}",
                builder=lambda frame: tk.Label(frame, text="Test").pack(),
            )

            layout_config = FlexContainer(
                direction=LayoutDirection.HORIZONTAL, children=[pane_config]
            )

            layout = EnhancedFlexibleLayout(root, layout_config)

            # Create other components
            scrollbar = ThemedScrollbar(root)
            menubar = CustomMenubar(root)
            menubar.add_menu("Test", [MenuItem("Item")])

            root.update_idletasks()

            # Destroy components
            layout.destroy()
            scrollbar.destroy()
            menubar.destroy()

            # Force garbage collection
            gc.collect()

        # Test should complete without memory errors
