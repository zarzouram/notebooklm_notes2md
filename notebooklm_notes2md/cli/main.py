"""
Command-line interface for NotebookLM notes to Markdown/PDF converter.
"""

import argparse
import os
import sys
from typing import Dict, Optional

from bs4 import BeautifulSoup
from markdown_pdf import MarkdownPdf, Section

from notebooklm_notes2md.core.parser import parse_notes
from notebooklm_notes2md.extractors.metadata import extract_metadata
from notebooklm_notes2md.formatters.obsidian import format_obsidian_markdown
from notebooklm_notes2md.formatters.standard import format_standard_markdown
from notebooklm_notes2md.utils.text_processing import clean_text


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        Namespace containing the parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Export NotebookLM notes to PDF or Markdown.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "input_path",
        type=str,
        help="Path to the input HTML file containing NotebookLM notes",
    )

    parser.add_argument(
        "output_path",
        type=str,
        help="Path to the output file (must end with .pdf or .md)",
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["standard", "obsidian"],
        default="standard",
        help="Output format style for Markdown files",
    )

    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    """
    Validate command line arguments.

    Args:
        args: Parsed command line arguments

    Raises:
        SystemExit: If arguments fail validation
    """
    # Validate input file exists
    if not os.path.isfile(args.input_path):
        print(f"Error: Input file not found: {args.input_path}")
        sys.exit(1)

    # Validate output file extension
    valid_extensions = [".pdf", ".md"]
    output_ext = "." + args.output_path.split(".")[-1].lower()

    if output_ext not in valid_extensions:
        extensions_str = ", ".join(valid_extensions)
        print(f"Error: Output path must end with one of: {extensions_str}")
        sys.exit(1)

    # Validate output directory exists
    output_dir = os.path.dirname(args.output_path)
    if output_dir and not os.path.exists(output_dir):
        print(f"Error: Output directory does not exist: {output_dir}")
        sys.exit(1)


def read_input_file(file_path: str) -> str:
    """
    Read and return the contents of the input file.

    Args:
        file_path: Path to the input file

    Returns:
        Contents of the file as a string

    Raises:
        SystemExit: If the file cannot be read
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                print(f"Warning: Input file is empty: {file_path}")
            return content
    except FileNotFoundError:
        print(f"Error: Input file not found: {file_path}")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when reading file: {file_path}")
        sys.exit(1)
    except UnicodeDecodeError:
        print("Error: File encoding issue.")
        print(f"Please ensure {file_path} is UTF-8 encoded.")
        sys.exit(1)
    except Exception as e:
        print("Error reading input file:")
        print(f"{e}")
        sys.exit(1)


def export_to_pdf(notes: list, output_path: str) -> None:
    """
    Export notes to a PDF file.

    Args:
        notes: List of note dictionaries
        output_path: Path to save the PDF file

    Raises:
        SystemExit: If there's an error creating the PDF
    """
    try:
        pdf = MarkdownPdf(toc_level=1, optimize=True)

        for item in notes:
            clean_content = clean_text(item["note"])
            pdf.add_section(Section(clean_content))

        pdf.save(output_path)
    except PermissionError:
        print(f"Error: Permission denied when writing to {output_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error creating PDF file: {e}")
        sys.exit(1)


def export_to_markdown(
    notes: list,
    output_path: str,
    format_type: str = "standard",
    metadata: Optional[Dict] = None
) -> None:
    """
    Export notes to a Markdown file.

    Args:
        notes: List of note dictionaries
        output_path: Path to save the Markdown file
        format_type: Format type ("standard" or "obsidian")
        metadata: Optional metadata dictionary

    Raises:
        SystemExit: If there's an error writing the file
    """
    try:
        if format_type == "obsidian" and metadata:
            content = format_obsidian_markdown(notes, metadata)
        else:
            content = format_standard_markdown(notes, metadata)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    except PermissionError:
        print(f"Error: Permission denied when writing to {output_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error writing Markdown file: {e}")
        sys.exit(1)


def export_notes(
    notes: list,
    output_path: str,
    format_type: str = "standard",
    metadata: Optional[Dict] = None
) -> None:
    """
    Export all notes to a single PDF or Markdown file based on extension.

    Args:
        notes: List of note dictionaries
        output_path: Path to save the output file
        format_type: Format type for Markdown output
        metadata: Optional metadata dictionary

    Raises:
        SystemExit: If the output path doesn't have a valid extension
    """
    if output_path.lower().endswith(".pdf"):
        export_to_pdf(notes, output_path)
    elif output_path.lower().endswith(".md"):
        export_to_markdown(notes, output_path, format_type, metadata)
    else:
        print("Error: Output path must end with .pdf or .md")
        sys.exit(1)


def main() -> None:
    """
    Main entry point for the script.

    Parses command line arguments, reads and processes the input file,
    extracts notes from HTML, and exports to the specified format.
    """
    args = parse_args()
    validate_args(args)

    note_data = read_input_file(args.input_path)
    soup = BeautifulSoup(note_data, "html.parser")

    # Extract metadata (for Cycle 1 features)
    metadata = extract_metadata(soup)

    # Parse notes
    notes = parse_notes(soup)
    if not notes:
        print("Warning: No notes were found in the input file.")

    # Export notes with the specified format
    export_notes(notes, args.output_path, args.format, metadata)
    print(f"Successfully exported {len(notes)} notes to {args.output_path}")


if __name__ == "__main__":
    main()
