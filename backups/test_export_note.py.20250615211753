"""
Basic tests for the export_note script.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# Add parent directory to path so we can import export_note
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import export_note  # noqa: E402


class TestExportNote(unittest.TestCase):
    """Test basic functionality of the export_note script."""

    def test_clean_text(self):
        """Test the clean_text function."""
        # Test cleaning of bullet points
        self.assertEqual(export_note.clean_text("- \n"), "- ")

        # Test cleaning of reference numbers
        self.assertEqual(export_note.clean_text("Text [1, 2, 3]"), "Text ")

        # Test cleaning of excessive whitespace
        self.assertEqual(export_note.clean_text("Line1\n\n\n\nLine2"), "Line1\n\nLine2")

        # Test cleaning of inline code formatting
        self.assertEqual(export_note.clean_text("`   code   `"), "`code`")

        # Test cleaning of bold text formatting
        self.assertEqual(export_note.clean_text("**  bold  **"), "**bold**")

    def test_find_parent_element_none(self):
        """Test find_parent_element returns None for invalid input."""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup("<html><body></body></html>", "html.parser")
        self.assertIsNone(export_note.find_parent_element(soup))

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_args(self, mock_parse_args):
        """Test the parse_args function."""
        mock_parse_args.return_value.input_path = "input.txt"
        mock_parse_args.return_value.output_path = "output.md"
        args = export_note.parse_args()
        self.assertEqual(args.input_path, "input.txt")
        self.assertEqual(args.output_path, "output.md")

    def test_create_note_from_texts(self):
        """Test the create_note_from_texts function."""
        # Test with empty list
        result = export_note.create_note_from_texts([])
        self.assertEqual(result["title"], "Untitled Note")
        self.assertEqual(result["note"], "")

        # Test with normal list
        result = export_note.create_note_from_texts(["# Title", "Content"])
        self.assertEqual(result["title"], "Title")
        self.assertEqual(result["note"], "# Title\nContent")

        # Test with empty title
        result = export_note.create_note_from_texts(["", "Content"])
        self.assertEqual(result["title"], "Untitled Note")
        self.assertEqual(result["note"], "\nContent")


if __name__ == "__main__":
    unittest.main()
