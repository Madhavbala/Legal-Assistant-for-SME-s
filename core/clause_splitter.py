import re

def split_clauses(text):
    clauses = re.split(r'[.;\n]', text)
    return [c.strip() for c in clauses if len(c.strip()) > 10]
