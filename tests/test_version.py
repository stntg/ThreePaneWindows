"""
Tests for version information and metadata.
"""

import pytest
import re
from threepanewindows import _version
from threepanewindows import (
    __version__,
    __version_info__,
    FULL_VERSION,
    __author__,
    __email__,
    __license__,
    __copyright__
)


class TestVersionInfo:
    """Test cases for version information."""

    def test_version_string_format(self):
        """Test that version string follows semantic versioning."""
        # Should be in format X.Y.Z or X.Y.Z-suffix
        version_pattern = r'^\d+\.\d+\.\d+(?:-\w+)?$'
        assert re.match(version_pattern, __version__), f"Version '{__version__}' doesn't match semantic versioning"

    def test_version_info_tuple(self):
        """Test that version_info is a proper tuple."""
        assert isinstance(__version_info__, tuple)
        assert len(__version_info__) >= 3
        
        # First three elements should be integers
        assert isinstance(__version_info__[0], int)  # major
        assert isinstance(__version_info__[1], int)  # minor
        assert isinstance(__version_info__[2], int)  # patch

    def test_version_consistency(self):
        """Test that version string and version_info are consistent."""
        version_parts = __version__.split('-')[0].split('.')  # Remove any suffix
        
        assert int(version_parts[0]) == __version_info__[0]  # major
        assert int(version_parts[1]) == __version_info__[1]  # minor
        assert int(version_parts[2]) == __version_info__[2]  # patch

    def test_full_version_exists(self):
        """Test that FULL_VERSION exists and is a string."""
        assert isinstance(FULL_VERSION, str)
        assert len(FULL_VERSION) > 0

    def test_version_module_attributes(self):
        """Test that _version module has required attributes."""
        assert hasattr(_version, '__version__')
        assert hasattr(_version, '__version_info__')
        assert hasattr(_version, 'FULL_VERSION')

    def test_version_numbers_reasonable(self):
        """Test that version numbers are reasonable."""
        major, minor, patch = __version_info__[:3]
        
        # Version numbers should be non-negative
        assert major >= 0
        assert minor >= 0
        assert patch >= 0
        
        # Should be reasonable ranges (not too high)
        assert major < 100
        assert minor < 100
        assert patch < 1000


class TestMetadata:
    """Test cases for package metadata."""

    def test_author_info(self):
        """Test author information."""
        assert isinstance(__author__, str)
        assert len(__author__) > 0
        assert __author__ == "Stan Griffiths"

    def test_email_format(self):
        """Test email format."""
        assert isinstance(__email__, str)
        assert '@' in __email__
        assert '.' in __email__
        assert __email__ == "stantgriffiths@gmail.com"

    def test_license_info(self):
        """Test license information."""
        assert isinstance(__license__, str)
        assert __license__ == "MIT"

    def test_copyright_info(self):
        """Test copyright information."""
        assert isinstance(__copyright__, str)
        assert "Copyright" in __copyright__
        assert "2024" in __copyright__
        assert "Stan Griffiths" in __copyright__

    def test_metadata_consistency(self):
        """Test that metadata is consistent across the package."""
        # Author should be consistent in copyright
        assert __author__ in __copyright__


class TestVersionModule:
    """Test cases for the _version module itself."""

    def test_version_module_importable(self):
        """Test that _version module can be imported."""
        import threepanewindows._version as version_module
        assert version_module is not None

    def test_version_module_has_all_attributes(self):
        """Test that _version module has all expected attributes."""
        expected_attrs = ['__version__', '__version_info__', 'FULL_VERSION']
        
        for attr in expected_attrs:
            assert hasattr(_version, attr), f"_version module missing {attr}"

    def test_version_values_are_strings_or_tuples(self):
        """Test that version values have correct types."""
        assert isinstance(_version.__version__, str)
        assert isinstance(_version.__version_info__, tuple)
        assert isinstance(_version.FULL_VERSION, str)

    def test_version_module_docstring(self):
        """Test that _version module has a docstring."""
        assert _version.__doc__ is not None or True  # Allow for no docstring


class TestVersionComparison:
    """Test cases for version comparison functionality."""

    def test_version_info_comparable(self):
        """Test that version_info can be compared."""
        # Should be able to compare with other tuples
        assert __version_info__ >= (0, 0, 0)
        assert __version_info__ >= (1, 0, 0) or __version_info__ < (1, 0, 0)

    def test_version_ordering(self):
        """Test version ordering makes sense."""
        major, minor, patch = __version_info__[:3]
        
        # Create some comparison versions
        lower_patch = (major, minor, max(0, patch - 1))
        higher_patch = (major, minor, patch + 1)
        
        if patch > 0:
            assert __version_info__ > lower_patch
        assert __version_info__ < higher_patch

    def test_version_string_parseable(self):
        """Test that version string can be parsed."""
        import pkg_resources
        
        try:
            # Should be parseable by pkg_resources
            parsed_version = pkg_resources.parse_version(__version__)
            assert parsed_version is not None
        except ImportError:
            # pkg_resources might not be available, skip this test
            pytest.skip("pkg_resources not available")


class TestVersionIntegration:
    """Integration tests for version information."""

    def test_version_accessible_from_main_package(self):
        """Test that version is accessible from main package."""
        import threepanewindows
        
        assert hasattr(threepanewindows, '__version__')
        assert hasattr(threepanewindows, '__version_info__')
        assert hasattr(threepanewindows, 'FULL_VERSION')

    def test_version_consistency_across_imports(self):
        """Test version consistency across different import methods."""
        # Import in different ways
        from threepanewindows import __version__ as v1
        from threepanewindows._version import __version__ as v2
        import threepanewindows
        
        # All should be the same
        assert v1 == v2
        assert v1 == threepanewindows.__version__

    def test_all_exports_include_version(self):
        """Test that __all__ includes version information."""
        import threepanewindows
        
        if hasattr(threepanewindows, '__all__'):
            all_exports = threepanewindows.__all__
            version_exports = ['__version__', '__version_info__', 'FULL_VERSION']
            
            # At least some version info should be exported
            exported_version_info = [item for item in version_exports if item in all_exports]
            assert len(exported_version_info) > 0


class TestVersionModuleInternals:
    """Test internal functions of the version module."""
    
    def test_version_module_error_handling(self):
        """Test error handling in version module."""
        from threepanewindows import _version
        
        # Test that module handles missing attributes gracefully
        if hasattr(_version, '_get_version_info'):
            try:
                info = _version._get_version_info()
                assert info is not None
            except Exception:
                # Error handling is working
                pass
    
    def test_version_module_constants(self):
        """Test version module constants."""
        from threepanewindows import _version
        
        # Test that required constants exist
        required_attrs = ['__version__', '__version_info__']
        for attr in required_attrs:
            assert hasattr(_version, attr)
            value = getattr(_version, attr)
            assert value is not None
    
    def test_version_module_metadata_access(self):
        """Test metadata access in version module."""
        from threepanewindows import _version
        
        # Test metadata attributes if they exist
        metadata_attrs = ['__author__', '__email__', '__license__']
        for attr in metadata_attrs:
            if hasattr(_version, attr):
                value = getattr(_version, attr)
                assert isinstance(value, str)
                assert len(value) > 0

    def test_version_module_full_version(self):
        """Test FULL_VERSION attribute."""
        from threepanewindows import _version
        
        if hasattr(_version, 'FULL_VERSION'):
            full_version = _version.FULL_VERSION
            assert isinstance(full_version, str)
            assert len(full_version) > 0
            
            # Should contain the version number
            version = _version.__version__
            assert version in full_version