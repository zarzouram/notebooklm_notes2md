"""
Core functionality for parsing and processing NotebookLM notes.
"""

from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from bs4.element import Tag

# Import original functionality from the script
from notebooklm_notes2md.utils.html_processing import (
    extract_tag_classes,
    format_span_text,
    process_div_prefix,
    drill_into_tag,
    is_comment_separator,
    inner_childs_with_split,
    find_parent_element
)
from notebooklm_notes2md.utils.text_processing import (
    clean_text,
    create_note_from_texts
)


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
