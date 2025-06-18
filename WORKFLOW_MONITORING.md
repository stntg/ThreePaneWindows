# GitHub Workflows Monitoring Guide

This document provides comprehensive guidance on monitoring GitHub workflows for the ThreePaneWindows project.

## 📋 Available Workflows

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **CI** | `ci.yml` | Push/PR to `main`/`develop` | Tests, linting, security, docs |
| **Documentation** | `docs.yml` | Push/PR to `main` | Build and deploy docs |
| **Release** | `release.yml` | Version tags (`v*`) | Full production release |
| **Test Release** | `test-release.yml` | Manual trigger | Test releases to Test PyPI |

## 🔍 Monitoring Methods

### Method 1: GitHub Web Interface (Primary)

**Direct Links:**
- **All Workflows**: https://github.com/stntg/ThreePaneWindows/actions
- **CI Workflow**: https://github.com/stntg/ThreePaneWindows/actions/workflows/ci.yml
- **Docs Workflow**: https://github.com/stntg/ThreePaneWindows/actions/workflows/docs.yml
- **Release Workflow**: https://github.com/stntg/ThreePaneWindows/actions/workflows/release.yml
- **Test Release**: https://github.com/stntg/ThreePaneWindows/actions/workflows/test-release.yml

**Navigation Steps:**
1. Go to your repository: https://github.com/stntg/ThreePaneWindows
2. Click the **"Actions"** tab
3. Select specific workflow from the left sidebar
4. Click on individual workflow runs to see details

### Method 2: GitHub CLI (if installed)

```bash
# List recent workflow runs
gh run list --limit 10

# List runs for specific workflow
gh run list --workflow=ci.yml --limit 5

# Watch a specific run (replace RUN_ID)
gh run watch RUN_ID

# View run details
gh run view RUN_ID

# Download artifacts
gh run download RUN_ID
```

### Method 3: Git Commands

```bash
# Check latest commits that might have triggered workflows
git log --oneline -5

# Check current branch and status
git status

# Check remote repository
git remote -v

# Check if there are any pending pushes
git log origin/develop..develop
```

## 📊 CI Workflow Details

### Test Matrix (15 combinations)
- **Operating Systems**: Ubuntu, Windows, macOS
- **Python Versions**: 3.8, 3.9, 3.10, 3.11, 3.12

### Jobs Overview
1. **Test Job** (~20-25 minutes)
   - Install dependencies
   - Lint with flake8
   - Type check with mypy
   - Run pytest with coverage
   - Upload coverage to Codecov

2. **Security Job** (~5-10 minutes)
   - Run bandit security checks
   - Check dependencies with safety

3. **Docs Job** (~10-15 minutes)
   - Build Sphinx documentation
   - Upload documentation artifacts

## 🚨 Common Issues and Solutions

### Test Failures
- **Import Errors**: Missing dependencies in `pyproject.toml`
- **GUI Issues**: Tkinter display problems (handled with Xvfb on Linux)
- **Path Issues**: Cross-platform path handling

### Linting Failures
- **flake8**: Code style violations
- **Line length**: Max 127 characters
- **Unused imports**: Remove or mark with `# noqa`

### Security Issues
- **bandit**: Security vulnerabilities in code
- **safety**: Known vulnerabilities in dependencies

### Documentation Failures
- **Sphinx errors**: RST syntax issues
- **Missing dependencies**: Documentation build requirements

## 📈 Monitoring Workflow Status

### Status Indicators
- ✅ **Green checkmark**: Job passed
- ❌ **Red X**: Job failed
- 🟡 **Yellow circle**: Job in progress
- ⚪ **Gray circle**: Job queued/pending
- ⏭️ **Gray arrow**: Job skipped

### Typical Workflow Duration
- **CI Workflow**: 15-30 minutes (depends on matrix size)
- **Documentation**: 10-20 minutes
- **Release**: 30-60 minutes (includes manual approval)
- **Test Release**: 20-40 minutes

## 🔔 Setting Up Notifications

### GitHub Notifications
1. Go to repository **Settings** → **Notifications**
2. Enable **Actions** notifications
3. Choose notification preferences (email, web, mobile)

### Email Notifications
- GitHub sends emails for workflow failures by default
- Configure in your GitHub notification settings

### Slack/Discord Integration
Add webhook integrations in repository settings for team notifications.

## 🛠️ Troubleshooting Commands

### Local Testing Before Push
```bash
# Run tests locally
python -m pytest tests/ -v

# Run linting
flake8 threepanewindows/

# Run type checking
mypy threepanewindows/ --ignore-missing-imports

# Run security checks
bandit -r threepanewindows/

# Build documentation
cd docs && make html
```

### Workflow Debugging
```bash
# Check workflow file syntax
# Use GitHub's workflow validator or VS Code YAML extension

# View workflow logs
# Use GitHub web interface or CLI: gh run view RUN_ID --log

# Re-run failed jobs
# Use GitHub web interface: "Re-run failed jobs" button
```

## 📝 Workflow Triggers Reference

### Automatic Triggers
```yaml
# CI Workflow
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

# Documentation Workflow  
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

# Release Workflow
on:
  push:
    tags: [ 'v*' ]
```

### Manual Triggers
```yaml
# Test Release Workflow
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to test'
        required: true
        type: string
```

## 🎯 Quick Actions

### Trigger CI Workflow
```bash
# Make a change and push to develop or main
git add .
git commit -m "Trigger CI workflow"
git push origin develop
```

### Trigger Documentation Workflow
```bash
# Push to main branch
git checkout main
git merge develop
git push origin main
```

### Trigger Release Workflow
```bash
# Create and push version tag
git tag v1.0.0
git push origin v1.0.0
```

### Trigger Test Release (Manual)
1. Go to Actions tab on GitHub
2. Select "Test Release" workflow
3. Click "Run workflow"
4. Enter version and options
5. Click "Run workflow" button

## 📊 Monitoring Dashboard

### Current Workflow Status
- **Repository**: https://github.com/stntg/ThreePaneWindows
- **Actions**: https://github.com/stntg/ThreePaneWindows/actions
- **Latest CI**: Check latest commit on develop branch
- **Latest Release**: Check tags and releases page

### Key Metrics to Monitor
- **Test Coverage**: Aim for >80%
- **Build Time**: Monitor for performance regression
- **Success Rate**: Track workflow reliability
- **Security Issues**: Zero tolerance for high-severity issues

## 🔧 Maintenance Tasks

### Weekly
- Review failed workflows and fix issues
- Update dependencies if security alerts appear
- Check test coverage reports

### Monthly
- Review workflow performance and optimize if needed
- Update GitHub Actions versions
- Review and update documentation

### Before Releases
- Ensure all CI checks pass
- Run test release workflow
- Verify documentation builds correctly
- Check security scan results

## 📞 Getting Help

### Resources
- **GitHub Actions Documentation**: https://docs.github.com/en/actions
- **Workflow Syntax**: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- **Troubleshooting**: https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows

### Support Channels
- GitHub Community Forum
- Stack Overflow (tag: github-actions)
- Project maintainers

---

**Last Updated**: $(date)
**Repository**: https://github.com/stntg/ThreePaneWindows
**Maintainer**: Project Team