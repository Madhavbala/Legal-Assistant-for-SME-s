import fitz  # PyMuPDF
import docx
import re
from langdetect import detect


def clean_text(text: str) -> str:
    """
    Normalize extracted text:
    - remove weird PDF symbols
    - fix broken newlines
    """
    text = text.replace("\x0c", " ")
    text = re.sub(r"[•·●▪]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def read_pdf(file) -> str:
    doc = fitz.open(stream=file.read(), filetype="pdf")
    pages = []
    for page in doc:
        pages.append(page.get_text())
    return clean_text(" ".join(pages))


def read_docx(file) -> str:
    document = docx.Document(file)
    text = " ".join([p.text for p in document.paragraphs])
    return clean_text(text)


def read_txt(file) -> str:
    raw = file.read().decode("utf-8", errors="ignore")
    return clean_text(raw)


def get_input_text(uploaded_file, pasted_text):
    """
    Unified input handler
    """

    if pasted_text and pasted_text.strip():
        text = pasted_text.strip()
    elif uploaded_file:
        name = uploaded_file.name.lower()

        if name.endswith(".pdf"):
            text = read_pdf(uploaded_file)

        elif name.endswith(".docx") or name.endswith(".doc"):
            text = read_docx(uploaded_file)

        elif name.endswith(".txt"):
            text = read_txt(uploaded_file)

        else:
            raise ValueError("Unsupported file format")

    else:
        return None, None

    try:
        lang = "Hindi" if detect(text) == "hi" else "English"
    except:
        lang = "English"

    return text, lang
