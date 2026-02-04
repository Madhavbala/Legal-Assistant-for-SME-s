def is_ip_clause(clause):
    keywords = [
        "intellectual property",
        "ip",
        "copyright",
        "patent",
        "shall vest",
        "exclusive"
    ]
    text = clause.lower()
    return any(k in text for k in keywords)
