# GitHub Workflows

This directory contains GitHub Actions workflows for the ThreePaneWindows project.

## Available Workflows

### 🔄 CI Workflow (`ci.yml`)
- **Trigger**: Push to main/develop, Pull Requests
- **Purpose**: Continuous Integration - runs tests, linting, and code quality checks
- **Environments**: Multiple Python versions (3.8-3.12) on Ubuntu, Windows, macOS

### 📚 Documentation Workflow (`docs.yml`)
- **Trigger**: Push to main, manual dispatch
- **Purpose**: Builds and deploys documentation to GitHub Pages
- **Output**: Updated documentation at project GitHub Pages

### 🚀 Release Workflow (`release.yml`)
- **Trigger**: Manual dispatch with version input
- **Purpose**: Creates official releases and publishes to PyPI
- **Features**: Git tagging, GitHub releases, PyPI publication

### 🧪 Test Release Workflow (`test-release.yml`)
- **Trigger**: Manual dispatch with version input
- **Purpose**: Full release testing including Test PyPI upload
- **Features**: 
  - Build and test package
  - Upload to Test PyPI
  - Verify installation from Test PyPI
  - Optional production release

### 📦 Test PyPI Upload Workflow (`test-pypi-upload.yml`)
- **Trigger**: 
  - Manual dispatch (with optional version suffix)
  - Automatic on push to develop/feature branches
- **Purpose**: Quick testing of package uploads to Test PyPI
- **Features**:
  - Automatic version generation with timestamps
  - Quick test suite execution
  - Test PyPI upload with unique versions
  - Installation verification

## Using the Test PyPI Upload Workflow

### Manual Trigger
1. Go to Actions tab in GitHub
2. Select "Test PyPI Upload" workflow
3. Click "Run workflow"
4. Optionally specify a version suffix (e.g., `rc1`, `alpha1`, `dev1`)
5. Optionally skip tests for faster uploads

### Automatic Trigger
The workflow automatically runs when you push to:
- `develop` branch
- Any `feature/*` branch

And the push includes changes to:
- `threepanewindows/` directory
- `pyproject.toml`
- `setup.py`

### Version Generation
- **Manual**: `{current_version}.{suffix}.{timestamp}`
- **Automatic**: `{current_version}.dev.{branch}.{commit}.{timestamp}`

Example versions:
- Manual with suffix "rc1": `0.1.0.rc1.20241215123045`
- Automatic from develop: `0.1.0.dev.develop.a1b2c3d.20241215123045`

### Installation from Test PyPI
After a successful upload, install using:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ threepanewindows==VERSION
```

## Environment Setup

### Required Secrets
The workflows now use **API tokens** instead of trusted publishing for better reliability:

- **`TEST_PYPI_API_TOKEN`**: Your Test PyPI API token
- **`PYPI_API_TOKEN`**: Your production PyPI API token

### Setup Instructions
1. Create accounts on [Test PyPI](https://test.pypi.org) and [PyPI](https://pypi.org)
2. Generate API tokens for both accounts
3. Add the tokens as repository secrets in GitHub
4. See [PYPI_API_TOKEN_SETUP.md](../PYPI_API_TOKEN_SETUP.md) for detailed instructions

### No GitHub Environments Required
The API token approach doesn't require GitHub environments, making setup much simpler!

## Monitoring Workflows

Use the provided monitoring scripts:

### PowerShell (Windows)
```powershell
.\monitor_workflows.ps1 status
.\monitor_workflows.ps1 open test-pypi-upload
```

### Python (Cross-platform)
```bash
python monitor_workflows.py status
python monitor_workflows.py open test-pypi-upload
```

## Troubleshooting

### Common Issues

1. **TOML parsing errors**: The workflow installs `tomli` for Python < 3.11
2. **Test PyPI upload conflicts**: Uses `skip-existing: true` to handle duplicates
3. **Installation delays**: Includes retry logic and wait periods
4. **GUI testing**: Uses virtual display (Xvfb) for headless testing

### Debug Tips

1. Check workflow logs in GitHub Actions tab
2. Verify environment configuration
3. Test locally with the same Python version
4. Check Test PyPI project page for upload status

## Best Practices

1. **Use manual triggers** for important testing
2. **Test locally first** before pushing to trigger automatic workflows
3. **Monitor Test PyPI** for successful uploads before production releases
4. **Clean up old test versions** periodically from Test PyPI
5. **Use meaningful version suffixes** for manual triggers