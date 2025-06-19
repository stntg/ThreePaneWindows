#!/usr/bin/env python3
"""
API Token Workflow Validator

This script validates that all GitHub Actions workflows are properly configured
to use API tokens instead of trusted publishing.
"""

import os
import yaml
import sys
from pathlib import Path

def load_workflow(workflow_path):
    """Load and parse a workflow YAML file."""
    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading {workflow_path}: {e}")
        return None

def check_for_trusted_publishing(workflow_data, workflow_name):
    """Check if workflow still uses trusted publishing."""
    issues = []
    
    jobs = workflow_data.get('jobs', {})
    for job_name, job_config in jobs.items():
        # Check for environment (indicates trusted publishing)
        if 'environment' in job_config:
            issues.append(f"Job '{job_name}' still uses environment '{job_config['environment']}' (trusted publishing)")
        
        # Check for id-token permission (indicates trusted publishing)
        permissions = job_config.get('permissions', {})
        if 'id-token' in permissions:
            issues.append(f"Job '{job_name}' still has 'id-token' permission (trusted publishing)")
        
        # Check for pypa/gh-action-pypi-publish usage
        steps = job_config.get('steps', [])
        for step in steps:
            if step.get('uses', '').startswith('pypa/gh-action-pypi-publish'):
                issues.append(f"Job '{job_name}' still uses pypa/gh-action-pypi-publish (should use twine)")
    
    return issues

def check_for_api_tokens(workflow_data, workflow_name):
    """Check if workflow properly uses API tokens."""
    good_practices = []
    missing_practices = []
    
    jobs = workflow_data.get('jobs', {})
    for job_name, job_config in jobs.items():
        steps = job_config.get('steps', [])
        
        has_token_check = False
        has_twine_upload = False
        has_skip_message = False
        
        for step in steps:
            step_name = step.get('name', '').lower()
            step_run = step.get('run', '')
            
            # Check for token availability check
            if 'token availability' in step_name or 'check-token' in step.get('id', ''):
                has_token_check = True
                good_practices.append(f"Job '{job_name}' checks token availability")
            
            # Check for twine upload
            if 'twine upload' in step_run:
                has_twine_upload = True
                good_practices.append(f"Job '{job_name}' uses twine for upload")
            
            # Check for skip message
            if 'upload was skipped' in step_run:
                has_skip_message = True
                good_practices.append(f"Job '{job_name}' provides helpful skip message")
        
        # Check if this job does PyPI uploads (more specific check)
        is_pypi_job = any(
            ('pypi' in step.get('name', '').lower() and 'upload' in step.get('name', '').lower()) or
            ('pypi' in step.get('name', '').lower() and 'publish' in step.get('name', '').lower()) or
            'twine upload' in step.get('run', '') or
            'pypa/gh-action-pypi-publish' in step.get('uses', '')
            for step in steps
        )
        
        if is_pypi_job:
            if not has_token_check:
                missing_practices.append(f"Job '{job_name}' should check token availability")
            if not has_twine_upload:
                missing_practices.append(f"Job '{job_name}' should use twine for upload")
            if not has_skip_message:
                missing_practices.append(f"Job '{job_name}' should provide skip message when token unavailable")
    
    return good_practices, missing_practices

def validate_workflow(workflow_path):
    """Validate a single workflow file."""
    print(f"\n🔍 Validating {workflow_path.name}...")
    
    workflow = load_workflow(workflow_path)
    if not workflow:
        return False
    
    # Check for trusted publishing remnants
    tp_issues = check_for_trusted_publishing(workflow, workflow_path.name)
    
    # Check for proper API token usage
    good_practices, missing_practices = check_for_api_tokens(workflow, workflow_path.name)
    
    # Report results
    if tp_issues:
        print(f"⚠️  {workflow_path.name} - Trusted publishing remnants found:")
        for issue in tp_issues:
            print(f"   • {issue}")
    
    if missing_practices:
        print(f"⚠️  {workflow_path.name} - Missing API token best practices:")
        for practice in missing_practices:
            print(f"   • {practice}")
    
    if good_practices:
        print(f"✅ {workflow_path.name} - Good API token practices:")
        for practice in good_practices:
            print(f"   • {practice}")
    
    if not tp_issues and not missing_practices:
        print(f"✅ {workflow_path.name} - Properly configured for API tokens!")
    
    return len(tp_issues) == 0 and len(missing_practices) == 0

def main():
    """Main validation function."""
    print("🔧 GitHub Actions API Token Validator")
    print("=" * 50)
    
    # Find workflow directory
    workflows_dir = Path(__file__).parent / 'workflows'
    if not workflows_dir.exists():
        print(f"❌ Workflows directory not found: {workflows_dir}")
        sys.exit(1)
    
    # Find all workflow files
    workflow_files = list(workflows_dir.glob('*.yml')) + list(workflows_dir.glob('*.yaml'))
    
    if not workflow_files:
        print(f"❌ No workflow files found in {workflows_dir}")
        sys.exit(1)
    
    print(f"Found {len(workflow_files)} workflow files")
    
    all_valid = True
    for workflow_file in sorted(workflow_files):
        if not validate_workflow(workflow_file):
            all_valid = False
    
    print("\n" + "=" * 50)
    if all_valid:
        print("✅ All workflows are properly configured for API tokens!")
        print("\n📋 Required GitHub Secrets:")
        print("   • TEST_PYPI_API_TOKEN - for Test PyPI uploads")
        print("   • PYPI_API_TOKEN - for production PyPI uploads")
        print("\n📖 Setup Guide:")
        print("   See .github/PYPI_API_TOKEN_SETUP.md for detailed instructions")
    else:
        print("❌ Some workflows need updates for proper API token usage!")
        print("Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main()