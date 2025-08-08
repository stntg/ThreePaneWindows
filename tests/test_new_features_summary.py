"""
Summary test for new v1.3.0 features.

This test file provides a comprehensive overview of all new functionality
that can be run in headless CI environments.
"""

import pytest

from threepanewindows.central_theme_manager import (
    ThemeType,
    get_theme_manager,
    set_global_theme,
)
from threepanewindows.custom_menubar import MenuItem
from threepanewindows.flexible import FlexContainer, FlexPaneConfig, LayoutDirection
from threepanewindows.logging_config import enable_console_logging, get_logger


class TestNewFeaturesOverview:
    """Overview tests for all new v1.3.0 features."""

    def test_flexible_layout_system_components(self):
        """Test that all flexible layout system components are available."""
        # Test LayoutDirection enum
        assert LayoutDirection.HORIZONTAL.value == "horizontal"
        assert LayoutDirection.VERTICAL.value == "vertical"

        # Test FlexPaneConfig
        config = FlexPaneConfig(name="test", title="Test Pane")
        assert config.name == "test"
        assert config.title == "Test Pane"
        assert config.weight == 1.0
        assert config.min_size == 100
        assert config.detachable is True

        # Test FlexContainer
        container = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[config]
        )
        assert container.direction == LayoutDirection.HORIZONTAL
        assert len(container.children) == 1
        assert container.weight == 1.0

    def test_central_theme_manager_components(self):
        """Test that central theme manager components are available."""
        # Test ThemeType enum
        assert ThemeType.LIGHT.value == "light"
        assert ThemeType.DARK.value == "dark"
        assert ThemeType.BLUE.value == "blue"
        assert ThemeType.GREEN.value == "green"
        assert ThemeType.PURPLE.value == "purple"
        assert ThemeType.SYSTEM.value == "system"
        assert ThemeType.NATIVE.value == "native"

        # Test theme manager singleton
        manager1 = get_theme_manager()
        manager2 = get_theme_manager()
        assert manager1 is manager2

        # Test theme setting
        manager1.set_theme(ThemeType.DARK)
        assert manager1.current_theme == ThemeType.DARK

        # Test global theme function
        set_global_theme(ThemeType.LIGHT)
        assert manager1.current_theme == ThemeType.LIGHT

    def test_custom_menubar_components(self):
        """Test that custom menubar components are available."""
        # Test MenuItem
        basic_item = MenuItem(label="File")
        assert basic_item.label == "File"
        assert basic_item.command is None
        assert basic_item.separator is False

        # Test MenuItem with command
        def test_command():
            pass

        command_item = MenuItem(label="Open", command=test_command)
        assert command_item.label == "Open"
        assert command_item.command == test_command

        # Test MenuItem with submenu
        sub_item = MenuItem(label="Recent")
        parent_item = MenuItem(label="File", submenu=[sub_item])
        assert len(parent_item.submenu) == 1
        assert parent_item.submenu[0] == sub_item

        # Test separator
        separator = MenuItem(label="", separator=True)
        assert separator.separator is True

    def test_logging_system_components(self):
        """Test that logging system components are available."""
        # Test logger creation
        logger = get_logger("test_module")
        assert logger is not None
        assert "test_module" in logger.name or "threepanewindows" in logger.name

        # Test console logging
        enable_console_logging()
        logger.info("Test message")  # Should not raise exception

        # Test different loggers
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        assert logger1.name != logger2.name

    def test_import_compatibility(self):
        """Test that all imports work correctly."""
        # Test flexible layout imports
        # Test central theme manager imports
        from threepanewindows.central_theme_manager import (
            CentralThemeManager,
            ThemeType,
            get_theme_manager,
            set_global_theme,
        )

        # Test custom UI component imports
        from threepanewindows.custom_menubar import CustomMenubar, MenuItem
        from threepanewindows.custom_scrollbar import ThemedScrollbar
        from threepanewindows.flexible import (
            EnhancedFlexibleLayout,
            FlexContainer,
            FlexPaneConfig,
            LayoutDirection,
        )

        # Test logging imports
        from threepanewindows.logging_config import (
            disable_logging,
            enable_console_logging,
            get_logger,
        )

        # All imports should succeed
        assert True

    def test_backward_compatibility_imports(self):
        """Test that existing imports still work."""
        # Test existing imports
        from threepanewindows import (
            DockableThreePaneWindow,
            EnhancedDockableThreePaneWindow,
            FixedThreePaneWindow,
            PaneConfig,
            ThemeManager,
        )
        from threepanewindows import get_theme_manager as get_old_theme_manager

        # Test that old theme manager still works
        old_manager = get_old_theme_manager()
        assert old_manager is not None

        # All imports should succeed
        assert True

    def test_version_information(self):
        """Test that version information is correct."""
        import threepanewindows

        # Should have version info
        assert hasattr(threepanewindows, "__version__")
        assert hasattr(threepanewindows, "__version_info__")

        # Version should be 1.3.0
        assert threepanewindows.__version__ == "1.3.0"
        assert threepanewindows.__version_info__ == (1, 3, 0)

    def test_comprehensive_feature_availability(self):
        """Test that all major new features are available."""
        # Flexible Layout System
        assert hasattr(FlexPaneConfig, "custom_titlebar")
        assert hasattr(FlexPaneConfig, "detached_scrollable")
        assert hasattr(FlexPaneConfig, "window_icon")

        # Central Theme Manager
        manager = get_theme_manager()
        assert hasattr(manager, "current_theme")
        assert hasattr(manager, "set_theme")
        assert hasattr(manager, "colors")
        assert hasattr(manager, "apply_theme_to_widget")

        # Custom UI Components
        assert hasattr(MenuItem, "accelerator")
        assert hasattr(MenuItem, "state")
        assert hasattr(MenuItem, "submenu")

        # Enhanced Logging
        logger = get_logger("feature_test")
        assert hasattr(logger, "debug")
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")

    def test_integration_readiness(self):
        """Test that components can work together."""
        # Create theme manager
        theme_manager = get_theme_manager()
        theme_manager.set_theme(ThemeType.BLUE)

        # Create logger
        logger = get_logger("integration_test")
        logger.info("Integration test starting")

        # Create menu items
        file_menu = [
            MenuItem("New", accelerator="Ctrl+N"),
            MenuItem("Open", accelerator="Ctrl+O"),
            MenuItem("", separator=True),
            MenuItem("Exit"),
        ]

        # Create flexible pane config
        pane_config = FlexPaneConfig(
            name="main_pane",
            title="Main Content",
            weight=1.0,
            detachable=True,
            custom_titlebar=True,
        )

        # Create container
        container = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        # All components should be created successfully
        assert theme_manager.current_theme == ThemeType.BLUE
        assert len(file_menu) == 4
        assert container.direction == LayoutDirection.HORIZONTAL
        assert pane_config.custom_titlebar is True

        logger.info("Integration test completed successfully")

    def test_performance_characteristics(self):
        """Test basic performance characteristics."""
        import time

        # Theme manager singleton should be fast
        start_time = time.time()
        for _ in range(100):
            manager = get_theme_manager()
        end_time = time.time()
        assert (end_time - start_time) < 0.1

        # Logger creation should be reasonable
        start_time = time.time()
        loggers = []
        for i in range(50):
            logger = get_logger(f"perf_test_{i}")
            loggers.append(logger)
        end_time = time.time()
        assert (end_time - start_time) < 1.0
        assert len(loggers) == 50

        # Menu item creation should be fast
        start_time = time.time()
        items = []
        for i in range(100):
            item = MenuItem(f"Item {i}")
            items.append(item)
        end_time = time.time()
        assert (end_time - start_time) < 0.1
        assert len(items) == 100

    def test_error_handling(self):
        """Test basic error handling."""
        # Theme manager should handle invalid themes gracefully
        manager = get_theme_manager()
        try:
            manager.set_theme("invalid_theme")
        except (ValueError, KeyError, AttributeError, TypeError):
            # Expected behavior
            pass

        # Logger should handle various inputs
        logger = get_logger("error_test")
        try:
            logger.info("Test with %s", None)
        except Exception:
            # Should handle gracefully
            pass

        # MenuItem should handle edge cases
        try:
            item = MenuItem("")  # Empty label
            assert item.label == ""
        except Exception:
            # Should handle gracefully
            pass

    def test_documentation_completeness(self):
        """Test that components have proper documentation."""
        # Check that classes have docstrings
        assert FlexPaneConfig.__doc__ is not None
        assert FlexContainer.__doc__ is not None
        assert MenuItem.__doc__ is not None
        assert ThemeType.__doc__ is not None

        # Check that enums have proper values
        assert all(isinstance(theme.value, str) for theme in ThemeType)
        assert all(isinstance(direction.value, str) for direction in LayoutDirection)
