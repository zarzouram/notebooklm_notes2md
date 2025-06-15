"""
Text processing utilities for NotebookLM notes.
"""

import re
from typing import Dict, List


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
