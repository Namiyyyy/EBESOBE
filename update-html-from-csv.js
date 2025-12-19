#!/usr/bin/env node

/**
 * Script to update index.html with data from act-list-template.csv
 * Run this script after editing the CSV file to update the HTML
 * Usage: node update-html-from-csv.js
 */

const fs = require('fs');
const path = require('path');

// Read CSV file
const csvPath = path.join(__dirname, 'act-list-template.csv');
const htmlPath = path.join(__dirname, 'index.html');

try {
    const csvContent = fs.readFileSync(csvPath, 'utf8');
    const lines = csvContent.split('\n').filter(line => line.trim());
    
    if (lines.length < 2) {
        console.log('CSV file is empty or has no data rows');
        process.exit(1);
    }
    
    // Detect delimiter
    const delimiter = lines[0].includes(';') ? ';' : ',';
    
    // Parse headers
    const headers = parseCSVLine(lines[0], delimiter).map(h => h.replace(/"/g, '').trim());
    
    // Parse data rows
    const data = [];
    for (let i = 1; i < lines.length; i++) {
        const values = parseCSVLine(lines[i], delimiter);
        if (values.length >= 5) {
            const item = {};
            headers.forEach((header, index) => {
                if (index < values.length) {
                    item[header] = values[index].replace(/^"|"$/g, '').trim();
                }
            });
            data.push(item);
        }
    }
    
    // Generate JavaScript data array
    const jsDataArray = data.map(item => {
        return `            { "Date": ${JSON.stringify(item['Date'] || '')}, "Location": ${JSON.stringify(item['Location'] || '')}, "Project Name Line 1": ${JSON.stringify(item['Project Name Line 1'] || '')}, "Project Name Line 2": ${JSON.stringify(item['Project Name Line 2'] || '')}, "Status": ${JSON.stringify(item['Status'] || '')}, "Clickable": ${JSON.stringify(item['Clickable'] || 'No')} }`;
    }).join(',\n');
    
    // Read HTML file
    let htmlContent = fs.readFileSync(htmlPath, 'utf8');
    
    // Find and replace the actListData array
    const dataPattern = /const actListData = \[[\s\S]*?\];/;
    const newData = `const actListData = [\n${jsDataArray}\n        ];`;
    
    if (dataPattern.test(htmlContent)) {
        htmlContent = htmlContent.replace(dataPattern, newData);
        fs.writeFileSync(htmlPath, htmlContent, 'utf8');
        console.log(`✅ Successfully updated HTML with ${data.length} act items from CSV`);
    } else {
        console.log('❌ Could not find actListData in HTML file');
        process.exit(1);
    }
    
} catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
}

// CSV line parser
function parseCSVLine(line, delimiter = ',') {
    const result = [];
    let current = '';
    let inQuotes = false;
    
    for (let i = 0; i < line.length; i++) {
        const char = line[i];
        if (char === '"') {
            inQuotes = !inQuotes;
        } else if (char === delimiter && !inQuotes) {
            result.push(current);
            current = '';
        } else {
            current += char;
        }
    }
    result.push(current);
    return result;
}

