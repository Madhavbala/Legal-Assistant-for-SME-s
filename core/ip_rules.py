def is_ip_clause(text: str) -> bool:
    if not text:
        return False

    text = text.lower()

    keywords = [
        "intellectual property",
        "ip",
        "copyright",
        "patent",
        "trademark",
        "license",
        "ownership",
        "assign",
        "assignment",
        "proprietary",
        "source code",
        "work product",
        "बौद्धिक संपदा",
        "कॉपीराइट",
        "पेटेंट",
        "स्वामित्व"
    ]

    return any(k in text for k in keywords)


def infer_ip_meaning(text: str) -> dict:
    text = text.lower()

    ownership = "Unclear"
    exclusivity = "Non-exclusive"

    if "exclusive" in text or "पूरी तरह" in text:
        exclusivity = "Exclusive"

    if "client" in text or "company" in text:
        ownership = "Client"
    elif "joint" in text or "both parties" in text or "संयुक्त" in text:
        ownership = "Shared"
    elif "service provider" in text or "developer" in text:
        ownership = "Service Provider"

    return {
        "ownership": ownership,
        "exclusivity": exclusivity
    }
