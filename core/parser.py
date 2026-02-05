# core/parser.py

import io

def get_input_text(input_source):
    """
    input_source:
      - UploadedFile (Streamlit)
      - str (pasted text)
    """

    # Case 1: pasted text
    if isinstance(input_source, str):
        return input_source.strip()

    # Case 2: uploaded file
    if input_source is not None:
        filename = input_source.name.lower()

        if filename.endswith(".txt"):
            return input_source.read().decode("utf-8")

        elif filename.endswith(".pdf"):
            from pypdf import PdfReader
            reader = PdfReader(input_source)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text

        elif filename.endswith(".docx"):
            from docx import Document
            doc = Document(io.BytesIO(input_source.read()))
            return "\n".join(p.text for p in doc.paragraphs)

        else:
            raise ValueError("Unsupported file type")

    return ""
