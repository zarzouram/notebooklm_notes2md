# notebooklm_notes2md

A Python script to convert HTML-formatted notes (from Google NotebookLM) into Markdown and export them as PDF files. The script parses a `notes.txt` file, extracts note sections, and generates a PDF for each note using Markdown formatting.

---

## Why This Script?

Google’s NotebookLM is a powerful tool for interacting with your documents and taking notes. However, exporting your saved notes is not straightforward:

- There is no export option in the app itself.
- The only official way to get your notes is by downloading them all at once, which dumps everything into a single file, ruining the structure and formatting.

This script solves the problem by:

- Parsing the raw HTML structure from the downloaded notes
- Converting each note into clean, readable Markdown
- Exporting each note as an individual PDF file

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

4. Paste the copied HTML into a file named `notes.txt` in the same directory as `export_note.py`.

   ![NotebookLM elements container highlighted in browser](images/notebooklm_elements_container.png)

> **Tip:** For screenshots and a visual walkthrough, see the original [Medium article](https://vivekhere.medium.com/how-to-export-google-notebooklm-saved-notes-as-pdf-10b5ce6c6c10).

---

## Requirements

- Python 3.12
- [uv](https://github.com/astral-sh/uv) (for fast virtual environment and package management)

## Installation

### Using uv (Recommended)

1. **Create and activate a virtual environment using uv:**

   ```bash
   uv venv nblm_notes_cov --python=3.12
   source nblm_notes_cov/bin/activate
   ```

2. **Install dependencies:**

   ```bash
   uv pip install beautifulsoup4==4.13.4 markdown_pdf==1.7
   ```

### Using pip

1. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your HTML-formatted notes in a file (e.g., `notes.txt`).
2. Run the script:

   ```bash
   python export_note.py input_path output_path
   ```

   For example:
   ```bash
   python export_note.py notes.txt my_notes.pdf  # Export to PDF
   # OR
   python export_note.py notes.txt my_notes.md   # Export to Markdown
   ```

3. The script will generate a single PDF or Markdown file with all your notes.

---

## Output Example

- Each PDF preserves Markdown formatting, including headings, bullet lists, and code blocks.
- The output is clean and ready for archiving, searching, or sharing.

---

## Notes

- The script expects the notes to be wrapped in a `<labs-tailwind-doc-viewer>` or similar tag in the HTML. Adjust the script if your HTML structure differs.
- For more details, troubleshooting, and screenshots, refer to the [original Medium article](https://vivekhere.medium.com/how-to-export-google-notebooklm-saved-notes-as-pdf-10b5ce6c6c10).

---

## License
MIT License
