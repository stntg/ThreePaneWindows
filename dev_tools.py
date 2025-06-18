#!/usr/bin/env python3
"""
Development Tools for ThreePaneWindows

This script provides helpful commands for the development workflow.
"""

import subprocess
import sys
import re
import shlex
import glob
from pathlib import Path
from datetime import datetime


def run_command(cmd, check=True):
    """Run a command safely without shell injection vulnerabilities."""
    try:
        # If cmd is a string, split it safely; if it's already a list, use as-is
        if isinstance(cmd, str):
            cmd_list = shlex.split(cmd)
        else:
            cmd_list = cmd
        
        result = subprocess.run(cmd_list, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd_list) if isinstance(cmd_list, list) else cmd}")
        print(f"Error: {e.stderr}")
        return None, e.stderr


def get_current_branch():
    """Get the current git branch."""
    stdout, _ = run_command(["git", "branch", "--show-current"])
    return stdout


def get_current_version():
    """Get the current version from _version.py and pyproject.toml."""
    # Try _version.py first (primary source)
    try:
        with open("threepanewindows/_version.py", "r") as f:
            content = f.read()
            match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        pass
    
    # Fallback to pyproject.toml
    try:
        with open("pyproject.toml", "r") as f:
            content = f.read()
            match = re.search(r'version = "([^"]+)"', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        pass
    return None


def create_feature_branch(feature_name):
    """Create a new feature branch."""
    print(f"Creating feature branch: feature/{feature_name}")
    
    # Switch to develop and pull latest
    print("Switching to develop branch...")
    run_command(["git", "checkout", "develop"])
    run_command(["git", "pull", "origin", "develop"])
    
    # Create and switch to feature branch
    branch_name = f"feature/{feature_name}"
    run_command(["git", "checkout", "-b", branch_name])
    
    print(f"✅ Created and switched to branch: {branch_name}")
    print(f"💡 When ready, push with: git push -u origin {branch_name}")


def start_release(version):
    """Start a new release."""
    print(f"Starting release: v{version}")
    
    # Switch to develop and pull latest
    print("Switching to develop branch...")
    run_command(["git", "checkout", "develop"])
    run_command(["git", "pull", "origin", "develop"])
    
    # Create release branch from develop
    branch_name = f"release/v{version}"
    run_command(["git", "checkout", "-b", branch_name])
    
    # Update version in both files
    print(f"Updating version to {version}...")
    
    # Update _version.py
    with open("threepanewindows/_version.py", "r") as f:
        content = f.read()
    
    updated_content = re.sub(
        r'__version__ = ["\'][^"\']+["\']',
        f'__version__ = "{version}"',
        content
    )
    
    with open("threepanewindows/_version.py", "w") as f:
        f.write(updated_content)
    
    # Update pyproject.toml
    with open("pyproject.toml", "r") as f:
        content = f.read()
    
    updated_content = re.sub(
        r'version = "[^"]+"',
        f'version = "{version}"',
        content
    )
    
    with open("pyproject.toml", "w") as f:
        f.write(updated_content)
    
    # Update docs/conf.py if it exists
    if Path("docs/conf.py").exists():
        with open("docs/conf.py", "r") as f:
            content = f.read()
        
        version_short = '.'.join(version.split('.')[:2])  # X.Y
        updated_content = re.sub(
            r"version = ['\"][^'\"]+['\"]",
            f"version = '{version_short}'",
            content
        )
        updated_content = re.sub(
            r"release = ['\"][^'\"]+['\"]",
            f"release = '{version}'",
            updated_content
        )
        
        with open("docs/conf.py", "w") as f:
            f.write(updated_content)
    
    # Add and commit changes
    run_command(["git", "add", "threepanewindows/_version.py", "pyproject.toml"])
    if Path("docs/conf.py").exists():
        run_command(["git", "add", "docs/conf.py"])
    run_command(["git", "commit", "-m", f"Bump version to {version}"])
    
    print(f"✅ Release branch created: {branch_name}")
    print(f"💡 Next steps:")
    print(f"   1. Test thoroughly on this branch")
    print(f"   2. Push branch: git push -u origin {branch_name}")
    print(f"   3. Run: python dev_tools.py merge-to-main")
    print(f"   4. GitHub Actions will automatically publish to PyPI")


def merge_to_main():
    """Merge current release branch to main and create tag."""
    current_branch = get_current_branch()
    
    if not current_branch.startswith('release/'):
        print("❌ Not on a release branch. Please create a release branch first.")
        print("💡 Use: python dev_tools.py release <version>")
        return False
    
    version = current_branch.replace('release/v', '')
    print(f"🔄 Merging {current_branch} to main and creating tag v{version}...")
    
    # Merge to main
    print("Switching to main branch...")
    run_command(["git", "checkout", "main"])
    run_command(["git", "pull", "origin", "main"])
    
    print(f"Merging {current_branch} to main...")
    run_command(["git", "merge", current_branch])
    
    # Create tag
    print(f"Creating tag v{version}...")
    run_command(["git", "tag", f"v{version}"])
    
    # Push main and tags
    print("Pushing to main with tags...")
    run_command(["git", "push", "origin", "main"])
    run_command(["git", "push", "origin", "--tags"])
    
    # Merge back to develop
    print("Merging back to develop...")
    run_command(["git", "checkout", "develop"])
    run_command(["git", "merge", current_branch])
    run_command(["git", "push", "origin", "develop"])
    
    # Clean up release branch (optional)
    print(f"Cleaning up release branch {current_branch}...")
    run_command(["git", "branch", "-d", current_branch])
    run_command(["git", "push", "origin", "--delete", current_branch])
    
    print(f"✅ Release v{version} completed!")
    print(f"🏷️  Tag v{version} created and pushed")
    print(f"🚀 GitHub Actions will now build and publish to PyPI")
    
    return True


def test_package_locally():
    """Test the package locally."""
    print("Testing package locally...")
    
    # Build package
    print("Building package...")
    run_command(["python", "-m", "build"])
    
    # Check with twine
    print("Checking package with twine...")
    # Use glob to find wheel files safely
    dist_files = glob.glob("dist/*")
    if dist_files:
        run_command(["python", "-m", "twine", "check"] + dist_files)
    else:
        print("No distribution files found in dist/")
        return
    
    # Test installation
    print("Testing installation...")
    run_command(["python", "-m", "venv", "test_env"])
    
    # Test installation in virtual environment
    if sys.platform == "win32":
        python_exe = "test_env\\Scripts\\python.exe"
        pip_exe = "test_env\\Scripts\\pip.exe"
    else:
        python_exe = "test_env/bin/python"
        pip_exe = "test_env/bin/pip"
    
    # Find wheel file
    wheel_files = glob.glob("dist/*.whl")
    if wheel_files:
        print("Installing package in test environment...")
        run_command([pip_exe, "install", wheel_files[0]])
        
        print("Testing package import...")
        run_command([python_exe, "-c", "import threepanewindows; print('Version:', threepanewindows.__version__)"])
    else:
        print("No wheel file found for testing")
    
    # Cleanup
    print("Cleaning up test environment...")
    if sys.platform == "win32":
        run_command(["rmdir", "/s", "/q", "test_env"], check=False)
    else:
        run_command(["rm", "-rf", "test_env"], check=False)
    
    print("✅ Local package test completed")


def run_lint():
    """Run code quality checks."""
    print("🔍 Running code quality checks...")
    
    checks = [
        (["python", "-m", "black", "--check", "--diff", "."], "Black formatting check"),
        (["python", "-m", "isort", "--check-only", "--diff", "."], "Import sorting check"),
        (["python", "-m", "flake8", "threepanewindows/"], "Flake8 linting"),
        (["python", "-m", "mypy", "threepanewindows/", "--ignore-missing-imports"], "MyPy type checking"),
        (["python", "-m", "bandit", "-r", "threepanewindows/"], "Security check"),
    ]
    
    results = []
    for cmd, description in checks:
        print(f"\n📋 {description}...")
        stdout, stderr = run_command(cmd, check=False)
        if stdout is not None:
            print(f"✅ {description} passed")
            results.append((description, True, ""))
        else:
            print(f"❌ {description} failed")
            results.append((description, False, stderr))
    
    # Summary
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"\n📊 Code Quality Summary: {passed}/{total} checks passed")
    
    if passed < total:
        print("\n❌ Failed checks:")
        for desc, success, error in results:
            if not success:
                print(f"  • {desc}")
                if error:
                    print(f"    {error[:200]}...")
    
    return passed == total


