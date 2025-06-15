"""
Tests for metadata extraction functionality.
"""

import os
import sys
import unittest
from bs4 import BeautifulSoup

# Add parent directory to path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from notebooklm_notes2md.extractors.metadata import (
    extract_document_title,
    extract_summary,
    extract_key_topics,
    extract_metadata
)


class TestMetadataExtraction(unittest.TestCase):
    """Test the metadata extraction functionality."""

    def setUp(self):
        """Set up test data."""
        # Path to test file
        test_file_path = os.path.join(os.path.dirname(__file__), 'full_summary.html')

        # Load test HTML
        with open(test_file_path, 'r', encoding='utf-8') as f:
            self.html_content = f.read()

        # Parse HTML
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def test_extract_document_title(self):
        """Test extraction of document title."""
        title = extract_document_title(self.soup)
        self.assertEqual(
            title,
            "Simulating a Fair Market: Mechanics and Price Behavior",
            "Failed to extract correct document title"
        )

    def test_extract_summary(self):
        """Test extraction of document summary."""
        summary = extract_summary(self.soup)
        self.assertIsNotNone(summary, "Failed to extract summary")
        self.assertTrue(
            "mechanics of simulating a fair market" in summary,
            "Summary does not contain expected content"
        )

    def test_extract_key_topics(self):
        """Test extraction of key topics."""
        topics = extract_key_topics(self.soup)
        expected_topics = [
            "Market Simulation Mechanics",
            "Auction Pricing",
            "Price Behavior",
            "Random Movement",
            "Wealth Limits"
        ]

        self.assertEqual(len(topics), 5, "Incorrect number of topics extracted")
        for topic in expected_topics:
            self.assertIn(topic, topics, f"Topic '{topic}' not found in extracted topics")

    def test_extract_metadata(self):
        """Test extraction of all metadata."""
        metadata = extract_metadata(self.soup)

        # Check that required keys exist
        self.assertIn("title", metadata, "Title missing from metadata")
        self.assertIn("tags", metadata, "Tags missing from metadata")
        self.assertIn("summary", metadata, "Summary missing from metadata")

        # Check tag count
        self.assertEqual(len(metadata["tags"]), 5, "Incorrect number of tags in metadata")


if __name__ == "__main__":
    unittest.main()
