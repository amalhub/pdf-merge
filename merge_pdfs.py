#!/usr/bin/env python3
"""
PDF Merger Tool
Merges two or more PDF files and images (PNG/JPG) into a single PDF file.
Supports page range selection for PDFs.
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


def merge_pdfs(file_items, output_path):
    """
    Merge multiple PDF files and images into one PDF.
    
    Args:
        file_items: List of tuples (file_path, start_page, end_page)
                   start_page and end_page can be None for full document
        output_path: Path where the merged PDF will be saved
    """
    merger = PdfMerger()
    temp_files = []  # Track temporary PDF files created from images
    
    print(f"\nMerging {len(file_items)} files...")
    
    for i, (file_path, start_page, end_page) in enumerate(file_items, 1):
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Check if it's an image file
            if file_ext in ['.png', '.jpg', '.jpeg']:
                print(f"  [{i}/{len(file_items)}] Converting image to PDF: {os.path.basename(file_path)}")
                temp_pdf = image_to_pdf(file_path)
                temp_files.append(temp_pdf)
                merger.append(temp_pdf)
            else:
                # It's a PDF file
                if start_page is not None and end_page is not None:
                    # Convert to 0-indexed for pypdf (it uses 0-based indexing)
                    # But we need to be careful: pages parameter expects (start, end) where end is exclusive
                    print(f"  [{i}/{len(file_items)}] Adding PDF: {os.path.basename(file_path)} (pages {start_page}-{end_page})")
                    merger.append(file_path, pages=(start_page - 1, end_page))
                else:
                    print(f"  [{i}/{len(file_items)}] Adding PDF: {os.path.basename(file_path)} (all pages)")
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
    
    # Ask if user wants to define page ranges
    define_pages = input("\nDo you want to specify page ranges for PDFs? (y/n): ").strip().lower()
    use_page_ranges = define_pages == 'y'
    
    # Supported file extensions
    supported_extensions = ('.pdf', '.png', '.jpg', '.jpeg')
    
    # Collect files one by one
    file_items = []
    file_count = 0
    
    print("\nEnter files one by one (press Enter without input to finish):")
    if use_page_ranges:
        print("For PDFs, you'll be asked for the page range.")
        print("Images will automatically be added as single pages.")
        print("Page range examples: 1, 1-5, 2-10")
    
    while True:
        file_count += 1
        
        # Ask for file path
        file_path = input(f"\nFile {file_count} path (or Enter to finish): ").strip().strip('"').strip("'")
        
        # If empty, user is done
        if not file_path:
            file_count -= 1  # Decrement since we didn't add a file
            break
        
        # Validate file exists
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            print("Please try again.")
            file_count -= 1
            continue
        
        # Validate file type
        if not file_path.lower().endswith(supported_extensions):
            print(f"Error: Unsupported file type: {file_path}")
            print(f"Supported formats: PDF, PNG, JPG, JPEG")
            print("Please try again.")
            file_count -= 1
            continue
        
        file_ext = os.path.splitext(file_path)[1].lower()
        start_page = None
        end_page = None
        
        # Ask for page range if in advanced mode
        if use_page_ranges:
            if file_ext == '.pdf':
                while True:
                    page_input = input(f"  Page range (e.g., 1-5 or 3, or Enter for all pages): ").strip()
                    
                    if not page_input:
                        # User wants all pages
                        break
                    
                    # Parse page range
                    if '-' in page_input:
                        try:
                            parts = page_input.split('-')
                            start_page = int(parts[0].strip())
                            end_page = int(parts[1].strip())
                            
                            if start_page < 1 or end_page < 1:
                                print("  Error: Page numbers must be >= 1")
                                continue
                            if start_page > end_page:
                                print("  Error: Start page must be <= end page")
                                continue
                            
                            break
                        except ValueError:
                            print("  Error: Invalid page range format. Use format like '1-5' or '3'")
                            continue
                    else:
                        # Single page
                        try:
                            page_num = int(page_input.strip())
                            if page_num < 1:
                                print("  Error: Page number must be >= 1")
                                continue
                            start_page = page_num
                            end_page = page_num
                            break
                        except ValueError:
                            print("  Error: Invalid page number")
                            continue
            else:
                # Image file - automatically use page 1 (no input needed)
                print(f"  Image file - automatically using page 1")
                start_page = 1
                end_page = 1
        
        # Add to list
        file_items.append((file_path, start_page, end_page))
        print(f"✓ Added: {os.path.basename(file_path)}" + 
              (f" (pages {start_page}-{end_page})" if start_page is not None else " (all pages)"))
    
    if len(file_items) < 1:
        print("\nError: No files were added. Exiting.")
        sys.exit(1)
    
    print(f"\n{len(file_items)} file(s) ready to merge.")
    
    # Get the directory of the first file
    first_file_path = file_items[0][0]
    first_file_dir = os.path.dirname(os.path.abspath(first_file_path))
    output_path = os.path.join(first_file_dir, "merged.pdf")
    
    # Check if output file already exists
    if os.path.exists(output_path):
        overwrite = input(f"\nWarning: '{output_path}' already exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Operation cancelled.")
            sys.exit(0)
    
    # Merge the PDFs
    merge_pdfs(file_items, output_path)
    print(f"\nOutput file: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