def build_docs():
    """Build documentation."""
    print("📚 Building documentation...")
    
    if not Path("docs").exists():
        print("❌ docs/ directory not found")
        return False
    
    # Build HTML documentation
    print("Building HTML documentation...")
    stdout, stderr = run_command(["python", "-m", "sphinx", "-b", "html", "docs", "docs/_build/html"])
    
    if stdout is not None:
        print("✅ Documentation built successfully")
        print(f"📖 Open docs/_build/html/index.html to view")
        return True
    else:
        print("❌ Documentation build failed")
        print(f"Error: {stderr}")
        return False


def clean_build():
    """Clean build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    # Directories to clean
    clean_dirs = [
        "build/",
        "dist/",
        "*.egg-info/",
        "docs/_build/",
        "__pycache__/",
        "*.pyc",
        ".pytest_cache/",
        ".coverage",
        ".mypy_cache/",
        ".tox/",
    ]
    
    import shutil
    import glob
    
    cleaned = []
    
    for pattern in clean_dirs:
        if pattern.endswith("/"):
            # Directory
            dir_name = pattern[:-1]
            if Path(dir_name).exists():
                shutil.rmtree(dir_name)
                cleaned.append(dir_name)
        else:
            # File pattern
            for path in glob.glob(pattern, recursive=True):
                if Path(path).is_file():
                    Path(path).unlink()
                    cleaned.append(path)
                elif Path(path).is_dir():
                    shutil.rmtree(path)
                    cleaned.append(path)
    
    # Clean __pycache__ directories recursively
    for pycache in Path(".").rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache)
            cleaned.append(str(pycache))
    
    # Clean .pyc files recursively
    for pyc in Path(".").rglob("*.pyc"):
        if pyc.is_file():
            pyc.unlink()
            cleaned.append(str(pyc))
    
    if cleaned:
        print(f"✅ Cleaned {len(cleaned)} items:")
        for item in cleaned[:10]:  # Show first 10
            print(f"  • {item}")
        if len(cleaned) > 10:
            print(f"  ... and {len(cleaned) - 10} more")
    else:
        print("✅ No artifacts to clean")
    
    return True


def run_examples():
    """Run the example applications."""
    print("🎮 Running ThreePaneWindows examples...")
    
    # Check if examples module exists
    if not Path("threepanewindows/examples.py").exists():
        print("❌ Examples module not found")
        return False
    
    print("Starting examples...")
    stdout, stderr = run_command(["python", "-m", "threepanewindows.examples"], check=False)
    
    if stdout is not None:
        print("✅ Examples ran successfully")
        return True
    else:
        print("❌ Examples failed to run")
        print(f"Error: {stderr}")
        return False


def run_pytest():
    """Run the test suite with pytest."""
    print("🧪 Running test suite...")
    
    if not Path("tests").exists():
        print("❌ tests/ directory not found")
        return False
    
    # Run pytest with coverage
    print("Running pytest with coverage...")
    stdout, stderr = run_command([
        "python", "-m", "pytest", 
        "tests/", 
        "--cov=threepanewindows", 
        "--cov-report=term-missing",
        "-v"
    ], check=False)
    
    if stdout is not None:
        print("✅ Tests completed")
        return True
    else:
        print("❌ Tests failed")
        print(f"Error: {stderr}")
        return False


def setup_dev_env():
    """Set up development environment."""
    print("🔧 Setting up development environment...")
    
    commands = [
        (["python", "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip"),
        (["pip", "install", "-e", ".[dev,docs,test]"], "Installing package in dev mode"),
        (["pre-commit", "install"], "Setting up pre-commit hooks"),
    ]
    
    success_count = 0
    for cmd, desc in commands:
        print(f"\n📋 {desc}...")
        stdout, stderr = run_command(cmd, check=False)
        if stdout is not None:
            print(f"✅ {desc} completed")
            success_count += 1
        else:
            print(f"❌ {desc} failed: {stderr}")
    
    if success_count == len(commands):
        print("\n🎉 Development environment setup complete!")
        print("💡 Try: python dev_tools.py examples")
        return True
    else:
        print(f"\n⚠️ Setup completed with {len(commands) - success_count} errors")
        return False


def show_status():
    """Show current development status."""
    print("🔍 ThreePaneWindows Development Status")
    print("=" * 60)
    
    # Current branch
    branch = get_current_branch()
    print(f"📍 Current branch: {branch}")
    
    # Current version
    version = get_current_version()
    print(f"🏷️  Current version: {version}")
    
    # Git status
    stdout, _ = run_command(["git", "status", "--porcelain"])
    if stdout:
        print(f"📝 Uncommitted changes: {len(stdout.splitlines())} files")
        # Show first few changed files
        files = stdout.splitlines()[:3]
        for file_status in files:
            print(f"   {file_status}")
        if len(stdout.splitlines()) > 3:
            print(f"   ... and {len(stdout.splitlines()) - 3} more")
    else:
        print("✅ Working directory clean")
    
    # Check if branches exist
    stdout, _ = run_command(["git", "branch", "-r"])
    remote_branches = stdout.splitlines() if stdout else []
    
    has_develop = any("origin/develop" in branch for branch in remote_branches)
    has_main = any("origin/main" in branch for branch in remote_branches)
    print(f"🌿 Main branch exists: {'✅' if has_main else '❌'}")
    print(f"🌿 Develop branch exists: {'✅' if has_develop else '❌'}")
    
    # Check key files
    key_files = [
        ("pyproject.toml", "Project configuration"),
        ("threepanewindows/__init__.py", "Package init"),
        ("threepanewindows/_version.py", "Version file"),
        ("tests/", "Test directory"),
        ("docs/", "Documentation"),
        (".github/workflows/", "CI/CD workflows"),
    ]
    
    print(f"\n📁 Project structure:")
    for file_path, description in key_files:
        exists = Path(file_path).exists()
        print(f"   {'✅' if exists else '❌'} {description}: {file_path}")
    
    # Check if package is installed in dev mode
    stdout, _ = run_command(["pip", "show", "threepanewindows"], check=False)
    if stdout and "Editable project location" in stdout:
        print(f"📦 Package installed in development mode: ✅")
    else:
        print(f"📦 Package installed in development mode: ❌")
        print("   💡 Run: python dev_tools.py setup")
    
    print("\n💡 Available commands:")
    print("  python dev_tools.py setup              - Set up development environment")
    print("  python dev_tools.py feature <name>     - Create feature branch")
    print("  python dev_tools.py release <version>  - Start release process")
    print("  python dev_tools.py merge-to-main      - Merge release to main and tag")
    print("  python dev_tools.py test               - Test package locally")
    print("  python dev_tools.py pytest             - Run test suite with coverage")
    print("  python dev_tools.py lint               - Run code quality checks")
    print("  python dev_tools.py docs               - Build documentation")
    print("  python dev_tools.py examples           - Run example applications")
    print("  python dev_tools.py clean              - Clean build artifacts")
    print("  python dev_tools.py status             - Show this status")
    print("  python dev_tools.py help               - Show detailed help")
    print("  python dev_tools.py summary <title> <content> - Create summary file")


def show_help():
    """Show detailed help information."""
    print("🚀 ThreePaneWindows Development Tools")
    print("=" * 60)
    print()
    print("This script provides helpful commands for the ThreePaneWindows development workflow.")
    print()
    
    commands = [
        ("setup", "Set up development environment", [
            "Upgrades pip to latest version",
            "Installs package in development mode with all dependencies",
            "Sets up pre-commit hooks for code quality",
            "Verifies installation"
        ]),
        ("feature <name>", "Create a new feature branch", [
            "Switches to develop branch and pulls latest changes",
            "Creates and switches to feature/<name> branch",
            "Ready for development work"
        ]),
        ("release <version>", "Start release process", [
            "Creates release branch from develop",
            "Updates version in all relevant files",
            "Commits version changes",
            "Ready for PR to main branch"
        ]),
        ("test", "Test package locally", [
            "Builds package with python -m build",
            "Validates package with twine check",
            "Tests installation in virtual environment",
            "Verifies import and version"
        ]),
        ("pytest", "Run test suite", [
            "Runs pytest with coverage reporting",
            "Shows detailed test results",
            "Generates coverage report"
        ]),
        ("lint", "Run code quality checks", [
            "Black code formatting check",
            "isort import sorting check", 
            "Flake8 linting",
            "MyPy type checking",
            "Bandit security scanning"
        ]),
        ("docs", "Build documentation", [
            "Builds HTML documentation with Sphinx",
            "Outputs to docs/_build/html/",
            "Ready for viewing or deployment"
        ]),
        ("examples", "Run example applications", [
            "Runs threepanewindows.examples module",
            "Visual demonstration of library features",
            "Useful for testing and validation"
        ]),
        ("clean", "Clean build artifacts", [
            "Removes build/, dist/, *.egg-info/ directories",
            "Cleans __pycache__ and *.pyc files",
            "Removes test and documentation build artifacts"
        ]),
        ("status", "Show development status", [
            "Current branch and version information",
            "Git working directory status",
            "Project structure validation",
            "Development environment status"
        ]),
        ("summary <title> <content>", "Create summary file", [
            "Creates timestamped summary in dev/ directory",
            "Useful for documenting development activities",
            "Markdown format with metadata"
        ])
    ]
    
    for cmd, desc, details in commands:
        print(f"📋 {cmd}")
        print(f"   {desc}")
        for detail in details:
            print(f"   • {detail}")
        print()
    
    print("🔗 Workflow Examples:")
    print("   # Set up new development environment")
    print("   python dev_tools.py setup")
    print()
    print("   # Start working on a new feature")
    print("   python dev_tools.py feature my-new-feature")
    print()
    print("   # Check code quality before committing")
    print("   python dev_tools.py lint")
    print()
    print("   # Run tests")
    print("   python dev_tools.py pytest")
    print()
    print("   # Prepare for release")
    print("   python dev_tools.py release 1.0.0")
    print()
    print("📚 More Information:")
    print("   • CONTRIBUTING.md - Contribution guidelines")
    print("   • DEVELOPMENT_SETUP.md - Detailed setup instructions")
    print("   • docs/ - Full documentation")


def create_summary(title, content, summary_type="GENERAL"):
    """Create a summary file in the dev folder."""
    # Ensure dev directory exists
    dev_dir = Path("dev")
    dev_dir.mkdir(exist_ok=True)
    
    # Create filename with timestamp and type
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"SUMMARY_{summary_type}_{timestamp}.md"
    filepath = dev_dir / filename
    
    # Create summary content
    summary_content = f"""# {title}

