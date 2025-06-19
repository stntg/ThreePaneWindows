"""Pytest configuration and fixtures for ThreePaneWindows tests."""

import pytest
import tkinter as tk
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Check if Tkinter is available at import time
try:
    import tkinter as tk
    _tkinter_available = True
except ImportError:
    _tkinter_available = False


def _create_tkinter_root():
    """Helper function to create a Tkinter root with proper error handling."""
    if not _tkinter_available:
        pytest.skip("Tkinter not available")
    
    try:
        root = tk.Tk()
        return root
    except tk.TclError as e:
        error_msg = str(e).lower()
        if any(keyword in error_msg for keyword in [
            "tcl_findlibrary", 
            "no display", 
            "couldn't connect to display",
            "invalid command name",
            "application-specific initialization failed",
            "can't find a usable init.tcl",
            "couldn't read file",
            "tcl wasn't installed properly"
        ]):
            pytest.skip(f"Tkinter/Tcl environment not available: {e}")
        else:
            raise
    except Exception as e:
        pytest.skip(f"Failed to initialize Tkinter: {e}")


@pytest.fixture
def root():
    """Create a Tkinter root window for testing."""
    root = _create_tkinter_root()
    root.withdraw()  # Hide the window during tests
    yield root
    try:
        root.destroy()
    except tk.TclError:
        pass  # Window already destroyed


@pytest.fixture
def visible_root():
    """Create a visible Tkinter root window for visual tests."""
    root = _create_tkinter_root()
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
    config.addinivalue_line(
        "markers", "gui: mark test as requiring GUI/Tkinter"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to handle GUI tests."""
    if not _tkinter_available:
        skip_gui = pytest.mark.skip(reason="Tkinter not available")
        for item in items:
            if "gui" in item.keywords or any(fixture in item.fixturenames for fixture in ["root", "visible_root"]):
                item.add_marker(skip_gui)