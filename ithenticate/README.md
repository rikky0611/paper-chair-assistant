# iThenticate PDF Processing

A set of Python scripts to prepare PDF submissions for iThenticate plagiarism checking by compressing and packaging them into appropriately sized ZIP files.

## Overview

This workflow helps prepare large batches of PDF submissions for iThenticate by:
1. **Compressing PDFs** to reduce file sizes using Ghostscript
2. **Packaging into ZIP files** that stay under iThenticate's size limits
3. **Manual upload** to iThenticate platform
4. **Automated download** of results using external scripts

## Workflow

### Step 1: Compress PDFs
```bash
python compress_pdfs.py
```

- **Input**: PDF files in `submissions/` directory
- **Output**: Compressed PDFs in `compressed/` directory
- **Tool**: Ghostscript with "screen" quality setting (highest compression)
- **Purpose**: Reduce file sizes for faster upload and processing

### Step 2: Create ZIP Packages
```bash
python zipping.py
```

- **Input**: Compressed PDFs from `compressed/` directory
- **Output**: ZIP files in `zipped/` directory (each ≤190MB)
- **Purpose**: Package files into manageable chunks for iThenticate upload

### Step 3: Manual Upload to iThenticate
1. Log into your iThenticate account
2. Upload the ZIP files from `zipped/` directory
3. Wait for plagiarism checking to complete
4. Download results when ready

### Step 4: Download Results (Optional)
Use the automated download script from:
[PC_A-Scripts/Plagiarism_Delivery](https://github.com/JakeC007/PC_A-Scripts/tree/main/Plagerism_Delivery)

## Requirements

### System Dependencies
- **Ghostscript**: Required for PDF compression
  - macOS: `brew install ghostscript`
  - Ubuntu/Debian: `sudo apt-get install ghostscript`
  - Windows: Download from [Ghostscript website](https://www.ghostscript.com/download/gsdnld.html)

### Python Dependencies
- Python 3.7+
- Standard library modules only (no additional pip packages required)

## Directory Structure

```
ithenticate/
├── compress_pdfs.py      # PDF compression script
├── zipping.py           # ZIP packaging script
├── submissions/         # Input directory for original PDFs
├── compressed/          # Output directory for compressed PDFs
└── zipped/             # Output directory for ZIP packages
```


## Tips

- **Test with small batches** first to verify compression settings
- **Monitor output sizes** to ensure ZIP files meet upload requirements
- **Keep original files** as backup until plagiarism checking is complete