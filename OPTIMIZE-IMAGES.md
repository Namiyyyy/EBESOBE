# Image Optimization Guide

## Why Images Are Slow to Load

Your background images are currently:
- **Very large files**: 10-14MB each (total ~50MB+)
- **High resolution**: 4726x2658 pixels (much larger than most screens)
- **PNG format**: Uncompressed, large file size

## Problems This Causes

1. **Slow loading**: 50MB+ takes 10-30+ seconds on average internet
2. **High bandwidth usage**: Users on mobile data pay for large downloads
3. **Browser restrictions**: Some browsers block large local files
4. **Poor user experience**: Black screen while images load

## Solution: Optimize Images

### Option 1: Use the Python Script (Recommended)

1. **Install Pillow** (if not already installed):
   ```bash
   pip3 install Pillow
   ```

2. **Run the optimization script**:
   ```bash
   python3 optimize-images.py
   ```

3. **Review the optimized images** in `background-images-optimized` folder

4. **Replace the original folder**:
   ```bash
   # Backup originals (optional)
   mv background-images background-images-original
   
   # Use optimized versions
   mv background-images-optimized background-images
   ```

5. **Update HTML** to use `.jpg` instead of `.png` (or keep PNG if you prefer)

### Option 2: Manual Optimization

Use online tools or image editors:
- **TinyPNG** (https://tinypng.com) - Compress PNG files
- **Squoosh** (https://squoosh.app) - Resize and compress
- **ImageOptim** (Mac app) - Batch optimize

**Recommended settings:**
- **Max dimensions**: 1920x1080 (Full HD)
- **Format**: JPEG (for photos) or WebP (best compression)
- **Quality**: 80-85% (good balance)

### Option 3: Use WebP Format (Best Compression)

WebP provides 25-35% better compression than JPEG:
- Smaller file sizes
- Better quality
- Supported by all modern browsers

## Expected Results

After optimization:
- **File sizes**: 200KB - 800KB each (instead of 10-14MB)
- **Total size**: ~5-8MB (instead of 50MB+)
- **Load time**: 1-3 seconds (instead of 10-30+ seconds)
- **90%+ size reduction**

## Quick Fix: Update HTML for JPG

If you optimize to JPG format, update the HTML image paths from `.png` to `.jpg`.

