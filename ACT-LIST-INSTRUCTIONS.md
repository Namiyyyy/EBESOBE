# Act List Excel Upload Instructions

## Excel Template Columns

Your Excel file should have the following columns (in this exact order):

1. **Date** - The date displayed on the left side (e.g., "Mar. 15, 2026")
2. **Code/ID** - The code/identifier displayed on the right side (e.g., "Lorem 01")
3. **Description Line 1** - First line of the description (e.g., "Urban Act: Berlin Alexanderplatz")
4. **Description Line 2** - Second line of the description (e.g., "Eiusmod Tempor, 2025")
5. **Status** - Either "Active" or "Canceled" (Canceled items will be struck through)
6. **Clickable** - Either "Yes" or "No" (Yes makes the item clickable to open details page)

## How to Use

1. **Open the template**: Open `act-list-template.csv` in Excel (or create a new Excel file with the column headers above)

2. **Fill in your data**: Add your act list items, one per row

3. **Save as Excel**: Save the file as `.xlsx` format (Excel Workbook)

4. **Upload to website**: 
   - Open `index.html` in your browser
   - Click the "Upload Act List (Excel)" button at the bottom of the yellow card
   - Select your Excel file
   - The act list will update automatically!

## Example Data Format

| Date | Code/ID | Description Line 1 | Description Line 2 | Status | Clickable |
|------|---------|-------------------|-------------------|--------|-----------|
| Mar. 15, 2026 | Lorem 01 | Urban Act: Berlin Alexanderplatz | Eiusmod Tempor, 2025 | Active | Yes |
| Mar. 22, 2026 | Lorem 02 | Nullam Varius Turpis ET | Scelerisque (Canceled) | Canceled | No |
| Mar. 23, 2026 | Lorem 03 | Fusce ID Dui Sit | Tellus, 2025 | Active | Yes |

## Notes

- The first row should contain the column headers
- Empty cells are allowed (will show as blank)
- Status is case-insensitive (Active/active/ACTIVE all work)
- Clickable is case-insensitive (Yes/yes/YES all work)
- You can add as many rows as you need

