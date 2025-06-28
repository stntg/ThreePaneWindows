#!/usr/bin/env python3
"""
Development environment setup script for ThreePaneWindows.

This script sets up the development environment with all necessary dependencies
and tools for contributing to the ThreePaneWindows project.

Features:
- Installing the package in development mode
- Installing all development dependencies
- Setting up pre-commit hooks
- Running initial tests to verify setup
- Secure subprocess execution (no shell injection vulnerabilities)

Usage:
    python scripts/setup-dev.py
"""

import shlex
import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True):
    """Run a command safely without shell injection vulnerabilities."""
    try:
        # If cmd is a string, split it safely; if it's already a list, use as-is
        if isinstance(cmd, str):
            cmd_list = shlex.split(cmd)
        else:
            cmd_list = cmd

        # SECURE: Using shell=False (default) to prevent shell injection
        result = subprocess.run(cmd_list, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        cmd_str = " ".join(cmd_list) if isinstance(cmd_list, list) else cmd
        print(f"Error running command: {cmd_str}")
        print(f"Return code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        return None, e.stderr
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, str(e)


def setup_dev_environment():
    """Set up development environment."""
    print("🚀 Setting up ThreePaneWindows development environment")
    print("=" * 60)

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)

    print(
        f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected"
    )

    # Change to project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    print(f"📁 Project root: {project_root}")

    commands = [
        (["python", "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip"),
        (
            ["pip", "install", "-e", ".[dev,docs,test]"],
            "Installing package in development mode",
        ),
        (["pre-commit", "install"], "Setting up pre-commit hooks"),
        (
            [
                "python",
                "-c",
                "import threepanewindows; print(f'ThreePaneWindows v{threepanewindows.__version__} imported successfully')",
            ],
            "Verifying package installation",
        ),
    ]

    success_count = 0
    for cmd, desc in commands:
        print(f"\n🔄 {desc}...")
        stdout, stderr = run_command(cmd, check=False)
        if stdout is not None:
            print(f"✅ {desc} completed successfully")
            if stdout:
                print(f"   Output: {stdout}")
            success_count += 1
        else:
            print(f"❌ {desc} failed: {stderr}")

    print("\n" + "=" * 60)
    if success_count == len(commands):
        print("🎉 Development environment setup completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Run tests: pytest")
        print("   2. Run linting: flake8 threepanewindows/")
        print("   3. Format code: black .")
        print("   4. Build docs: cd docs && make html")
        print("   5. Run examples: python -m threepanewindows.examples")
        print("\n🔧 Development commands:")
        print("   • Run all checks: tox")
        print(
            "   • Test release: python scripts/release.py --version 0.1.0 --type minor"
        )
        print("   • Build package: python -m build")
        print("\n📚 Documentation:")
        print("   • Contributing: CONTRIBUTING.md")
        print("   • API docs: docs/api/")
        print("   • Examples: threepanewindows/examples.py")
        return True
    else:
        print(f"⚠️  Setup completed with {len(commands) - success_count} errors")
        print("   Please check the error messages above and resolve any issues")
        return False


def main():
    """Main entry point."""
    try:
        success = setup_dev_environment()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
