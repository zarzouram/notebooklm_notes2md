"""
Tests for tag formatting in Obsidian export.
"""

import os
import sys
import unittest

# Add parent directory to path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from notebooklm_notes2md.formatters.obsidian import format_yaml_frontmatter


class TestTagFormatting(unittest.TestCase):
    """Test the tag formatting for Obsidian compatibility."""

    def test_space_to_hyphen_conversion(self):
        """Test that spaces in tags are converted to hyphens."""
        metadata = {
            "title": "Test Document",
            "tags": ["Tag with spaces", "Another multi word tag", "SingleWord"]
        }

        frontmatter = format_yaml_frontmatter(metadata)

        # Check that spaces are converted to hyphens
        self.assertIn('  - "Tag-with-spaces"', frontmatter,
                      "Spaces in tags should be converted to hyphens")
        self.assertIn('  - "Another-multi-word-tag"', frontmatter,
                      "Spaces in multi-word tags should be converted to hyphens")
        self.assertIn('  - "SingleWord"', frontmatter,
                      "Tags without spaces should remain unchanged")

        # Ensure the original tag wasn't used
        self.assertNotIn('  - "Tag with spaces"', frontmatter,
                         "Original tag with spaces should not be in frontmatter")

    def test_special_character_handling(self):
        """Test that special characters in tags are properly handled."""
        metadata = {
            "title": "Test Document",
            "tags": [
                "Tag with #special! chars&",
                "123-numeric-start",
                "Valid_under_score",
                "Mixed-Case-Tag"
            ]
        }

        frontmatter = format_yaml_frontmatter(metadata)

        # Check that special characters are removed
        self.assertIn('  - "Tag-with-special-chars"', frontmatter,
                     "Special characters should be removed from tags")

        # Check that numeric prefixes are handled
        self.assertIn('  - "t123-numeric-start"', frontmatter,
                     "Tags starting with numbers should be prefixed with 't'")

        # Check that valid characters are preserved
        self.assertIn('  - "Valid_under_score"', frontmatter,
                     "Underscores should be preserved in tags")
        self.assertIn('  - "Mixed-Case-Tag"', frontmatter,
                     "Mixed case should be preserved in tags")


if __name__ == "__main__":
    unittest.main()
