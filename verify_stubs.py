#!/usr/bin/env python3
"""
Verification script for threepanewindows type stubs.

This script tests that the stubs are properly structured and can be imported.
"""


import sys
from pathlib import Path


def verify_stub_file(stub_path: Path) -> bool:
    """Verify that a stub file can be parsed."""
    try:
        with open(stub_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Basic syntax check - compile the stub as Python code
        compile(content, str(stub_path), "exec")
        print(f"✓ {stub_path.name} - syntax OK")
        return True
    except SyntaxError as e:
        print(f"✗ {stub_path.name} - syntax error: {e}")
        return False
    except Exception as e:
        print(f"✗ {stub_path.name} - error: {e}")
        return False


def main():
    """Verify threepanewindows type stubs."""
    stubs_dir = Path(__file__).parent / "threepanewindows-stubs"

    if not stubs_dir.exists():
        print(f"Error: Stubs directory not found: {stubs_dir}")
        sys.exit(1)

    print("Verifying threepanewindows type stubs...")
    print("=" * 50)

    # Find all .pyi files
    stub_files = list(stubs_dir.rglob("*.pyi"))

    if not stub_files:
        print("Error: No .pyi files found in stubs directory")
        sys.exit(1)

    success_count = 0
    total_count = len(stub_files)

    for stub_file in sorted(stub_files):
        if verify_stub_file(stub_file):
            success_count += 1

    print("=" * 50)
    print(f"Results: {success_count}/{total_count} stub files verified successfully")

    # Check for py.typed file
    py_typed = stubs_dir / "py.typed"
    if py_typed.exists():
        print("✓ py.typed file found")
    else:
        print("✗ py.typed file missing")
        success_count -= 1

    if success_count == total_count:
        print("\n🎉 All stubs verified successfully!")
        return 0
    else:
        print(f"\n❌ {total_count - success_count} issues found")
        return 1


if __name__ == "__main__":
    sys.exit(main())
