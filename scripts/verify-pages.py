#!/usr/bin/env python3
"""
Verify GitHub Pages deployment for ThreePaneWindows documentation.
"""

import sys
import time
from urllib.parse import urljoin

import requests


def check_url(url, timeout=10):
    """Check if a URL is accessible."""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200, response.status_code
    except requests.RequestException as e:
        return False, str(e)


def verify_pages_deployment(base_url):
    """Verify that GitHub Pages deployment is working."""

    print(f"🔍 Verifying GitHub Pages deployment at: {base_url}")
    print("=" * 60)

    # Essential pages to check
    pages_to_check = [
        ("Main Page", ""),
        ("API Reference", "api/"),
        ("Installation Guide", "installation.html"),
        ("Quick Start", "quickstart.html"),
        ("Examples", "examples/"),
        ("User Guide", "user_guide/"),
        ("Contributing", "contributing.html"),
        ("Changelog", "changelog.html"),
        ("License", "license.html"),
    ]

    results = []

    for name, path in pages_to_check:
        url = urljoin(base_url.rstrip("/") + "/", path)
        print(f"Checking {name}: {url}")

        success, status = check_url(url)
        results.append((name, url, success, status))

        if success:
            print(f"  ✅ {name} - OK")
        else:
            print(f"  ❌ {name} - Failed ({status})")

        # Small delay to avoid overwhelming the server
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print("📊 Summary:")

    successful = sum(1 for _, _, success, _ in results if success)
    total = len(results)

    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")

    if successful == total:
        print(
            "\n🎉 All pages are accessible! GitHub Pages deployment is working correctly."
        )
        return True
    else:
        print(f"\n⚠️  {total - successful} page(s) failed to load.")
        print("Failed pages:")
        for name, url, success, status in results:
            if not success:
                print(f"  • {name}: {url} ({status})")

        print(
            f"\n🔄 If the deployment is still in progress, try again in a few minutes."
        )
        print(
            "📖 Check the Actions tab in your GitHub repository for deployment status."
        )
        return False


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python verify-pages.py <base_url>")
        print(
            "Example: python verify-pages.py https://username.github.io/threepanewindows/"
        )
        sys.exit(1)

    base_url = sys.argv[1]
    success = verify_pages_deployment(base_url)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
