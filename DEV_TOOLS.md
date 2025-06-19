# Development Tools (dev_tools.py)

The `dev_tools.py` script provides a comprehensive set of commands for ThreePaneWindows development workflow. This tool was adapted from your existing development workflow and customized for this project.

## Quick Start

```bash
# Show current status
python dev_tools.py

# Get detailed help
python dev_tools.py help

# Set up development environment
python dev_tools.py setup
```

## Available Commands

### Environment Setup

- `setup` - Set up development environment with all dependencies
- `clean` - Clean build artifacts and cache files

### Development Workflow

- `feature <name>` - Create a new feature branch from develop
- `release <version>` - Start release process with version updates
- `status` - Show current development status

### Testing & Quality

- `test` - Test package locally with build and installation
- `pytest` - Run test suite with coverage reporting
- `lint` - Run all code quality checks (black, flake8, mypy, bandit)
- `examples` - Run example applications

### Documentation

- `docs` - Build Sphinx documentation

### Utilities

- `summary <title> <content>` - Create timestamped summary files
- `help` - Show detailed help information

## Workflow Examples

### Starting a New Feature

```bash
python dev_tools.py feature my-awesome-feature
# Creates feature/my-awesome-feature branch from develop
# Automatically switches to the new branch
```

### Pre-commit Checks

```bash
python dev_tools.py lint
# Runs black, isort, flake8, mypy, and bandit
# Shows detailed results for each check
```

### Testing

```bash
python dev_tools.py pytest
# Runs full test suite with coverage
# Generates detailed coverage report
```

### Release Process

```bash
python dev_tools.py release 1.0.0
# Creates release/v1.0.0 branch
# Updates version in all files
# Commits changes automatically
```

## Features

### Automatic Summary Generation

Every command automatically creates a timestamped summary file in the `dev/` directory with:

- Command details and results
- Actions performed
- Next steps
- Metadata and timestamps

### Comprehensive Status Display

The status command shows:

- Current branch and version
- Git working directory status
- Project structure validation
- Development environment status
- Available commands

### Safe Command Execution

- Uses `shlex.split()` for safe command parsing
- Proper error handling and reporting
- Cross-platform compatibility (Windows/Unix)

### Integration with Project Structure

- Understands ThreePaneWindows project layout
- Updates multiple version files consistently
- Works with existing CI/CD workflows
- Integrates with pre-commit hooks

## Customization

The tool is designed to be easily customizable for your workflow. Key areas for customization:

### Adding New Commands

Add new functions and integrate them in the `main()` function following the existing pattern.

### Modifying Workflows

Update the branch creation and release processes to match your preferred Git workflow.

### Extending Status Checks

Add more project-specific status checks in the `show_status()` function.

## Summary Files

All commands generate summary files in `dev/SUMMARY_<TYPE>_<timestamp>.md` with:

- Detailed action logs
- Results and status
- Next steps
- Metadata for tracking

This provides a complete audit trail of development activities.

## Integration with Existing Tools

The dev_tools.py integrates seamlessly with:

- **GitHub Actions** - Workflows use same commands
- **Pre-commit hooks** - Lint command matches hook configuration  
- **Tox** - Commands align with tox environments
- **PyPI publishing** - Release process matches CI/CD pipeline

## Tips

1. **Always run status first** to understand current state
2. **Use lint before committing** to catch issues early
3. **Test locally** before pushing with the test command
4. **Check summaries** in dev/ directory for activity history
5. **Use help** for detailed command information

This tool streamlines the entire development workflow from feature creation to release, making it easy to maintain high code quality and consistent processes.
