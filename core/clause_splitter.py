import re

def split_clauses(text: str) -> list:
    # Split on ., ;, or Hindi danda (।)
    clauses = re.split(r"[।.;]\s*", text)
    # Remove empty strings
    return [c.strip() for c in clauses if c.strip()]
