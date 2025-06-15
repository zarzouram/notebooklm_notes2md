"""
Tests for Obsidian formatter functionality.
"""

import datetime
import os
import sys
import unittest
from typing import Any, Dict

# Add parent directory to path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from notebooklm_notes2md.formatters.obsidian import (
    format_obsidian_markdown,
    format_summary_as_callout,
    format_yaml_frontmatter,
)


class TestObsidianFormatter(unittest.TestCase):
    """Test the Obsidian formatter functionality."""

    def setUp(self):
        """Set up test data."""
        self.metadata = {
            "title": "Test Document",
            "tags": ["Tag1", "Tag2", "Tag3"],
            "summary": "This is a test summary with **bold** text."
        }

        self.notes = [
            {"title": "Note 1", "note": "# Note 1\n\nThis is note 1 content."},
            {"title": "Note 2", "note": "# Note 2\n\nThis is note 2 content."}
        ]

    def test_format_yaml_frontmatter(self):
        """Test formatting of YAML frontmatter."""
        frontmatter = format_yaml_frontmatter(self.metadata)

        # Check that frontmatter is valid
        self.assertTrue(frontmatter.startswith("---\n"), "Frontmatter should start with ---")
        self.assertTrue("---\n\n" in frontmatter, "Frontmatter should end with ---")

        # Check that metadata is included
        self.assertIn('title: "Test Document"', frontmatter, "Title missing from frontmatter")
        self.assertIn("tags:", frontmatter, "Tags section missing from frontmatter")
        self.assertIn('  - "Tag1"', frontmatter, "Tag1 missing from frontmatter")

        # Check that citation fields are included
        self.assertIn("citekey: {{citekey}}", frontmatter, "Citekey missing from frontmatter")
        self.assertIn("status: unread", frontmatter, "Status missing from frontmatter")

        # Check that current date is included
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.assertIn(f"date: {today}", frontmatter, "Current date missing from frontmatter")

    def test_format_summary_as_callout(self):
        """Test formatting of summary as callout block."""
        callout = format_summary_as_callout(self.metadata["summary"])

        # Check that callout is properly formatted
        self.assertTrue(callout.startswith("> [!summary]\n"), "Callout should start with summary marker")
        self.assertIn("> This is a test summary with **bold** text.", callout, "Summary content missing from callout")

    def test_format_obsidian_markdown(self):
        """Test formatting of complete Obsidian markdown."""
        markdown = format_obsidian_markdown(self.notes, self.metadata)

        # Check that all components are present
        self.assertTrue(markdown.startswith("---\n"), "Markdown should start with frontmatter")
        self.assertIn("> [!summary]\n", markdown, "Summary callout missing from markdown")
        self.assertIn("# Test Document", markdown, "Document title missing from markdown")
        self.assertIn("This is note 1 content.", markdown, "Note 1 content missing from markdown")
        self.assertIn("This is note 2 content.", markdown, "Note 2 content missing from markdown")


if __name__ == "__main__":
    unittest.main()
