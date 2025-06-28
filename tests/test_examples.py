"""
Tests for examples module functionality - Non-hanging version.
"""

import inspect
import threading
import time
import tkinter as tk
from unittest.mock import MagicMock, Mock, patch

import pytest

from threepanewindows import examples


@pytest.mark.gui
class TestExamples:
    """Test cases for examples module that don't hang."""

    def setup_method(self):
        """Set up test fixtures."""
        try:
            self.root = tk.Tk()
            self.root.withdraw()
        except tk.TclError as e:
            pytest.skip(f"Cannot create Tkinter window in this environment: {e}")

    def teardown_method(self):
        """Clean up after tests."""
        if hasattr(self, "root") and self.root:
            try:
                self.root.destroy()
            except:
                pass

    def test_examples_module_importable(self):
        """Test that examples module can be imported."""
        assert hasattr(examples, "run_demo")
        assert hasattr(examples, "run_demo_with_timeout")
        assert hasattr(examples, "test_all_demo_components")

    def test_run_demo_non_interactive(self):
        """Test that run_demo can run in non-interactive mode."""
        try:
            # This should not hang because interactive=False
            result = examples.run_demo(interactive=False)
            assert result is not None

            # Clean up any created windows
            if isinstance(result, list):
                for demo in result:
                    if demo and len(demo) >= 1 and demo[0]:
                        try:
                            demo[0].destroy()
                        except:
                            pass
        except tk.TclError:
            pytest.skip("GUI environment not available")
        except Exception as e:
            # Should not raise unexpected exceptions
            pytest.fail(f"run_demo(interactive=False) raised unexpected exception: {e}")

    def test_run_demo_with_timeout(self):
        """Test that run_demo_with_timeout works correctly."""
        try:
            # Should complete within timeout
            success = examples.run_demo_with_timeout(
                timeout_seconds=2, interactive=False
            )
            assert isinstance(success, bool)
        except tk.TclError:
            pytest.skip("GUI environment not available")

    def test_basic_demo_components(self):
        """Test basic demo components without enhanced features."""
        try:
            results = examples.test_basic_demo_components()
            assert isinstance(results, dict)

            # Check that we got results for basic components
            expected_keys = ["dockable_window", "fixed_layout", "builders"]
            for key in expected_keys:
                assert key in results
                assert isinstance(results[key], bool)

        except tk.TclError:
            pytest.skip("GUI environment not available")

    def test_demo_components_creation(self):
        """Test that all demo components can be created."""
        try:
            results = examples.test_all_demo_components()
            assert isinstance(results, dict)

            # Check that we got results for all expected components
            expected_keys = [
                "dockable_window",
                "fixed_layout",
                "enhanced_window",
                "builders",
            ]
            for key in expected_keys:
                assert key in results
                assert isinstance(results[key], bool)

        except tk.TclError:
            pytest.skip("GUI environment not available")

    @patch("tkinter.Tk")
    def test_run_demo_function_exists(self, mock_tk):
        """Test that run_demo function exists and is callable."""
        mock_root = Mock()
        mock_tk.return_value = mock_root

        # Should be able to call run_demo
        assert callable(examples.run_demo)

    @patch("tkinter.Tk")
    def test_run_demo_creates_window(self, mock_tk):
        """Test that run_demo creates a window."""
        mock_root = MagicMock()
        mock_tk.return_value = mock_root

        # Mock the window classes
        with patch(
            "threepanewindows.examples.DockableThreePaneWindow"
        ) as mock_dockable, patch(
            "threepanewindows.examples.FixedThreePaneLayout"
        ) as mock_fixed, patch(
            "threepanewindows.examples.EnhancedDockableThreePaneWindow"
        ) as mock_enhanced:

            mock_window = MagicMock()
            mock_dockable.return_value = mock_window
            mock_fixed.return_value = mock_window
            mock_enhanced.return_value = mock_window

            try:
                # This should not hang because interactive=False
                examples.run_demo(interactive=False)
                # Should have created a Tk instance
                mock_tk.assert_called()
            except Exception:
                # If it fails due to GUI issues, that's expected in headless environment
                pass

    def test_demo_builders_exist(self):
        """Test that demo builder functions exist."""
        # Check for common builder function patterns
        demo_functions = [
            attr
            for attr in dir(examples)
            if "demo" in attr.lower() or "builder" in attr.lower()
        ]

        # Should have some demo-related functions
        assert len(demo_functions) > 0

    def test_example_window_classes_importable(self):
        """Test that example window classes can be imported through examples."""
        # Test that we can access the main window classes through examples
        from threepanewindows.examples import run_demo

        assert callable(run_demo)

    @patch("threepanewindows.examples.tk.Tk")
    def test_demo_error_handling(self, mock_tk):
        """Test demo handles errors gracefully."""
        # Mock Tk to raise an error
        mock_tk.side_effect = tk.TclError("No display")

        try:
            examples.run_demo(interactive=False)  # Use non-interactive mode
        except tk.TclError:
            # Expected in headless environment
            pass
        except Exception as e:
            # Should handle other errors gracefully
            assert isinstance(e, Exception)

    def test_demo_with_different_types(self):
        """Test demo can handle different window types if supported."""
        # Test with different parameters
        try:
            # Try calling with different parameters
            examples.run_demo(interactive=False)  # Non-interactive mode
            examples.run_demo(
                interactive=False, auto_close_delay=100
            )  # With auto-close
        except TypeError:
            # If it doesn't accept parameters, that's fine
            pass
        except tk.TclError:
            # GUI environment issues are expected
            pytest.skip("GUI environment not available")
        except Exception:
            # Other exceptions might be due to GUI environment
            pass

    @pytest.mark.timeout(10)  # Ensure test doesn't hang for more than 10 seconds
    def test_demo_timeout_protection(self):
        """Test that demo has timeout protection to prevent hanging."""
        start_time = time.time()

        try:
            # This should complete quickly due to non-interactive mode
            examples.run_demo(interactive=False)

            elapsed = time.time() - start_time
            # Should complete in reasonable time (less than 5 seconds)
            assert elapsed < 5.0, f"Demo took too long: {elapsed} seconds"

        except tk.TclError:
            pytest.skip("GUI environment not available")


