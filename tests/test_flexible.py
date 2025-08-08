"""
Tests for the Enhanced Flexible Layout System.
"""

import tkinter as tk
from unittest.mock import Mock, patch

import pytest

from threepanewindows.flexible import (
    EnhancedFlexibleLayout,
    FlexContainer,
    FlexPaneConfig,
    LayoutDirection,
)


class TestLayoutDirection:
    """Test cases for LayoutDirection enum."""

    def test_layout_direction_values(self):
        """Test LayoutDirection enum values."""
        assert LayoutDirection.HORIZONTAL.value == "horizontal"
        assert LayoutDirection.VERTICAL.value == "vertical"

    def test_layout_direction_members(self):
        """Test LayoutDirection enum members."""
        assert len(LayoutDirection) == 2
        assert LayoutDirection.HORIZONTAL in LayoutDirection
        assert LayoutDirection.VERTICAL in LayoutDirection


class TestFlexPaneConfig:
    """Test cases for FlexPaneConfig dataclass."""

    def test_default_flex_pane_config(self):
        """Test FlexPaneConfig with default values."""
        config = FlexPaneConfig(name="test", title="Test Pane")

        assert config.name == "test"
        assert config.title == "Test Pane"
        assert config.weight == 1.0
        assert config.min_size == 100
        assert config.max_size is None
        assert config.detachable is True
        assert config.fill_detached_space is True
        assert config.builder is None

        # Enhanced detached window properties
        assert config.custom_titlebar is True
        assert config.default_width == 500
        assert config.detached_height == 400
        assert config.min_width == 300
        assert config.max_width == 0
        assert config.detached_scrollable is False
        assert config.window_icon == ""
        assert config.icon == ""

    def test_custom_flex_pane_config(self):
        """Test FlexPaneConfig with custom values."""

        def mock_builder(frame):
            pass

        config = FlexPaneConfig(
            name="custom",
            title="Custom Pane",
            weight=0.5,
            min_size=200,
            max_size=800,
            detachable=False,
            fill_detached_space=False,
            builder=mock_builder,
            custom_titlebar=False,
            default_width=600,
            detached_height=500,
            min_width=400,
            max_width=1000,
            detached_scrollable=True,
            window_icon="test.ico",
            icon="📁",
        )

        assert config.name == "custom"
        assert config.title == "Custom Pane"
        assert config.weight == 0.5
        assert config.min_size == 200
        assert config.max_size == 800
        assert config.detachable is False
        assert config.fill_detached_space is False
        assert config.builder == mock_builder
        assert config.custom_titlebar is False
        assert config.default_width == 600
        assert config.detached_height == 500
        assert config.min_width == 400
        assert config.max_width == 1000
        assert config.detached_scrollable is True
        assert config.window_icon == "test.ico"
        assert config.icon == "📁"


class TestFlexContainer:
    """Test cases for FlexContainer dataclass."""

    def test_default_flex_container(self):
        """Test FlexContainer with default values."""
        pane_config = FlexPaneConfig(name="test", title="Test")
        container = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        assert container.direction == LayoutDirection.HORIZONTAL
        assert len(container.children) == 1
        assert container.children[0] == pane_config
        assert container.weight == 1.0

    def test_custom_flex_container(self):
        """Test FlexContainer with custom values."""
        pane1 = FlexPaneConfig(name="pane1", title="Pane 1")
        pane2 = FlexPaneConfig(name="pane2", title="Pane 2")

        container = FlexContainer(
            direction=LayoutDirection.VERTICAL, children=[pane1, pane2], weight=0.8
        )

        assert container.direction == LayoutDirection.VERTICAL
        assert len(container.children) == 2
        assert container.children[0] == pane1
        assert container.children[1] == pane2
        assert container.weight == 0.8

    def test_nested_flex_container(self):
        """Test nested FlexContainer structure."""
        pane1 = FlexPaneConfig(name="pane1", title="Pane 1")
        pane2 = FlexPaneConfig(name="pane2", title="Pane 2")
        pane3 = FlexPaneConfig(name="pane3", title="Pane 3")

        # Create nested container
        inner_container = FlexContainer(
            direction=LayoutDirection.VERTICAL, children=[pane2, pane3]
        )

        outer_container = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane1, inner_container]
        )

        assert len(outer_container.children) == 2
        assert outer_container.children[0] == pane1
        assert isinstance(outer_container.children[1], FlexContainer)
        assert len(outer_container.children[1].children) == 2


