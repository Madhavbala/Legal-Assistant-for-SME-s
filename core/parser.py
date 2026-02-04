import os
from PyPDF2 import PdfReader
import docx

def get_file_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == ".pdf":
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"

    elif ext == ".docx":
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    return text.strip()
