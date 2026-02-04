import re

def split_clauses(text: str):
    # Split by period or new line for simplicity
    raw_clauses = re.split(r'\n+|(?<=\.)\s+', text)
    return [c.strip() for c in raw_clauses if c.strip()]
