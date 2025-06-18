"""Pytest configuration and fixtures for ThreePaneWindows tests."""

import pytest
import tkinter as tk
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def root():
    """Create a Tkinter root window for testing."""
    root = tk.Tk()
    root.withdraw()  # Hide the window during tests
    yield root
    try:
        root.destroy()
    except tk.TclError:
        pass  # Window already destroyed


@pytest.fixture
def visible_root():
    """Create a visible Tkinter root window for visual tests."""
    root = tk.Tk()
    root.geometry("800x600")
    yield root
    try:
        root.destroy()
    except tk.TclError:
        pass  # Window already destroyed


class MockEvent:
    """Mock event object for testing event handlers."""
    
    def __init__(self, x=0, y=0, widget=None, **kwargs):
        self.x = x
        self.y = y
        self.widget = widget
        for key, value in kwargs.items():
            setattr(self, key, value)


@pytest.fixture
def mock_event():
    """Create a mock event object."""
    return MockEvent


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "visual: mark test as requiring visual inspection"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )