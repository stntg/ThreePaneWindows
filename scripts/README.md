# Markdown Checker Scripts

This directory contains scripts to automatically check and fix Markdown files in
the project.

## Scripts Overview

### 1. `check_fix_markdown.py` - Full-Featured Checker

The comprehensive Markdown checker that handles all types of issues:

- **Heading formatting** - Fixes hierarchy, spacing, and format
- **Code block validation** - Ensures proper formatting and language tags
- **Link validation** - Checks for broken links and malformed URLs
- **List formatting** - Standardizes list markers and indentation
- **Table validation** - Checks table structure and formatting
- **Whitespace cleanup** - Removes trailing spaces and fixes indentation
- **Typo detection** - Finds and fixes common typos
- **Emoji standardization** - Converts emoji codes to Unicode
- **General formatting** - Ensures consistent Markdown style

**Usage:**

```bash
# Check and fix all issues
python scripts/check_fix_markdown.py

# Check only (no fixes)
python scripts/check_fix_markdown.py --check-only

# Verbose output
python scripts/check_fix_markdown.py --verbose

# Check specific file
python scripts/check_fix_markdown.py --file README.md

# Exclude patterns
python scripts/check_fix_markdown.py --exclude "docs/*"
```

### 2. `quick_md_check.py` - Quick Checker

A lightweight checker for the most common issues:

- Trailing whitespace
- Tab characters
- Heading format issues
- Basic typos
- Broken relative links
- Multiple blank lines

**Usage:**

```bash
# Quick check
python scripts/quick_md_check.py

# Quick check and fix
python scripts/quick_md_check.py --fix

# Check specific file
python scripts/quick_md_check.py --file README.md

# Verbose output
python scripts/quick_md_check.py --verbose
```

### 3. Platform-Specific Scripts

#### Windows: `check_markdown.bat`

```cmd
REM Full check and fix
check_markdown.bat

REM Check only
check_markdown.bat --check-only

REM Quick mode with fixes
check_markdown.bat --quick --fix

REM Verbose output
check_markdown.bat --verbose
```

#### Linux/macOS: `check_markdown.sh`

```bash
# Make executable (first time only)
chmod +x scripts/check_markdown.sh

# Full check and fix
./scripts/check_markdown.sh

# Check only
./scripts/check_markdown.sh --check-only

# Quick mode with fixes
./scripts/check_markdown.sh --quick --fix

# Verbose output
./scripts/check_markdown.sh --verbose
```

## Issue Types Detected

### Critical Issues (Errors)

- **Broken links** - Relative links to non-existent files
- **Malformed code blocks** - Unclosed or improperly formatted code blocks
- **Invalid table structure** - Tables with incorrect formatting
- **File encoding issues** - Files that cannot be read properly

### Warnings

- **Heading hierarchy problems** - Skipping heading levels (h1 → h3)
- **Missing language tags** - Code blocks without language specification
- **Inconsistent formatting** - Mixed emphasis styles, inconsistent lists
- **Potential typos** - Common misspellings detected

### Info/Style Issues

- **Trailing whitespace** - Extra spaces at end of lines
- **Tab characters** - Tabs instead of spaces
- **Multiple blank lines** - More than 2 consecutive empty lines
- **Emoji standardization** - Converting :emoji_codes: to Unicode
- **List marker consistency** - Standardizing to `-` for unordered lists

## Configuration

### Typo Detection

The scripts include common typo patterns:

- `their` → `their`
- `receive` → `receive`
- `occurred` → `occurred`
- `separate` → `separate`
- `definitely` → `definitely`

### Emoji Standardization

Common emoji codes are converted to Unicode:

- `✅` → `✅`
- `❌` → `❌`
- `⚠️` → `⚠️`
- `🚀` → `🚀`

### Exclusion Patterns

By default, these directories are excluded:

- `.git`
- `node_modules`
- `**pycache**`
- `.venv`
- `venv`

## Integration with Development Workflow

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
# !/bin/bash
python scripts/quick_md_check.py
if [ $? -ne 0 ]; then
    echo "Markdown issues found."
    echo "Run 'python scripts/quick_md_check.py --fix' to fix them."
    echo "See the documentation for more details."
    exit 1
fi
```bash

### CI/CD Integration

For GitHub Actions (`.github/workflows/markdown-check.yml`):
```yaml
name: Markdown Check
on: [push, pull_request]
jobs:
  markdown-check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Check Markdown files
      run: python scripts/check_fix_markdown.py --check-only
```

### VS Code Integration

Add to `.vscode/tasks.json`:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Check Markdown",
            "type": "shell",
            "command": "python",
            "args": ["scripts/quick_md_check.py"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "Fix Markdown",
            "type": "shell",
            "command": "python",
            "args": ["scripts/check_fix_markdown.py"],
            "group": "build"
        }
    ]
}
```

## Examples

### Check All Files

```bash
# Windows
check_markdown.bat

# Linux/macOS
./scripts/check_markdown.sh

# Direct Python
python scripts/check_fix_markdown.py
```

### Check Only (No Fixes)

```bash
# Windows
check_markdown.bat --check-only

# Linux/macOS
./scripts/check_markdown.sh --check-only

# Direct Python
python scripts/check_fix_markdown.py --check-only
```

### Quick Check and Fix

```bash
# Windows
check_markdown.bat --quick --fix

# Linux/macOS
./scripts/check_markdown.sh --quick --fix

# Direct Python
python scripts/quick_md_check.py --fix
```

### Verbose Output

```bash
# Any platform
python scripts/check_fix_markdown.py --verbose
```

### Check Specific File

```bash
python scripts/check_fix_markdown.py --file README.md
python scripts/quick_md_check.py --file docs/API.md
```

## Output Examples

### Successful Check

```text
✅ No issues found in Markdown files!

📋 Summary:
Files checked: 15
Files with issues: 0
Total issues found: 0
```

### Issues Found

```text
📄 README.md
  ⚠️  Line 23: Trailing whitespace
  ⚠️  Line 45: Missing space after heading #
  ℹ️  Line 67: Consider adding language to code block

📄 docs/API.md
  ❌ Line 12: Broken link - nonexistent.md
  ⚠️  Line 34: Possible typo - 'receive' should be 'receive'

📋 Summary:
Files checked: 15
Files with issues: 2
Total issues found: 5
Files fixed: 2
```sql

## Troubleshooting

### Python Not Found
- **Windows**: Install Python from python.org and ensure it's in PATH
- **Linux**: `sudo apt-get install python3` (Ubuntu/Debian)
- **macOS**: `brew install python3` (with Homebrew)

### Permission Denied (Linux/macOS)
```bash
chmod +x scripts/check_markdown.sh
```

### Encoding Issues

The scripts handle both UTF-8 and Latin-1 encodings automatically.

### Large Files

For very large Markdown files, use the quick checker for better performance:

```bash
python scripts/quick_md_check.py --file large_file.md
```

## Contributing

To add new checks:

1. **Add pattern to `setup_patterns()`** - Define regex patterns
2. **Create check function** - Follow naming convention `check_*`
3. **Add to `check_file()`** - Include in the checking pipeline
4. **Add fix logic** - Implement in `fix_file()` if applicable
5. **Update documentation** - Add to this README

Example new check:

```python
def check_custom_issue(self, file_path: str, lines: List[str]) -> List[MarkdownIssue]:
    """Check for custom issue."""
    issues = []
    for i, line in enumerate(lines, 1):
        if "custom_pattern" in line:
            issues.append(MarkdownIssue(
                file_path=file_path,
                line_number=i,
                issue_type="custom",
                description="Custom issue found",
                original_line=line.rstrip(),
                suggested_fix=line.replace("custom_pattern", "fixed_pattern"),
                severity="warning"
            ))
    return issues
```

## License

These scripts are part of the ThreePaneWindows project and follow the same license
terms.
