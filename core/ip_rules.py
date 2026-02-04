def is_ip_clause(text: str) -> bool:
    if not text:
        return False

    text = text.lower()

    ip_keywords = [
        "intellectual property",
        "ip rights",
        "copyright",
        "patent",
        "trademark",
        "ownership",
        "proprietary",
        "source code",
        "work product",
        "derivative works",
        "license",
        "assign",
        "assignment",
        "exclusive rights",
        "बौद्धिक संपदा",     # Hindi
        "कॉपीराइट",
        "पेटेंट",
        "स्वामित्व"
    ]

    return any(keyword in text for keyword in ip_keywords)
