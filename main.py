from scraper import scrape_site
from clean_data import clean_text
from features import extract_features
from risk_score import calculate_risk
from database import init_db, save_result
from subdomain_enum import enumerate_subdomains
from report import generate_pdf_report


def analyze_target(url):
    try:
        text, links, emails = scrape_site(url)

        if not text:
            return None, 0, "Low"

        cleaned_text = clean_text(text)
        features = extract_features(cleaned_text, emails, links)
        score, level = calculate_risk(features)

        save_result(url, features, score, level)

        return features, score, level

    except Exception:
        return None, 0, "Low"


def main():
    domain = input("Enter domain (example.com): ").strip()

    init_db()

    subdomains = enumerate_subdomains(domain)
    targets = [domain] + subdomains

    highest_score = 0
    highest_level = "Low"
    highest_features = None

    all_results = []

    print("\n=========== SCANNING TARGETS ===========")

    for target in targets:
        url = "https://" + target
        print(f"Scanning: {url}")

        features, score, level = analyze_target(url)

        if features is not None:
            all_results.append({
                "url": url,
                "features": features,
                "score": score,
                "level": level
            })

        if score > highest_score:
            highest_score = score
            highest_level = level
            highest_features = features

    print("\n=========== SUMMARY ===========")
    print("Highest Risk Score :", highest_score)
    print("Overall Risk Level :", highest_level)

    # Generate PDF (includes graph)
    if all_results:
        generate_pdf_report(all_results)


if __name__ == "__main__":
    main()