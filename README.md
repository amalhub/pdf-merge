# PDF Merger Tool

A simple Python script to merge PDF files and images (PNG/JPG) into a single PDF file with support for page range selection.

## Installation

1. Install Python 3.6 or higher (if not already installed)
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
   or
   ```bash
   pip install pypdf Pillow
   ```

## Usage

Run the script:

```bash
python merge_pdfs.py
```

The tool will guide you through an interactive process:

### Option 1: Simple Mode (Without Page Ranges)

If you answer `n` to page ranges, the tool will ask for each file one by one:

1. Enter the first file path
2. Enter the second file path
3. Continue entering file paths
4. Press Enter without typing anything to finish

You can use:

- Relative paths: `document1.pdf`
- Absolute paths: `C:\Files\doc1.pdf`
- Paths with spaces (quotes optional): `"C:\My Files\doc1.pdf"` or `C:\My Files\doc1.pdf`

### Option 2: Advanced Mode (With Page Ranges)

If you answer `y` to page ranges, for each file the tool will:

1. Ask for the file path
2. **For PDFs only**: Ask for the page range
   - Single page: `1`, `5`, `10`
   - Page range: `1-5`, `2-10`, `3-7`
   - Press Enter for all pages
3. **For images** (PNG/JPG): Automatically uses page 1 (no prompt)
4. Press Enter without a file path to finish

## Output

The merged PDF will be saved as `merged.pdf` in the same directory as the first input file.

## Features

- **Interactive one-by-one file input** - Easier to add files one at a time
- Merges PDF files and images (PNG/JPG/JPEG) into a single PDF
- **Page range selection** - Extract specific pages from PDFs (e.g., pages 2-4)
- Automatically converts images to PDF pages
- Handles transparent images (converts to white background)
- Validates all input files before merging
- Warns if output file already exists
- Shows progress during merging
- Clear error messages

## Examples

### Example 1: Simple Mode (No Page Ranges)

```
==============================================================
PDF Merger Tool
==============================================================

Do you want to specify page ranges for PDFs? (y/n): n

Enter files one by one (press Enter without input to finish):

File 1 path (or Enter to finish): doc1.pdf
✓ Added: doc1.pdf (all pages)

File 2 path (or Enter to finish): image.png
✓ Added: image.png (all pages)

File 3 path (or Enter to finish): photo.jpg
✓ Added: photo.jpg (all pages)

File 4 path (or Enter to finish):

3 file(s) ready to merge.

Merging 3 files...
  [1/3] Adding PDF: doc1.pdf (all pages)
  [2/3] Converting image to PDF: image.png
  [3/3] Converting image to PDF: photo.jpg

Saving merged PDF to: C:\Files\merged.pdf
✓ Successfully merged files into PDF!

Output file: C:\Files\merged.pdf
==============================================================
```

### Example 2: Advanced Mode (With Page Ranges)

```
==============================================================
PDF Merger Tool
==============================================================

Do you want to specify page ranges for PDFs? (y/n): y

Enter files one by one (press Enter without input to finish):
For PDFs, you'll be asked for the page range.
Images will automatically be added as single pages.
Page range examples: 1, 1-5, 2-10

File 1 path (or Enter to finish): document.pdf
  Page range (e.g., 1-5 or 3, or Enter for all pages): 2-4
✓ Added: document.pdf (pages 2-4)

File 2 path (or Enter to finish): image.png
  Image file - automatically using page 1
✓ Added: image.png (pages 1-1)

File 3 path (or Enter to finish): report.pdf
  Page range (e.g., 1-5 or 3, or Enter for all pages): 10
✓ Added: report.pdf (pages 10-10)

File 4 path (or Enter to finish):

3 file(s) ready to merge.

Merging 3 files...
  [1/3] Adding PDF: document.pdf (pages 2-4)
  [2/3] Converting image to PDF: image.png
  [3/3] Adding PDF: report.pdf (pages 10-10)

Saving merged PDF to: C:\Files\merged.pdf
✓ Successfully merged files into PDF!

Output file: C:\Files\merged.pdf
==============================================================
```
