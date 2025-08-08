# ThreePaneWindows Test Suite

This directory contains comprehensive tests for ThreePaneWindows, with special
focus on the new v1.3.0 features.

## 📁 Test Files Overview

### New Features Tests (v1.3.0)

These tests validate all new functionality introduced in version 1.3.0:

| File | Component | Tests | Non-GUI | Description |
|------|-----------|-------|---------|-------------|
| `test_flexible.py` | Enhanced Flexible Layout | 28 | 7 | Layout direction, pane config |
| `test_custom_menubar.py` | Custom UI Components | 43 | 8 | Menu items, commands |
| `test_central_theme_manager_simple.py` | Central Theme Manager | 35 | 23 | Theme types, switching |
| `test_logging_ci_safe.py` | Enhanced Logging System | 30 | 30 | Logger creation, CI-safe |
| `test_new_features_summary.py` | Integration & Summary | 12 | 12 | Cross-component validation |

**Total New Features Tests**: 148 tests (80 non-GUI, 68 GUI)

### Legacy Tests

Additional test files for existing functionality:

- `test_*.py` - Various component tests
- Tests marked with `@pytest.mark.gui` require display/GUI environment
- Tests without GUI marker run in headless CI environments

## 🚀 Quick Start

### Run All New Feature Tests

```bash
# Using the test runner (recommended)
python run_new_features_tests.py

# Using pytest directly
pytest tests/test_flexible.py tests/test_custom_menubar.py \
    tests/test_central_theme_manager_simple.py tests/test_logging_ci_safe.py \
    tests/test_new_features_summary.py -m "not gui" -v
```

### Run Individual Test Files

```bash
# Enhanced Flexible Layout System
pytest tests/test_flexible.py -m "not gui" -v

# Central Theme Manager
pytest tests/test_central_theme_manager_simple.py -m "not gui" -v

# Custom UI Components
pytest tests/test_custom_menubar.py -m "not gui" -v

# Enhanced Logging System (CI-safe)
pytest tests/test_logging_ci_safe.py -v

# Integration Summary
pytest tests/test_new_features_summary.py -v
```

### Run All Tests (Including GUI)

```bash
# Run all new feature tests including GUI tests
pytest tests/test_flexible.py tests/test_custom_menubar.py \
    tests/test_central_theme_manager_simple.py tests/test_logging_ci_safe.py \
    tests/test_new_features_summary.py -v
```

## 🏷️ Test Markers

Tests use pytest markers to categorize functionality:

- `@pytest.mark.gui` - Requires GUI/display (skipped in headless CI)
- `@pytest.mark.integration` - Integration tests across components
- `@pytest.mark.slow` - Performance/long-running tests

### Running by Marker

```bash
# Run only non-GUI tests (CI-safe)
pytest -m "not gui"

# Run only integration tests
pytest -m "integration"

# Skip slow tests
pytest -m "not slow"
```

## 🔧 Test Environment Setup

### Requirements

```bash
pip install pytest pytest-cov
pip install -e .  # Install ThreePaneWindows in development mode
```

### CI/CD Environment

For headless environments (GitHub Actions, Docker, etc.):

```bash
# Always use the "not gui" marker
pytest tests/ -m "not gui" -v
```

### Local Development

For local development with GUI available:

```bash
# Run all tests including GUI
pytest tests/ -v
```

## 📊 Test Coverage

### New Features Coverage (v1.3.0)

- **Enhanced Flexible Layout System**: ✅ Complete
  - LayoutDirection enum
  - FlexPaneConfig dataclass
  - FlexContainer dataclass
  - EnhancedFlexibleLayout class

- **Central Theme Manager**: ✅ Complete
  - ThemeType enum (7 themes)
  - Singleton pattern
  - Theme switching
  - Widget theming
  - Performance validation

- **Custom UI Components**: ✅ Complete
  - MenuItem dataclass
  - Command handling
  - Submenu support
  - Accelerator keys
  - State management

- **Enhanced Logging System**: ✅ Complete
  - ThreePaneWindowsLogger singleton
  - get_logger() function
  - Logger hierarchy
  - CI-safe console logging
  - Thread safety
  - Error handling

## 🐛 Troubleshooting

### Common Issues

#### 1. "I/O operation on closed file" Error

**Problem**: Logging tests fail with file operation errors.
**Solution**: Use `test_logging_ci_safe.py` instead of `test_logging_config_simple.py`.

#### 2. GUI Tests Failing in Headless Environment

**Problem**: Tests try to create Tkinter widgets without display.
**Solution**: Always use `-m "not gui"` flag in headless environments.

#### 3. Import Errors

**Problem**: Cannot import threepanewindows modules.
**Solution**: Install package in development mode: `pip install -e .`

### Test-Specific Issues

#### Theme Manager Tests

- `get_current_theme()` returns `ThemeColors` object, not `ThemeType`
- `get_themed_widget_types()` returns `set`, not `list`
- Use `current_theme` property for `ThemeType` enum

#### Logging Tests

- Use `test_logging_ci_safe.py` for CI environments
- Avoid `test_logging_config_simple.py` in headless environments
- Platform-specific behavior is mocked for consistency

## 📈 Performance

### Test Execution Times

- **Full new features suite**: ~1-2 seconds
- **Individual test files**: ~0.1-0.5 seconds each
- **CI-safe tests only**: ~1 second

### Memory Usage

- Tests are designed to be memory-efficient
- No memory leaks in repeated test runs
- Proper cleanup in setup/teardown methods

## 🔄 Continuous Integration

### GitHub Actions

A complete workflow is provided at `.github/workflows/test-new-features.yml`:

- Multi-platform: Ubuntu, Windows, macOS
- Multi-version: Python 3.8-3.12
- Coverage reporting
- Headless compatibility

### Local CI Testing

Simulate CI environment locally:

```bash
# Test like GitHub Actions would
pytest tests/test_flexible.py tests/test_custom_menubar.py \
    tests/test_central_theme_manager_simple.py tests/test_logging_ci_safe.py \
    tests/test_new_features_summary.py -m "not gui" --tb=short
```

## 📚 Documentation

- `NEW_FEATURES_TESTING_SUMMARY.md` - Comprehensive test overview
- `FIXED_TESTS_SUMMARY.md` - Details on test fixes and improvements
- Individual test files contain detailed docstrings
- GitHub Actions workflow includes inline documentation

## 🎯 Best Practices

### Writing New Tests

1. Use descriptive test names: `test_component_specific_behavior`
2. Add appropriate markers: `@pytest.mark.gui` for GUI tests
3. Include docstrings explaining test purpose
4. Use setup/teardown methods for cleanup
5. Mock external dependencies for CI compatibility

### Running Tests

1. Always use `-m "not gui"` in CI environments
2. Use the test runner script for consistency
3. Run individual files during development
4. Use verbose mode (`-v`) for detailed output
5. Check coverage with `--cov=threepanewindows`

### Debugging Tests

1. Use `--tb=long` for detailed tracebacks
2. Add `--pdb` to drop into debugger on failure
3. Use `--lf` to run only last failed tests
4. Check test collection with `--collect-only`
