"""
Obsidian-compatible Markdown formatter for NotebookLM notes.
"""

import datetime
import re
from typing import Any, Dict, List, Optional

from notebooklm_notes2md.utils.text_processing import clean_text


def format_yaml_frontmatter(metadata: Dict[str, Any]) -> str:
    """
    Create YAML frontmatter for Obsidian markdown from metadata.

    Args:
        metadata: Dictionary of metadata extracted from the document

    Returns:
        YAML frontmatter as a string
    """
    frontmatter = ["---"]

    # Add title
    if "title" in metadata and metadata["title"]:
        frontmatter.append(f'title: "{metadata["title"]}"')

    # Add tags if available
    if "tags" in metadata and metadata["tags"]:
        frontmatter.append("tags:")
        for tag in metadata["tags"]:
            # Convert spaces to hyphens (kebab-case) for Obsidian compatibility
            # Also remove special characters that may cause issues in Obsidian tags
            import re

            # Replace spaces with hyphens and remove special characters except for alphanumeric, hyphen, and underscore
            obsidian_tag = re.sub(r'[^\w\-]', '', tag.replace(" ", "-"))
            # Ensure tag doesn't start with a number (Obsidian requirement)
            if obsidian_tag and obsidian_tag[0].isdigit():
                obsidian_tag = f"t{obsidian_tag}"
            # Skip empty tags
            if obsidian_tag:
                frontmatter.append(f'  - "{obsidian_tag}"')

    # Add date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    frontmatter.append(f"date: {current_date}")

    # Add citation placeholder
    frontmatter.append("citekey: {{citekey}}")
    frontmatter.append("status: unread")

    # Add closing delimiter with a newline after
    frontmatter.append("---")
    
    # Join everything with newlines and add an extra newline after the frontmatter
    return "\n".join(frontmatter) + "\n\n"


def format_summary_as_callout(summary: str) -> str:
    """
    Format the summary as an Obsidian callout block.

    Args:
        summary: The text of the summary

    Returns:
        Formatted callout block
    """
    if not summary:
        return ""

    clean_summary = clean_text(summary)
    callout = "> [!summary]\n"

    # Add each line of the summary with a ">" prefix
    # Make sure there is proper spacing around bold markers
    clean_summary = re.sub(r'(\*\*)([^\s])', r'\1 \2', clean_summary)
    clean_summary = re.sub(r'([^\s])(\*\*)', r'\1 \2', clean_summary)
    
    # Process each line
    for line in clean_summary.split("\n"):
        callout += f"> {line}\n"

    return callout + "\n"


def format_obsidian_markdown(
    notes: List[Dict[str, str]],
    metadata: Dict[str, Any]
) -> str:
    """
    Format notes as Obsidian-compatible Markdown.

    Args:
        notes: List of note dictionaries
        metadata: Dictionary of metadata extracted from the document

    Returns:
        Obsidian-formatted markdown as a string
    """
    # Start with YAML frontmatter
    result = format_yaml_frontmatter(metadata)

    # Add summary if available
    if "summary" in metadata and metadata["summary"]:
        result += format_summary_as_callout(metadata["summary"])

    # Add document title as main heading
    result += f"# {metadata['title']}\n\n"

    # Add all notes
    for note in notes:
        clean_content = clean_text(note["note"])
        result += clean_content + "\n\n"

    return result
