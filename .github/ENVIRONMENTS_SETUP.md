# GitHub Environments Setup

This document explains how to set up the required GitHub environments for the workflows to function properly.

## Required Environments

### 1. `test-release`

- **Purpose**: For publishing to Test PyPI
- **Required Secrets**: None (uses OIDC trusted publishing)
- **Protection Rules**: None required
- **Reviewers**: None required

### 2. `production-release`

- **Purpose**: For publishing to production PyPI and creating GitHub releases
- **Required Secrets**: None (uses OIDC trusted publishing)
- **Protection Rules**: Recommended - require manual approval
- **Reviewers**: Repository maintainers

### 3. `github-pages`

- **Purpose**: For deploying documentation to GitHub Pages
- **Required Secrets**: None (automatic)
- **Protection Rules**: None required
- **Reviewers**: None required

## Setup Instructions

### Step 1: Enable GitHub Pages

1. Go to your repository settings
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select "GitHub Actions"
4. Save the settings

### Step 2: Create Environments

1. Go to your repository settings
2. Navigate to "Environments" in the left sidebar
3. Click "New environment" for each required environment:

#### For `test-release`

- Name: `test-release`
- No protection rules needed
- No secrets needed (uses OIDC)

#### For `production-release`

- Name: `production-release`
- **Recommended**: Add protection rules:
  - ✅ Required reviewers (add yourself)
  - ✅ Wait timer: 0 minutes
- No secrets needed (uses OIDC)

#### For `github-pages`

- This is automatically created when you enable GitHub Pages

### Step 3: Set up PyPI Trusted Publishing

#### For Test PyPI

1. Go to <https://test.pypi.org/manage/account/publishing/>
2. Add a new trusted publisher:
   - **PyPI Project Name**: `threepanewindows`
   - **Owner**: `stntg`
   - **Repository name**: `ThreePaneWindows`
   - **Workflow filename**: `release.yml`
   - **Environment name**: `test-release`

#### For Production PyPI

1. Go to <https://pypi.org/manage/account/publishing/>
2. Add a new trusted publisher:
   - **PyPI Project Name**: `threepanewindows`
   - **Owner**: `stntg`
   - **Repository name**: `ThreePaneWindows`
   - **Workflow filename**: `release.yml`
   - **Environment name**: `production-release`

## Workflow Permissions

The workflows now include proper permissions:

- `contents: read` - For checking out code
- `contents: write` - For creating releases
- `id-token: write` - For OIDC trusted publishing
- `pages: write` - For GitHub Pages deployment

## Testing the Setup

1. **Test CI**: Push to `develop` branch - should run CI tests
2. **Test Docs**: Push to `main` branch - should build and deploy docs
3. **Test Release**: Create a tag like `v0.1.1` - should run full release workflow

## Troubleshooting

### Common Issues

1. **Environment not found**: Make sure environments are created in repository settings
2. **Permission denied**: Check that workflows have correct permissions
3. **PyPI publishing fails**: Verify trusted publishing is set up correctly
4. **GUI tests fail**: Virtual display (Xvfb) is now configured for Linux runners

### Workflow Status

- ✅ Timeouts added to prevent hanging
- ✅ Virtual display configured for GUI testing
- ✅ Proper permissions set
- ✅ Error handling improved
- ✅ Continue-on-error for non-critical checks
