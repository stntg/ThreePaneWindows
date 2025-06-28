#!/usr/bin/env python3
"""
Release script for ThreePaneWindows.

This script helps automate the release process by:
1. Validating the current state
2. Updating version numbers
3. Updating changelog
4. Creating release branch
5. Running tests
6. Creating and pushing tags

Usage:
    python scripts/release.py --version 1.0.0 --type minor
    python scripts/release.py --version 1.0.1 --type patch
    python scripts/release.py --version 2.0.0 --type major
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Tuple


class ReleaseManager:
    """Manages the release process for ThreePaneWindows."""

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.version_file = root_dir / "threepanewindows" / "_version.py"
        self.pyproject_file = root_dir / "pyproject.toml"
        self.changelog_file = root_dir / "CHANGELOG.md"
        self.docs_conf_file = root_dir / "docs" / "conf.py"

    def run_command(
        self, cmd: List[str], check: bool = True
    ) -> subprocess.CompletedProcess:
        """Run a shell command."""
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.root_dir)

        if check and result.returncode != 0:
            print(f"Command failed with return code {result.returncode}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            sys.exit(1)

        return result

    def get_current_version(self) -> str:
        """Get the current version from _version.py."""
        with open(self.version_file, "r") as f:
            content = f.read()

        match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
        if not match:
            raise ValueError("Could not find version in _version.py")

        return match.group(1)

    def validate_version(self, version: str) -> bool:
        """Validate version format (semantic versioning)."""
        pattern = r"^\d+\.\d+\.\d+(?:-(?:alpha|beta|rc)\d*)?$"
        return bool(re.match(pattern, version))

    def update_version_file(self, new_version: str) -> None:
        """Update the version in _version.py."""
        with open(self.version_file, "r") as f:
            content = f.read()

        # Update __version__
        content = re.sub(
            r'__version__ = ["\'][^"\']+["\']',
            f'__version__ = "{new_version}"',
            content,
        )

        # Update version components
        major, minor, patch = new_version.split(".")[:3]
        content = re.sub(
            r'__version_info__ = tuple\(int\(x\) for x in __version__\.split\("\.")\)',
            f"__version_info__ = ({major}, {minor}, {patch})",
            content,
        )

        with open(self.version_file, "w") as f:
            f.write(content)

        print(f"Updated {self.version_file}")

    def update_pyproject_toml(self, new_version: str) -> None:
        """Update the version in pyproject.toml."""
        with open(self.pyproject_file, "r") as f:
            content = f.read()

        content = re.sub(
            r'version = ["\'][^"\']+["\']', f'version = "{new_version}"', content
        )

        with open(self.pyproject_file, "w") as f:
            f.write(content)

        print(f"Updated {self.pyproject_file}")

    def update_docs_conf(self, new_version: str) -> None:
        """Update the version in docs/conf.py."""
        if not self.docs_conf_file.exists():
            return

        with open(self.docs_conf_file, "r") as f:
            content = f.read()

        # Update version and release
        version_short = ".".join(new_version.split(".")[:2])  # X.Y

        content = re.sub(
            r"version = ['\"][^'\"]+['\"]", f"version = '{version_short}'", content
        )

        content = re.sub(
            r"release = ['\"][^'\"]+['\"]", f"release = '{new_version}'", content
        )

        with open(self.docs_conf_file, "w") as f:
            f.write(content)

        print(f"Updated {self.docs_conf_file}")

    def update_changelog(self, new_version: str, release_type: str) -> None:
        """Update CHANGELOG.md with new version."""
        if not self.changelog_file.exists():
            print("CHANGELOG.md not found, skipping changelog update")
            return

        with open(self.changelog_file, "r") as f:
            content = f.read()

        # Find the "Unreleased" section
        today = datetime.now().strftime("%Y-%m-%d")

        # Replace [Unreleased] with the new version
        content = re.sub(
            r"## \[Unreleased\]", f"## [{new_version}] - {today}", content, count=1
        )

        # Add new Unreleased section at the top
        unreleased_section = f"""## [Unreleased]

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [{new_version}] - {today}"""

        content = re.sub(
            f"## \\[{re.escape(new_version)}\\] - {today}",
            unreleased_section,
            content,
            count=1,
        )

        with open(self.changelog_file, "w") as f:
            f.write(content)

        print(f"Updated {self.changelog_file}")

    def run_tests(self) -> bool:
        """Run the test suite."""
        print("Running tests...")
        try:
            self.run_command(["python", "-m", "pytest", "tests/", "-v"])
            return True
        except SystemExit:
            print("Tests failed!")
            return False

    def run_linting(self) -> bool:
        """Run linting checks."""
        print("Running linting checks...")
        try:
            self.run_command(["python", "-m", "flake8", "threepanewindows/"])
            self.run_command(
                [
                    "python",
                    "-m",
                    "mypy",
                    "threepanewindows/",
                    "--ignore-missing-imports",
                ]
            )
            return True
        except SystemExit:
            print("Linting failed!")
            return False

    def check_git_status(self) -> bool:
        """Check if git working directory is clean."""
        result = self.run_command(["git", "status", "--porcelain"], check=False)
        if result.stdout.strip():
            print("Git working directory is not clean:")
            print(result.stdout)
            return False
        return True

    def create_release_branch(self, version: str) -> None:
        """Create a release branch."""
        branch_name = f"release/v{version}"

        # Ensure we're on develop
        self.run_command(["git", "checkout", "develop"])
        self.run_command(["git", "pull", "origin", "develop"])

        # Create release branch
        self.run_command(["git", "checkout", "-b", branch_name])

        print(f"Created release branch: {branch_name}")

    def commit_changes(self, version: str) -> None:
        """Commit version changes."""
        self.run_command(["git", "add", str(self.version_file)])
        self.run_command(["git", "add", str(self.pyproject_file)])
        self.run_command(["git", "add", str(self.changelog_file)])

        if self.docs_conf_file.exists():
            self.run_command(["git", "add", str(self.docs_conf_file)])

        self.run_command(["git", "commit", "-m", f"Bump version to {version}"])

        print(f"Committed version changes for {version}")

    def create_tag(self, version: str) -> None:
        """Create and push a git tag."""
        tag_name = f"v{version}"

        self.run_command(["git", "tag", "-a", tag_name, "-m", f"Release {version}"])

        print(f"Created tag: {tag_name}")
        print(f"To push the tag, run: git push origin {tag_name}")

    def release(
        self, new_version: str, release_type: str, skip_tests: bool = False
    ) -> None:
        """Perform the complete release process."""
        print(f"Starting release process for version {new_version}")

        # Validate version format
        if not self.validate_version(new_version):
            print(f"Invalid version format: {new_version}")
            sys.exit(1)

        # Get current version
        current_version = self.get_current_version()
        print(f"Current version: {current_version}")
        print(f"New version: {new_version}")

        # Check git status
        if not self.check_git_status():
            print("Please commit or stash your changes before releasing")
            sys.exit(1)

        # Run tests and linting
        if not skip_tests:
            if not self.run_tests():
                sys.exit(1)

            if not self.run_linting():
                sys.exit(1)

        # Create release branch
        self.create_release_branch(new_version)

        # Update version files
        self.update_version_file(new_version)
        self.update_pyproject_toml(new_version)
        self.update_docs_conf(new_version)
        self.update_changelog(new_version, release_type)

        # Commit changes
        self.commit_changes(new_version)

        # Create tag
        self.create_tag(new_version)

        print(f"\n✅ Release {new_version} prepared successfully!")
        print("\nNext steps:")
        print(f"1. Push the release branch: git push -u origin release/v{new_version}")
        print(f"2. Create a PR from release/v{new_version} to main")
        print(f"3. After PR is merged, push the tag: git push origin v{new_version}")
        print("4. The GitHub Actions workflow will handle the rest!")


def main():
    parser = argparse.ArgumentParser(description="Release script for ThreePaneWindows")
    parser.add_argument(
        "--version", required=True, help="New version number (e.g., 1.0.0)"
    )
    parser.add_argument(
        "--type",
        choices=["major", "minor", "patch"],
        required=True,
        help="Type of release",
    )
    parser.add_argument(
        "--skip-tests", action="store_true", help="Skip running tests and linting"
    )

    args = parser.parse_args()

    # Find project root
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent

    # Create release manager and run release
    manager = ReleaseManager(root_dir)
    manager.release(args.version, args.type, args.skip_tests)


if __name__ == "__main__":
    main()
