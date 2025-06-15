"""
HTML processing utilities for NotebookLM notes.
"""

from typing import Any, Generator, List, Optional

from bs4 import BeautifulSoup
from bs4.element import Comment, Tag


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
