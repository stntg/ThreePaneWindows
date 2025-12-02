# Dependency Updates - ThreePaneWindows (2024-2025)

## Overview

This document outlines all dependency version updates made to the ThreePaneWindows project to ensure compatibility with the latest package versions, security patches, and Python 3.13 support.

**Update Date**: December 2025  
**Update Scope**: All dependencies, workflows, and configuration files

---

## Summary of Changes

### Build System & Core Dependencies

#### pyproject.toml

| Component | Old Version | New Version | Reason |
|-----------|------------|------------|--------|
| setuptools | >=61.0 | >=75.0 | Latest stable with improved build system |
| wheel | (implicit) | >=0.43.0 | Explicit requirement for latest wheel format |
| build | (implicit) | >=1.2.0 | Explicit requirement for Python packaging |
| typing-extensions | >=4.0.0 | >=4.12.0 | Latest version with improved type hints |

### Development Dependencies

#### Code Quality Tools

| Tool | Old Version | New Version | Changes |
|------|------------|------------|---------|
| black | >=22.0 | >=24.12.0 | +2 years of improvements, Python 3.13 support |
| flake8 | >=5.0 | >=7.1.0 | Enhanced linting capabilities |
| isort | >=5.0 | >=5.13.0 | Latest version, Python 3.13 compatible |
| mypy | >=1.0 | >=1.14.0 | Improved type checking, new error codes |
| pre-commit | >=2.20 | >=3.7.0 | Major version update with new features |
| bandit | >=1.7 | >=1.8.0 | Enhanced security checks |
| safety | >=2.0 | >=3.2.0 | Improved vulnerability detection |

#### Testing Tools

| Tool | Old Version | New Version | Changes |
|------|------------|------------|---------|
| pytest | >=7.0 | >=8.0 | Major version, improved concurrency |
| pytest-cov | >=4.0 | >=5.0 | New coverage features |
| pytest-timeout | >=2.0 | >=2.1 | Better timeout handling |
| pytest-xvfb | >=2.0 | >=2.0 | No change (Linux only) |

#### Documentation Tools

| Tool | Old Version | New Version | Reason |
|------|------------|------------|---------|
| sphinx | >=5.0 | >=7.4.0 | Major version with performance improvements |
| sphinx-rtd-theme | >=1.0 | >=2.0.0 | Modern dark mode support, responsive design |
| myst-parser | >=0.18 | >=2.1.0 | Better markdown support |
| sphinx-autodoc-typehints | >=1.19 | >=2.4.0 | Improved type hint documentation |
| sphinx-copybutton | >=0.5 | >=0.5.2 | Bug fixes and improvements |
| linkify-it-py | >=2.0.0 | >=2.1.0 | Enhanced link detection |

#### Optional Theme Support

| Tool | Old Version | New Version | Reason |
|------|------------|------------|---------|
| darkdetect | >=0.7.0 | >=1.5.0 | Major version, improved OS detection |

### Pre-commit Hook Versions

#### .pre-commit-config.yaml

| Hook | Old Version | New Version | Enhancements |
|------|------------|------------|--------------|
| pre-commit-hooks | v4.5.0 | v4.6.0 | Latest bug fixes |
| black | 24.3.0 | 24.12.1 | Recent improvements |
| flake8 | 7.0.0 | 7.1.1 | Bug fixes, new rules |
| mypy | v1.8.0 | v1.14.1 | Improved type checking |
| bandit | 1.7.7 | 1.8.1 | Enhanced security |

**Additional Enhancements**:

- Added `flake8-docstrings`, `flake8-bugbear`, `flake8-comprehensions` to flake8
- Increased `max-large-files` check to 1000KB
- Added `--show-error-codes` to mypy
- Excluded test directories from bandit

### GitHub Actions Workflows

#### All Workflows (ci.yml, release.yml, docs.yml)

- **Python version bump**: 3.11 → 3.12 for workflow runs
- **Cache improvements**: Added pip caching with `cache: 'pip'` on setup-python
- **Build tools**: Added explicit setuptools and wheel installation
- **Artifact actions**: Updated upload-pages-artifact from v3 to v4

#### Specific Changes by Workflow

##### CI Workflow (ci.yml)

- Added `fetch-depth: 0` for better git history analysis
- Upgraded build tool versions
- Added `--show-error-codes` to mypy
- Enhanced codecov action with verbose mode
- Updated security tools to latest versions

##### Docs Workflow (docs.yml)

- Changed to Python 3.12
- Added `-W --keep-going` to sphinx-build (treat warnings as errors)
- Improved package listing for debugging
- Updated documentation artifact actions

##### Release Workflow (release.yml)

- Python 3.12 for consistency
- Explicit build>=1.2.0 and twine>=5.1.0
- Enhanced dependency installation

---

## Python Version Support

### Updated Support Matrix

```text
Python 3.9   ✓ (minimum supported)
Python 3.10  ✓
Python 3.11  ✓
Python 3.12  ✓ (primary CI version)
Python 3.13  ✓ (newly added)
```

### Tool Configuration Updates

#### pyproject.toml

- **black**: Updated target-version to include py313
- **mypy**:
  - Bumped python_version from 3.9 to 3.10
  - Added `enable_error_code` for better error detection

#### .pre-commit-config.yaml

