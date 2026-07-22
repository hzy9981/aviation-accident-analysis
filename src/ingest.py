import os
import argparse
from pathlib import Path
from pypdf import PdfReader
import docx
import shutil

def parse_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def parse_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def clean_text(text):
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned_lines)

def main():
    parser = argparse.ArgumentParser(description="Ingest aviation accident reports into GraphRAG input directory.")
    parser.add_argument("--source", type=str, required=True, help="Path to source directory containing PDF/DOCX files.")
    parser.add_argument("--output", type=str, default="input", help="Path to GraphRAG input directory.")
    parser.add_argument("--clear", action="store_true", help="Clear the output directory before ingestion.")
    args = parser.parse_args()

    source_dir = Path(args.source)
    output_dir = Path(args.output)

    if args.clear and output_dir.exists():
        print(f"Clearing output directory: {output_dir}")
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    for file_path in source_dir.iterdir():
        if file_path.is_dir():
            continue
            
        filename = file_path.name
        content = ""
        
        if file_path.suffix.lower() == ".pdf":
            print(f"Parsing PDF: {filename}")
            content = parse_pdf(file_path)
        elif file_path.suffix.lower() == ".docx":
            print(f"Parsing DOCX: {filename}")
            content = parse_docx(file_path)
        elif file_path.suffix.lower() == ".txt":
            print(f"Reading TXT: {filename}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        if content:
            cleaned_content = clean_text(content)
            # Use original stem and append .txt
            output_filename = file_path.stem + ".txt"
            with open(output_dir / output_filename, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f"Saved to {output_dir}/{output_filename}")

if __name__ == "__main__":
    main()