@pytest.mark.gui
class TestEnhancedFlexibleLayout:
    """Test cases for EnhancedFlexibleLayout class."""

    def test_initialization(self, root):
        """Test EnhancedFlexibleLayout initialization."""

        def build_pane(frame):
            tk.Label(frame, text="Test").pack()

        pane_config = FlexPaneConfig(
            name="test_pane", title="Test Pane", builder=build_pane
        )

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)

        assert isinstance(layout, tk.Frame)
        assert layout.winfo_parent() == str(root)

    def test_initialization_with_theme(self, root):
        """Test EnhancedFlexibleLayout initialization with theme."""
        pane_config = FlexPaneConfig(name="test", title="Test")
        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config, theme_name="dark")

        assert isinstance(layout, tk.Frame)

    def test_get_pane(self, root):
        """Test getting pane by name."""

        def build_pane(frame):
            tk.Label(frame, text="Test").pack()

        pane_config = FlexPaneConfig(
            name="test_pane", title="Test Pane", builder=build_pane
        )

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)
        root.update_idletasks()

        pane = layout.get_pane("test_pane")
        assert pane is not None
        assert isinstance(pane, tk.Frame)

    def test_get_nonexistent_pane(self, root):
        """Test getting non-existent pane returns None."""
        pane_config = FlexPaneConfig(name="test", title="Test")
        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)

        pane = layout.get_pane("nonexistent")
        assert pane is None

    def test_multiple_panes(self, root):
        """Test layout with multiple panes."""

        def build_left(frame):
            tk.Label(frame, text="Left").pack()

        def build_center(frame):
            tk.Text(frame).pack(fill="both", expand=True)

        def build_right(frame):
            tk.Label(frame, text="Right").pack()

        left_config = FlexPaneConfig(
            name="left", title="Left Pane", weight=0.2, builder=build_left
        )

        center_config = FlexPaneConfig(
            name="center", title="Center Pane", weight=0.6, builder=build_center
        )

        right_config = FlexPaneConfig(
            name="right", title="Right Pane", weight=0.2, builder=build_right
        )

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL,
            children=[left_config, center_config, right_config],
        )

        layout = EnhancedFlexibleLayout(root, layout_config)
        root.update_idletasks()

        # Test all panes exist
        assert layout.get_pane("left") is not None
        assert layout.get_pane("center") is not None
        assert layout.get_pane("right") is not None

    def test_vertical_layout(self, root):
        """Test vertical layout direction."""
        top_config = FlexPaneConfig(name="top", title="Top", weight=0.3)
        bottom_config = FlexPaneConfig(name="bottom", title="Bottom", weight=0.7)

        layout_config = FlexContainer(
            direction=LayoutDirection.VERTICAL, children=[top_config, bottom_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)
        root.update_idletasks()

        assert layout.get_pane("top") is not None
        assert layout.get_pane("bottom") is not None

    def test_nested_layout(self, root):
        """Test nested container layout."""
        left_config = FlexPaneConfig(name="left", title="Left")
        top_right_config = FlexPaneConfig(name="top_right", title="Top Right")
        bottom_right_config = FlexPaneConfig(name="bottom_right", title="Bottom Right")

        # Create nested right section
        right_section = FlexContainer(
            direction=LayoutDirection.VERTICAL,
            children=[top_right_config, bottom_right_config],
        )

        # Main horizontal layout
        main_layout = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[left_config, right_section]
        )

        layout = EnhancedFlexibleLayout(root, main_layout)
        root.update_idletasks()

        # Test all panes exist
        assert layout.get_pane("left") is not None
        assert layout.get_pane("top_right") is not None
        assert layout.get_pane("bottom_right") is not None

    def test_pane_config_access(self, root):
        """Test getting pane configuration."""
        pane_config = FlexPaneConfig(
            name="test", title="Test Pane", weight=0.5, min_size=200
        )

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)

        retrieved_config = layout.get_pane_config("test")
        assert retrieved_config is not None
        assert retrieved_config.name == "test"
        assert retrieved_config.title == "Test Pane"
        assert retrieved_config.weight == 0.5
        assert retrieved_config.min_size == 200

    def test_nonexistent_pane_config(self, root):
        """Test getting config for non-existent pane."""
        pane_config = FlexPaneConfig(name="test", title="Test")
        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)

        config = layout.get_pane_config("nonexistent")
        assert config is None

    def test_layout_info(self, root):
        """Test getting layout information."""
        pane_config = FlexPaneConfig(name="test", title="Test")
        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)

        info = layout.get_layout_info()
        assert isinstance(info, dict)
        assert "panes" in info or "layout" in info  # Should contain layout information

    def test_apply_theme(self, root):
        """Test applying theme to layout."""
        pane_config = FlexPaneConfig(name="test", title="Test")
        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)

        # Should not raise exception
        layout.apply_theme("dark")
        layout.apply_theme("light")

    def test_detach_functionality_exists(self, root):
        """Test that detach methods exist (functionality tested in integration)."""
        pane_config = FlexPaneConfig(name="test", title="Test", detachable=True)
        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)

        # Methods should exist
        assert hasattr(layout, "detach_pane")
        assert hasattr(layout, "reattach_pane")
        assert hasattr(layout, "is_pane_detached")
        assert hasattr(layout, "get_detached_windows")
        assert hasattr(layout, "close_all_detached")

    def test_state_management_methods_exist(self, root):
        """Test that state management methods exist."""
        pane_config = FlexPaneConfig(name="test", title="Test")
        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)

        # Methods should exist
        assert hasattr(layout, "save_layout_state")
        assert hasattr(layout, "restore_layout_state")

    def test_update_pane_config_method_exists(self, root):
        """Test that update pane config method exists."""
        pane_config = FlexPaneConfig(name="test", title="Test")
        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)

        # Method should exist
        assert hasattr(layout, "update_pane_config")

    def test_empty_layout_handling(self, root):
        """Test handling of empty layout."""
        layout_config = FlexContainer(direction=LayoutDirection.HORIZONTAL, children=[])

        # Should not raise exception
        layout = EnhancedFlexibleLayout(root, layout_config)
        assert isinstance(layout, tk.Frame)

    def test_single_pane_layout(self, root):
        """Test layout with single pane."""

        def build_single(frame):
            tk.Label(frame, text="Single Pane").pack()

        pane_config = FlexPaneConfig(
            name="single", title="Single Pane", builder=build_single
        )

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)
        root.update_idletasks()

        pane = layout.get_pane("single")
        assert pane is not None

    def test_weight_distribution_setup(self, root):
        """Test that panes with different weights are set up correctly."""
        light_config = FlexPaneConfig(name="light", title="Light", weight=0.2)
        heavy_config = FlexPaneConfig(name="heavy", title="Heavy", weight=0.8)

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[light_config, heavy_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)
        root.update_idletasks()

        # Both panes should exist
        assert layout.get_pane("light") is not None
        assert layout.get_pane("heavy") is not None

    def test_constraint_setup(self, root):
        """Test that panes with constraints are set up correctly."""
        constrained_config = FlexPaneConfig(
            name="constrained", title="Constrained", min_size=200, max_size=600
        )

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[constrained_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)
        root.update_idletasks()

        pane = layout.get_pane("constrained")
        assert pane is not None

    @patch("threepanewindows.flexible.get_logger")
    def test_logging_integration(self, mock_get_logger, root):
        """Test that logging is properly integrated."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        pane_config = FlexPaneConfig(name="test", title="Test")
        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)

        # Logger should have been requested
        mock_get_logger.assert_called()

    def test_builder_function_execution(self, root):
        """Test that builder functions are executed."""
        builder_called = False

        def test_builder(frame):
            nonlocal builder_called
            builder_called = True
            tk.Label(frame, text="Built").pack()

        pane_config = FlexPaneConfig(name="test", title="Test", builder=test_builder)

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)
        root.update_idletasks()

        # Builder should have been called
        assert builder_called

    def test_multiple_builder_functions(self, root):
        """Test multiple builder functions are executed."""
        builders_called = []

        def builder1(frame):
            builders_called.append("builder1")
            tk.Label(frame, text="Pane 1").pack()

        def builder2(frame):
            builders_called.append("builder2")
            tk.Label(frame, text="Pane 2").pack()

        pane1_config = FlexPaneConfig(name="pane1", title="Pane 1", builder=builder1)
        pane2_config = FlexPaneConfig(name="pane2", title="Pane 2", builder=builder2)

        layout_config = FlexContainer(
            direction=LayoutDirection.HORIZONTAL, children=[pane1_config, pane2_config]
        )

        layout = EnhancedFlexibleLayout(root, layout_config)
        root.update_idletasks()

        # Both builders should have been called
        assert "builder1" in builders_called
        assert "builder2" in builders_called
