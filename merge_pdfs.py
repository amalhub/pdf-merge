#!/usr/bin/env python3
"""
PDF Merger Tool
Merges two or more PDF files into a single PDF file.
"""

import os
import sys

try:
    from pypdf import PdfMerger
except ImportError:
    print("Error: pypdf library is not installed.")
    print("Please install it using: pip install pypdf")
    sys.exit(1)


def merge_pdfs(file_paths, output_path):
    """
    Merge multiple PDF files into one.
    
    Args:
        file_paths: List of PDF file paths to merge
        output_path: Path where the merged PDF will be saved
    """
    merger = PdfMerger()
    
    print(f"\nMerging {len(file_paths)} PDF files...")
    
    for i, pdf_path in enumerate(file_paths, 1):
        try:
            print(f"  [{i}/{len(file_paths)}] Adding: {os.path.basename(pdf_path)}")
            merger.append(pdf_path)
        except Exception as e:
            print(f"Error adding {pdf_path}: {e}")
            merger.close()
            sys.exit(1)
    
    try:
        print(f"\nSaving merged PDF to: {output_path}")
        merger.write(output_path)
        merger.close()
        print("✓ Successfully merged PDFs!")
    except Exception as e:
        print(f"Error saving merged PDF: {e}")
        merger.close()
        sys.exit(1)


def main():
    print("=" * 60)
    print("PDF Merger Tool")
    print("=" * 60)
    
    # Get comma-separated file paths from user
    user_input = input("\nEnter PDF file paths (comma-separated): ").strip()
    
    if not user_input:
        print("Error: No file paths provided.")
        sys.exit(1)
    
    # Split and clean file paths
    file_paths = [path.strip().strip('"').strip("'") for path in user_input.split(',')]
    
    # Validate file paths
    valid_paths = []
    for path in file_paths:
        if not path:
            continue
        
        if not os.path.exists(path):
            print(f"Error: File not found: {path}")
            sys.exit(1)
        
        if not path.lower().endswith('.pdf'):
            print(f"Error: Not a PDF file: {path}")
            sys.exit(1)
        
        valid_paths.append(path)
    
    if len(valid_paths) < 2:
        print("Error: Please provide at least 2 PDF files to merge.")
        sys.exit(1)
    
    # Get the directory of the first file
    first_file_dir = os.path.dirname(os.path.abspath(valid_paths[0]))
    output_path = os.path.join(first_file_dir, "merged.pdf")
    
    # Check if output file already exists
    if os.path.exists(output_path):
        overwrite = input(f"\nWarning: '{output_path}' already exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Operation cancelled.")
            sys.exit(0)
    
    # Merge the PDFs
    merge_pdfs(valid_paths, output_path)
    print(f"\nOutput file: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
