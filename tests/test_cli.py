"""
Tests for CLI functionality.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# Add parent directory to path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from notebooklm_notes2md.cli.main import export_notes, parse_args, validate_args


class TestCLI(unittest.TestCase):
    """Test the CLI functionality."""

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_args(self, mock_parse_args):
        """Test the parse_args function."""
        # Set up mock arguments
        mock_parse_args.return_value.input_path = "input.html"
        mock_parse_args.return_value.output_path = "output.md"
        mock_parse_args.return_value.format = "obsidian"

        # Call parse_args
        args = parse_args()

        # Check results
        self.assertEqual(args.input_path, "input.html")
        self.assertEqual(args.output_path, "output.md")
        self.assertEqual(args.format, "obsidian")

    @patch('sys.exit')
    def test_validate_args_file_not_found(self, mock_exit):
        """Test validate_args with non-existent input file."""
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(suffix='.md') as temp_file:
            args_mock = unittest.mock.Mock()
            args_mock.input_path = "nonexistent_file.html"
            args_mock.output_path = temp_file.name

            # Call validate_args
            validate_args(args_mock)

            # Check that sys.exit was called
            mock_exit.assert_called_once()

    @patch('sys.exit')
    def test_validate_args_invalid_extension(self, mock_exit):
        """Test validate_args with invalid output extension."""
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile() as temp_input:
            args_mock = unittest.mock.Mock()
            args_mock.input_path = temp_input.name
            args_mock.output_path = "output.txt"  # Invalid extension

            # Call validate_args
            validate_args(args_mock)

            # Check that sys.exit was called
            mock_exit.assert_called_once()

    @patch('notebooklm_notes2md.cli.main.export_to_markdown')
    def test_export_notes_markdown(self, mock_export_to_markdown):
        """Test export_notes with markdown output."""
        notes = [{"title": "Test", "note": "Test note"}]
        metadata = {"title": "Test Document", "tags": ["test"]}

        # Call export_notes with markdown output
        export_notes(notes, "output.md", "standard", metadata)

        # Check that export_to_markdown was called
        mock_export_to_markdown.assert_called_once()

    @patch('notebooklm_notes2md.cli.main.export_to_pdf')
    def test_export_notes_pdf(self, mock_export_to_pdf):
        """Test export_notes with PDF output."""
        notes = [{"title": "Test", "note": "Test note"}]
        metadata = {"title": "Test Document", "tags": ["test"]}

        # Call export_notes with PDF output
        export_notes(notes, "output.pdf", "standard", metadata)

        # Check that export_to_pdf was called
        mock_export_to_pdf.assert_called_once()


if __name__ == "__main__":
    unittest.main()
