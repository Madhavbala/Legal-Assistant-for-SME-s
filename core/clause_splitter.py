"""
Clause Splitter
---------------
Splits contract text into clean, readable legal clauses.
Designed to work on Streamlit Cloud (no spaCy model downloads).
"""

import re
import spacy


def _get_nlp():
    """
    Create a lightweight spaCy pipeline without external models.
    Uses sentencizer for sentence boundary detection.
    """
    nlp = spacy.blank("en")
    nlp.add_pipe("sentencizer")
    return nlp


nlp = _get_nlp()


def _clean_text(text: str) -> str:
    """
    Clean noisy PDF / DOC extracted text.
    - Removes bullet symbols
    - Normalizes spaces
    - Fixes broken lines
    """
    if not text:
        return ""

    # Remove common bullet / list symbols
    text = re.sub(r"[•▪●◦►▪–—]", " ", text)

    # Remove multiple dots caused by PDF extraction
    text = re.sub(r"\.{2,}", ".", text)

    # Merge broken lines inside sentences
    text = re.sub(r"\n+", " ", text)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_clauses(text: str):
    """
    Split cleaned text into meaningful legal clauses.

    Returns:
        List[str] : list of clauses
    """
    cleaned_text = _clean_text(text)

    if not cleaned_text:
        return []

    doc = nlp(cleaned_text)

    clauses = []
    buffer = ""

    for sent in doc.sents:
        sentence = sent.text.strip()

        # Merge short fragments with previous sentence
        if len(sentence) < 40:
            buffer += " " + sentence
            continue

        if buffer:
            sentence = buffer.strip() + " " + sentence
            buffer = ""

        clauses.append(sentence.strip())

    # Add leftover buffer
    if buffer.strip():
        clauses.append(buffer.strip())

    return clauses
