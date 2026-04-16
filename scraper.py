import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin


def scrape_site(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=3)

        if response.status_code != 200:
            return "", [], []

        soup = BeautifulSoup(response.text, "html.parser")

        # -------- Extract text --------
        text = soup.get_text()

        # -------- Extract links (CLEANED) --------
        raw_links = [a.get("href") for a in soup.find_all("a", href=True)]

        clean_links = set()

        for link in raw_links:
            if not link:
                continue

            # ❌ Skip unwanted links
            if link.startswith("javascript"):
                continue
            if link.startswith("#"):
                continue
            if link.startswith("mailto"):
                continue

            # Convert relative to full URL
            full_link = urljoin(url, link)

            clean_links.add(full_link)

        links = list(clean_links)

        # -------- Extract emails --------
        emails = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            response.text
        )

        emails = list(set(emails))  # remove duplicates

        return text, links, emails

    except Exception:
        return "", [], []