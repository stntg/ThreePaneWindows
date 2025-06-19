#!/usr/bin/env python3
"""
Development environment setup script for ThreePaneWindows.

This script sets up the development environment with all necessary dependencies
and tools for contributing to the ThreePaneWindows project.
"""

import subprocess
import sys
import shlex
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
        cmd_str = ' '.join(cmd_list) if isinstance(cmd_list, list) else cmd
        print(f"Error running command: {cmd_str}")
        print(f"Return code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        return None, e.stderr
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, str(e)


def setup_dev_environment():
    """Set up development environment."""
    print("🔧 Setting up ThreePaneWindows development environment...")
    print("=" * 60)

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
        (["python", "-m", "pytest", "--version"], "Verifying pytest installation"),
    ]

    success_count = 0
    for cmd, desc in commands:
        print(f"\n📋 {desc}...")
        stdout, stderr = run_command(cmd, check=False)
        if stdout is not None:
            print(f"✅ {desc} completed")
            if stdout:
                print(f"   Output: {stdout}")
            success_count += 1
        else:
            print(f"❌ {desc} failed: {stderr}")

    print("\n" + "=" * 60)
    if success_count == len(commands):
        print("🎉 Development environment setup completed successfully!")
        print("\n💡 Next steps:")
        print("   • Run 'python dev_tools.py test' to run tests")
        print("   • Run 'python dev_tools.py lint' to check code quality")
        print("   • Run 'python verify_package.py' to verify installation")
        return True
    else:
        print(f"⚠️  Setup completed with {len(commands) - success_count} failures")
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