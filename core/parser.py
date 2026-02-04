import streamlit as st
from io import StringIO
from PyPDF2 import PdfReader
import docx

def get_input_text(mode):
    if mode == "Paste IP Clause":
        return st.text_area("Enter IP clause or contract text")
    
    uploaded_file = st.file_uploader("Upload contract file", type=["pdf", "docx", "txt"])
    if uploaded_file is None:
        return None

    # PDF
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    # DOCX
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    # TXT
    if uploaded_file.type == "text/plain":
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        return stringio.read()

    return None
