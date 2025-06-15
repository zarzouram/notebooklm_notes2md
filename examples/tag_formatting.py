"""
Example script demonstrating the tag formatting for Obsidian compatibility.

This script shows how the Obsidian formatter handles different types of tags,
converting them to be compatible with Obsidian's requirements.
"""

import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from notebooklm_notes2md.formatters.obsidian import format_yaml_frontmatter

# Example metadata with various tag formats
metadata = {
    "title": "Tag Formatting Example",
    "tags": [
        "Simple Tag",                     # Will become "Simple-Tag"
        "Tag with #special! chars&",      # Will become "Tag-with-special-chars"
        "123-numeric-start",              # Will become "t123-numeric-start"
        "Valid_under_score",              # Will remain "Valid_under_score"
        "Mixed-Case-Tag",                 # Will remain "Mixed-Case-Tag"
        "Very long tag with many words"   # Will become "Very-long-tag-with-many-words"
    ]
}

# Generate the YAML frontmatter
frontmatter = format_yaml_frontmatter(metadata)

# Display the result
print("Original tags:")
for tag in metadata["tags"]:
    print(f"  - {tag}")

print("\nObsidian-compatible tags (in YAML frontmatter):")
print(frontmatter)

print("\nThis formatting ensures that all tags work correctly in Obsidian's tag system.")
