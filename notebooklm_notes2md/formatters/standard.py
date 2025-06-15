"""
Standard Markdown formatter for NotebookLM notes.
"""

from typing import Any, Dict, List, Optional

from notebooklm_notes2md.utils.text_processing import clean_text


def format_standard_markdown(
    notes: List[Dict[str, str]],
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Format notes as standard Markdown.

    Args:
        notes: List of note dictionaries
        metadata: Optional dictionary of metadata extracted from the document

    Returns:
        Standard markdown as a string
    """
    result = ""

    # Add document title as main heading if metadata is available
    if metadata and "title" in metadata:
        result += f"# {metadata['title']}\n\n"

    # Add all notes
    for note in notes:
        clean_content = clean_text(note["note"])
        result += clean_content + "\n\n"

    return result
