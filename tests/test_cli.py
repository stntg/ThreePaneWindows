"""
Tests for CLI functionality.
"""

from unittest.mock import Mock, patch

import pytest

from threepanewindows.cli import main, show_info


class TestCLI:
    """Test cases for CLI functionality."""

    def test_main_no_args(self):
        """Test main function with no arguments shows help."""
        with patch("sys.argv", ["threepane"]):
            with patch("argparse.ArgumentParser.print_help") as mock_help:
                main()
                mock_help.assert_called_once()

    def test_main_version(self):
        """Test version argument."""
        with patch("sys.argv", ["threepane", "--version"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            # Version should exit with code 0
            assert exc_info.value.code == 0

    @patch("threepanewindows.cli.run_demo")
    def test_main_demo_command(self, mock_run_demo):
        """Test demo command."""
        with patch("sys.argv", ["threepane", "demo"]):
            with patch("builtins.print") as mock_print:
                main()
                mock_print.assert_called_with("Starting ThreePaneWindows demo...")
                mock_run_demo.assert_called_once()

    @patch("threepanewindows.cli.run_demo")
    def test_main_demo_with_type(self, mock_run_demo):
        """Test demo command with type argument."""
        with patch("sys.argv", ["threepane", "demo", "--type", "dockable"]):
            main()
            mock_run_demo.assert_called_once()

    def test_main_info_command(self):
        """Test info command."""
        with patch("sys.argv", ["threepane", "info"]):
            with patch("builtins.print") as mock_print:
                main()
                # Should print package information
                mock_print.assert_called()

    def test_show_info(self):
        """Test show_info function."""
        with patch("builtins.print") as mock_print:
            show_info()
            # Should print version and description
            mock_print.assert_called()
            # Check that it prints something about ThreePaneWindows
            printed_text = "".join(call.args[0] for call in mock_print.call_args_list)
            assert "ThreePaneWindows" in printed_text

    def test_invalid_demo_type(self):
        """Test invalid demo type argument."""
        with patch("sys.argv", ["threepane", "demo", "--type", "invalid"]):
            with pytest.raises(SystemExit):
                main()

    def test_help_command(self):
        """Test help is shown for invalid commands."""
        with patch("sys.argv", ["threepane", "invalid_command"]):
            with pytest.raises(SystemExit):
                main()


class TestCLIIntegration:
    """Integration tests for CLI."""

    def test_cli_module_importable(self):
        """Test that CLI module can be imported."""
        from threepanewindows import cli

        assert hasattr(cli, "main")
        assert hasattr(cli, "show_info")

    def test_cli_functions_callable(self):
        """Test that CLI functions are callable."""
        from threepanewindows.cli import main, show_info

        assert callable(main)
        assert callable(show_info)

    @patch("threepanewindows.cli.run_demo")
    def test_demo_integration(self, mock_run_demo):
        """Test that demo command integrates with examples module."""
        with patch("sys.argv", ["threepane", "demo"]):
            main()
            mock_run_demo.assert_called_once()

    def test_argument_parser_setup(self):
        """Test argument parser is set up correctly."""
        from threepanewindows.cli import main

        # Mock ArgumentParser to capture its configuration
        with patch("argparse.ArgumentParser") as mock_parser_class:
            mock_parser = Mock()
            mock_subparsers = Mock()
            mock_demo_parser = Mock()

            mock_parser_class.return_value = mock_parser
            mock_parser.add_subparsers.return_value = mock_subparsers
            mock_subparsers.add_parser.return_value = mock_demo_parser
            mock_parser.parse_args.return_value = Mock(command=None)

            main()

            # Verify parser was configured
            mock_parser_class.assert_called_once()
            mock_parser.add_argument.assert_called()
            mock_parser.add_subparsers.assert_called_once()

    def test_cli_error_handling(self):
        """Test CLI handles errors gracefully."""
        with patch("sys.argv", ["threepane", "demo"]):
            with patch(
                "threepanewindows.cli.run_demo", side_effect=Exception("Test error")
            ):
                # Should not crash, but might print error
                try:
                    main()
                except Exception as e:
                    # If it raises an exception, it should be the expected one
                    assert str(e) == "Test error"
