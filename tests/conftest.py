"""Pytest configuration and fixtures for ThreePaneWindows tests."""

import os
import sys
import tkinter as tk

import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

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

    # Add retry logic for resource contention issues
    max_retries = 3
    for attempt in range(max_retries):
        try:
            root = tk.Tk()
            # Force update to ensure proper initialization
            root.update_idletasks()
            return root
        except tk.TclError as e:
            error_msg = str(e).lower()

            # Check for temporary resource issues that might resolve with retry
            temporary_issues = [
                "invalid command name",
                "application-specific initialization failed",
            ]

            # Check for permanent environment issues
            permanent_issues = [
                "tcl_findlibrary",
                "no display",
                "couldn't connect to display",
                "can't find a usable init.tcl",
                "couldn't read file",
                "tcl wasn't installed properly",
            ]

            if any(keyword in error_msg for keyword in permanent_issues):
                pytest.skip(f"Tkinter/Tcl environment not available: {e}")
            elif (
                any(keyword in error_msg for keyword in temporary_issues)
                and attempt < max_retries - 1
            ):
                # Wait a bit and retry for temporary issues
                import time

                time.sleep(0.1 * (attempt + 1))  # Progressive backoff
                continue
            elif attempt == max_retries - 1:
                # Last attempt failed, skip the test
                pytest.skip(
                    f"Tkinter initialization failed after {max_retries} attempts: {e}"
                )
            else:
                raise
        except Exception as e:
            if attempt == max_retries - 1:
                pytest.skip(
                    f"Failed to initialize Tkinter after {max_retries} attempts: {e}"
                )
            else:
                import time

                time.sleep(0.1 * (attempt + 1))
                continue


@pytest.fixture
def root():
    """Create a Tkinter root window for testing."""
    root = _create_tkinter_root()
    root.withdraw()  # Hide the window during tests
    yield root
    try:
        # Ensure all child windows are destroyed first
        for child in root.winfo_children():
            try:
                if hasattr(child, "destroy"):
                    child.destroy()
            except tk.TclError:
                pass

        # Force update before destroying root
        root.update_idletasks()
        root.destroy()

        # Small delay to allow cleanup
        import time

        time.sleep(0.01)
    except tk.TclError:
        pass  # Window already destroyed


@pytest.fixture
def visible_root():
    """Create a visible Tkinter root window for visual tests."""
    root = _create_tkinter_root()
    root.geometry("800x600")
    yield root
    try:
        # Ensure all child windows are destroyed first
        for child in root.winfo_children():
            try:
                if hasattr(child, "destroy"):
                    child.destroy()
            except tk.TclError:
                pass

        # Force update before destroying root
        root.update_idletasks()
        root.destroy()

        # Small delay to allow cleanup
        import time

        time.sleep(0.01)
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
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "gui: mark test as requiring GUI/Tkinter")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to handle GUI tests."""
    if not _tkinter_available:
        skip_gui = pytest.mark.skip(reason="Tkinter not available")
        for item in items:
            if "gui" in item.keywords or any(
                fixture in item.fixturenames for fixture in ["root", "visible_root"]
            ):
                item.add_marker(skip_gui)
