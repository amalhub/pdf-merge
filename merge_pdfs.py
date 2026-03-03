#!/usr/bin/env python3
"""
PDF Merger Tool
Merges two or more PDF files and images (PNG/JPG) into a single PDF file.
"""

import os
import sys
import tempfile

try:
    from pypdf import PdfMerger
except ImportError:
    print("Error: pypdf library is not installed.")
    print("Please install it using: pip install pypdf")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow library is not installed.")
    print("Please install it using: pip install Pillow")
    sys.exit(1)


def image_to_pdf(image_path):
    """
    Convert an image file to a temporary PDF file.
    
    Args:
        image_path: Path to the image file (PNG/JPG)
        
    Returns:
        Path to the temporary PDF file
    """
    try:
        # Open image and convert to RGB (in case it's RGBA or other mode)
        img = Image.open(image_path)
        
        # Convert to RGB if necessary (PDF doesn't support RGBA)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create a white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Create a temporary PDF file
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_pdf.close()
        
        # Save image as PDF
        img.save(temp_pdf.name, 'PDF', resolution=100.0)
        
        return temp_pdf.name
    except Exception as e:
        raise Exception(f"Failed to convert image to PDF: {e}")


def merge_pdfs(file_paths, output_path):
    """
    Merge multiple PDF files and images into one PDF.
    
    Args:
        file_paths: List of PDF/image file paths to merge
        output_path: Path where the merged PDF will be saved
    """
    merger = PdfMerger()
    temp_files = []  # Track temporary PDF files created from images
    
    print(f"\nMerging {len(file_paths)} files...")
    
    for i, file_path in enumerate(file_paths, 1):
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Check if it's an image file
            if file_ext in ['.png', '.jpg', '.jpeg']:
                print(f"  [{i}/{len(file_paths)}] Converting image to PDF: {os.path.basename(file_path)}")
                temp_pdf = image_to_pdf(file_path)
                temp_files.append(temp_pdf)
                merger.append(temp_pdf)
            else:
                print(f"  [{i}/{len(file_paths)}] Adding PDF: {os.path.basename(file_path)}")
                merger.append(file_path)
                
        except Exception as e:
            print(f"Error adding {file_path}: {e}")
            merger.close()
            # Clean up temporary files
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass
            sys.exit(1)
    
    try:
        print(f"\nSaving merged PDF to: {output_path}")
        merger.write(output_path)
        merger.close()
        print("✓ Successfully merged files into PDF!")
    except Exception as e:
        print(f"Error saving merged PDF: {e}")
        merger.close()
        # Clean up temporary files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        sys.exit(1)
    
    # Clean up temporary files
    for temp_file in temp_files:
        try:
            os.unlink(temp_file)
        except:
            pass


def main():
    print("=" * 60)
    print("PDF Merger Tool")
    print("=" * 60)
    
    # Get comma-separated file paths from user
    user_input = input("\nEnter file paths (PDF/PNG/JPG, comma-separated): ").strip()
    
    if not user_input:
        print("Error: No file paths provided.")
        sys.exit(1)
    
    # Split and clean file paths
    file_paths = [path.strip().strip('"').strip("'") for path in user_input.split(',')]
    
    # Supported file extensions
    supported_extensions = ('.pdf', '.png', '.jpg', '.jpeg')
    
    # Validate file paths
    valid_paths = []
    for path in file_paths:
        if not path:
            continue
        
        if not os.path.exists(path):
            print(f"Error: File not found: {path}")
            sys.exit(1)
        
        if not path.lower().endswith(supported_extensions):
            print(f"Error: Unsupported file type: {path}")
            print(f"Supported formats: PDF, PNG, JPG, JPEG")
            sys.exit(1)
        
        valid_paths.append(path)
    
    if len(valid_paths) < 1:
        print("Error: Please provide at least 1 file to convert/merge.")
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
