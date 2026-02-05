import re
import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")  # Install with: python -m spacy download en_core_web_sm

def clean_text(text):
    """
    Cleans text from unwanted symbols, multiple spaces, bullets, and line breaks.
    """
    # Replace newlines or tabs with space
    text = re.sub(r'[\n\t]+', ' ', text)

    # Remove unwanted symbols (bullets, diamonds, arrows, etc.)
    text = re.sub(r'[•♦◦■►●–—]', '', text)

    # Remove multiple spaces
    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip()


def split_clauses(text, lang="en"):
    """
    Split text into clauses intelligently using spaCy for English.
    For Hindi or other languages, fallback to regex split.
    """
    text = clean_text(text)

    clauses = []

    if lang.lower().startswith("en"):
        # Use spaCy sentence segmentation for English
        doc = nlp(text)
        clauses = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    else:
        # Simple regex split for Hindi or other languages
        clauses = re.split(
            r'(?<=।|\?|;|:)\s+|\d+\.\s+|\([a-zA-Z0-9]+\)\s+',
            text
        )
        clauses = [c.strip() for c in clauses if c.strip()]

    return clauses
