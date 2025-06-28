#!/usr/bin/env python3
"""
Automated Version Bump and Changelog Update Script

This script automatically:
1. Bumps the version number in all relevant files
2. Updates the changelog with recent changes
3. Commits the changes to git

Usage:
    python scripts/version_bump.py patch    # 1.0.0 -> 1.0.1
    python scripts/version_bump.py minor    # 1.0.0 -> 1.1.0
    python scripts/version_bump.py major    # 1.0.0 -> 2.0.0
    python scripts/version_bump.py 1.2.3    # Set specific version
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd, check=True, capture_output=True):
    """Run a command and return the result."""
    print(f"Running: {cmd}")
    if isinstance(cmd, str):
        cmd = cmd.split()

    result = subprocess.run(cmd, check=check, capture_output=capture_output, text=True)

    if capture_output and result.stdout:
        print(result.stdout.strip())

    return result


def get_current_version():
    """Get the current version from _version.py."""
    version_file = Path("threepanewindows/_version.py")
    if not version_file.exists():
        print("Error: _version.py not found")
        sys.exit(1)

    content = version_file.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)

    print("Error: Version not found in _version.py")
    sys.exit(1)


def parse_version(version_str):
    """Parse version string into major, minor, patch components."""
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-(.+))?$", version_str)
    if not match:
        print(f"Error: Invalid version format: {version_str}")
        sys.exit(1)

    major, minor, patch, suffix = match.groups()
    return int(major), int(minor), int(patch), suffix


def bump_version(current_version, bump_type):
    """Calculate new version based on bump type."""
    major, minor, patch, suffix = parse_version(current_version)

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        # Assume it's a specific version
        if re.match(r"^\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+)?$", bump_type):
            return bump_type
        else:
            print(f"Error: Invalid bump type or version: {bump_type}")
            sys.exit(1)


def update_version_in_file(file_path, old_version, new_version):
    """Update version in a specific file."""
    if not Path(file_path).exists():
        print(f"Warning: {file_path} not found")
        return False

    content = Path(file_path).read_text()

    # Handle different version patterns
    patterns = [
        (
            rf'__version__\s*=\s*["\']({re.escape(old_version)})["\']',
            f'__version__ = "{new_version}"',
        ),
        (
            rf'version\s*=\s*["\']({re.escape(old_version)})["\']',
            f'version = "{new_version}"',
        ),
        (
            rf"version=get_version\(\),",
            f"version=get_version(),",
        ),  # Skip setup.py dynamic version
    ]

    updated = False
    for pattern, replacement in patterns:
        if re.search(pattern, content):
            if "get_version()" not in replacement:  # Skip dynamic version functions
                content = re.sub(pattern, replacement, content)
                updated = True
                break

    if updated:
        Path(file_path).write_text(content)
        print(f"✓ Updated version in {file_path}")
        return True
    else:
        print(f"- No version pattern found in {file_path}")
        return False


def get_recent_commits():
    """Get recent commits for changelog."""
    try:
        result = run_command("git log --oneline -10")
        commits = result.stdout.strip().split("\n")
        return commits
    except subprocess.CalledProcessError:
        print("Warning: Could not get git log")
        return []


def categorize_commit(commit_msg):
    """Categorize commit based on message."""
    commit_lower = commit_msg.lower()

    if any(word in commit_lower for word in ["security", "vulnerability", "cve"]):
        return "Security"
    elif any(word in commit_lower for word in ["fix", "bug", "error", "issue"]):
        return "Fixed"
    elif any(word in commit_lower for word in ["feat", "add", "new"]):
        return "Added"
    elif any(
        word in commit_lower for word in ["refactor", "improve", "enhance", "update"]
    ):
        return "Changed"
    elif any(word in commit_lower for word in ["remove", "delete"]):
        return "Removed"
    elif any(word in commit_lower for word in ["deprecate"]):
        return "Deprecated"
    else:
        return "Changed"


def update_changelog(new_version, old_version):
    """Update CHANGELOG.md with new version and recent changes."""
    changelog_path = Path("CHANGELOG.md")
    if not changelog_path.exists():
        print("Warning: CHANGELOG.md not found")
        return False

    content = changelog_path.read_text()
    date = datetime.now().strftime("%Y-%m-%d")

    # Get recent commits since last version
    commits = get_recent_commits()

    # Categorize commits
    categories = {
        "Security": [],
        "Added": [],
        "Changed": [],
        "Fixed": [],
        "Removed": [],
        "Deprecated": [],
    }

    for commit in commits:
        if commit.strip():
            # Extract commit message (remove hash)
            parts = commit.split(" ", 1)
            if len(parts) > 1:
                commit_msg = parts[1]
                category = categorize_commit(commit_msg)
                categories[category].append(commit_msg)

    # Build new changelog entry
    new_entry = f"\n## [{new_version}] - {date}\n\n"

    # Add categories with content
    for category, items in categories.items():
        if items:
            new_entry += f"### {category}\n\n"
            for item in items:
                # Clean up commit message
                item = item.strip()
                if not item.endswith("."):
                    item += "."
                new_entry += f"- {item}\n"
            new_entry += "\n"

    # If no categorized changes, add a generic entry
    if not any(categories.values()):
        new_entry += "### Changed\n\n- Minor improvements and bug fixes.\n\n"

    # Insert new entry after [Unreleased] section
    unreleased_pattern = r"(## \[Unreleased\].*?(?=## \[|\Z))"
    match = re.search(unreleased_pattern, content, re.DOTALL)

    if match:
        # Insert after unreleased section
        insert_pos = match.end()
        updated_content = content[:insert_pos] + new_entry + content[insert_pos:]
    else:
        # Fallback: insert after first ## heading
        lines = content.split("\n")
        insert_line = 0
        for i, line in enumerate(lines):
            if line.startswith("## "):
                insert_line = i
                break

        if insert_line > 0:
            lines.insert(insert_line, new_entry.strip())
            updated_content = "\n".join(lines)
        else:
            updated_content = content + new_entry

    changelog_path.write_text(updated_content)
    print(f"✓ Updated CHANGELOG.md with version {new_version}")
    return True


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Bump version and update changelog")
    parser.add_argument(
        "bump_type",
        help="Version bump type (major, minor, patch) or specific version (e.g., 1.2.3)",
    )
    parser.add_argument(
        "--no-commit", action="store_true", help="Don't commit changes automatically"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )

    args = parser.parse_args()

    # Change to project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    import os

    os.chdir(project_root)

    # Get current version
    current_version = get_current_version()
    print(f"Current version: {current_version}")

    # Calculate new version
    new_version = bump_version(current_version, args.bump_type)
    print(f"New version: {new_version}")

    if args.dry_run:
        print("\n🔍 DRY RUN - No changes will be made")
        print(f"Would bump version from {current_version} to {new_version}")
        return

    print(f"\n🚀 Bumping version from {current_version} to {new_version}")
    print("=" * 50)

    # Files to update
    files_to_update = [
        "threepanewindows/_version.py",
        "pyproject.toml",
        # __init__.py imports from _version.py, so we don't need to update it
    ]

    updated_files = []

    # Update version in files
    for file_path in files_to_update:
        if update_version_in_file(file_path, current_version, new_version):
            updated_files.append(file_path)

    # Update changelog
    if update_changelog(new_version, current_version):
        updated_files.append("CHANGELOG.md")

    if not updated_files:
        print("No files were updated")
        return

    print(f"\n✓ Updated {len(updated_files)} files:")
    for file_path in updated_files:
        print(f"  - {file_path}")

    # Commit changes
    if not args.no_commit:
        try:
            # Add files
            for file_path in updated_files:
                run_command(f"git add {file_path}")

            # Commit
            commit_msg = f"chore: bump version to {new_version}\n\n- Update version in package files\n- Update CHANGELOG.md with recent changes"
            run_command(["git", "commit", "-m", commit_msg])

            print(
                f"\n✅ Successfully bumped version to {new_version} and committed changes"
            )
            print(f"\nNext steps:")
            print(f"1. Review the changes: git show HEAD")
            print(f"2. Push changes: git push")
            print(f"3. Create a tag: git tag v{new_version}")
            print(f"4. Push tag: git push origin v{new_version}")

        except subprocess.CalledProcessError as e:
            print(f"\n❌ Failed to commit changes: {e}")
            print("Files have been updated but not committed")
    else:
        print(f"\n✅ Successfully bumped version to {new_version}")
        print("Files updated but not committed (--no-commit flag used)")


if __name__ == "__main__":
    main()
