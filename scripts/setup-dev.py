#!/usr/bin/env python3
"""
Development setup script for ThreePaneWindows.

This script helps set up the development environment by:
1. Installing the package in development mode
2. Installing all development dependencies
3. Setting up pre-commit hooks
4. Running initial tests to verify setup

Usage:
    python scripts/setup-dev.py
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command safely without shell injection vulnerabilities."""
    import shlex
    print(f"\n🔄 {description}...")
    try:
        # SECURE: Parse command safely and use shell=False (default) to prevent shell injection
        if isinstance(cmd, str):
            cmd_list = shlex.split(cmd)
        else:
            cmd_list = cmd
        
        result = subprocess.run(cmd_list, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr.strip()}")
        return False


def main():
    """Main setup function."""
    print("🚀 Setting up ThreePaneWindows development environment")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    print(f"📁 Working in: {project_root}")
    
    # Install package in development mode with all dependencies
    commands = [
        ("python -m pip install --upgrade pip", "Upgrading pip"),
        ("pip install -e .[dev,docs,test]", "Installing package in development mode"),
        ("pre-commit install", "Setting up pre-commit hooks"),
        ("python -c \"import threepanewindows; print(f'ThreePaneWindows v{threepanewindows.__version__} imported successfully')\"", "Verifying package installation"),
    ]
    
    success_count = 0
    for cmd, desc in commands:
        if run_command(cmd, desc):
            success_count += 1
    
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
        print("   • Test release: python scripts/release.py --version 0.1.0 --type minor")
        print("   • Build package: python -m build")
        print("\n📚 Documentation:")
        print("   • Contributing: CONTRIBUTING.md")
        print("   • API docs: docs/api/")
        print("   • Examples: threepanewindows/examples.py")
    else:
        print(f"⚠️  Setup completed with {len(commands) - success_count} errors")
        print("   Please check the error messages above and resolve any issues")
        sys.exit(1)


if __name__ == "__main__":
    main()