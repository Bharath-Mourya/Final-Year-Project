import re

def clean_text(text):
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r'[^a-z0-9\s.:/-]', '', text)  # keep useful characters
    text = " ".join(text.split())

    return text