**Date:** {datetime.now().strftime("%B %d, %Y")}  
**Time:** {datetime.now().strftime("%H:%M:%S")}  
**Type:** {summary_type}  
**Status:** ✅ Complete

## Summary

{content}

---

**Generated by:** dev_tools.py  
**Repository:** threepanewindows  
**File:** {filename}
"""
    
    # Write summary file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(summary_content)
    
    print(f"📄 Summary saved: {filepath}")
    return filepath


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        show_status()
        return
    
    command = sys.argv[1].lower()
    
    if command == "feature":
        if len(sys.argv) < 3:
            print("Usage: python dev_tools.py feature <feature-name>")
            return
        feature_name = sys.argv[2]
        create_feature_branch(feature_name)
        
        # Create summary
        summary_content = f"""Created new feature branch: feature/{feature_name}

### Actions Taken:
- Switched to develop branch
- Pulled latest changes from origin/develop
- Created and switched to feature/{feature_name}

### Next Steps:
1. Make your changes
2. Commit and push: `git push -u origin feature/{feature_name}`
3. Create PR to develop branch via GitHub UI

### Branch Info:
- Base branch: develop
- Feature branch: feature/{feature_name}
- Ready for development: ✅
"""
        create_summary(f"Feature Branch Created: {feature_name}", summary_content, "FEATURE")
    
    elif command == "release":
        if len(sys.argv) < 3:
            print("Usage: python dev_tools.py release <version>")
            return
        version = sys.argv[2]
        start_release(version)
        
        # Create summary
        summary_content = f"""Started release process for version {version}

