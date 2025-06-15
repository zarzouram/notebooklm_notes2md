# notebooklm_notes2md

A Python script to convert HTML-formatted notes (from Google NotebookLM) into Markdown and export them as a single PDF or Markdown file. The script parses the HTML input, extracts note sections, and generates a formatted output file.

---

## Why This Script?

Google’s NotebookLM is a powerful tool for interacting with your documents and taking notes. However, exporting your saved notes is not straightforward:

- There is no export option in the app itself.
- The only official way to get your notes is by downloading them all at once, which dumps everything into a single file, ruining the structure and formatting.

This script solves the problem by:

- Parsing the raw HTML structure from the downloaded notes
- Converting each note into clean, readable Markdown
- Exporting the notes to either a single PDF or Markdown file

---

## How to Export Your Notes from NotebookLM

1. **Open your NotebookLM notebook.**
2. In the Studio section, find the option to **Convert all notes to source**.
3. This creates a new file in your sources section. You need to get the HTML source of this file:
   - Press `F12` or right-click and select **Inspect** to open your browser’s DevTools.
   - Use the **Select Element** tool (top-left in DevTools) and hover over the notes section.
   - Find the `<div>` with class `elements-container` (or similar) that contains your notes.
   - Right-click this element and choose **Copy > Copy element**.

   ![Selecting and copying the elements container in DevTools](images/devtools_copy_element.png)

4. Paste the copied HTML into a text file (you can name it anything, e.g., `notes.txt`).

   ![NotebookLM elements container highlighted in browser](images/notebooklm_elements_container.png)

> **Tip:** For screenshots and a visual walkthrough, see the original [Medium article](https://vivekhere.medium.com/how-to-export-google-notebooklm-saved-notes-as-pdf-10b5ce6c6c10).

---

## Requirements

- Python 3.12
- [uv](https://github.com/astral-sh/uv) (for fast virtual environment and package management)

## Installation

### Using pip (from PyPI)

```bash
# Coming soon!
pip install notebooklm-notes2md
```

### Using pip (from GitHub)

```bash
pip install git+https://github.com/zarzouram/notebooklm_notes2md.git
```

### Manual Installation

#### Using uv (Recommended)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/zarzouram/notebooklm_notes2md.git
   cd notebooklm_notes2md
   ```

2. **Create and activate a virtual environment using uv:**

   ```bash
   uv venv nblm_notes_cov --python=3.12
   source nblm_notes_cov/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   uv pip install beautifulsoup4==4.13.4 markdown_pdf==1.7
   ```

#### Using pip

1. **Clone the repository:**

   ```bash
   git clone https://github.com/zarzouram/notebooklm_notes2md.git
   cd notebooklm_notes2md
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Development Installation

For development, install the package in editable mode:

```bash
pip install -e .
```

## Usage

1. Place your HTML-formatted notes in a text file (with any file name).
2. Run the script with input and output file paths:

   ```bash
   # If installed via pip
   notebooklm-export <input_path> <output_path>
   
   # OR directly using the script
   python export_note.py <input_path> <output_path>
   ```

   For example:

   ```bash
   notebooklm-export my_notes_html.txt my_notes.pdf  # Export to PDF
   # OR
   notebooklm-export my_notes_html.txt my_notes.md   # Export to Markdown
   ```

3. The script will generate a single PDF or Markdown file containing all your notes.

---

## Output Example

- The output preserves Markdown formatting, including headings, bullet lists, and code blocks.
- PDF output includes proper formatting and is easy to read.
- Markdown output maintains the original structure for further editing.
- The output is clean and ready for archiving, searching, or sharing.

---

## Notes

- The script expects the notes to be wrapped in a `<labs-tailwind-doc-viewer>` or similar tag in the HTML. Adjust the script if your HTML structure differs.
- All notes are combined into a single output file (PDF or Markdown).
- The script preserves formatting including headings, bullet lists, and code blocks.
- For more details, troubleshooting, and screenshots, refer to the [original Medium article](https://vivekhere.medium.com/how-to-export-google-notebooklm-saved-notes-as-pdf-10b5ce6c6c10).

---

## License
MIT License

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For major changes, please open an issue first to discuss what you would like to change.

## Development

### Running Tests

Run the test suite using pytest:

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest
```

### Code Quality

Ensure code quality with:

```bash
# Install linting tools
pip install flake8 mypy

# Run linters
flake8 export_note.py
mypy export_note.py
```
