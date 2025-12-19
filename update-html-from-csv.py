#!/usr/bin/env python3
"""
Script to update index.html with data from act-list-template.csv
Run this script after editing the CSV file to update the HTML
Usage: python3 update-html-from-csv.py
"""

import csv
import re
import json
import os

# File paths
csv_path = 'act-list-template.csv'
html_path = 'index.html'

try:
    # Read CSV file
    with open(csv_path, 'r', encoding='utf-8') as f:
        # Detect delimiter
        first_line = f.readline()
        delimiter = ';' if ';' in first_line else ','
        f.seek(0)
        
        # Read CSV
        reader = csv.DictReader(f, delimiter=delimiter)
        data = list(reader)
    
    if not data:
        print('CSV file is empty or has no data rows')
        exit(1)
    
    # Generate JavaScript data array
    js_items = []
    for item in data:
        js_item = (
            f'            {{ "Date": {json.dumps(item.get("Date", ""))}, '
            f'"Code/ID": {json.dumps(item.get("Code/ID", ""))}, '
            f'"Description Line 1": {json.dumps(item.get("Description Line 1", ""))}, '
            f'"Description Line 2": {json.dumps(item.get("Description Line 2", ""))}, '
            f'"Status": {json.dumps(item.get("Status", ""))}, '
            f'"Clickable": {json.dumps(item.get("Clickable", "No"))} }}'
        )
        js_items.append(js_item)
    
    js_data_array = ',\n'.join(js_items)
    
    # Read HTML file
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find and replace the actListData array
    pattern = r'const actListData = \[[\s\S]*?\];'
    new_data = f'const actListData = [\n{js_data_array}\n        ];'
    
    if re.search(pattern, html_content):
        html_content = re.sub(pattern, new_data, html_content)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f'✅ Successfully updated HTML with {len(data)} act items from CSV')
    else:
        print('❌ Could not find actListData in HTML file')
        exit(1)
        
except FileNotFoundError as e:
    print(f'❌ File not found: {e.filename}')
    exit(1)
except Exception as e:
    print(f'❌ Error: {e}')
    exit(1)