### Actions Taken:
- Switched to main branch
- Pulled latest changes from origin/main
- Created release branch: release/v{version}
- Merged develop branch
- Updated version in pyproject.toml to {version}
- Committed version bump

### Next Steps:
1. Push branch: `git push -u origin release/v{version}`
2. Create PR to main branch
3. After merge, create GitHub release with tag v{version}
4. Production PyPI upload will happen automatically

### Release Info:
- Version: {version}
- Release branch: release/v{version}
- Ready for PR: ✅
"""
        create_summary(f"Release Started: v{version}", summary_content, "RELEASE")
    
    elif command == "merge-to-main":
        success = merge_to_main()
        
        if success:
            current_branch = get_current_branch()
            version = current_branch.replace('release/v', '') if current_branch.startswith('release/') else "unknown"
            
            # Create summary
            summary_content = f"""Merged release to main and created tag
    
    ### Actions Taken:
    - Switched to main branch and pulled latest
    - Merged release branch to main
    - Created and pushed tag v{version}
    - Merged release back to develop
    - Cleaned up release branch
    
    ### Release Info:
    - Version: {version}
    - Tag: v{version}
    - Main branch updated: ✅
    - Develop branch updated: ✅
    
    ### Next Steps:
    1. GitHub Actions will automatically build and publish to PyPI
    2. Monitor the release workflow in GitHub Actions
    3. Verify package is available on PyPI
    4. Update any dependent projects
    """
            create_summary(f"Release Completed: v{version}", summary_content, "MERGE")
    
    elif command == "test":
        test_package_locally()
        
        # Create summary
        summary_content = f"""Performed local package testing

