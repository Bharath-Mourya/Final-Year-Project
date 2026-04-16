import sqlite3

def init_db():
    conn = sqlite3.connect("risk_results.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        email_count INTEGER,
        keyword_hits INTEGER,
        link_count INTEGER,
        risk_score INTEGER,
        risk_level TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_result(url, features, score, level):
    try:
        conn = sqlite3.connect("risk_results.db")
        cursor = conn.cursor()

        email = features.get("email_count", 0)
        keywords = features.get("keyword_hits", 0)
        links = features.get("link_count", 0)

        cursor.execute("""
        INSERT INTO results (url, email_count, keyword_hits, link_count, risk_score, risk_level)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (url, email, keywords, links, score, level))

        conn.commit()
        print(f"[+] Data saved for {url}")

    except Exception as e:
        print("Database error:", e)

    finally:
        conn.close()