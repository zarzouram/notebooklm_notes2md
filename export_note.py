"""
NotebookLM Notes to PDF/Markdown Converter

This script converts HTML-formatted notes exported from Google NotebookLM
into Markdown format and exports them as PDF or Markdown files.

Usage:
    python export_note.py <input_path> <output_path>

Args:
    input_path: Path to the input HTML file containing NotebookLM notes
    output_path: Path to the output file (must end with .pdf or .md)
"""

import argparse
import os
import re
import sys
from typing import Any, Dict, Generator, List, Optional

from bs4 import BeautifulSoup
from bs4.element import Comment, Tag
from markdown_pdf import MarkdownPdf, Section


def extract_tag_classes(tag: Tag) -> List[str]:
    """
    Extract classes from a BeautifulSoup tag safely.

    Args:
        tag: The BeautifulSoup tag to extract classes from

    Returns:
        A list of class names
    """
    tag_classes_raw = tag.get("class")
    if isinstance(tag_classes_raw, (list, tuple)):
        return list(tag_classes_raw)
    return []


def format_span_text(text: str, tag_classes: List[str]) -> str:
    """
    Format span text based on its classes.

    Args:
        text: The text content of the span
        tag_classes: List of classes applied to the span

    Returns:
        Formatted text with markdown syntax
    """
    if "bold" in tag_classes:
        text = f" **{text}** "
    if "code" in tag_classes:
        text = f" `{text}` "
    return text


def process_div_prefix(tag_classes: List[str]) -> str:
    """
    Determine prefix for div content based on its classes.

    Args:
        tag_classes: List of classes applied to the div

    Returns:
        Prefix string to be added before div content
    """
    if "heading3" in tag_classes:
        return "## "
    elif "paragraph" in tag_classes:
        return "\n"
    elif "bullet" in tag_classes:
        return "- "
    return ""


def drill_into_tag(tag: Any) -> str:
    """
    Recursively extract and format text from a BeautifulSoup tag.

    Args:
        tag: The BeautifulSoup tag to process

    Returns:
        Formatted Markdown text
    """
    if not isinstance(tag, Tag):
        return ""

    tag_classes = extract_tag_classes(tag)

    # Handle span elements (leaf nodes with text)
    if tag.name == "span":
        return format_span_text(tag.text, tag_classes)

    # Handle div elements (may contain other elements)
    elif tag.name == "div":
        prefix = process_div_prefix(tag_classes)
        if prefix in ["- "]:  # Special case for bullet points
            return prefix

        # Process all children and combine their results
        texts = prefix
        for child in getattr(tag, "children", []):
            texts += drill_into_tag(child)
        return texts

    # Process any other tag with children
    texts = ""
    for child in getattr(tag, "children", []):
        texts += drill_into_tag(child)
    return texts


def is_comment_separator(child: Any) -> bool:
    """
    Check if a node is an empty comment separator.

    Args:
        child: A BeautifulSoup node

    Returns:
        True if the node is an empty comment, False otherwise
    """
    return getattr(child, "string", None) == "" and isinstance(child, Comment)


def inner_childs_with_split(tag: Any) -> Generator[Any, None, None]:
    """
    Yield children of a tag, marking HTML comments as separators.

    Args:
        tag: The BeautifulSoup tag whose children to process

    Yields:
        Either the child node or an empty string for comment separators
    """
    for child in getattr(tag, "children", []):
        if is_comment_separator(child):
            yield ""  # Empty string as a split marker
        else:
            yield child


def find_parent_element(soup: BeautifulSoup) -> Optional[Tag]:
    """
    Find the parent element containing all notes.

    Args:
        soup: The BeautifulSoup object of the parsed HTML

    Returns:
        The parent Tag object or None if not found
    """
    parent = soup.find("labs-tailwind-doc-viewer")
    if (
        not parent
        or not hasattr(parent, "children")
        or not isinstance(parent, Tag)
    ):
        return None
    return parent


