# Act Images Folder Structure

## Folder Organization

Images for each act are stored in the `act-images/` folder, with subfolders named by the act's date in a filesystem-friendly format.

## Naming Convention

**Folder names are based on the Date column from your CSV:**
- Format: `YYYY-MM-DD` or `YYYY-MM-XX` for partial dates
- If multiple acts share the same date, add a number: `YYYY-MM-XX-1`, `YYYY-MM-XX-2`, etc.

## Examples

Based on your current CSV:
- `act-images/2025-02-17/` - For "Feb. 17, 2025"
- `act-images/2026-01-XX-1/` - For first "Jan. XX, 2026" act
- `act-images/2026-01-XX-2/` - For second "Jan. XX, 2026" act  
- `act-images/2025-12-14/` - For "Dec. 14, 2025"

## Image Naming

Inside each act folder, name your images:
- `1.jpg`, `2.jpg`, `3.jpg`, etc. (sequential numbering)
- Or use descriptive names: `main.jpg`, `detail-1.jpg`, `detail-2.jpg`, etc.

## How It Works

1. When you click an act in the detail page table, the code automatically:
   - Converts the Date from CSV to folder name format
   - Looks for images in the corresponding folder
   - Displays all images found in that folder

2. To add images for a new act:
   - Add the act to your CSV
   - Create a folder: `act-images/YYYY-MM-DD/`
   - Add images to that folder
   - Run `python3 update-html-from-csv.py` to sync

## Image Recommendations

- **Format**: JPG (smaller file size) or PNG (if you need transparency)
- **Size**: Optimize images to 1920x1080 max (use `optimize-images.py` script)
- **Naming**: Use sequential numbers (1.jpg, 2.jpg, etc.) for automatic ordering

