#!/usr/bin/env python3
"""
Quick script to fix common mypy type annotation issues
"""
import re
import os
from pathlib import Path

def fix_common_type_issues(file_path):
    """Fix common type annotation issues in a Python file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix common patterns
    # 1. Add -> None to methods that don't return anything
    content = re.sub(
        r'(\s+def\s+\w+\([^)]*\)):\s*\n(\s+"""[^"]*"""\s*\n)?(\s+)',
        lambda m: f"{m.group(1)} -> None:\n{m.group(2) or ''}{m.group(3)}",
        content
    )
    
    # 2. Add basic type hints to common parameters
    content = re.sub(r'def\s+(\w+)\(self,\s*([^)]+)\):', 
                    lambda m: f"def {m.group(1)}(self, {add_basic_types(m.group(2))}):", 
                    content)
    
    # Only write if content changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {file_path}")

def add_basic_types(params_str):
    """Add basic type hints to parameters."""
    # This is a simple heuristic - in practice you'd want more sophisticated logic
    params = [p.strip() for p in params_str.split(',')]
    typed_params = []
    
    for param in params:
        if '=' in param:
            name, default = param.split('=', 1)
            name = name.strip()
            default = default.strip()
            
            # Guess type from default value
            if default == 'None':
                typed_params.append(f"{name}: Optional[Any] = {default}")
            elif default.isdigit():
                typed_params.append(f"{name}: int = {default}")
            elif default in ['True', 'False']:
                typed_params.append(f"{name}: bool = {default}")
            elif default.startswith('"') or default.startswith("'"):
                typed_params.append(f"{name}: str = {default}")
            else:
                typed_params.append(f"{name}: Any = {default}")
        else:
            # No default value - assume Any for now
            typed_params.append(f"{param}: Any")
    
    return ', '.join(typed_params)

if __name__ == "__main__":
    # This is too risky to run automatically - let's do it manually
    print("This script is for reference only - manual fixes are safer")