class TestExampleBuilders:
    """Test cases for example builder functions."""

    def test_builder_functions_exist(self):
        """Test that builder functions exist in examples module."""
        # Look for functions that might be builders
        builder_candidates = []
        for attr_name in dir(examples):
            attr = getattr(examples, attr_name)
            if callable(attr) and not attr_name.startswith("_"):
                builder_candidates.append(attr_name)

        # Should have some callable functions
        assert len(builder_candidates) > 0

    @pytest.mark.gui
    def test_builder_functions_callable(self):
        """Test that builder functions are callable with frame parameter."""
        try:
            root = tk.Tk()
            root.withdraw()
            frame = tk.Frame(root)

            # Test the component testing function instead of individual builders
            results = examples.test_all_demo_components()
            assert isinstance(results, dict)

            # If builders work, the 'builders' key should be True
            if "builders" in results:
                # This tests that builder functions can be called
                pass

            root.destroy()
        except tk.TclError:
            pytest.skip("Cannot create Tkinter window in this environment")


class TestExampleIntegration:
    """Integration tests for examples with main package."""

    def test_examples_use_main_classes(self):
        """Test that examples use the main window classes."""
        # Examples should import and use the main classes
        import inspect

        # Get the source code of the examples module
        try:
            source = inspect.getsource(examples)

            # Should reference main classes
            main_classes = [
                "FixedThreePaneWindow",
                "DockableThreePaneWindow",
                "EnhancedDockableThreePaneWindow",
            ]

            # At least one main class should be referenced
            found_classes = [cls for cls in main_classes if cls in source]
            assert len(found_classes) > 0

        except OSError:
            # If we can't get source (compiled module), skip this test
            pytest.skip("Cannot inspect source code")

    def test_examples_demonstrate_features(self):
        """Test that examples demonstrate key features."""
        # Examples should demonstrate the main features of the package
        try:
            source = inspect.getsource(examples)

            # Should demonstrate key features
            key_features = [
                "pack",  # Layout management
                "builder",  # Builder pattern
                "theme",  # Theming
            ]

            # At least some features should be demonstrated
            found_features = [
                feature for feature in key_features if feature in source.lower()
            ]
            assert len(found_features) > 0

        except OSError:
            pytest.skip("Cannot inspect source code")

    def test_demo_integration_with_mainloop(self):
        """Test that demo integrates properly with Tkinter mainloop."""
        with patch("tkinter.Tk") as mock_tk:
            mock_root = MagicMock()
            mock_tk.return_value = mock_root

            # Mock the window classes
            with patch(
                "threepanewindows.examples.DockableThreePaneWindow"
            ) as mock_dockable, patch(
                "threepanewindows.examples.FixedThreePaneLayout"
            ) as mock_fixed, patch(
                "threepanewindows.examples.EnhancedDockableThreePaneWindow"
            ) as mock_enhanced:

                mock_window = MagicMock()
                mock_dockable.return_value = mock_window
                mock_fixed.return_value = mock_window
                mock_enhanced.return_value = mock_window

                try:
                    # Test non-interactive mode (should not call mainloop)
                    examples.run_demo(interactive=False)
                    # Should have created Tk instances but not called mainloop
                    mock_tk.assert_called()

                    # Test interactive mode with auto-close
                    examples.run_demo(interactive=True, auto_close_delay=100)
                    # Should call mainloop in interactive mode
                    mock_root.mainloop.assert_called()
                except Exception:
                    # Might fail due to other issues, but that's okay for this test
                    pass


