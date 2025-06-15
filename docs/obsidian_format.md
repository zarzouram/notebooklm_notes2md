# Obsidian Export Format

This document explains the Obsidian export format available in the `notebooklm_notes2md` tool.

## Overview

[Obsidian](https://obsidian.md/) is a powerful knowledge base that works on top of a local folder of Markdown files. The Obsidian export format generates Markdown files that are specially formatted to work well with Obsidian's features, including YAML frontmatter, callouts, and more.

## Features

When you export to Obsidian format, the following elements are included:

### 1. YAML Frontmatter

The YAML frontmatter contains metadata extracted from the NotebookLM notes:

```yaml
---
title: "Document Title"
tags:
  - "Tag 1"
  - "Tag 2"
date: 2025-06-15
citekey: {{citekey}}
status: unread
---
```

- **title**: Extracted from the NotebookLM document title
- **tags**: Extracted from the key topics in NotebookLM
- **date**: The date when the export was created
- **citekey**: A placeholder for academic citation (to be filled manually)
- **status**: Reading status (unread/read/edited)

### 2. Summary Callout

The summary is formatted as an Obsidian callout block:

```markdown
> [!summary]
> This is the summary text extracted from NotebookLM. It preserves **formatting** and structure.
```

### 3. Document Content

The content of the notes is formatted as standard Markdown with proper headings and structure.

## Usage

To export in Obsidian format, use the `--format obsidian` flag:

```bash
notebooklm-export input.html output.md --format obsidian
```

## Citation Management

The Obsidian format includes fields for citation management that can be manually edited:

- **citekey**: Replace `{{citekey}}` with your citation key (e.g., `smith2023market`)
- **status**: Update the reading status as you progress (unread/read/edited)

These fields can be used with Obsidian plugins like [Citations](https://github.com/hans/obsidian-citation-plugin) to integrate with reference management tools like Zotero.

## Example

See the [example file](examples/obsidian_format_example.md) for a complete demonstration of the Obsidian export format.
