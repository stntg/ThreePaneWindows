# GitHub Workflows and CI/CD

This directory contains GitHub Actions workflows and configuration files for continuous integration and deployment.

## CI Workflow

The main CI workflow (`ci.yml`) runs on push to main/develop branches and on pull requests. It:

1. Runs on multiple platforms (Ubuntu, Windows, macOS)
2. Tests against multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)
3. Performs linting, type checking, and testing
4. Uploads coverage reports to Codecov

### Python 3.8 Special Handling

Python 3.8 requires special handling in the CI workflow:

- Uses a dedicated pytest configuration file (`pytest_py38.ini`)
- Skips certain tests that cause issues in Python 3.8:
  - `test_demo_integration_with_mainloop`
  - `test_run_demo_creates_window`
  - `test_examples_no_longer_hang`
- May require additional dependencies (typing-extensions)

### Workflow Configuration

The workflow is configured to:

- Use a virtual display (Xvfb) for GUI tests on Linux
- Continue on mypy errors (type checking is not strictly enforced yet)
- Skip GUI tests in headless environments
- Use different test configurations for different Python versions

## Release Workflow

The release workflow (`release.yml`) is triggered when a new tag is pushed. It:

1. Builds the package
2. Publishes to PyPI
3. Creates a GitHub release

## Documentation Workflow

The documentation workflow (`docs.yml`) builds and deploys documentation to GitHub Pages.

## Modifying Workflows

When modifying workflows:

1. Test changes locally when possible
2. Be aware of platform-specific differences
3. Consider the impact on all supported Python versions
4. Update this README if you make significant changes

## Local Testing

To test workflows locally before pushing:

1. Install [act](https://github.com/nektos/act)
2. Run: `act -j test`

Or manually run the equivalent commands:

```bash
# Linting
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Type checking
mypy threepanewindows --ignore-missing-imports

# Testing (Python 3.9+)
pytest -c pytest_ci.ini tests/ -m "not gui"

# Testing (Python 3.8)
pytest -c pytest_py38.ini tests/ -m "not gui" -k "not test_demo_integration_with_mainloop and not test_run_demo_creates_window and not test_examples_no_longer_hang"
```
