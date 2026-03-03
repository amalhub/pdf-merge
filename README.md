# PDF Merger Tool

A simple Python script to merge PDF files and images (PNG/JPG) into a single PDF file.

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

When prompted, enter the file paths (PDF, PNG, or JPG) separated by commas:

```
Enter file paths (PDF/PNG/JPG, comma-separated): file1.pdf, image1.png, photo.jpg
```

You can use:

- Relative paths: `document1.pdf, image.png`
- Absolute paths: `C:\Files\doc1.pdf, C:\Images\photo.jpg`
- Mixed formats: `document.pdf, image1.png, image2.jpg`
- Paths with quotes: `"C:\My Files\doc1.pdf", photo.png`

## Output

The merged PDF will be saved as `merged.pdf` in the same directory as the first input file.

## Features

- Merges PDF files and images (PNG/JPG/JPEG) into a single PDF
- Automatically converts images to PDF pages
- Handles transparent images (converts to white background)
- Validates all input files before merging
- Warns if output file already exists
- Shows progress during merging
- Clear error messages

## Example

```
==============================================================
PDF Merger Tool
==============================================================

Enter file paths (PDF/PNG/JPG, comma-separated): doc1.pdf, image.png, photo.jpg

Merging 3 files...
  [1/3] Adding PDF: doc1.pdf
  [2/3] Converting image to PDF: image.png
  [3/3] Converting image to PDF: photo.jpg

Saving merged PDF to: C:\Files\merged.pdf
✓ Successfully merged files into PDF!

Output file: C:\Files\merged.pdf
==============================================================
```
