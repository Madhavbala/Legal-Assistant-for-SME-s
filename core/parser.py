import fitz  # PyMuPDF
import docx


def get_input_text(uploaded_file, pasted_text):
    """
    Extract text from uploaded file OR pasted text.
    Supports PDF, DOC/DOCX, TXT.
    """

    # 1️⃣ If pasted text is provided
    if pasted_text and pasted_text.strip():
        return pasted_text.strip()

    # 2️⃣ If no file uploaded
    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    # 3️⃣ PDF
    if file_name.endswith(".pdf"):
        text = ""
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()

    # 4️⃣ DOC / DOCX
    if file_name.endswith(".docx") or file_name.endswith(".doc"):
        document = docx.Document(uploaded_file)
        return "\n".join(p.text for p in document.paragraphs).strip()

    # 5️⃣ TXT
    if file_name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8").strip()

    return ""
