# PyPI API Token Setup Guide

This guide explains how to set up PyPI API tokens for your GitHub Actions workflows. This approach is simpler and more reliable than trusted publishing.

## 🔧 Why API Tokens Instead of Trusted Publishing?

**API Tokens are:**
- ✅ Simpler to set up
- ✅ More reliable
- ✅ Work immediately without complex configuration matching
- ✅ Easier to troubleshoot
- ✅ Used by many successful projects (like GUI Image Studio)

**Trusted Publishing requires:**
- ❌ Exact configuration matching between PyPI and GitHub
- ❌ Complex environment setup
- ❌ Specific workflow file names and paths
- ❌ More prone to configuration errors

## 🚀 Setup Instructions

### Step 1: Create Test PyPI Account and Token

1. **Create Test PyPI Account**:
   - Go to https://test.pypi.org/account/register/
   - Create an account with your email

2. **Generate Test PyPI API Token**:
   - Go to https://test.pypi.org/manage/account/
   - Scroll down to "API tokens"
   - Click "Add API token"
   - Name: `ThreePaneWindows-GitHub-Actions`
   - Scope: `Entire account` (or specific to your project if it exists)
   - Click "Add token"
   - **COPY THE TOKEN** - you won't see it again!

### Step 2: Create Production PyPI Account and Token

1. **Create PyPI Account**:
   - Go to https://pypi.org/account/register/
   - Create an account with your email

2. **Generate PyPI API Token**:
   - Go to https://pypi.org/manage/account/
   - Scroll down to "API tokens"
   - Click "Add API token"
   - Name: `ThreePaneWindows-GitHub-Actions`
   - Scope: `Entire account` (or specific to your project if it exists)
   - Click "Add token"
   - **COPY THE TOKEN** - you won't see it again!

### Step 3: Add Tokens to GitHub Secrets

1. **Go to your GitHub repository**:
   - Navigate to: `https://github.com/stntg/ThreePaneWindows`

2. **Access Repository Secrets**:
   - Click **Settings** tab
   - Click **Secrets and variables** → **Actions**

3. **Add Test PyPI Token**:
   - Click **New repository secret**
   - Name: `TEST_PYPI_API_TOKEN`
   - Value: Paste your Test PyPI token (starts with `pypi-`)
   - Click **Add secret**

4. **Add Production PyPI Token**:
   - Click **New repository secret**
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your PyPI token (starts with `pypi-`)
   - Click **Add secret**

## 🧪 Testing the Setup

### Test with Test PyPI Upload Workflow

1. **Manual Test**:
   ```bash
   # Go to your repository on GitHub
   # Click Actions tab
   # Select "Test PyPI Upload" workflow
   # Click "Run workflow"
   # Enter a version suffix like "test1"
   # Click "Run workflow"
   ```

2. **Automatic Test**:
   ```bash
   # Make a small change to your code
   git add .
   git commit -m "Test PyPI upload workflow"
   git push origin develop
   ```

### Test with Test Release Workflow

1. **Manual Test**:
   ```bash
   # Go to your repository on GitHub
   # Click Actions tab
   # Select "Test Release" workflow
   # Click "Run workflow"
   # Enter version like "0.1.1-test1"
   # Set "Upload to Test PyPI only" to true
   # Click "Run workflow"
   ```

## 📋 Verification Checklist

After setup, verify these items:

- [ ] Test PyPI account created
- [ ] Production PyPI account created
- [ ] `TEST_PYPI_API_TOKEN` secret added to GitHub
- [ ] `PYPI_API_TOKEN` secret added to GitHub
- [ ] Test PyPI upload workflow runs successfully
- [ ] Package appears on Test PyPI: https://test.pypi.org/project/threepanewindows/
- [ ] Package can be installed from Test PyPI

## 🔍 Troubleshooting

### Common Issues

1. **"Invalid or expired token"**:
   - Regenerate the token on PyPI/Test PyPI
   - Update the GitHub secret with the new token

2. **"Package already exists"**:
   - This is normal for Test PyPI
   - The workflow uses `--skip-existing` to handle this

3. **"Package not found on Test PyPI"**:
   - Wait a few minutes for propagation
   - Check the workflow logs for upload errors

4. **"Secret not found"**:
   - Verify the secret name matches exactly: `TEST_PYPI_API_TOKEN` or `PYPI_API_TOKEN`
   - Check that the secret is added to the correct repository

### Debug Commands

Check your workflow logs for these messages:

```bash
# Success messages
✅ Package successfully uploaded to Test PyPI!
✅ Package successfully published to PyPI!

# Token availability
Test PyPI token available. Proceeding with upload.
PyPI token available. Proceeding with upload.

# Skip messages (when token not configured)
⚠️ Test PyPI upload was skipped because TEST_PYPI_API_TOKEN secret is not configured.
⚠️ PyPI upload was skipped because PYPI_API_TOKEN secret is not configured.
```

## 🔗 Useful Links

- [Test PyPI](https://test.pypi.org/)
- [Production PyPI](https://pypi.org/)
- [PyPI API Token Documentation](https://pypi.org/help/#apitoken)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

## 🎯 Next Steps

1. **Set up the tokens** following the steps above
2. **Test the workflows** to ensure they work
3. **Create your first release** using the test-release workflow
4. **Publish to production** when ready

This approach is much more straightforward than trusted publishing and follows the same pattern used by many successful Python projects!