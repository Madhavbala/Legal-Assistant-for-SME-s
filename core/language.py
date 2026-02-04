from langdetect import detect

def detect_language(text):
    try:
        lang = detect(text)
        if lang == "en":
            return "English"
        if lang == "hi":
            return "Hindi"
        return "Unknown"
    except:
        return "Unknown"
