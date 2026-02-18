#!/usr/bin/env python3
"""
Image Optimization Script
Converts and resizes background images for web use.

Requirements: pip install Pillow
Usage:
  python3 optimize-images.py           - Process PNGs from background-images -> optimized
  python3 optimize-images.py --optimize-existing  - Re-optimize images in optimized folder (reduces large files)
"""

import os
import tempfile
from PIL import Image
import sys

# Configuration
INPUT_FOLDER = "background-images"
OUTPUT_FOLDER = "background-images/optimized"
MAX_WIDTH = 1920  # Full HD width (good for most screens)
MAX_HEIGHT = 1080  # Full HD height
QUALITY = 82  # JPG quality (good balance, smaller files)
FORMAT = "JPEG"  # Use JPEG for photos (smaller than PNG)

def optimize_image(input_path, output_path):
    """Optimize a single image"""
    try:
        # Open image
        img = Image.open(input_path)
        
        # Convert RGBA to RGB if needed (for JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get original size
        orig_width, orig_height = img.size
        print(f"  Original: {orig_width}x{orig_height}")
        
        # Calculate new size maintaining aspect ratio
        ratio = min(MAX_WIDTH / orig_width, MAX_HEIGHT / orig_height)
        if ratio < 1:  # Only resize if image is larger than max
            new_width = int(orig_width * ratio)
            new_height = int(orig_height * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(f"  Resized: {new_width}x{new_height}")
        else:
            print(f"  No resize needed (already smaller)")
        
        # Save optimized image
        img.save(output_path, FORMAT, quality=QUALITY, optimize=True)
        
        # Get file sizes
        orig_size = os.path.getsize(input_path)
        new_size = os.path.getsize(output_path)
        reduction = ((orig_size - new_size) / orig_size) * 100
        
        print(f"  Size: {orig_size / 1024 / 1024:.1f}MB → {new_size / 1024 / 1024:.1f}MB ({reduction:.1f}% reduction)")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def optimize_existing():
    """Re-optimize images already in the optimized folder (reduces large file sizes)"""
    if not os.path.exists(OUTPUT_FOLDER):
        print(f"❌ Error: Folder '{OUTPUT_FOLDER}' not found!")
        sys.exit(1)

    extensions = ('.jpg', '.jpeg', '.png', '.webp')
    files = [f for f in os.listdir(OUTPUT_FOLDER)
             if f.lower().endswith(extensions) and not f.startswith('.')]

    if not files:
        print(f"❌ No image files found in '{OUTPUT_FOLDER}'")
        sys.exit(1)

    print(f"📸 Re-optimizing {len(files)} images in {OUTPUT_FOLDER}\n")

    success_count = 0
    total_orig_size = 0
    total_new_size = 0

    for filename in sorted(files):
        input_path = os.path.join(OUTPUT_FOLDER, filename)
        base, ext = os.path.splitext(filename)
        output_filename = base + '.jpg'
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        orig_size = os.path.getsize(input_path)
        total_orig_size += orig_size

        print(f"Processing: {filename} ({orig_size / 1024 / 1024:.1f}MB)")

        try:
            img = Image.open(input_path)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            orig_w, orig_h = img.size
            ratio = min(MAX_WIDTH / orig_w, MAX_HEIGHT / orig_h)
            if ratio < 1:
                new_w = int(orig_w * ratio)
                new_h = int(orig_h * ratio)
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                print(f"  Resized: {orig_w}x{orig_h} → {new_w}x{new_h}")

            fd, temp_path = tempfile.mkstemp(suffix='.jpg', dir=OUTPUT_FOLDER)
            os.close(fd)
            try:
                img.save(temp_path, FORMAT, quality=QUALITY, optimize=True)
                new_size = os.path.getsize(temp_path)
                os.replace(temp_path, output_path)
                if input_path != output_path and os.path.exists(input_path):
                    os.remove(input_path)
            except Exception:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                raise

            total_new_size += new_size
            reduction = ((orig_size - new_size) / orig_size) * 100
            print(f"  Size: {orig_size / 1024 / 1024:.1f}MB → {new_size / 1024 / 1024:.1f}MB ({reduction:.1f}% reduction)")
            success_count += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
        print()

    if success_count > 0:
        print("=" * 50)
        print("📊 SUMMARY")
        print("=" * 50)
        print(f"✅ Optimized: {success_count}/{len(files)} images")
        print(f"📦 Total: {total_orig_size / 1024 / 1024:.1f}MB → {total_new_size / 1024 / 1024:.1f}MB")
        print(f"💾 Saved: {(total_orig_size - total_new_size) / 1024 / 1024:.1f}MB")


def main():
    # Check if input folder exists
    if not os.path.exists(INPUT_FOLDER):
        print(f"❌ Error: Folder '{INPUT_FOLDER}' not found!")
        sys.exit(1)
    
    # Create output folder
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"✅ Created output folder: {OUTPUT_FOLDER}")
    
    # Get all PNG files
    png_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith('.png')]
    
    if not png_files:
        print(f"❌ No PNG files found in '{INPUT_FOLDER}'")
        sys.exit(1)
    
    print(f"📸 Found {len(png_files)} images to optimize\n")
    
    success_count = 0
    total_orig_size = 0
    total_new_size = 0
    
    for filename in sorted(png_files):
        input_path = os.path.join(INPUT_FOLDER, filename)
        # Change extension to .jpg
        output_filename = os.path.splitext(filename)[0] + '.jpg'
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        print(f"Processing: {filename}")
        
        orig_size = os.path.getsize(input_path)
        total_orig_size += orig_size
        
        if optimize_image(input_path, output_path):
            success_count += 1
            total_new_size += os.path.getsize(output_path)
        print()
    
    # Summary
    print("=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    print(f"✅ Successfully optimized: {success_count}/{len(png_files)} images")
    print(f"📦 Total size: {total_orig_size / 1024 / 1024:.1f}MB → {total_new_size / 1024 / 1024:.1f}MB")
    print(f"💾 Space saved: {(total_orig_size - total_new_size) / 1024 / 1024:.1f}MB")
    print(f"📉 Reduction: {((total_orig_size - total_new_size) / total_orig_size) * 100:.1f}%")
    print()
    print("Next steps:")
    print(f"1. Review images in '{OUTPUT_FOLDER}' folder")
    print("2. If they look good, replace the original folder")
    print("3. Update HTML to use .jpg instead of .png")

if __name__ == "__main__":
    try:
        if "--optimize-existing" in sys.argv:
            optimize_existing()
        else:
            main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
        sys.exit(1)
    except ImportError:
        print("❌ Error: Pillow library not installed")
        print("Install it with: pip3 install Pillow")
        sys.exit(1)