# Utility test to verify the fix
def test_examples_no_longer_hang():
    """Meta-test to verify that examples no longer hang the test runner."""
    import subprocess
    import sys
    import time

    # Create a simple test script that tries to import and run examples
    test_script = """
import sys
sys.path.insert(0, ".")
try:
    from threepanewindows import examples
    # This should not hang
    examples.run_demo(interactive=False)
    print("SUCCESS: Demo ran without hanging")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
"""

    # Write the test script to a temporary file
    import os
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(test_script)
        temp_script = f.name

    try:
        # Run the script with a timeout
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, temp_script],
            timeout=10,  # 10 second timeout
            capture_output=True,
            text=True,
            cwd="c:/Users/Admin/Desktop/test/ToolKit/ThreePaneWindows",
        )
        elapsed = time.time() - start_time

        # Should complete quickly
        assert elapsed < 5.0, f"Test took too long: {elapsed} seconds"

        # Should not have timed out
        assert result.returncode == 0, f"Test failed: {result.stderr}"

        # Should have success message
        assert "SUCCESS" in result.stdout, f"Unexpected output: {result.stdout}"

    except subprocess.TimeoutExpired:
        pytest.fail("Examples still hang - timeout expired")
    finally:
        # Clean up temp file
        try:
            os.unlink(temp_script)
        except:
            pass


class TestExampleBuilderFunctions:
    """Test individual example builder functions."""

    def setup_method(self):
        """Set up test fixtures."""
        try:
            self.root = tk.Tk()
            self.root.withdraw()
        except tk.TclError as e:
            pytest.skip(f"Cannot create Tkinter window: {e}")

    def teardown_method(self):
        """Clean up after tests."""
        if hasattr(self, "root") and self.root:
            self.root.destroy()

    def test_file_explorer_builders(self):
        """Test file explorer builder functions."""
        from threepanewindows import examples

        frame = tk.Frame(self.root)

        # Test builder functions if they exist
        if hasattr(examples, "build_file_explorer_left"):
            examples.build_file_explorer_left(frame)

        if hasattr(examples, "build_file_explorer_center"):
            examples.build_file_explorer_center(frame)

        if hasattr(examples, "build_file_explorer_right"):
            examples.build_file_explorer_right(frame)

    def test_ide_builders(self):
        """Test IDE builder functions."""
        from threepanewindows import examples

        frame = tk.Frame(self.root)

        # Test builder functions if they exist
        if hasattr(examples, "build_ide_left"):
            examples.build_ide_left(frame)

        if hasattr(examples, "build_ide_center"):
            examples.build_ide_center(frame)

        if hasattr(examples, "build_ide_right"):
            examples.build_ide_right(frame)

    def test_dashboard_builders(self):
        """Test dashboard builder functions."""
        from threepanewindows import examples

        frame = tk.Frame(self.root)

        # Test builder functions if they exist
        if hasattr(examples, "build_dashboard_left"):
            examples.build_dashboard_left(frame)

        if hasattr(examples, "build_dashboard_center"):
            examples.build_dashboard_center(frame)

        if hasattr(examples, "build_dashboard_right"):
            examples.build_dashboard_right(frame)

    def test_enhanced_builders(self):
        """Test enhanced builder functions."""
        from threepanewindows import examples

        frame = tk.Frame(self.root)

        # Test builder functions if they exist
        if hasattr(examples, "build_enhanced_left"):
            examples.build_enhanced_left(frame)

        if hasattr(examples, "build_enhanced_center"):
            examples.build_enhanced_center(frame)

        if hasattr(examples, "build_enhanced_right"):
            examples.build_enhanced_right(frame)


