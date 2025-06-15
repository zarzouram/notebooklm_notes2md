#!/usr/bin/env python3
"""
Example script demonstrating how to customize metadata extraction and
create your own custom formatter for NotebookLM notes.
"""

import argparse
import datetime
import sys
from typing import Any, Dict, List

from bs4 import BeautifulSoup

from notebooklm_notes2md.core.parser import parse_notes
from notebooklm_notes2md.extractors.metadata import extract_metadata
from notebooklm_notes2md.utils.text_processing import clean_text


def format_academic_markdown(notes: List[Dict[str, str]], metadata: Dict[str, Any]) -> str:
    """
    Custom formatter for academic-style markdown.

    Args:
        notes: List of note dictionaries
        metadata: Dictionary of metadata extracted from the document

    Returns:
        Academic-formatted markdown as a string
    """
    # Start with frontmatter
    frontmatter = ["---"]

    # Add title
    if "title" in metadata and metadata["title"]:
        frontmatter.append(f'title: "{metadata["title"]}"')

    # Add tags if available
    if "tags" in metadata and metadata["tags"]:
        frontmatter.append("keywords:")
        for tag in metadata["tags"]:
            frontmatter.append(f'  - "{tag}"')

    # Add date and author
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    frontmatter.append(f"date: {current_date}")
    frontmatter.append('author: "Generated from NotebookLM"')

    # Add bibliography reference
    frontmatter.append("bibliography: references.bib")
    frontmatter.append("reference-section-title: References")

    frontmatter.append("---\n")
    result = "\n".join(frontmatter)

    # Add abstract if summary is available
    if "summary" in metadata and metadata["summary"]:
        result += "## Abstract\n\n"
        result += metadata["summary"] + "\n\n"

    # Add document title as main heading
    result += f"# {metadata['title']}\n\n"

    # Add all notes
    for note in notes:
        clean_content = clean_text(note["note"])
        result += clean_content + "\n\n"

    return result


def main():
    """Parse command line arguments and process the input file."""
    parser = argparse.ArgumentParser(
        description="Example script for creating custom formatters."
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

    # Add custom metadata
    metadata["custom_field"] = "This is a custom field"

    # Parse notes
    notes = parse_notes(soup)

    # Format with custom academic formatter
    markdown_content = format_academic_markdown(notes, metadata)

    # Write to output file
    try:
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Successfully exported to academic format: {args.output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
