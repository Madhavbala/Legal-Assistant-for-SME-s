import streamlit as st
import fitz  # PyMuPDF
from docx import Document

def extract_text(file, file_type):
    """
    Extract text from uploaded file based on file type
    """
    if file_type == "pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    elif file_type == "docx":
        document = Document(file)
        return "\n".join([p.text for p in document.paragraphs])

    elif file_type == "txt":
        return file.read().decode("utf-8")

    else:
        return ""


def get_input_text(mode):
    """
    Handles both paste mode and upload mode
    """

    if mode == "Paste IP Clause":
        return st.text_area(
            "Paste IP clause here",
            height=200,
            placeholder="Paste intellectual property clause here..."
        )

    # File upload mode
    uploaded = st.file_uploader(
        "Upload contract file",
        type=["pdf", "docx", "txt"]
    )

    if uploaded:
        file_type = uploaded.name.split(".")[-1].lower()
        return extract_text(uploaded, file_type)

    return None
