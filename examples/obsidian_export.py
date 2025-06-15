#!/usr/bin/env python3
"""
Example script demonstrating how to use the NotebookLM notes2md package
programmatically to extract metadata and format as Obsidian markdown.
"""

import argparse
import sys

from bs4 import BeautifulSoup

from notebooklm_notes2md.core.parser import parse_notes
from notebooklm_notes2md.extractors.metadata import extract_metadata
from notebooklm_notes2md.formatters.obsidian import format_obsidian_markdown


def main():
    """Parse command line arguments and process the input file."""
    parser = argparse.ArgumentParser(
        description="Example script for extracting metadata and formatting as Obsidian markdown."
    )
    parser.add_argument(
        "input_file",
        help="Path to the input HTML file containing NotebookLM notes"
    )
    parser.add_argument(
        "output_file",
        help="Path to the output Markdown file"
    )

    args = parser.parse_args()

    # Read the input file
    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found: {args.input_file}")
        sys.exit(1)

    # Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract metadata
    metadata = extract_metadata(soup)
    print(f"Extracted metadata:")
    print(f"  Title: {metadata['title']}")
    print(f"  Tags: {', '.join(metadata['tags']) if metadata['tags'] else 'None'}")
    print(f"  Summary: {'Found' if 'summary' in metadata else 'Not found'}")

    # Parse notes
    notes = parse_notes(soup)
    print(f"Found {len(notes)} notes in the input file")

    # Format as Obsidian markdown
    markdown_content = format_obsidian_markdown(notes, metadata)

    # Write to output file
    try:
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Successfully exported to Obsidian format: {args.output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
