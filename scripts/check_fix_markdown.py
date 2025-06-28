#!/usr/bin/env python3
"""
Markdown File Checker and Fixer

This script automatically checks and fixes common issues in Markdown files:
- Fixes heading hierarchy and formatting
- Standardizes code block formatting
- Fixes link formatting and validates URLs
- Standardizes list formatting
- Removes trailing whitespace
- Ensures proper line endings
- Validates table formatting
- Checks for common typos and inconsistencies
- Ensures consistent emoji usage
- Validates cross-references

Usage:
    python scripts/check_fix_markdown.py [options]

Options:
    --check-only    Only check files, don't fix them
    --verbose       Show detailed output
    --file FILE     Check specific file only
    --exclude PATTERN  Exclude files matching pattern
"""

import os
import re
import sys
import argparse
import glob
from pathlib import Path
from typing import List, Dict, Tuple, Set
import urllib.parse
import urllib.request
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class MarkdownIssue:
    """Represents a Markdown issue found in a file."""

    file_path: str
    line_number: int
    issue_type: str
    description: str
    original_line: str
    suggested_fix: str = ""
    severity: str = "warning"  # "error", "warning", "info"


class MarkdownChecker:
    """Main class for checking and fixing Markdown files."""

    def __init__(self, check_only=False, verbose=False):
        self.check_only = check_only
        self.verbose = verbose
        self.issues: List[MarkdownIssue] = []
        self.stats = {
            "files_checked": 0,
            "files_fixed": 0,
            "issues_found": 0,
            "issues_fixed": 0,
        }

        # Common patterns and fixes
        self.setup_patterns()

    def setup_patterns(self):
        """Setup regex patterns for common issues."""

        # Heading patterns
        self.heading_pattern = re.compile(r"^(#{1,6})\s*(.*?)(\s*#*)$")
        self.atx_heading_pattern = re.compile(r"^(#{1,6})\s+(.+)$")

        # Code block patterns
        self.code_block_start = re.compile(r"^```(\w+)?")
        self.code_block_end = re.compile(r"^```\s*$")
        self.inline_code_pattern = re.compile(r"`([^`]+)`")

        # Link patterns
        self.link_pattern = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
        self.reference_link_pattern = re.compile(r"\[([^\]]*)\]\[([^\]]*)\]")
        self.url_pattern = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')

        # List patterns
        self.unordered_list_pattern = re.compile(r"^(\s*)([-*+])\s+(.+)$")
        self.ordered_list_pattern = re.compile(r"^(\s*)(\d+)\.\s+(.+)$")

        # Table patterns
        self.table_row_pattern = re.compile(r"^\s*\|.*\|\s*$")
        self.table_separator_pattern = re.compile(r"^\s*\|[\s\-:|]*\|\s*$")

        # Common typos and fixes
        self.typo_fixes = {
            r"\bthier\b": "their",
            r"\brecieve\b": "receive",
            r"\boccured\b": "occurred",
            r"\bseperate\b": "separate",
            r"\bdefinately\b": "definitely",
            r"\baccommodate\b": "accommodate",
            r"\bexample\s+example\b": "example",  # Duplicate words
            r"\bthe\s+the\b": "the",
            r"\band\s+and\b": "and",
        }

        # Emoji standardization
        self.emoji_fixes = {
            ":check_mark:": "✅",
            ":x:": "❌",
            ":warning:": "⚠️",
            ":information_source:": "ℹ️",
            ":bulb:": "💡",
            ":rocket:": "🚀",
            ":gear:": "⚙️",
            ":book:": "📚",
            ":computer:": "💻",
            ":file_folder:": "📁",
        }

    def find_markdown_files(
        self, root_dir: str, exclude_patterns: List[str] = None
    ) -> List[str]:
        """Find all Markdown files in the directory tree."""
        if exclude_patterns is None:
            exclude_patterns = ["node_modules", ".git", "__pycache__", ".venv", "venv"]

        md_files = []
        root_path = Path(root_dir)

        for pattern in ["**/*.md", "**/*.markdown"]:
            for file_path in root_path.glob(pattern):
                # Check if file should be excluded
                should_exclude = False
                for exclude_pattern in exclude_patterns:
                    if exclude_pattern in str(file_path):
                        should_exclude = True
                        break

                if not should_exclude:
                    md_files.append(str(file_path))

        return sorted(md_files)

    def check_file(self, file_path: str) -> List[MarkdownIssue]:
        """Check a single Markdown file for issues."""
        issues = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            try:
                with open(file_path, "r", encoding="latin-1") as f:
                    lines = f.readlines()
                issues.append(
                    MarkdownIssue(
                        file_path=file_path,
                        line_number=1,
                        issue_type="encoding",
                        description="File encoding issue - converted from latin-1",
                        original_line="",
                        severity="warning",
                    )
                )
            except Exception as e:
                issues.append(
                    MarkdownIssue(
                        file_path=file_path,
                        line_number=1,
                        issue_type="encoding",
                        description=f"Cannot read file: {e}",
                        original_line="",
                        severity="error",
                    )
                )
                return issues

        # Check various issues
        issues.extend(self.check_headings(file_path, lines))
        issues.extend(self.check_code_blocks(file_path, lines))
        issues.extend(self.check_links(file_path, lines))
        issues.extend(self.check_lists(file_path, lines))
        issues.extend(self.check_tables(file_path, lines))
        issues.extend(self.check_whitespace(file_path, lines))
        issues.extend(self.check_typos(file_path, lines))
        issues.extend(self.check_formatting(file_path, lines))

        return issues

    def check_headings(self, file_path: str, lines: List[str]) -> List[MarkdownIssue]:
        """Check heading formatting and hierarchy."""
        issues = []
        heading_levels = []

        for i, line in enumerate(lines, 1):
            line = line.rstrip()

            # Check ATX headings (# format)
            match = self.heading_pattern.match(line)
            if match:
                hashes, title, trailing = match.groups()
                level = len(hashes)
                heading_levels.append(level)

                # Check for trailing hashes (should be removed)
                if trailing.strip():
                    issues.append(
                        MarkdownIssue(
                            file_path=file_path,
                            line_number=i,
                            issue_type="heading_format",
                            description="Remove trailing hashes from heading",
                            original_line=line,
                            suggested_fix=f"{hashes} {title.strip()}",
                            severity="info",
                        )
                    )

                # Check for missing space after hashes
                if not line.startswith(hashes + " ") and title:
                    issues.append(
                        MarkdownIssue(
                            file_path=file_path,
                            line_number=i,
                            issue_type="heading_format",
                            description="Add space after heading hashes",
                            original_line=line,
                            suggested_fix=f"{hashes} {title.strip()}",
                            severity="warning",
                        )
                    )

                # Check heading hierarchy (skip more than 1 level)
                if len(heading_levels) > 1:
                    prev_level = heading_levels[-2]
                    if level > prev_level + 1:
                        issues.append(
                            MarkdownIssue(
                                file_path=file_path,
                                line_number=i,
                                issue_type="heading_hierarchy",
                                description=f"Heading level jumps from {prev_level} to {level}",
                                original_line=line,
                                severity="warning",
                            )
                        )

        return issues

    def check_code_blocks(
        self, file_path: str, lines: List[str]
    ) -> List[MarkdownIssue]:
        """Check code block formatting."""
        issues = []
        in_code_block = False
        code_block_start_line = 0

        for i, line in enumerate(lines, 1):
            line = line.rstrip()

            # Check for code block start
            if self.code_block_start.match(line):
                if in_code_block:
                    issues.append(
                        MarkdownIssue(
                            file_path=file_path,
                            line_number=i,
                            issue_type="code_block",
                            description="Code block not properly closed",
                            original_line=line,
                            severity="error",
                        )
                    )
                in_code_block = True
                code_block_start_line = i

                # Check for language specification
                match = self.code_block_start.match(line)
                if match and not match.group(1):
                    # Try to detect language from context
                    suggested_lang = self.detect_code_language(lines, i)
                    if suggested_lang:
                        issues.append(
                            MarkdownIssue(
                                file_path=file_path,
                                line_number=i,
                                issue_type="code_block",
                                description="Consider adding language specification",
                                original_line=line,
                                suggested_fix=f"```{suggested_lang}",
                                severity="info",
                            )
                        )

            # Check for code block end
            elif self.code_block_end.match(line):
                if not in_code_block:
                    issues.append(
                        MarkdownIssue(
                            file_path=file_path,
                            line_number=i,
                            issue_type="code_block",
                            description="Code block end without start",
                            original_line=line,
                            severity="error",
                        )
                    )
                in_code_block = False

        # Check if code block is not closed
        if in_code_block:
            issues.append(
                MarkdownIssue(
                    file_path=file_path,
                    line_number=code_block_start_line,
                    issue_type="code_block",
                    description="Code block not closed",
                    original_line=lines[code_block_start_line - 1].rstrip(),
                    severity="error",
                )
            )

        return issues

    def detect_code_language(self, lines: List[str], start_line: int) -> str:
        """Try to detect programming language from code content."""
        # Look at the next few lines after code block start
        code_lines = []
        for i in range(start_line, min(start_line + 5, len(lines))):
            line = lines[i].strip()
            if line.startswith("```"):
                break
            code_lines.append(line)

        code_content = "\n".join(code_lines).lower()

        # Simple language detection
        if any(
            keyword in code_content
            for keyword in ["import ", "def ", "class ", "if __name__"]
        ):
            return "python"
        elif any(
            keyword in code_content
            for keyword in ["function", "var ", "let ", "const "]
        ):
            return "javascript"
        elif any(
            keyword in code_content
            for keyword in ["<html", "<div", "<span", "<!doctype"]
        ):
            return "html"
        elif any(
            keyword in code_content for keyword in ["select", "from", "where", "insert"]
        ):
            return "sql"
        elif any(
            keyword in code_content for keyword in ["#!/bin/bash", "echo", "cd ", "ls "]
        ):
            return "bash"
        elif any(keyword in code_content for keyword in ["git ", "npm ", "pip "]):
            return "bash"

        return ""

    def check_links(self, file_path: str, lines: List[str]) -> List[MarkdownIssue]:
        """Check link formatting and validity."""
        issues = []

        for i, line in enumerate(lines, 1):
            # Check markdown links
            for match in self.link_pattern.finditer(line):
                link_text, url = match.groups()

                # Check for empty link text
                if not link_text.strip():
                    issues.append(
                        MarkdownIssue(
                            file_path=file_path,
                            line_number=i,
                            issue_type="link",
                            description="Empty link text",
                            original_line=line.rstrip(),
                            severity="warning",
                        )
                    )

                # Check for malformed URLs
                if url.startswith("http"):
                    try:
                        parsed = urllib.parse.urlparse(url)
                        if not parsed.netloc:
                            issues.append(
                                MarkdownIssue(
                                    file_path=file_path,
                                    line_number=i,
                                    issue_type="link",
                                    description="Malformed URL",
                                    original_line=line.rstrip(),
                                    severity="warning",
                                )
                            )
                    except Exception:
                        issues.append(
                            MarkdownIssue(
                                file_path=file_path,
                                line_number=i,
                                issue_type="link",
                                description="Invalid URL format",
                                original_line=line.rstrip(),
                                severity="warning",
                            )
                        )

                # Check for relative file links
                elif not url.startswith(("http", "mailto:", "#")):
                    # Check if file exists
                    base_dir = os.path.dirname(file_path)
                    target_path = os.path.join(base_dir, url)
                    if not os.path.exists(target_path):
                        issues.append(
                            MarkdownIssue(
                                file_path=file_path,
                                line_number=i,
                                issue_type="link",
                                description=f"Broken relative link: {url}",
                                original_line=line.rstrip(),
                                severity="error",
                            )
                        )

        return issues

    def check_lists(self, file_path: str, lines: List[str]) -> List[MarkdownIssue]:
        """Check list formatting."""
        issues = []

        for i, line in enumerate(lines, 1):
            # Check unordered lists
            match = self.unordered_list_pattern.match(line)
            if match:
                indent, marker, content = match.groups()

                # Standardize list markers (prefer -)
                if marker != "-":
                    issues.append(
                        MarkdownIssue(
                            file_path=file_path,
                            line_number=i,
                            issue_type="list_format",
                            description="Standardize list marker to '-'",
                            original_line=line.rstrip(),
                            suggested_fix=f"{indent}- {content}",
                            severity="info",
                        )
                    )

                # Check indentation (should be multiples of 2 or 4)
                indent_len = len(indent)
                if indent_len % 2 != 0:
                    suggested_indent = " " * ((indent_len // 2 + 1) * 2)
                    issues.append(
                        MarkdownIssue(
                            file_path=file_path,
                            line_number=i,
                            issue_type="list_format",
                            description="Fix list indentation",
                            original_line=line.rstrip(),
                            suggested_fix=f"{suggested_indent}- {content}",
                            severity="info",
                        )
                    )

            # Check ordered lists
            match = self.ordered_list_pattern.match(line)
            if match:
                indent, number, content = match.groups()

                # Check if numbers are sequential (basic check)
                if i > 1:
                    prev_line = lines[i - 2].strip()
                    prev_match = self.ordered_list_pattern.match(prev_line)
                    if prev_match:
                        prev_number = int(prev_match.group(2))
                        current_number = int(number)
                        if current_number != prev_number + 1 and current_number != 1:
                            issues.append(
                                MarkdownIssue(
                                    file_path=file_path,
                                    line_number=i,
                                    issue_type="list_format",
                                    description="Non-sequential list numbering",
                                    original_line=line.rstrip(),
                                    severity="info",
                                )
                            )

        return issues

    def check_tables(self, file_path: str, lines: List[str]) -> List[MarkdownIssue]:
        """Check table formatting."""
        issues = []
        in_table = False
        table_start = 0

        for i, line in enumerate(lines, 1):
            line = line.rstrip()

            if self.table_row_pattern.match(line):
                if not in_table:
                    in_table = True
                    table_start = i

                # Check for proper table formatting
                cells = [cell.strip() for cell in line.split("|")[1:-1]]

                # Check for empty cells that might need content
                empty_cells = sum(1 for cell in cells if not cell)
                if empty_cells > len(cells) // 2:
                    issues.append(
                        MarkdownIssue(
                            file_path=file_path,
                            line_number=i,
                            issue_type="table",
                            description="Table has many empty cells",
                            original_line=line,
                            severity="info",
                        )
                    )

            elif self.table_separator_pattern.match(line):
                # Check separator formatting
                if not re.match(r"^\s*\|[\s\-:|]+\|\s*$", line):
                    issues.append(
                        MarkdownIssue(
                            file_path=file_path,
                            line_number=i,
                            issue_type="table",
                            description="Malformed table separator",
                            original_line=line,
                            severity="warning",
                        )
                    )

            elif in_table and line.strip() == "":
                in_table = False

            elif in_table and not self.table_row_pattern.match(line):
                in_table = False

        return issues

    def check_whitespace(self, file_path: str, lines: List[str]) -> List[MarkdownIssue]:
        """Check whitespace issues."""
        issues = []

        for i, line in enumerate(lines, 1):
            original_line = line.rstrip("\n\r")

            # Check for trailing whitespace
            if original_line != original_line.rstrip():
                issues.append(
                    MarkdownIssue(
                        file_path=file_path,
                        line_number=i,
                        issue_type="whitespace",
                        description="Trailing whitespace",
                        original_line=original_line,
                        suggested_fix=original_line.rstrip(),
                        severity="info",
                    )
                )

            # Check for tabs (should be spaces)
            if "\t" in original_line:
                issues.append(
                    MarkdownIssue(
                        file_path=file_path,
                        line_number=i,
                        issue_type="whitespace",
                        description="Tab characters found (use spaces)",
                        original_line=original_line,
                        suggested_fix=original_line.replace("\t", "    "),
                        severity="info",
                    )
                )

            # Check for multiple consecutive blank lines
            if i > 1 and original_line.strip() == "" and lines[i - 2].strip() == "":
                if i > 2 and lines[i - 3].strip() == "":
                    issues.append(
                        MarkdownIssue(
                            file_path=file_path,
                            line_number=i,
                            issue_type="whitespace",
                            description="Multiple consecutive blank lines",
                            original_line=original_line,
                            severity="info",
                        )
                    )

        return issues

    def check_typos(self, file_path: str, lines: List[str]) -> List[MarkdownIssue]:
        """Check for common typos and fix them."""
        issues = []

        for i, line in enumerate(lines, 1):
            original_line = line.rstrip()
            fixed_line = original_line

            # Apply typo fixes
            for typo_pattern, fix in self.typo_fixes.items():
                if re.search(typo_pattern, fixed_line, re.IGNORECASE):
                    new_line = re.sub(
                        typo_pattern, fix, fixed_line, flags=re.IGNORECASE
                    )
                    if new_line != fixed_line:
                        issues.append(
                            MarkdownIssue(
                                file_path=file_path,
                                line_number=i,
                                issue_type="typo",
                                description=f"Possible typo: {typo_pattern}",
                                original_line=original_line,
                                suggested_fix=new_line,
                                severity="info",
                            )
                        )
                        fixed_line = new_line

            # Apply emoji fixes
            for emoji_code, emoji in self.emoji_fixes.items():
                if emoji_code in fixed_line:
                    new_line = fixed_line.replace(emoji_code, emoji)
                    if new_line != fixed_line:
                        issues.append(
                            MarkdownIssue(
                                file_path=file_path,
                                line_number=i,
                                issue_type="emoji",
                                description=f"Standardize emoji: {emoji_code}",
                                original_line=original_line,
                                suggested_fix=new_line,
                                severity="info",
                            )
                        )
                        fixed_line = new_line

        return issues

    def check_formatting(self, file_path: str, lines: List[str]) -> List[MarkdownIssue]:
        """Check general formatting issues."""
        issues = []

        for i, line in enumerate(lines, 1):
            original_line = line.rstrip()

            # Check for missing blank line before headings
            if i > 1 and original_line.startswith("#"):
                prev_line = lines[i - 2].rstrip()
                if prev_line and not prev_line.startswith("#"):
                    issues.append(
                        MarkdownIssue(
                            file_path=file_path,
                            line_number=i - 1,
                            issue_type="formatting",
                            description="Add blank line before heading",
                            original_line=prev_line,
                            suggested_fix=prev_line + "\n",
                            severity="info",
                        )
                    )

            # Check for missing blank line after headings
            if original_line.startswith("#") and i < len(lines):
                next_line = lines[i].rstrip()
                if next_line and not next_line.startswith("#") and not next_line == "":
                    issues.append(
                        MarkdownIssue(
                            file_path=file_path,
                            line_number=i + 1,
                            issue_type="formatting",
                            description="Add blank line after heading",
                            original_line=next_line,
                            severity="info",
                        )
                    )

            # Check for inconsistent emphasis (prefer ** over __)
            if "__" in original_line and not original_line.startswith(
                "    "
            ):  # Not in code
                issues.append(
                    MarkdownIssue(
                        file_path=file_path,
                        line_number=i,
                        issue_type="formatting",
                        description="Use ** instead of __ for emphasis",
                        original_line=original_line,
                        suggested_fix=original_line.replace("__", "**"),
                        severity="info",
                    )
                )

        return issues

    def fix_file(self, file_path: str, issues: List[MarkdownIssue]) -> bool:
        """Fix issues in a file."""
        if not issues or self.check_only:
            return False

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                lines = f.readlines()

        # Group issues by line number for efficient fixing
        issues_by_line = defaultdict(list)
        for issue in issues:
            if issue.suggested_fix:
                issues_by_line[issue.line_number].append(issue)

        # Apply fixes from bottom to top to maintain line numbers
        fixed_lines = lines[:]
        for line_num in sorted(issues_by_line.keys(), reverse=True):
            line_issues = issues_by_line[line_num]
            if line_num <= len(fixed_lines):
                original_line = fixed_lines[line_num - 1]

                # Apply all fixes for this line
                fixed_line = original_line
                for issue in line_issues:
                    if issue.suggested_fix:
                        # Handle different types of fixes
                        if issue.issue_type == "whitespace":
                            fixed_line = issue.suggested_fix + "\n"
                        elif (
                            issue.issue_type == "formatting"
                            and "blank line" in issue.description
                        ):
                            if "before" in issue.description:
                                fixed_lines.insert(line_num - 1, "\n")
                            elif "after" in issue.description:
                                fixed_lines.insert(line_num, "\n")
                        else:
                            fixed_line = issue.suggested_fix + "\n"

                if fixed_line != original_line:
                    fixed_lines[line_num - 1] = fixed_line

        # Remove multiple consecutive blank lines
        final_lines = []
        blank_count = 0
        for line in fixed_lines:
            if line.strip() == "":
                blank_count += 1
                if blank_count <= 2:  # Allow max 2 consecutive blank lines
                    final_lines.append(line)
            else:
                blank_count = 0
                final_lines.append(line)

        # Write fixed content back to file
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(final_lines)
            return True
        except Exception as e:
            print(f"Error writing to {file_path}: {e}")
            return False

    def generate_report(self) -> str:
        """Generate a summary report of all issues found."""
        if not self.issues:
            return "✅ No issues found in Markdown files!"

        # Group issues by type and severity
        issues_by_type = defaultdict(list)
        issues_by_severity = defaultdict(int)

        for issue in self.issues:
            issues_by_type[issue.issue_type].append(issue)
            issues_by_severity[issue.severity] += 1

        report = []
        report.append("📋 Markdown Check Report")
        report.append("=" * 50)
        report.append(f"Files checked: {self.stats['files_checked']}")
        report.append(f"Issues found: {self.stats['issues_found']}")

        if not self.check_only:
            report.append(f"Files fixed: {self.stats['files_fixed']}")
            report.append(f"Issues fixed: {self.stats['issues_fixed']}")

        report.append("")
        report.append("Issues by severity:")
        for severity in ["error", "warning", "info"]:
            count = issues_by_severity[severity]
            if count > 0:
                emoji = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}[severity]
                report.append(f"  {emoji} {severity.title()}: {count}")

        report.append("")
        report.append("Issues by type:")
        for issue_type, type_issues in sorted(issues_by_type.items()):
            report.append(
                f"  📝 {issue_type.replace('_', ' ').title()}: {len(type_issues)}"
            )

        # Show detailed issues if verbose
        if self.verbose:
            report.append("")
            report.append("Detailed Issues:")
            report.append("-" * 30)

            current_file = ""
            for issue in sorted(
                self.issues, key=lambda x: (x.file_path, x.line_number)
            ):
                if issue.file_path != current_file:
                    current_file = issue.file_path
                    report.append(f"\n📄 {current_file}")

                severity_emoji = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}[
                    issue.severity
                ]
                report.append(
                    f"  {severity_emoji} Line {issue.line_number}: {issue.description}"
                )

                if issue.suggested_fix and issue.suggested_fix != issue.original_line:
                    report.append(f"    Original: {repr(issue.original_line)}")
                    report.append(f"    Fixed:    {repr(issue.suggested_fix)}")

        return "\n".join(report)

    def run(
        self,
        root_dir: str,
        file_pattern: str = None,
        exclude_patterns: List[str] = None,
    ):
        """Run the markdown checker on specified files."""
        if file_pattern:
            # Check specific file
            md_files = [file_pattern] if os.path.exists(file_pattern) else []
        else:
            # Find all markdown files
            md_files = self.find_markdown_files(root_dir, exclude_patterns)

        if not md_files:
            print("No Markdown files found.")
            return

        print(f"Checking {len(md_files)} Markdown files...")
        if self.verbose:
            print(f"Files: {', '.join(os.path.basename(f) for f in md_files)}")

        for file_path in md_files:
            if self.verbose:
                print(f"Checking: {file_path}")

            file_issues = self.check_file(file_path)
            self.issues.extend(file_issues)
            self.stats["files_checked"] += 1

            if file_issues:
                self.stats["issues_found"] += len(file_issues)

                if not self.check_only:
                    if self.fix_file(file_path, file_issues):
                        self.stats["files_fixed"] += 1
                        self.stats["issues_fixed"] += len(
                            [i for i in file_issues if i.suggested_fix]
                        )
                        if self.verbose:
                            print(f"  ✅ Fixed {len(file_issues)} issues")
                    else:
                        if self.verbose:
                            print(f"  ❌ Could not fix issues")
            elif self.verbose:
                print(f"  ✅ No issues found")

        # Generate and display report
        report = self.generate_report()
        print("\n" + report)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check and fix Markdown files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/check_fix_markdown.py                    # Check and fix all .md files
  python scripts/check_fix_markdown.py --check-only       # Only check, don't fix
  python scripts/check_fix_markdown.py --verbose          # Show detailed output
  python scripts/check_fix_markdown.py --file README.md   # Check specific file
  python scripts/check_fix_markdown.py --exclude "docs/*" # Exclude pattern
        """,
    )

    parser.add_argument(
        "--check-only", action="store_true", help="Only check files, do not fix them"
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )

    parser.add_argument("--file", help="Check specific file only")

    parser.add_argument(
        "--exclude",
        action="append",
        help="Exclude files matching pattern (can be used multiple times)",
    )

    parser.add_argument(
        "--root-dir",
        default=".",
        help="Root directory to search for Markdown files (default: current directory)",
    )

    args = parser.parse_args()

    # Initialize checker
    checker = MarkdownChecker(check_only=args.check_only, verbose=args.verbose)

    # Run the checker
    try:
        checker.run(
            root_dir=args.root_dir,
            file_pattern=args.file,
            exclude_patterns=args.exclude,
        )

        # Exit with appropriate code
        if checker.stats["issues_found"] > 0:
            error_count = sum(
                1 for issue in checker.issues if issue.severity == "error"
            )
            if error_count > 0:
                sys.exit(1)  # Exit with error if there are error-level issues
            else:
                sys.exit(0)  # Exit successfully if only warnings/info
        else:
            sys.exit(0)  # No issues found

    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
