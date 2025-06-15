"""
Metadata extractors for NotebookLM notes.

This module contains functions for extracting metadata from NotebookLM HTML.
"""

from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag


def extract_document_title(soup: BeautifulSoup) -> str:
    """
    Extract the document title from the NotebookLM HTML.

    Args:
        soup: BeautifulSoup object containing the parsed HTML

    Returns:
        The document title or a default title if not found
    """
    title_element = soup.select_one('.source-title')
    if title_element and title_element.text:
        return title_element.text.strip()
    return "Untitled Document"


def extract_summary(soup: BeautifulSoup) -> Optional[str]:
    """
    Extract the document summary from the NotebookLM HTML.

    Args:
        soup: BeautifulSoup object containing the parsed HTML

    Returns:
        The document summary or None if not found
    """
    summary_element = soup.select_one('.summary .mat-body-medium p')
    if summary_element and summary_element.text:
        return summary_element.text.strip()
    return None


def extract_key_topics(soup: BeautifulSoup) -> List[str]:
    """
    Extract key topics from the NotebookLM HTML.

    Args:
        soup: BeautifulSoup object containing the parsed HTML

    Returns:
        List of key topics or empty list if none found
    """
    topics = []
    topic_elements = soup.select('.key-topics-chip .key-topics-text p')

    for topic in topic_elements:
        if topic.text.strip():
            topics.append(topic.text.strip())

    return topics


def extract_metadata(soup: BeautifulSoup) -> Dict[str, Any]:
    """
    Extract all available metadata from the NotebookLM HTML.

    Args:
        soup: BeautifulSoup object containing the parsed HTML

    Returns:
        Dictionary containing all extracted metadata
    """
    metadata = {
        "title": extract_document_title(soup),
        "tags": extract_key_topics(soup),
        "date": None,  # Will be filled in by the formatter
    }

    summary = extract_summary(soup)
    if summary:
        metadata["summary"] = summary

    return metadata
