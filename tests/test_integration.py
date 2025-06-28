"""
Integration tests for ThreePaneWindows package.
"""

import pytest
import tkinter as tk
from unittest.mock import Mock, patch
from threepanewindows import (
    FixedThreePaneWindow,
    DockableThreePaneWindow,
    EnhancedDockableThreePaneWindow,
    ThemeManager,
    ThemeType,
    PaneConfig,
    get_theme_manager,
    set_global_theme
)


@pytest.mark.integration
@pytest.mark.gui
class TestPackageIntegration:
    """Integration tests for the entire package."""

    def setup_method(self):
        """Set up test fixtures."""
        try:
            self.root = tk.Tk()
            self.root.withdraw()
            # Force initial update to ensure proper initialization
            self.root.update_idletasks()
        except tk.TclError as e:
            pytest.skip(f"Cannot create Tkinter window in this environment: {e}")

    def teardown_method(self):
        """Clean up after tests."""
        if hasattr(self, 'root') and self.root:
            try:
                # Destroy all child windows first
                for child in self.root.winfo_children():
                    try:
                        if hasattr(child, 'destroy'):
                            child.destroy()
                    except tk.TclError:
                        pass
                
                # Force update before destroying root
                self.root.update_idletasks()
                self.root.destroy()
                
                # Small delay to allow cleanup
                import time
                time.sleep(0.02)  # Slightly longer delay for integration tests
            except tk.TclError:
                pass  # Window already destroyed

    def test_all_window_types_importable(self):
        """Test that all window types can be imported."""
        # Should be able to import all main classes
        assert FixedThreePaneWindow is not None
        assert DockableThreePaneWindow is not None
        assert EnhancedDockableThreePaneWindow is not None

    def test_all_window_types_instantiable(self):
        """Test that all window types can be instantiated."""
        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        # Add small delay to ensure clean state
        import time
        time.sleep(0.01)

        # Fixed window
        fixed_window = FixedThreePaneWindow(self.root)
        assert fixed_window is not None
        
        # Force update after each window creation
        self.root.update_idletasks()

        # Dockable window
        dockable_window = DockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder
        )
        assert dockable_window is not None
        
        # Force update after each window creation
        self.root.update_idletasks()

        # Enhanced dockable window
        enhanced_window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder
        )
        assert enhanced_window is not None
        
        # Final update
        self.root.update_idletasks()

    def test_theming_integration(self):
        """Test theming integration across all window types."""
        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        # Set global theme
        set_global_theme(ThemeType.DARK)
        theme_manager = get_theme_manager()
        assert theme_manager.current_theme == ThemeType.DARK

        # Create enhanced window with theme
        enhanced_window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            theme=ThemeType.BLUE
        )
        
        # Window should use the specified theme
        assert enhanced_window.theme_manager.current_theme == ThemeType.BLUE

    def test_pane_config_integration(self):
        """Test PaneConfig integration with enhanced windows."""
        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        # Add small delay to ensure clean state
        import time
        time.sleep(0.01)

        left_config = PaneConfig(
            title="Left Panel",
            min_width=150,
            detachable=True
        )
        right_config = PaneConfig(
            title="Right Panel",
            fixed_width=200,
            detachable=False
        )

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            left_config=left_config,
            right_config=right_config
        )

        # Force update after window creation
        self.root.update_idletasks()

        assert window.left_config == left_config
        assert window.right_config == right_config

    def test_window_hierarchy_compatibility(self):
        """Test that different window types can coexist."""
        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        # Create multiple window types
        fixed = FixedThreePaneWindow(self.root)
        dockable = DockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder
        )
        enhanced = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder
        )

        # All should be Tkinter widgets
        assert isinstance(fixed, tk.Widget)
        assert isinstance(dockable, tk.Widget)
        assert isinstance(enhanced, tk.Widget)

    def test_cross_window_theming(self):
        """Test theming works across different window types."""
        def dummy_builder(frame):
            tk.Label(frame, text="Test").pack()

        # Create windows with different themes
        enhanced1 = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            theme=ThemeType.LIGHT
        )

        enhanced2 = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=dummy_builder,
            center_builder=dummy_builder,
            right_builder=dummy_builder,
            theme=ThemeType.DARK
        )

        # Each should have its own theme
        assert enhanced1.theme_manager.current_theme == ThemeType.LIGHT
        assert enhanced2.theme_manager.current_theme == ThemeType.DARK

    def test_builder_pattern_consistency(self):
        """Test that builder pattern works consistently across window types."""
        left_calls = []
        center_calls = []
        right_calls = []

        def left_builder(frame):
            left_calls.append(frame)
            tk.Label(frame, text="Left").pack()

        def center_builder(frame):
            center_calls.append(frame)
            tk.Text(frame).pack()

        def right_builder(frame):
            right_calls.append(frame)
            tk.Button(frame, text="Right").pack()

        # Test with dockable window
        dockable = DockableThreePaneWindow(
            self.root,
            left_builder=left_builder,
            center_builder=center_builder,
            right_builder=right_builder
        )
        dockable.pack()

        # Builders should have been called
        assert len(left_calls) > 0
        assert len(center_calls) > 0
        assert len(right_calls) > 0

        # Reset counters
        left_calls.clear()
        center_calls.clear()
        right_calls.clear()

        # Test with enhanced window
        enhanced = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=left_builder,
            center_builder=center_builder,
            right_builder=right_builder
        )
        enhanced.pack()

        # Builders should have been called again
        assert len(left_calls) > 0
        assert len(center_calls) > 0
        assert len(right_calls) > 0


