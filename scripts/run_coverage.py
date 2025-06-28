#!/usr/bin/env python3
"""
Coverage runner script for ThreePaneWindows.
Provides various coverage reporting options and utilities.
"""

import argparse
import os
import subprocess
import sys
import webbrowser
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and handle errors."""
    if description:
        print(f"\n🔄 {description}")

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Command failed with exit code {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return False

    print(f"✅ {description or 'Command'} completed successfully")
    if result.stdout:
        print(result.stdout)
    return True


def run_basic_coverage():
    """Run basic coverage with terminal report."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--cov=threepanewindows",
        "--cov-report=term-missing",
        "--cov-config=.coveragerc",
    ]
    return run_command(cmd, "Running basic coverage")


def run_full_coverage():
    """Run full coverage with all report formats."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--cov=threepanewindows",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-report=xml",
        "--cov-report=json",
        "--cov-config=.coveragerc",
    ]
    return run_command(cmd, "Running full coverage with all reports")


def run_coverage_with_branch():
    """Run coverage with branch coverage enabled."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--cov=threepanewindows",
        "--cov-branch",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-config=.coveragerc",
    ]
    return run_command(cmd, "Running coverage with branch analysis")


def run_coverage_no_gui():
    """Run coverage excluding GUI components."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--cov=threepanewindows",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--ignore=tests/test_gui_components.py",  # Skip GUI-dependent tests
        "--cov-config=.coveragerc",
    ]
    return run_command(cmd, "Running coverage (excluding GUI components)")


def open_html_report():
    """Open the HTML coverage report in the default browser."""
    html_file = Path("htmlcov/index.html")
    if html_file.exists():
        print(f"🌐 Opening coverage report: {html_file.absolute()}")
        webbrowser.open(f"file://{html_file.absolute()}")
    else:
        print("❌ HTML coverage report not found. Run coverage first.")


def clean_coverage():
    """Clean coverage files and reports."""
    files_to_clean = [
        ".coverage",
        ".coverage.*",
        "coverage.xml",
        "coverage.json",
        "htmlcov",
    ]

    for pattern in files_to_clean:
        if "*" in pattern:
            # Handle glob patterns
            import glob

            for file in glob.glob(pattern):
                try:
                    if os.path.isfile(file):
                        os.remove(file)
                        print(f"🗑️  Removed: {file}")
                    elif os.path.isdir(file):
                        import shutil

                        shutil.rmtree(file)
                        print(f"🗑️  Removed directory: {file}")
                except Exception as e:
                    print(f"⚠️  Could not remove {file}: {e}")
        else:
            try:
                if os.path.exists(pattern):
                    if os.path.isfile(pattern):
                        os.remove(pattern)
                        print(f"🗑️  Removed: {pattern}")
                    elif os.path.isdir(pattern):
                        import shutil

                        shutil.rmtree(pattern)
                        print(f"🗑️  Removed directory: {pattern}")
            except Exception as e:
                print(f"⚠️  Could not remove {pattern}: {e}")


def show_coverage_summary():
    """Show a summary of coverage files."""
    print("\n📊 Coverage Files Summary:")

    files_to_check = [
        (".coverage", "Coverage data file"),
        ("coverage.xml", "XML coverage report"),
        ("coverage.json", "JSON coverage report"),
        ("htmlcov/index.html", "HTML coverage report"),
    ]

    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path) if os.path.isfile(file_path) else "N/A"
            print(f"  ✅ {description}: {file_path} ({size} bytes)")
        else:
            print(f"  ❌ {description}: {file_path} (not found)")


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Coverage runner for GUI Image Studio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_coverage.py --basic          # Basic coverage report
  python scripts/run_coverage.py --full           # Full coverage with all formats
  python scripts/run_coverage.py --branch         # Include branch coverage
  python scripts/run_coverage.py --no-gui         # Exclude GUI components
  python scripts/run_coverage.py --open           # Open HTML report
  python scripts/run_coverage.py --clean          # Clean coverage files
  python scripts/run_coverage.py --summary        # Show coverage files summary
        """,
    )

    parser.add_argument(
        "--basic", action="store_true", help="Run basic coverage with terminal report"
    )
    parser.add_argument(
        "--full", action="store_true", help="Run full coverage with all report formats"
    )
    parser.add_argument(
        "--branch", action="store_true", help="Run coverage with branch analysis"
    )
    parser.add_argument(
        "--no-gui", action="store_true", help="Run coverage excluding GUI components"
    )
    parser.add_argument(
        "--open", action="store_true", help="Open HTML coverage report in browser"
    )
    parser.add_argument(
        "--clean", action="store_true", help="Clean coverage files and reports"
    )
    parser.add_argument(
        "--summary", action="store_true", help="Show summary of coverage files"
    )

    args = parser.parse_args()

    # Change to project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    if args.clean:
        clean_coverage()
    elif args.open:
        open_html_report()
    elif args.summary:
        show_coverage_summary()
    elif args.basic:
        run_basic_coverage()
    elif args.full:
        run_full_coverage()
    elif args.branch:
        run_coverage_with_branch()
    elif args.no_gui:
        run_coverage_no_gui()
    else:
        # Default: run basic coverage
        print("No specific option provided. Running basic coverage...")
        run_basic_coverage()

    if not args.clean and not args.open and not args.summary:
        print("\n" + "=" * 60)
        show_coverage_summary()
        print("\n💡 Tip: Use --open to view the HTML report in your browser")


if __name__ == "__main__":
    main()
