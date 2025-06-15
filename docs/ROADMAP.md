# NotebookLM Notes2MD Enhancement Roadmap

*Last updated: June 15, 2025*

This document outlines the planned enhancements to the `notebooklm_notes2md` tool. The features are organized into implementation cycles to ensure manageable, testable updates.

## Current Status

🟢 **Cycle 0: Base Functionality** - COMPLETE

- Basic NotebookLM HTML to Markdown/PDF conversion
- Command line interface
- Single file processing

🟢 **Cycle 1: Metadata Extraction & Basic Obsidian Support** - COMPLETE

- [x] Summary extraction
- [x] Key topics extraction
- [x] Basic Obsidian format with YAML frontmatter

🟡 **Cycle 2: Citation Management & Advanced Metadata** - PLANNED

- [ ] Citation field support
- [ ] Extended metadata
- [ ] Configurable output templates

⚪ **Cycle 3: Integration & Interoperability** - PLANNED

- [ ] Zotero basic integration
- [ ] Multi-format export
- [ ] Batch processing

⚪ **Cycle 4: Advanced Features & UI** - PLANNED

- [ ] Advanced Zotero integration
- [ ] Content transformation
- [ ] Simple GUI interface

## Detailed Roadmap

### Cycle 1: Metadata Extraction & Basic Obsidian Support

**Goal**: Extract key metadata and support basic Obsidian formatting

**Features**:

1. **Summary Extraction**
   - Parse and extract summary content from NotebookLM HTML
   - Preserve formatting (bold, lists, etc.) in the extracted summary

2. **Key Topics Extraction**
   - Identify and extract key topics from the HTML
   - Convert to appropriate tag/topic format in output

3. **Basic Obsidian Format**
   - Add YAML frontmatter with title and tags
   - Format summary as Obsidian callout blocks
   - Add basic command-line flag `--format obsidian`

**Timeline**: 2-3 weeks (Target completion: July 5, 2025)

**Success Criteria**:

- Successfully extracts summary and key topics from test files
- Generates valid Obsidian-compatible Markdown with proper YAML frontmatter
- All existing functionality continues to work without regression

### Cycle 2: Citation Management & Advanced Metadata

**Goal**: Add academic reference capabilities and enhanced metadata

**Features**:

1. **Citation Field Support**
   - Add citekey and status fields in YAML frontmatter
   - Provide placeholder templates for user customization
   - Document citation format conventions

2. **Extended Metadata**
   - Extract document title and source information
   - Add creation date, modified date, and export date fields
   - Support custom user-defined metadata fields

3. **Configurable Output Templates**
   - Create template system for customizable output formats
   - Allow users to define their own templates
   - Include several pre-defined templates (academic, note-taking, etc.)

**Timeline**: 3-4 weeks (Target completion: August 1, 2025)

**Success Criteria**:

- Correctly formats citation fields in YAML frontmatter
- Preserves extended metadata from source documents
- Templates produce consistent and valid Markdown

### Cycle 3: Integration & Interoperability

**Goal**: Connect with external tools and enhance interoperability

**Features**:

1. **Zotero Basic Integration**
   - Parse Zotero citation keys if provided
   - Generate compatible citation formats
   - Document workflow for using with Zotero

2. **Multi-Format Export**
   - Support additional output formats (e.g., Academic Markdown, LaTeX)
   - Implement format conversion utilities
   - Create format validation to ensure output compatibility

3. **Batch Processing**
   - Support processing multiple files in one command
   - Maintain directory structure when batch processing
   - Add progress reporting for batch operations

**Timeline**: 4-5 weeks (Target completion: September 5, 2025)

**Success Criteria**:

- Successfully processes citation keys from Zotero
- Correctly generates multiple output formats from the same input
- Efficiently handles batch processing with proper error handling

### Cycle 4: Advanced Features & UI

**Goal**: Add advanced features and improve user experience

**Features**:

1. **Advanced Zotero Integration**
   - Fetch metadata directly from Zotero API
   - Support bibliography generation
   - Allow bidirectional status updates

2. **Content Transformation**
   - Support note splitting/merging
   - Add content filtering options
   - Implement custom transformations via plugins

3. **Simple GUI Interface**
   - Create basic graphical interface for non-technical users
   - Provide preview functionality
   - Add drag-and-drop support

**Timeline**: 6-8 weeks (Target completion: October 31, 2025)

**Success Criteria**:

- Successfully connects to Zotero API and retrieves metadata
- Correctly processes complex content transformations
- GUI provides intuitive access to core functionality

## Implementation Approach

For each cycle:

1. **Research & Design (Week 1)**
   - Study HTML structure of relevant elements
   - Design data models and interfaces
   - Create mockups of output formats

2. **Core Implementation (Weeks 1-2)**
   - Implement parsing logic
   - Build formatting functions
   - Create command-line interfaces

3. **Testing & Refinement (Week 3)**
   - Develop automated tests
   - Conduct user testing with sample files
   - Refine based on feedback

4. **Documentation & Release (Week 3-4)**
   - Update README and documentation
   - Create examples and tutorials
   - Package and release new version

## Technical Considerations

1. **Backward Compatibility**
   - Maintain existing functionality
   - Make new features opt-in
   - Provide migration guides for breaking changes

2. **Testing Strategy**
   - Expand test suite with each feature
   - Include sample files for each HTML structure variant
   - Add integration tests for external tool compatibility

3. **Code Organization**
   - Refactor to modular architecture
   - Separate concerns: parsing, formatting, export
   - Create plugin system for extensibility