- **black**: Updated language_version to python3.12

---

## Installation Instructions

### For Users

No changes required. Install as usual:

```bash
pip install threepanewindows
```

### For Developers

Update development environment:

```bash
# Fresh installation
pip install -e ".[dev,test,docs]"

# Update existing environment
pip install --upgrade -e ".[dev,test,docs]"

# Or install specific extras
pip install -e ".[dev]"      # Development tools
pip install -e ".[test]"     # Testing tools
pip install -e ".[docs]"     # Documentation tools
pip install -e ".[theme]"    # Theme support (darkdetect)
```

### For Documentation Builders

```bash
pip install -r docs/requirements.txt
```

---

## Migration Guide

### For Contributors

1. **Update pre-commit hooks**:

   ```bash
   pre-commit autoupdate
   # or manually update with new versions
   ```

2. **Update local development environment**:

   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -e ".[dev,test]"
   ```

3. **Run quality checks**:

   ```bash
   black threepanewindows/
   isort threepanewindows/
   flake8 threepanewindows/
   mypy threepanewindows/
   pytest
   ```

### For CI/CD Integration

- All GitHub workflows have been updated automatically
- No manual CI/CD changes required
- Tests will run on Python 3.9-3.13
- Primary CI version is now Python 3.12

---

## Breaking Changes

### For Users

**None** - The library remains backward compatible with Python 3.9+

### For Contributors

- Minimum Python version for local development should be 3.9
- Pre-commit now requires Python 3.10+ (use python3.12 as language_version)
- Sphinx 7.4.0+ requires Python 3.9+ (already satisfied)

---

## Security Updates

### Enhanced Security Checks

1. **bandit 1.8.0**: More comprehensive security vulnerability detection
2. **safety 3.2.0**: Updated CVE database and detection
3. **mypy 1.14.0**: Better type checking for security-sensitive operations
4. **Updated dependencies**: All transitive dependencies to latest secure versions

### Security Features

- Stricter type checking enabled in mypy
- Enhanced flake8 checks with bugbear and comprehensions
- Regular bandit scanning in CI pipeline
- Dependency vulnerability scanning with safety

---

## Performance Improvements

### Build & Installation

- **Faster wheel building**: setuptools 75.0 improvements
- **pip caching**: Speeds up CI/CD pipelines significantly
- **Parallel testing**: pytest 8.0 supports better concurrency

### Type Checking

- **Improved mypy performance**: 1.14.0+ optimizations
- **Better error messages**: Enhanced error codes and reporting

### Documentation

- **Faster builds**: Sphinx 7.4+ performance improvements
- **Modern UI**: sphinx-rtd-theme 2.0 improvements
- **Better rendering**: Enhanced markdown support with myst-parser 2.1

---

## Verification Steps

### Verify Installation

```python
import threepanewindows
print(threepanewindows.__version__)
```

### Verify Development Environment

```bash
# Check tool versions
black --version
mypy --version
pytest --version
sphinx-build --version

# Run tests
pytest tests/
pytest --cov=threepanewindows

# Run quality checks
flake8 threepanewindows/
mypy threepanewindows/

# Build documentation
cd docs && make html
```

---

## Troubleshooting

### Issue: Import errors after update

**Solution**: Reinstall the package in development mode:

```bash
pip install --force-reinstall -e .
```

### Issue: Pre-commit hooks fail

**Solution**: Reinstall pre-commit configuration:

```bash
pre-commit install
pre-commit autoupdate
pre-commit run --all-files
```

### Issue: Type checking errors

**Solution**: These are likely improvements in mypy detection:

```bash
mypy threepanewindows --show-error-codes
# Fix reported issues or add type: ignore comments
```

### Issue: Documentation build errors

**Solution**: Update docs dependencies and rebuild:

```bash
pip install -r docs/requirements.txt --upgrade
cd docs && make clean && make html
```

---

## Future Maintenance

### Recommended Update Schedule

- **Dependencies**: Check for updates monthly
- **Python versions**: Drop support for EOL versions annually
- **Pre-commit hooks**: Autoupdate quarterly
- **GitHub Actions**: Review for new features semi-annually

### Version Tracking

- Monitor PyPI for security updates
- Subscribe to security advisories
- Use tools like Dependabot for automatic updates

---

## References

### Updated Packages

- [Black 24.12.1](https://github.com/psf/black)
- [Flake8 7.1.1](https://github.com/PyCQA/flake8)
- [MyPy 1.14.1](https://github.com/python/mypy)
- [Pytest 8.0+](https://pytest.org/)
- [Sphinx 7.4.0](https://www.sphinx-doc.org/)
- [Bandit 1.8.1](https://bandit.readthedocs.io/)

### Documentation

- [Python 3.13 Release](https://www.python.org/downloads/release/python-3130/)
- [setuptools 75.0](https://setuptools.pypa.io/)
- [PEP 517 - Build System Interface](https://www.python.org/dev/peps/pep-0517/)

---

## Support

For issues related to these updates:

1. Check this document first
2. Review [CONTRIBUTING.md](CONTRIBUTING.md)
3. Submit an issue on GitHub
4. Include Python version and tool versions in reports

---

**Last Updated**: January 2025  
**Maintained By**: ThreePaneWindows Team
