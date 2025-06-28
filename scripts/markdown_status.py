#!/usr/bin/env python3
"""
Markdown Status Report

Generate a comprehensive status report of all Markdown files in the project.
Shows file counts, issue summaries, and overall health metrics.

Usage:
    python scripts/markdown_status.py
"""

import os
import sys
from pathlib import Path
from quick_md_check import find_md_files, check_md_file


def generate_status_report():
    """Generate comprehensive markdown status report."""

    print("📋 ThreePaneWindows Markdown Status Report")
    print("=" * 60)
    print()

    # Find all markdown files
    md_files = find_md_files()

    if not md_files:
        print("❌ No Markdown files found.")
        return

    # Categorize files
    categories = {
        "root": [],
        "docs": [],
        "dev_files": [],
        "tests": [],
        "scripts": [],
        "other": [],
    }

    for file_path in md_files:
        path_parts = Path(file_path).parts

        if len(path_parts) == 1:
            categories["root"].append(file_path)
        elif "docs" in path_parts:
            categories["docs"].append(file_path)
        elif "dev_files" in path_parts:
            categories["dev_files"].append(file_path)
        elif "tests" in path_parts:
            categories["tests"].append(file_path)
        elif "scripts" in path_parts:
            categories["scripts"].append(file_path)
        else:
            categories["other"].append(file_path)

    # File statistics
    print("📊 File Statistics:")
    print(f"Total Markdown files: {len(md_files)}")
    print()

    for category, files in categories.items():
        if files:
            print(f"  📁 {category.replace('_', ' ').title()}: {len(files)} files")
            if category == "root":
                for file_path in sorted(files):
                    print(f"    • {os.path.basename(file_path)}")

    print()

    # Check all files for issues
    print("🔍 Issue Analysis:")
    print("-" * 30)

    total_issues = 0
    files_with_issues = 0
    issue_types = {"critical": 0, "warnings": 0, "suggestions": 0}

    critical_keywords = ["broken link", "cannot read", "malformed", "invalid"]
    warning_keywords = [
        "trailing whitespace",
        "tab characters",
        "missing space",
        "typo",
    ]

    files_by_status = {"clean": [], "minor_issues": [], "needs_attention": []}

    for file_path in md_files:
        issues, _ = check_md_file(file_path, fix_mode=False)

        if not issues:
            files_by_status["clean"].append(file_path)
        else:
            total_issues += len(issues)
            files_with_issues += 1

            # Categorize issues
            critical_count = 0
            warning_count = 0
            suggestion_count = 0

            for issue in issues:
                issue_lower = issue.lower()
                if any(keyword in issue_lower for keyword in critical_keywords):
                    critical_count += 1
                    issue_types["critical"] += 1
                elif any(keyword in issue_lower for keyword in warning_keywords):
                    warning_count += 1
                    issue_types["warnings"] += 1
                else:
                    suggestion_count += 1
                    issue_types["suggestions"] += 1

            # Categorize file by severity
            if critical_count > 0:
                files_by_status["needs_attention"].append((file_path, len(issues)))
            else:
                files_by_status["minor_issues"].append((file_path, len(issues)))

    # Issue summary
    print(f"Files with issues: {files_with_issues}/{len(md_files)}")
    print(f"Total issues found: {total_issues}")
    print()

    print("Issue breakdown:")
    if issue_types["critical"] > 0:
        print(f"  ❌ Critical: {issue_types['critical']}")
    if issue_types["warnings"] > 0:
        print(f"  ⚠️  Warnings: {issue_types['warnings']}")
    if issue_types["suggestions"] > 0:
        print(f"  💡 Suggestions: {issue_types['suggestions']}")

    print()

    # File status breakdown
    print("📈 File Health Status:")
    print(f"  ✅ Clean files: {len(files_by_status['clean'])}")
    print(f"  💛 Minor issues: {len(files_by_status['minor_issues'])}")
    print(f"  🔴 Needs attention: {len(files_by_status['needs_attention'])}")

    print()

    # Show files needing attention
    if files_by_status["needs_attention"]:
        print("🚨 Files Needing Attention:")
        for file_path, issue_count in sorted(
            files_by_status["needs_attention"], key=lambda x: x[1], reverse=True
        ):
            print(f"  • {file_path} ({issue_count} issues)")
        print()

    # Show files with minor issues (top 5)
    if files_by_status["minor_issues"]:
        print("💛 Files with Minor Issues (top 5):")
        top_minor = sorted(
            files_by_status["minor_issues"], key=lambda x: x[1], reverse=True
        )[:5]
        for file_path, issue_count in top_minor:
            print(f"  • {file_path} ({issue_count} issues)")

        if len(files_by_status["minor_issues"]) > 5:
            print(f"  ... and {len(files_by_status['minor_issues']) - 5} more")
        print()

    # Overall health score
    clean_percentage = (len(files_by_status["clean"]) / len(md_files)) * 100

    print("🏥 Overall Health Score:")
    if clean_percentage >= 90:
        health_emoji = "🟢"
        health_status = "Excellent"
    elif clean_percentage >= 75:
        health_emoji = "🟡"
        health_status = "Good"
    elif clean_percentage >= 50:
        health_emoji = "🟠"
        health_status = "Fair"
    else:
        health_emoji = "🔴"
        health_status = "Needs Work"

    print(f"  {health_emoji} {clean_percentage:.1f}% clean files - {health_status}")

    # Recommendations
    print()
    print("💡 Recommendations:")

    if issue_types["critical"] > 0:
        print(
            "  1. ❗ Fix critical issues immediately (broken links, malformed content)"
        )

    if issue_types["warnings"] > 0:
        print("  2. ⚠️  Address warnings for better consistency")
        print("     Run: python scripts/quick_md_check.py --fix")

    if issue_types["suggestions"] > 0:
        print("  3. 💡 Consider implementing suggestions for improved quality")
        print("     Run: python scripts/check_fix_markdown.py")

    if len(files_by_status["clean"]) == len(md_files):
        print("  🎉 All files are clean! Great job maintaining quality documentation!")

    print()
    print("🔧 Quick Actions:")
    print("  • Fix all auto-fixable issues: python scripts/quick_md_check.py --fix")
    print("  • Comprehensive check: python scripts/check_fix_markdown.py --verbose")
    print("  • Check specific file: python scripts/quick_md_check.py --file <filename>")

    return len(files_by_status["clean"]) == len(md_files)


def main():
    """Main entry point."""
    try:
        all_clean = generate_status_report()
        sys.exit(0 if all_clean else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