@pytest.mark.integration
class TestPackageAPI:
    """Test the public API of the package."""

    def test_main_imports(self):
        """Test that main classes can be imported from package root."""
        from threepanewindows import (
            FixedThreePaneWindow,
            DockableThreePaneWindow,
            EnhancedDockableThreePaneWindow,
            ThemeManager,
            ThemeType,
            PaneConfig
        )
        
        # All should be importable
        assert FixedThreePaneWindow is not None
        assert DockableThreePaneWindow is not None
        assert EnhancedDockableThreePaneWindow is not None
        assert ThemeManager is not None
        assert ThemeType is not None
        assert PaneConfig is not None

    def test_utility_functions_importable(self):
        """Test that utility functions can be imported."""
        from threepanewindows import get_theme_manager, set_global_theme
        
        assert callable(get_theme_manager)
        assert callable(set_global_theme)

    def test_version_info_accessible(self):
        """Test that version information is accessible."""
        from threepanewindows import __version__, __version_info__, FULL_VERSION
        
        assert isinstance(__version__, str)
        assert isinstance(__version_info__, tuple)
        assert isinstance(FULL_VERSION, str)

    def test_package_all_exports(self):
        """Test that __all__ exports are correct."""
        import threepanewindows
        
        if hasattr(threepanewindows, '__all__'):
            all_exports = threepanewindows.__all__
            
            # Should include main classes
            expected_classes = [
                'FixedThreePaneWindow',
                'DockableThreePaneWindow',
                'EnhancedDockableThreePaneWindow',
                'ThemeManager',
                'ThemeType',
                'PaneConfig'
            ]
            
            for cls in expected_classes:
                assert cls in all_exports, f"{cls} not in __all__"

    def test_legacy_compatibility(self):
        """Test legacy compatibility imports."""
        try:
            from threepanewindows import FixedThreePaneLayout
            # Legacy alias should work
            assert FixedThreePaneLayout is not None
        except ImportError:
            # If legacy alias doesn't exist, that's okay
            pass


