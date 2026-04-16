import matplotlib.pyplot as plt

def generate_graph(features, score, level, filename="risk_graph.png"):
    labels = ["Emails", "Keywords", "Links", "Risk Score"]
    values = [
        features.get("email_count", 0),
        features.get("keyword_hits", 0),
        features.get("link_count", 0),
        score
    ]

    plt.figure(figsize=(6, 4))
    bars = plt.bar(labels, values)

    plt.title(f"Risk Analysis (Level: {level})")

    # Add values on top
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval),
                 ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

    return filename