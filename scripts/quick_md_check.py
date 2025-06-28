#!/usr/bin/env python3
"""
Quick Markdown Checker

A simplified version of the markdown checker for quick validation.
Focuses on the most common and critical issues.

Usage:
    python scripts/quick_md_check.py
    python scripts/quick_md_check.py --fix
"""

import argparse
import os
import re
import sys
from pathlib import Path


def find_md_files(root_dir="."):
    """Find all Markdown files."""
    md_files = []
    for pattern in ["*.md", "*.markdown"]:
        md_files.extend(Path(root_dir).rglob(pattern))

    # Exclude common directories
    exclude_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv"}
    filtered_files = []

    for file_path in md_files:
        if not any(exclude_dir in file_path.parts for exclude_dir in exclude_dirs):
            filtered_files.append(str(file_path))

    return sorted(filtered_files)


def check_md_file(file_path, fix_mode=False):
    """Check a single Markdown file for common issues."""
    issues = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                lines = f.readlines()
        except Exception as e:
            return [f"Cannot read file: {e}"]

    fixed_lines = lines[:] if fix_mode else None

    for i, line in enumerate(lines, 1):
        original_line = line.rstrip("\n\r")

        # Check 1: Trailing whitespace
        if original_line != original_line.rstrip():
            issues.append(f"Line {i}: Trailing whitespace")
            if fix_mode:
                fixed_lines[i - 1] = original_line.rstrip() + "\n"

        # Check 2: Tab characters
        if "\t" in original_line:
            issues.append(f"Line {i}: Tab characters (use spaces)")
            if fix_mode:
                fixed_lines[i - 1] = original_line.replace("\t", "    ") + "\n"

        # Check 3: Heading format
        if original_line.startswith("#"):
            # Check for space after #
            if not re.match(r"^#+\s+", original_line) and len(original_line) > 1:
                issues.append(f"Line {i}: Missing space after heading #")
                if fix_mode:
                    match = re.match(r"^(#+)(.+)", original_line)
                    if match:
                        hashes, title = match.groups()
                        fixed_lines[i - 1] = f"{hashes} {title.strip()}\n"

            # Check for trailing #
            if original_line.rstrip().endswith(
                "#"
            ) and not original_line.rstrip().endswith("##"):
                issues.append(f"Line {i}: Remove trailing # from heading")
                if fix_mode:
                    fixed_lines[i - 1] = (
                        original_line.rstrip().rstrip("#").rstrip() + "\n"
                    )

        # Check 4: Code blocks
        if original_line.strip() == "```":
            # Look ahead to see if there's a language
            if i < len(lines):
                next_line = lines[i].strip()
                if next_line and not next_line.startswith("```"):
                    # This might be a code block without language
                    issues.append(f"Line {i}: Consider adding language to code block")

        # Check 5: Common typos
        typos = {
            r"\bthier\b": "their",
            r"\brecieve\b": "receive",
            r"\boccured\b": "occurred",
            r"\bseperate\b": "separate",
        }

        for typo_pattern, correction in typos.items():
            if re.search(typo_pattern, original_line, re.IGNORECASE):
                issues.append(
                    f"Line {i}: Possible typo - '{typo_pattern}' should be '{correction}'"
                )
                if fix_mode:
                    fixed_lines[i - 1] = (
                        re.sub(
                            typo_pattern, correction, original_line, flags=re.IGNORECASE
                        )
                        + "\n"
                    )

        # Check 6: Broken relative links
        link_pattern = r"\[([^\]]*)\]\(([^)]+)\)"
        for match in re.finditer(link_pattern, original_line):
            link_text, url = match.groups()
            if not url.startswith(("http", "mailto:", "#")):
                # Check if relative file exists
                base_dir = os.path.dirname(file_path)
                target_path = os.path.join(base_dir, url)
                if not os.path.exists(target_path):
                    issues.append(f"Line {i}: Broken link - {url}")

    # Check for multiple consecutive blank lines
    if fix_mode and fixed_lines:
        final_lines = []
        blank_count = 0
        for line in fixed_lines:
            if line.strip() == "":
                blank_count += 1
                if blank_count <= 2:
                    final_lines.append(line)
            else:
                blank_count = 0
                final_lines.append(line)

        # Write back if changes were made
        if final_lines != lines:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(final_lines)
                return issues, True  # Fixed
            except Exception as e:
                issues.append(f"Error writing file: {e}")
                return issues, False

    return issues, fix_mode and len(issues) > 0


def main():
    parser = argparse.ArgumentParser(description="Quick Markdown file checker")
    parser.add_argument("--fix", action="store_true", help="Fix issues automatically")
    parser.add_argument("--file", help="Check specific file only")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.file:
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        md_files = [args.file]
    else:
        md_files = find_md_files()

    if not md_files:
        print("No Markdown files found.")
        return

    print(
        f"{'Checking and fixing' if args.fix else 'Checking'} {len(md_files)} Markdown files..."
    )

    total_issues = 0
    files_with_issues = 0
    files_fixed = 0

    for file_path in md_files:
        if args.verbose:
            print(f"Checking: {file_path}")

        result = check_md_file(file_path, args.fix)

        if isinstance(result, tuple):
            issues, was_fixed = result
        else:
            issues = result
            was_fixed = False

        if issues:
            files_with_issues += 1
            total_issues += len(issues)

            if was_fixed:
                files_fixed += 1

            print(f"\n📄 {file_path}")
            for issue in issues:
                print(f"  ⚠️  {issue}")

            if was_fixed:
                print(f"  ✅ Fixed {len(issues)} issues")
        elif args.verbose:
            print(f"  ✅ No issues found")

    # Summary
    print(f"\n📋 Summary:")
    print(f"Files checked: {len(md_files)}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Total issues found: {total_issues}")

    if args.fix:
        print(f"Files fixed: {files_fixed}")

    if total_issues == 0:
        print("✅ All Markdown files are clean!")
    elif args.fix and files_fixed > 0:
        print("✅ Issues have been fixed!")
    else:
        print("⚠️  Issues found. Run with --fix to automatically fix them.")
        sys.exit(1)


if __name__ == "__main__":
    main()
