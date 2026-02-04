import re

def split_clauses(text):
    text = text.replace("\n", " ").strip()

    clauses = re.split(
        r'(?<=[.;])\s+(?=[A-Z])',
        text
    )

    return [c.strip() for c in clauses if len(c.strip()) > 20]