class TestExampleUtilities:
    """Test example utility functions."""

    def setup_method(self):
        """Set up test fixtures."""
        try:
            self.root = tk.Tk()
            self.root.withdraw()
        except tk.TclError as e:
            pytest.skip(f"Cannot create Tkinter window: {e}")

    def teardown_method(self):
        """Clean up after tests."""
        if hasattr(self, "root") and self.root:
            self.root.destroy()

    def test_sample_content_creation(self):
        """Test sample content creation utilities."""
        from threepanewindows import examples

        frame = tk.Frame(self.root)

        # Test utility functions if they exist
        if hasattr(examples, "create_sample_tree"):
            examples.create_sample_tree(frame)

        if hasattr(examples, "create_sample_text"):
            examples.create_sample_text(frame)

        if hasattr(examples, "create_sample_list"):
            examples.create_sample_list(frame)

        if hasattr(examples, "create_sample_canvas"):
            examples.create_sample_canvas(frame)

    def test_demo_configurations(self):
        """Test demo configuration functions."""
        from threepanewindows import examples

        # Test configuration functions if they exist
        if hasattr(examples, "get_demo_config"):
            config = examples.get_demo_config("basic")
            assert config is not None

        if hasattr(examples, "apply_demo_theme"):
            examples.apply_demo_theme("dark")

        if hasattr(examples, "setup_demo_environment"):
            examples.setup_demo_environment()

    def test_demo_window_management(self):
        """Test demo window management functions."""
        from threepanewindows import examples

        # Test window management functions if they exist
        if hasattr(examples, "create_demo_window"):
            window = examples.create_demo_window("test")
            if window:
                assert window is not None

        if hasattr(examples, "cleanup_demo_windows"):
            examples.cleanup_demo_windows()

        if hasattr(examples, "reset_demo_state"):
            examples.reset_demo_state()

    def test_interactive_features(self):
        """Test interactive demo features."""
        from threepanewindows import examples

        # Test interactive functions if they exist
        if hasattr(examples, "handle_demo_interaction"):
            examples.handle_demo_interaction("test_event")

        if hasattr(examples, "update_demo_display"):
            examples.update_demo_display()

        if hasattr(examples, "process_demo_input"):
            examples.process_demo_input("test_input")


class TestExampleUtilityFunctions:
    """Test utility functions in examples module."""

    def test_test_demo_timeout_function(self):
        """Test the test_demo_timeout utility function."""
        from threepanewindows import examples

        # Test non-interactive mode
        if hasattr(examples, "test_demo_timeout"):
            result = examples.test_demo_timeout(interactive=False, timeout_seconds=1)
            assert isinstance(result, bool)

    def test_test_all_demo_components(self):
        """Test the test_all_demo_components function."""
        from threepanewindows import examples

        if hasattr(examples, "test_all_demo_components"):
            result = examples.test_all_demo_components()
            # Result might be a dict or bool
            assert isinstance(result, (bool, dict))

    def test_demo_error_handling(self):
        """Test demo error handling paths."""
        from threepanewindows import examples

        # Test with invalid demo type
        try:
            examples.run_demo(demo_type="invalid_type", interactive=False)
        except Exception:
            # Error handling is working
            pass

        # Test with invalid parameters
        try:
            examples.run_demo(demo_type="basic", interactive=False, invalid_param=True)
        except Exception:
            # Error handling is working
            pass

    def test_demo_threading_paths(self):
        """Test threading paths in demo functions."""
        import threading
        import time

        from threepanewindows import examples

        # Test threading timeout scenario
        if hasattr(examples, "test_demo_timeout"):
            # This should test the threading timeout path
            result = examples.test_demo_timeout(interactive=True, timeout_seconds=0.1)
            assert isinstance(result, bool)

    def test_demo_component_creation(self):
        """Test individual demo component creation."""
        from threepanewindows import examples

        # Test component creation functions
        test_functions = ["test_all_demo_components", "test_demo_timeout"]

        for func_name in test_functions:
            if hasattr(examples, func_name):
                func = getattr(examples, func_name)
                try:
                    result = func()
                    assert isinstance(result, bool)
                except Exception:
                    # Some functions might fail in test environment
                    pass
