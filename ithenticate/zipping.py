import os
import glob
import zipfile

# Configuration
INPUT_DIR = "compressed"
OUTPUT_DIR = "zipped"
MAX_ZIP_SIZE = 190 * 1024 * 1024  # 190MB in bytes

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get all PDF files with their file sizes
pdf_files = [(f, os.path.getsize(f)) for f in glob.glob(os.path.join(INPUT_DIR, "*.pdf"))]
pdf_files = sorted(pdf_files, key=lambda x: x[0], reverse=True)

# Group files by size
groups = []
current_group = []
current_size = 0

for filepath, size in pdf_files:
    if current_size + size > MAX_ZIP_SIZE and current_group:
        groups.append(current_group)
        current_group = []
        current_size = 0
    current_group.append(filepath)
    current_size += size

if current_group:
    groups.append(current_group)

# Write each group to a ZIP file
for i, group in enumerate(groups, start=1):
    zip_filename = os.path.join(OUTPUT_DIR, f"submissions_{i}.zip")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filepath in group:
            arcname = os.path.basename(filepath)
            zipf.write(filepath, arcname)
    print(f"Created {zip_filename} with {len(group)} files.")

print("Done.")
