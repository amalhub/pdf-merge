# PDF Merger Tool

A simple Python script to merge two or more PDF files into a single PDF file.

## Installation

1. Install Python 3.6 or higher (if not already installed)
2. Install the required library:
   ```bash
   pip install -r requirements.txt
   ```
   or
   ```bash
   pip install pypdf
   ```

## Usage

Run the script:

```bash
python merge_pdfs.py
```

When prompted, enter the PDF file paths separated by commas:

```
Enter PDF file paths (comma-separated): file1.pdf, file2.pdf, file3.pdf
```

You can use:

- Relative paths: `document1.pdf, document2.pdf`
- Absolute paths: `C:\Files\doc1.pdf, C:\Files\doc2.pdf`
- Mixed paths with quotes: `"C:\My Files\doc1.pdf", document2.pdf`

## Output

The merged PDF will be saved as `merged.pdf` in the same directory as the first input file.

## Features

- Merges 2 or more PDF files
- Validates all input files before merging
- Warns if output file already exists
- Shows progress during merging
- Clear error messages

## Example

```
==============================================================
PDF Merger Tool
==============================================================

Enter PDF file paths (comma-separated): doc1.pdf, doc2.pdf

Merging 2 PDF files...
  [1/2] Adding: doc1.pdf
  [2/2] Adding: doc2.pdf

Saving merged PDF to: C:\Files\merged.pdf
✓ Successfully merged PDFs!

Output file: C:\Files\merged.pdf
==============================================================
```
