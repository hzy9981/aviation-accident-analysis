from pathlib import Path
from pypdf import PdfReader
import docx

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

def parse_file(file_path):
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
        
    if file_path.suffix.lower() == ".pdf":
        content = parse_pdf(file_path)
    elif file_path.suffix.lower() == ".docx":
        content = parse_docx(file_path)
    elif file_path.suffix.lower() == ".txt":
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
    return clean_text(content)
