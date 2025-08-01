#!/usr/bin/env python3
"""Test script to validate documentation build configuration.

This script helps identify issues before pushing to GitHub.
"""

import os
import subprocess  # nosec B404
import sys
from pathlib import Path


def main() -> int:
    """Test documentation build locally."""
    # Get the project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_dir = project_root / "docs"

    print("ThreePaneWindows Documentation Build Test")
    print("=" * 50)

    # Check if we're in the right directory
    if not docs_dir.exists():
        print(f"Error: docs directory not found at {docs_dir}")
        return 1

    # Check Python version
    print(f"Python version: {sys.version}")

    # Check if required packages are installed
    try:
        import sphinx

        print(f"Sphinx version: {sphinx.__version__}")
    except ImportError:
        print("Error: Sphinx not installed. Run: pip install -r docs/requirements.txt")
        return 1

    try:
        import myst_parser

        print(f"MyST Parser version: {myst_parser.__version__}")
    except ImportError:
        print(
            "Warning: MyST Parser not installed. Markdown files will not be processed."
        )

    try:
        import sphinx_rtd_theme  # noqa: F401

        print("Sphinx RTD Theme available")
    except ImportError:
        print("Warning: Sphinx RTD Theme not installed.")

    try:
        import linkify_it  # noqa: F401

        print("Linkify-it-py available")
    except ImportError:
        print(
            "Warning: Linkify-it-py not installed. Linkify extension will be disabled."
        )

    # Change to docs directory
    os.chdir(docs_dir)

    # Ensure _static directory exists
    static_dir = docs_dir / "_static"
    static_dir.mkdir(exist_ok=True)
    status = "exists" if static_dir.exists() else "created"
    print(f"Static directory: {static_dir} ({status})")

    # Test configuration loading
    print("\nTesting Sphinx configuration...")
    try:
        cmd = [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, '.'); import conf; "
            "print('Configuration loaded successfully')",
        ]
        result = subprocess.run(  # nosec B603
            cmd, capture_output=True, text=True, cwd=docs_dir
        )

        if result.returncode == 0:
            print("✓ Configuration loaded successfully")
            if result.stdout:
                print(f"Output: {result.stdout.strip()}")
        else:
            print("✗ Configuration failed to load")
            print(f"Error: {result.stderr}")
            return 1
    except Exception as e:
        print(f"✗ Error testing configuration: {e}")
        return 1

    # Test documentation build
    print("\nTesting documentation build...")
    try:
        cmd = ["sphinx-build", "-b", "html", "-v", ".", "_build/html"]
        result = subprocess.run(  # nosec B603 B607
            cmd, capture_output=True, text=True, cwd=docs_dir
        )

        if result.returncode == 0:
            print("✓ Documentation built successfully")
            build_dir = docs_dir / "_build" / "html"
            if (build_dir / "index.html").exists():
                print(f"✓ index.html created at {build_dir / 'index.html'}")
            else:
                print("✗ index.html not found in build output")
                return 1
        else:
            print("✗ Documentation build failed")
            print(f"stdout: {result.stdout}")
            print(f"stderr: {result.stderr}")
            return 1
    except Exception as e:
        print(f"✗ Error building documentation: {e}")
        return 1

    print("\n" + "=" * 50)
    print("✓ All tests passed! Documentation should build successfully on GitHub.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
