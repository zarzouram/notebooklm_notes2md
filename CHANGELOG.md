# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-06-15

### Added

- Metadata extraction from NotebookLM HTML
  - Document title extraction
  - Summary extraction
  - Key topics/tags extraction
- Obsidian-compatible Markdown format
  - YAML frontmatter with title, tags, and date
  - Citation fields (citekey and status)
  - Summary formatted as callout block
  - Improved tag formatting for Obsidian compatibility:
    - Converting spaces to hyphens
    - Removing special characters
    - Handling numeric tag prefixes
- New command-line option: `--format` to select output format
- Modular project structure for better maintainability
- Additional tests for new functionality
- Documentation for Obsidian format
- Example files showing new features

### Changed

- Refactored code to use a modular package structure
- Fixed bullet point formatting in text processing
- Improved test reliability and coverage

### Removed

- Legacy `export_note.py` script (replaced by the modular package)
- Redundant configuration files
- Tests for deprecated functionality

## [0.1.0] - 2025-06-14

### Added

- Initial release
- Convert HTML-formatted notes from Google NotebookLM to Markdown or PDF
- Command-line interface
- Support for exporting to PDF or Markdown format
- Clean formatting of notes
- Support for installing as a Python package
- Basic test suite

### Fixed

- Type error in the `find_parent_element` function
- Code formatting issues by breaking long lines and removing trailing whitespace
