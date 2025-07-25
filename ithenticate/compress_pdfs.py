import os
import subprocess
from glob import glob

INPUT_DIR = "submissions"
OUTPUT_DIR = "compressed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def compress_pdf_ghostscript(input_path, output_path, quality="screen"):
    # quality: 'screen' (highest compression) | 'ebook' | 'printer' | 'prepress'
    gs_command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]
    subprocess.run(gs_command, check=True)

pdf_files = glob(os.path.join(INPUT_DIR, "*.pdf"))
print(f"📄 Compressing {len(pdf_files)} PDFs with Ghostscript...")

for i, input_pdf in enumerate(pdf_files, 1):
    filename = os.path.basename(input_pdf)
    output_pdf = os.path.join(OUTPUT_DIR, filename)
    print(f"🔧 [{i}/{len(pdf_files)}] Compressing: {filename}")
    compress_pdf_ghostscript(input_pdf, output_pdf, quality="screen")

print("✅ All PDF compression completed!")
