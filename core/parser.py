import fitz
import docx


def _clean(text: str) -> str:
    return " ".join(text.replace("\n", " ").split())


def read_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return _clean(text)


def read_docx(file):
    doc = docx.Document(file)
    return _clean(" ".join(p.text for p in doc.paragraphs))


def read_txt(file):
    return _clean(file.read().decode("utf-8", errors="ignore"))


def get_input_text(uploaded_file, pasted_text):
    if uploaded_file:
        name = uploaded_file.name.lower()
        if name.endswith(".pdf"):
            return read_pdf(uploaded_file)
        if name.endswith(".docx"):
            return read_docx(uploaded_file)
        if name.endswith(".txt"):
            return read_txt(uploaded_file)
    return pasted_text