def create_note_from_texts(texts: List[str]) -> Dict[str, str]:
    """
    Create a note dictionary from a list of text fragments.

    Args:
        texts: List of text fragments that make up a note

    Returns:
        Dictionary with title and note content
    """
    if not texts:
        return {"title": "Untitled Note", "note": ""}

    # Clean up the first line for title extraction
    title_line = texts[0].strip()

    # Remove markdown heading markers for title
    title = re.sub(r"^#+\s*", "", title_line).strip()

    # Use a default title if empty
    if not title:
        title = "Untitled Note"

    return {"title": title, "note": "\n".join(texts)}


def parse_notes(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """
    Parse the soup and extract notes as a list of dicts with title and note.

    Args:
        soup: The BeautifulSoup object of the parsed HTML

    Returns:
        List of dictionaries, each containing a note with its title
    """
    notes: List[Dict[str, str]] = []
    texts: List[str] = []

    parent = find_parent_element(soup)
    if not parent:
        print("Could not find 'labs-tailwind-doc-viewer' in the HTML.")
        return notes

    # Process each structural element
    for child in getattr(parent, "children", []):
        if not isinstance(child, Tag):
            continue

        # Process inner elements
        for inner_child in inner_childs_with_split(child):
            if not isinstance(inner_child, Tag):
                # Handle separator (empty string)
                if inner_child == "" and texts:
                    notes.append(create_note_from_texts(texts))
                    texts = []
                continue

            # Process content
            text = drill_into_tag(inner_child).strip()
            if texts and text == "":
                # Empty text after content signals end of a note
                notes.append(create_note_from_texts(texts))
                texts = []
            elif text:
                texts.append(text)
                texts.append("\n")

    # Add the last note if there's remaining text
    if texts:
        notes.append(create_note_from_texts(texts))

    # Reverse to maintain original order
    if notes:
        notes.reverse()

    return notes


def clean_text(text: str) -> str:
    """
    Clean up text by fixing formatting issues and removing references.

    Args:
        text: Raw note text

    Returns:
        Cleaned text ready for export
    """
    # Fix bullet point formatting
    text = re.sub(r"-(\n+)", "- ", text)

    # Remove reference numbers like [1, 2] or [3]
    text = re.sub(r"\[\s*\d+(?:\s*[-,]\s*\d+)*\s*\]", "", text)

    # Fix excessive whitespace between paragraphs
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Fix inline code formatting
    text = re.sub(r"`\s+", "`", text)
    text = re.sub(r"\s+`", "`", text)

    # Ensure proper spacing around bold text
    text = re.sub(r"\*\*\s+", "**", text)
    text = re.sub(r"\s+\*\*", "**", text)

    return text


def export_to_pdf(notes: List[Dict[str, str]], output_path: str) -> None:
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


def export_to_markdown(notes: List[Dict[str, str]], output_path: str) -> None:
    """
    Export notes to a Markdown file.

    Args:
        notes: List of note dictionaries
        output_path: Path to save the Markdown file

    Raises:
        SystemExit: If there's an error writing the file
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            for item in notes:
                clean_content = clean_text(item["note"])
                f.write(clean_content)
                f.write("\n\n")
    except PermissionError:
        print(f"Error: Permission denied when writing to {output_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error writing Markdown file: {e}")
        sys.exit(1)


def export_notes(notes: List[Dict[str, str]], output_path: str) -> None:
    """
    Export all notes to a single PDF or Markdown file based on extension.

    Args:
        notes: List of note dictionaries
        output_path: Path to save the output file

    Raises:
        SystemExit: If the output path doesn't have a valid extension
    """
    if output_path.lower().endswith(".pdf"):
        export_to_pdf(notes, output_path)
    elif output_path.lower().endswith(".md"):
        export_to_markdown(notes, output_path)
    else:
        print("Error: Output path must end with .pdf or .md")
        sys.exit(1)


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

    return parser.parse_args()


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

    notes = parse_notes(soup)
    if not notes:
        print("Warning: No notes were found in the input file.")

    export_notes(notes, args.output_path)
    print(f"Successfully exported {len(notes)} notes to {args.output_path}")


if __name__ == "__main__":
    main()
