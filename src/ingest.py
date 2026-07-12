import os
import argparse
from pypdf import PdfReader
import docx

def parse_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        # Simple header/footer cleaning: ignore top and bottom 5% of the page
        # This is a placeholder for more sophisticated logic
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def parse_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def clean_text(text):
    # Placeholder for cleaning logic: remove redundant whitespace, headers, etc.
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned_lines)

def main():
    parser = argparse.ArgumentParser(description="Ingest aviation accident reports into GraphRAG input directory.")
    parser.add_argument("--source", type=str, required=True, help="Path to source directory containing PDF/DOCX files.")
    parser.add_argument("--output", type=str, default="input", help="Path to GraphRAG input directory.")
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    for i, filename in enumerate(os.listdir(args.source)):
        file_path = os.path.join(args.source, filename)
        content = ""
        if filename.endswith(".pdf"):
            print(f"Parsing PDF: {filename}")
            content = parse_pdf(file_path)
        elif filename.endswith(".docx"):
            print(f"Parsing DOCX: {filename}")
            content = parse_docx(file_path)
        elif filename.endswith(".txt"):
            print(f"Reading TXT: {filename}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        if content:
            cleaned_content = clean_text(content)
            output_filename = f"report_{i}.txt"
            with open(os.path.join(args.output, output_filename), 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f"Saved to {args.output}/{output_filename}")

if __name__ == "__main__":
    main()
