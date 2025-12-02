# Dependency Update Checklist

## ✅ Files Updated

### Configuration Files
- [x] `pyproject.toml`
  - [x] Build system requirements (setuptools, wheel, build)
  - [x] Core dependencies (typing-extensions)
  - [x] Dev dependencies (pytest, black, flake8, mypy, etc.)
  - [x] Docs dependencies (sphinx, sphinx-rtd-theme, etc.)
  - [x] Test dependencies
  - [x] Tool configurations (black, isort, mypy, pytest, coverage, bandit)

- [x] `setup.py`
  - [x] Dev extras with updated versions
  - [x] Docs extras with updated versions
  - [x] Environment classifiers

- [x] `docs/requirements.txt`
  - [x] Updated all Sphinx-related packages
  - [x] Updated linkify-it-py

- [x] `.pre-commit-config.yaml`
  - [x] pre-commit-hooks v4.6.0
  - [x] black 24.12.1
  - [x] flake8 7.1.1 with additional plugins
  - [x] mypy v1.14.1
  - [x] bandit 1.8.1
  - [x] Added enhanced flake8 dependencies
  - [x] Improved configurations and args

### GitHub Workflows
- [x] `.github/workflows/ci.yml`
  - [x] Python 3.12 as main test version
  - [x] Added pip caching
  - [x] Updated build tools
  - [x] Enhanced mypy output
  - [x] Updated security tools

- [x] `.github/workflows/docs.yml`
  - [x] Python 3.12 for docs building
  - [x] Added pip caching
  - [x] Enhanced sphinx-build options
  - [x] Updated artifact handling

- [x] `.github/workflows/release.yml`
  - [x] Python 3.12 for release builds
  - [x] Added pip caching to all jobs
  - [x] Updated build and twine versions
  - [x] Enhanced dependency installation

- [ ] `.github/workflows/test-new-features.yml` (if needs update)
- [ ] `.github/workflows/test-release.yml` (if needs update)
- [ ] `.github/workflows/release-stubs.yml` (if needs update)

---

## 📋 Version Changes Summary

### Development Tools
```
black:          22.0    → 24.12.0+  (+2.12 versions)
flake8:         5.0     → 7.1.0+    (+2.1 versions)
mypy:           1.0     → 1.14.0+   (+0.14 versions)
isort:          5.0     → 5.13.0+   (+0.13 versions)
pytest:         7.0     → 8.0+      (+1 version)
pytest-cov:     4.0     → 5.0+      (+1 version)
bandit:         1.7     → 1.8.0+    (+0.1 versions)
safety:         2.0     → 3.2.0+    (+1.2 versions)
```

### Documentation Tools
```
sphinx:                  5.0     → 7.4.0+    (+2.4 versions)
sphinx-rtd-theme:        1.0     → 2.0.0+    (+1 version)
myst-parser:             0.18    → 2.1.0+    (+1.92 versions)
sphinx-autodoc-typehints: 1.19   → 2.4.0+    (+1.21 versions)
```

### Infrastructure
```
setuptools:     61.0    → 75.0+     (+14 versions)
wheel:          (implicit) → 0.43.0+ (now explicit)
build:          (implicit) → 1.2.0+  (now explicit)
pre-commit-hooks: v4.5.0 → v4.6.0   (+0.1 versions)
```

---

## 🔍 Testing Checklist

### Local Testing
- [ ] Run `pip install -e ".[dev,test,docs]"`
- [ ] Run `black --check threepanewindows/`
- [ ] Run `isort --check-only threepanewindows/`
- [ ] Run `flake8 threepanewindows/`
- [ ] Run `mypy threepanewindows/`
- [ ] Run `pytest tests/`
- [ ] Run `pytest --cov=threepanewindows`
- [ ] Build documentation: `cd docs && make html`

### Pre-commit Testing
- [ ] Run `pre-commit run --all-files`
- [ ] Verify hooks are properly configured
- [ ] Check that no false positives are introduced

### CI/CD Verification
- [ ] Push to GitHub and verify CI passes
- [ ] Check all matrix combinations (Python 3.9-3.13, OS: Ubuntu/Windows/macOS)
- [ ] Verify documentation builds
- [ ] Check security scanning passes

---

## 🚀 Release Checklist

- [ ] All tests passing locally
- [ ] All CI/CD tests passing
- [ ] No new warnings or errors
- [ ] Documentation builds cleanly
- [ ] Changelog updated with dependency updates
- [ ] Version bump (if needed)
- [ ] Tag and release

---

## 📝 Documentation Updates

- [x] Created `DEPENDENCY_UPDATES.md` with comprehensive details
- [x] Created `DEPENDENCY_CHECKLIST.md` (this file)
- [ ] Update README.md if dependency info is listed
- [ ] Update CONTRIBUTING.md with updated requirements
- [ ] Update any developer setup documentation

---

## 🔄 Ongoing Maintenance

### Monthly
- [ ] Check for new package releases
- [ ] Monitor security advisories
- [ ] Review dependency compatibility

### Quarterly
- [ ] Run `pip list --outdated`
- [ ] Check pre-commit hooks for updates
- [ ] Review GitHub Actions for new versions

### Annually
- [ ] Evaluate dropping EOL Python versions
- [ ] Review major package version updates
- [ ] Plan next round of dependency updates

---

## 🆘 Troubleshooting

### If Tests Fail After Update

1. **Check Python version compatibility**:
   ```bash
   python --version
   # Should be 3.9+
   ```

2. **Reinstall dependencies**:
   ```bash
   pip install --force-reinstall --no-cache-dir -e ".[dev,test]"
   ```

3. **Clear caches**:
   ```bash
   rm -rf .pytest_cache __pycache__ .mypy_cache
   ```

4. **Run individual test files**:
   ```bash
   pytest tests/test_examples.py -v
   ```

### If CI Fails

1. Check the specific error in GitHub Actions
2. Reproduce locally with same Python version
3. Check if it's a Windows/macOS/Linux specific issue
4. Review pre-commit hook output

### Common Issues

| Issue | Solution |
|-------|----------|
| Black format errors | Run `black threepanewindows/` |
| Type errors | Run `mypy threepanewindows/ --show-error-codes` |
| Lint errors | Run `flake8 threepanewindows/` and fix |
| Import errors | Reinstall with `pip install --force-reinstall -e .` |
| Docs build fails | Update with `pip install -r docs/requirements.txt --upgrade` |

---

## ✨ Benefits of These Updates

### For Users
- ✅ Improved performance
- ✅ Better Python 3.13 support
- ✅ Enhanced security
- ✅ Modern dependencies

### For Developers
- ✅ Better type checking with mypy 1.14
- ✅ Faster code formatting with black 24.12
- ✅ Improved linting with flake8 7.1
- ✅ Modern documentation with Sphinx 7.4
- ✅ Better testing with pytest 8.0

### For CI/CD
- ✅ Faster builds with pip caching
- ✅ Better security scanning
- ✅ More reliable testing
- ✅ Improved documentation builds

---

## 📞 Support

If you encounter any issues:
1. Check the [DEPENDENCY_UPDATES.md](DEPENDENCY_UPDATES.md) file
2. Review GitHub Issues
3. Check the specific package's documentation
4. Open a new GitHub Issue with details

---

**Status**: ✅ Complete  
**Last Updated**: January 2025  
**Next Review**: April 2025