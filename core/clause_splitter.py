import re
import spacy
from spacy.util import is_package, get_package_path
from spacy.cli import download

# Ensure the model is installed in the environment
if not is_package("en_core_web_sm"):
    download("en_core_web_sm")

import en_core_web_sm
nlp = en_core_web_sm.load()

def clean_text(text):
    text = re.sub(r'[\n\t]+', ' ', text)
    text = re.sub(r'[•♦◦■►●–—]', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def split_clauses(text, lang="en"):
    text = clean_text(text)
    clauses = []

    if lang.lower().startswith("en"):
        doc = nlp(text)
        clauses = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    else:
        clauses = re.split(r'(?<=।|\?|;|:)\s+|\d+\.\s+|\([a-zA-Z0-9]+\)\s+', text)
        clauses = [c.strip() for c in clauses if c.strip()]

    return clauses