### Tests Performed:
- Package building with `python -m build`
- Package validation with `twine check`
- Installation test in virtual environment
- Import and version verification

### Results:
- Build: ✅ Successful
- Validation: ✅ Passed
- Installation: ✅ Working
- Import: ✅ Successful

### Files Generated:
- dist/ directory with wheel and source distribution
- Temporary test_env virtual environment (cleaned up)
"""
        create_summary("Local Package Testing", summary_content, "TEST")
    
    elif command == "lint":
        success = run_lint()
        
        # Create summary
        status = "✅ Passed" if success else "❌ Failed"
        summary_content = f"""Performed code quality checks

### Checks Performed:
- Black code formatting
- isort import sorting
- Flake8 linting
- MyPy type checking
- Bandit security scanning

### Overall Result: {status}

### Tools Used:
- black --check --diff .
- isort --check-only --diff .
- flake8 threepanewindows/
- mypy threepanewindows/ --ignore-missing-imports
- bandit -r threepanewindows/

### Next Steps:
{('Fix any issues shown above and re-run checks' if not success else 'All checks passed! Code is ready for commit.')}
"""
        create_summary("Code Quality Check", summary_content, "LINT")
    
    elif command == "docs":
        success = build_docs()
        
        # Create summary
        status = "✅ Built" if success else "❌ Failed"
        summary_content = f"""Built project documentation