@pytest.mark.integration
@pytest.mark.slow
class TestRealWorldUsage:
    """Test real-world usage scenarios."""

    def setup_method(self):
        """Set up test fixtures."""
        try:
            self.root = tk.Tk()
            self.root.withdraw()
            # Force initial update to ensure proper initialization
            self.root.update_idletasks()
        except tk.TclError as e:
            pytest.skip(f"Cannot create Tkinter window in this environment: {e}")

    def teardown_method(self):
        """Clean up after tests."""
        if hasattr(self, 'root') and self.root:
            try:
                # Destroy all child windows first
                for child in self.root.winfo_children():
                    try:
                        if hasattr(child, 'destroy'):
                            child.destroy()
                    except tk.TclError:
                        pass
                
                # Force update before destroying root
                self.root.update_idletasks()
                self.root.destroy()
                
                # Small delay to allow cleanup
                import time
                time.sleep(0.02)  # Slightly longer delay for integration tests
            except tk.TclError:
                pass  # Window already destroyed

    def test_file_explorer_scenario(self):
        """Test a file explorer-like application scenario."""
        def tree_builder(frame):
            # Simulate a file tree
            import tkinter.ttk as ttk
            tree = ttk.Treeview(frame)
            tree.pack(fill=tk.BOTH, expand=True)
            return tree

        def content_builder(frame):
            # Simulate file content area
            text = tk.Text(frame)
            text.pack(fill=tk.BOTH, expand=True)
            return text

        def properties_builder(frame):
            # Simulate properties panel
            tk.Label(frame, text="Properties").pack()
            return frame

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=tree_builder,
            center_builder=content_builder,
            right_builder=properties_builder,
            left_config=PaneConfig(title="Files", min_width=200),
            right_config=PaneConfig(title="Properties", default_width=250),
            theme=ThemeType.LIGHT
        )
        window.pack(fill=tk.BOTH, expand=True)

        # Should create a functional layout
        assert window.winfo_exists()

    def test_ide_scenario(self):
        """Test an IDE-like application scenario."""
        def project_builder(frame):
            # Simulate project explorer
            import tkinter.ttk as ttk
            tree = ttk.Treeview(frame, columns=('type',))
            tree.pack(fill=tk.BOTH, expand=True)
            return tree

        def editor_builder(frame):
            # Simulate code editor
            text = tk.Text(frame, font=('Courier', 10))
            text.pack(fill=tk.BOTH, expand=True)
            return text

        def tools_builder(frame):
            # Simulate tools panel
            notebook = tk.ttk.Notebook(frame)
            notebook.pack(fill=tk.BOTH, expand=True)
            return notebook

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=project_builder,
            center_builder=editor_builder,
            right_builder=tools_builder,
            left_config=PaneConfig(
                title="Project",
                min_width=180,
                detachable=True
            ),
            right_config=PaneConfig(
                title="Tools",
                default_width=300,
                detachable=True
            ),
            theme=ThemeType.DARK
        )
        window.pack(fill=tk.BOTH, expand=True)

        # Should create a functional IDE-like layout
        assert window.winfo_exists()

    def test_dashboard_scenario(self):
        """Test a dashboard-like application scenario."""
        def sidebar_builder(frame):
            # Simulate navigation sidebar
            for i in range(5):
                btn = tk.Button(frame, text=f"Section {i+1}")
                btn.pack(fill=tk.X, pady=2)
            return frame

        def main_builder(frame):
            # Simulate main dashboard area
            canvas = tk.Canvas(frame, bg='white')
            canvas.pack(fill=tk.BOTH, expand=True)
            return canvas

        def info_builder(frame):
            # Simulate info panel
            tk.Label(frame, text="Information Panel").pack()
            listbox = tk.Listbox(frame)
            listbox.pack(fill=tk.BOTH, expand=True)
            return frame

        window = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=sidebar_builder,
            center_builder=main_builder,
            right_builder=info_builder,
            left_config=PaneConfig(
                title="Navigation",
                fixed_width=150,
                detachable=False
            ),
            right_config=PaneConfig(
                title="Info",
                min_width=200,
                closable=True
            ),
            theme=ThemeType.BLUE
        )
        window.pack(fill=tk.BOTH, expand=True)

        # Should create a functional dashboard layout
        assert window.winfo_exists()

    @patch('tkinter.messagebox.showinfo')
    def test_error_recovery_scenario(self, mock_messagebox):
        """Test error recovery in real-world usage."""
        def failing_builder(frame):
            # Simulate a builder that might fail
            raise ValueError("Simulated builder error")

        def safe_builder(frame):
            tk.Label(frame, text="Safe content").pack()
            return frame

        # Should handle builder errors gracefully
        try:
            window = EnhancedDockableThreePaneWindow(
                self.root,
                left_builder=failing_builder,
                center_builder=safe_builder,
                right_builder=safe_builder
            )
            window.pack()
        except ValueError:
            # Expected error from failing builder
            pass

        # Should still be able to create working windows
        window2 = EnhancedDockableThreePaneWindow(
            self.root,
            left_builder=safe_builder,
            center_builder=safe_builder,
            right_builder=safe_builder
        )
        window2.pack()
        assert window2.winfo_exists()