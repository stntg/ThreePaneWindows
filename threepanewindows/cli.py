#!/usr/bin/env python3
"""
Command-line interface for ThreePaneWindows.

This module provides a simple CLI to run demos and examples.
"""

import argparse

from .examples import run_demo


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ThreePaneWindows - Tkinter three-pane layouts", prog="threepane"
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run interactive demo")
    demo_parser.add_argument(
        "--type",
        choices=["dockable", "fixed", "both"],
        default="both",
        help="Type of demo to run (default: both)",
    )

    # Info command
    subparsers.add_parser("info", help="Show package information")

    args = parser.parse_args()

    if args.command == "demo":
        print("Starting ThreePaneWindows demo...")
        run_demo()
    elif args.command == "info":
        show_info()
    else:
        parser.print_help()


def show_info() -> None:
    """Show package information."""
    info_text = """
ThreePaneWindows v1.0.0

A Python library for creating dockable and fixed three-pane window layouts in Tkinter.

Features:
  • DockableThreePaneWindow - Advanced layout with detachable panels
  • FixedThreePaneLayout - Simple fixed layout with customization
  • Pure Tkinter implementation (no external dependencies)
  • Cross-platform compatibility

Usage:
  threepane demo          # Run interactive demo
  threepane info          # Show this information

For more information, visit: https://github.com/stntg/threepanewindows
"""
    print(info_text)


if __name__ == "__main__":
    main()