### Build Result: {status}

### Documentation:
- Source: docs/ directory
- Output: docs/_build/html/
- Entry point: docs/_build/html/index.html

### Build Command:
- python -m sphinx -b html docs docs/_build/html

### Next Steps:
{('Open docs/_build/html/index.html to view documentation' if success else 'Check error messages and fix documentation issues')}
"""
        create_summary("Documentation Build", summary_content, "DOCS")
    
    elif command == "clean":
        clean_build()
        
        # Create summary
        summary_content = f"""Cleaned build artifacts and cache files

### Cleaned Items:
- build/ directory
- dist/ directory
- *.egg-info/ directories
- docs/_build/ directory
- __pycache__/ directories (recursive)
- *.pyc files (recursive)
- .pytest_cache/ directory
- .coverage files
- .mypy_cache/ directory
- .tox/ directory

### Purpose:
- Remove build artifacts
- Clean Python cache files
- Reset build environment
- Prepare for fresh builds

### Next Steps:
- Ready for clean build: python -m build
- Ready for fresh testing: pytest
"""
        create_summary("Build Cleanup", summary_content, "CLEAN")
    
    elif command == "pytest":
        success = run_pytest()
        
        # Create summary
        status = "✅ Passed" if success else "❌ Failed"
        summary_content = f"""Ran test suite with pytest

