import os
import argparse
from pathlib import Path
from pypdf import PdfReader
import docx
import shutil

from src.parser import parse_file

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
        try:
            print(f"Processing: {filename}")
            cleaned_content = parse_file(file_path)
            # Use original stem and append .txt
            output_filename = file_path.stem + ".txt"
            with open(output_dir / output_filename, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f"Saved to {output_dir}/{output_filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main()
