import re

def extract_features(text, emails, links):
    text = (text or "").lower()
    emails = emails or []
    links = links or []

    keywords = [
        "admin", "login", "password", "backup", "config",
        "root", "database", "secret", "api", "token", "key"
    ]

    found_keywords = [
        k for k in keywords if re.search(rf"\b{k}\b", text)
    ]

    return {
        "email_count": len(emails),
        "emails": list(set(emails)),
        "link_count": len(links),
        "links": links[:10],
        "keyword_hits": len(found_keywords),
        "keywords_found": found_keywords
    }