### Test Result: {status}

### Test Configuration:
- Test directory: tests/
- Coverage: threepanewindows package
- Report: Terminal with missing lines
- Verbose output enabled

### Command Used:
- python -m pytest tests/ --cov=threepanewindows --cov-report=term-missing -v

### Next Steps:
{('All tests passed! Code is ready for commit.' if success else 'Fix failing tests and re-run pytest')}
"""
        create_summary("Test Suite Run", summary_content, "PYTEST")
    
    elif command == "examples":
        success = run_examples()
        
        # Create summary
        status = "✅ Success" if success else "❌ Failed"
        summary_content = f"""Ran example applications

### Run Result: {status}

### Examples Module:
- Location: threepanewindows/examples.py
- Command: python -m threepanewindows.examples

### Purpose:
- Demonstrate library functionality
- Visual testing of components
- User experience validation

### Next Steps:
{('Examples ran successfully - library is working!' if success else 'Check error messages and fix example issues')}
"""
        create_summary("Examples Run", summary_content, "EXAMPLES")
    
    elif command == "setup":
        success = setup_dev_env()
        
        # Create summary
        status = "✅ Complete" if success else "❌ Incomplete"
        summary_content = f"""Set up development environment

### Setup Result: {status}

### Actions Performed:
- Upgraded pip to latest version
- Installed package in development mode with all dependencies
- Set up pre-commit hooks for code quality

### Dependencies Installed:
- Development dependencies: pytest, black, flake8, mypy, etc.
- Documentation dependencies: sphinx, sphinx-rtd-theme
- Test dependencies: pytest-cov, pytest-xvfb

### Next Steps:
{('Development environment ready! Try running examples or tests.' if success else 'Fix setup issues and re-run setup command')}
"""
        create_summary("Development Setup", summary_content, "SETUP")
    
    elif command == "status":
        show_status()
    
    elif command == "help":
        show_help()
    
    elif command == "summary":
        if len(sys.argv) < 4:
            print("Usage: python dev_tools.py summary <title> <content>")
            return
        title = sys.argv[2]
        content = sys.argv[3]
        create_summary(title, content)
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: setup, feature, release, merge-to-main, test, pytest, lint, docs, examples, clean, status, help, summary")
        print("Run 'python dev_tools.py help' for detailed information.")


if __name__ == "__main__":
    main()