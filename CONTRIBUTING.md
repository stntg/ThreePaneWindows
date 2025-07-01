# Contributing to ThreePaneWindows

Thank you for your interest in contributing to ThreePaneWindows! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

   ```bash
   git clone https://github.com/yourusername/threepanewindows.git
   cd threepanewindows
   ```

3. **Set up the development environment**:

   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate it (Windows)
   venv\Scripts\activate
   # Or on Unix/macOS
   source venv/bin/activate

   # Install in development mode
   pip install -e .[dev,docs,test]
   ```

4. **Install pre-commit hooks**:

   ```bash
   pre-commit install
   ```

5. **Verify the setup**:

   ```bash
   pytest
   python -m threepanewindows.examples
   ```

## Making Changes

### Branching Strategy

We use a Git Flow-inspired branching model:

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Feature branches
- `hotfix/*` - Critical bug fixes
- `release/*` - Release preparation

### Creating a Feature Branch


```bash
# Switch to develop branch
git checkout develop
git pull origin develop

# Create a new feature branch
git checkout -b feature/your-feature-name

# Make your changes...

# Push the branch
git push -u origin feature/your-feature-name
```

### Coding Standards

We follow these coding standards:

- **PEP 8** for Python code style
- **Black** for code formatting (line length: 88)
- **isort** for import sorting
- **Type hints** for all public APIs
- **Docstrings** for all public functions and classes

### Python Version Compatibility

This project supports Python 3.8 and above. When developing, be aware of:

1. **Python 3.8 Compatibility**: Some features require special handling in Python 3.8:
   - Use `typing-extensions` for newer typing features (like TypedDict, Literal, Protocol)
   - Avoid f-strings with `=` debugging syntax (Python 3.8 doesn't support it)
   - Be careful with Unicode handling in Python 3.8
   - Test your changes with Python 3.8 specifically

2. **CI Testing**: The CI workflow uses different configurations for Python 3.8 vs newer versions:
   - Python 3.8 uses `pytest_py38.ini` and skips certain problematic tests
   - Python 3.9+ uses `pytest_ci.ini` for testing

### Code Quality Tools

Before submitting, ensure your code passes all checks:


```bash
# Format code
black .
isort .

# Lint code
flake8 .
mypy threepanewindows

# Run security checks
bandit -r threepanewindows/
safety check

# Or run all checks with tox
tox -e lint
```

## Testing

### Running Tests


```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=threepanewindows

# Run specific test file
pytest tests/test_fixed.py

# Run tests for specific Python versions
tox -e py38,py39,py310,py311,py312
```

### CI Workflow Tests

To run tests as they would run in the CI workflow:

```bash
# For Python 3.9 and above
pytest -c pytest_ci.ini tests/ -m "not gui"

# For Python 3.8 (which has special handling)
pytest -c pytest_py38.ini tests/ -m "not gui" -k "not test_demo_integration_with_mainloop and not test_run_demo_creates_window and not test_examples_no_longer_hang"
```

The Python 3.8 configuration skips certain tests that may cause stack overflow errors or have compatibility issues with Python 3.8.

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names
- Include both unit and integration tests
- Mock external dependencies
- Test edge cases and error conditions

Example test structure:

```python
import pytest
import tkinter as tk
from threepanewindows import FixedThreePaneWindow

class TestFixedThreePaneWindow:
    def test_initialization(self, root):
        """Test basic initialization."""
        window = FixedThreePaneWindow(root)
        assert window.master == root

    def test_custom_dimensions(self, root):
        """Test initialization with custom dimensions."""
        window = FixedThreePaneWindow(root, left_width=200)
        assert window.left_width == 200
```

### Visual Tests

For GUI components, we have visual tests marked with `@pytest.mark.visual`:


```bash
# Run visual tests (requires display)
pytest -m visual

# Skip visual tests
pytest -m "not visual"
```

## Documentation

### Building Documentation


```bash
# Install documentation dependencies
pip install -e .[docs]

# Build documentation
cd docs
make html

# Or use tox
tox -e docs
```

### Writing Documentation

- Use **reStructuredText** for Sphinx documentation
- Include **docstrings** for all public APIs
- Add **examples** for complex features
- Update **CHANGELOG.md** for user-facing changes

### Documentation Structure

```text
docs/
├── index.rst           # Main documentation page
├── installation.rst    # Installation instructions
├── quickstart.rst      # Quick start guide
├── user_guide/         # Detailed user guides
├── examples/           # Example code and tutorials
├── api/                # API reference
└── _static/            # Static assets
```

## Submitting Changes

### Pull Request Process

1. **Ensure your branch is up to date**:

   ```bash
   git checkout develop
   git pull origin develop
   git checkout feature/your-feature-name
   git rebase develop
   ```

2. **Run the full test suite**:

   ```bash
   tox
   ```

3. **Create a pull request** on GitHub:
    - Use a descriptive title
    - Reference any related issues
    - Describe what changes you made and why
    - Include screenshots for UI changes

4. **Address review feedback**:
    - Make requested changes
    - Push updates to your branch
    - Respond to reviewer comments

### Pull Request Template


```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

## Release Process

### Version Management

We use semantic versioning (SemVer):

- `MAJOR.MINOR.PATCH`
- `MAJOR`: Breaking changes
- `MINOR`: New features (backward compatible)
- `PATCH`: Bug fixes (backward compatible)

### Creating a Release

1. **Create a release branch**:

   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b release/v1.2.0
   ```

2. **Update version numbers**:
    - `threepanewindows/_version.py`
    - `pyproject.toml`
    - `docs/conf.py`

3. **Update CHANGELOG.md**:
    - Add release notes
    - List all changes since last release

4. **Test the release**:

   ```bash
   tox
   python -m build
   twine check dist/*
   ```

5. **Create pull request** to `main`

6. **After merge, create and push tag**:

   ```bash
   git checkout main
   git pull origin main
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin v1.2.0
   ```

7. **GitHub Actions will automatically**:
    - Run tests
    - Build packages
    - Publish to PyPI
    - Create GitHub release

### Hotfix Process

For critical bugs in production:

1. **Create hotfix branch from main**:

   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/critical-bug-fix
   ```

2. **Make minimal fix**
3. **Test thoroughly**
4. **Create PR to main**
5. **After merge, also merge to develop**

## Getting Help

- **GitHub Issues**: Report bugs or request features
- **GitHub Discussions**: Ask questions or discuss ideas
- **Documentation**: Check the docs first
- **Code Review**: Ask for feedback on your changes

## Recognition

Contributors are recognized in:

- `CONTRIBUTORS.md` file
- GitHub contributors page
- Release notes for significant contributions

Thank you for contributing to ThreePaneWindows! 🎉
