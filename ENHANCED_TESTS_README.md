# Enhanced Test Coverage Documentation

## Overview

This document describes the enhanced test suite that achieves 70%+ code coverage for the ThreePaneWindows library. The tests are designed to work in both local development and headless CI/CD environments.

## Test Coverage Achievement

### Current Coverage: **70.76%**

| Module | Coverage | Status |
|--------|----------|--------|
| `__init__.py` | 100% | ✅ |
| `cli.py` | 100% | ✅ |
| `themes.py` | 88% | ✅ |
| `_version.py` | 86% | ✅ |
| `fixed.py` | 84% | ✅ |
| `dockable.py` | 82% | ✅ |
| `examples.py` | 67% | ✅ |
| `enhanced_dockable.py` | 63% | ✅ |

## Headless Compatibility

### Design Principles

The enhanced tests are designed with headless compatibility in mind:

1. **Automatic Environment Detection**: Tests detect CI/CD environments
2. **Graceful Degradation**: GUI tests skip gracefully when no display is available
3. **Mock-Heavy Testing**: Uses mocks and patches to test logic without GUI
4. **Error Handling**: Comprehensive error handling for display issues

### Environment Detection

```python
# Tests automatically detect headless environments
if os.environ.get('CI') or os.environ.get('GITHUB_ACTIONS'):
    # Headless mode - skip GUI tests or use virtual display
    pytest.skip("Headless environment detected")
```

### CI/CD Configuration

For GitHub Actions or other CI systems, use the provided `pytest_ci.ini`:

```bash
# Run tests with CI configuration
python -m pytest -c pytest_ci.ini
```

## Test Files

### Core Test Files (Included in Remote Repo)

1. **`test_enhanced_coverage.py`** - Comprehensive coverage tests
   - Icon utility testing with platform mocking
   - PaneConfig comprehensive testing
   - DragHandle event simulation
   - Enhanced window initialization paths
   - Theme integration testing
   - Error scenario testing

2. **Enhanced existing test files** - Improved coverage for:
   - `test_dockable.py` - Additional edge cases
   - `test_examples.py` - Utility function testing
   - `test_fixed.py` - Advanced feature testing
   - `test_themes.py` - Advanced theme management
   - `test_version.py` - Version module internals

### Local-Only Test Files (Excluded from Remote Repo)

- `test_runner.py` - Local test runner utilities
- `pytest_local.ini` - Local-specific configuration
- `LOCAL_TESTING_README.md` - Local development docs

## Running Tests

### Local Development

```bash
# Run all tests with coverage
python -m pytest --cov=threepanewindows --cov-report=html:htmlcov_local --cov-fail-under=70

# Run specific test file
python -m pytest tests/test_enhanced_coverage.py -v

# Run with local configuration
python -m pytest -c pytest_local.ini
```

### CI/CD Environment

```bash
# Run with CI configuration
python -m pytest -c pytest_ci.ini

# Run with coverage for CI
python -m pytest --cov=threepanewindows --cov-report=xml --cov-fail-under=70
```

### Headless Environment Setup

For headless environments that need GUI testing:

```bash
# Install virtual display (Ubuntu/Debian)
sudo apt-get install xvfb

# Run tests with virtual display
xvfb-run -a python -m pytest --cov=threepanewindows --cov-fail-under=70
```

## Test Categories

### Unit Tests
- Icon utility functions
- Configuration classes
- Theme management
- Version handling

### Integration Tests
- Window creation and management
- Theme application
- Event handling
- State management

### Mock-Based Tests
- Platform-specific behavior
- Error conditions
- Edge cases
- Resource constraints

## Coverage Strategies

### High-Coverage Modules (80%+)
- Focus on edge cases and error handling
- Test advanced features and configurations
- Verify state management and cleanup

### Medium-Coverage Modules (60-80%)
- Target specific uncovered lines
- Add comprehensive configuration testing
- Test error scenarios and recovery

### GUI-Heavy Modules
- Use mocking for display-independent testing
- Test logic separately from UI
- Focus on event handling and state changes

## Best Practices

### Writing Headless-Compatible Tests

1. **Always use try/catch for Tkinter creation**:
```python
try:
    self.root = tk.Tk()
    self.root.withdraw()
except tk.TclError as e:
    pytest.skip(f"Cannot create Tkinter window: {e}")
```

2. **Use environment detection**:
```python
if os.environ.get('CI'):
    pytest.skip("Headless environment")
```

3. **Mock external dependencies**:
```python
with patch('platform.system', return_value='Linux'):
    # Test platform-specific code
```

4. **Test logic, not UI**:
```python
# Test the logic behind UI operations
assert window.is_detached == True
# Rather than testing visual appearance
```

## Troubleshooting

### Common Issues

1. **"Cannot create Tkinter window"**
   - Expected in headless environments
   - Tests should skip gracefully
   - Use virtual display if GUI testing is required

2. **"Display not found"**
   - Set up Xvfb for headless GUI testing
   - Or ensure tests skip GUI components

3. **Import errors**
   - Ensure all dependencies are installed
   - Check Python version compatibility

### Debug Mode

Enable debug output for troubleshooting:

```bash
python -m pytest -v -s --tb=long tests/test_enhanced_coverage.py
```

## Maintenance

### Adding New Tests

1. Follow headless compatibility patterns
2. Add appropriate error handling
3. Use mocks for external dependencies
4. Update coverage targets if needed

### Updating Coverage Targets

Current target: 70%
- Monitor coverage trends
- Adjust targets based on new code
- Focus on critical path coverage

## Integration with CI/CD

### GitHub Actions Example

```yaml
- name: Run tests with coverage
  run: |
    python -m pytest -c pytest_ci.ini
    
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

### Local Development Workflow

1. Write tests locally with full GUI support
2. Test headless compatibility with `CI=true python -m pytest`
3. Verify coverage meets requirements
4. Commit enhanced tests to repository

The enhanced test suite provides comprehensive coverage while maintaining compatibility with both local development and headless CI/CD environments.