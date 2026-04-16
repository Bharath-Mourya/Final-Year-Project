from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from visualize import generate_graph


# ---------------- REMEDIATION FUNCTION ----------------
def get_remediation(features, level):
    emails = features.get("email_count", 0)
    keywords = features.get("keyword_hits", 0)
    links = features.get("link_count", 0)

    recommendations = []

    if emails > 0:
        recommendations.append("Remove or obfuscate exposed email addresses to prevent phishing attacks.")

    if keywords > 0:
        recommendations.append("Avoid exposing sensitive keywords like admin, login, or password in public pages.")

    if links > 100:
        recommendations.append("Reduce excessive links to minimize attack surface.")

    if level == "High":
        recommendations.append("Perform full security audit and implement strict access control.")

    if not recommendations:
        recommendations.append("No major risks detected. Continue monitoring and maintain best practices.")

    return recommendations


def generate_pdf_report(results, filename="risk_report.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["Normal"]

    content = []

    # ---------------- TITLE ----------------
    content.append(Paragraph("AI Web Recon - Risk Analysis Report", title_style))
    content.append(Spacer(1, 15))

    # ---------------- DESCRIPTION ----------------
    content.append(Paragraph(
        "This report presents the results of an AI-based web reconnaissance system "
        "that analyzes websites and their subdomains to identify potential security risks.",
        normal_style
    ))
    content.append(Spacer(1, 20))

    # ---------------- TABLE ----------------
    table_data = [["Target URL", "Emails", "Keywords", "Links", "Score", "Level"]]

    highest_score = 0
    overall_level = "Low"
    highest_result = None

    for result in results:
        features = result["features"]
        score = result["score"]
        level = result["level"]

        if score > highest_score:
            highest_score = score
            overall_level = level
            highest_result = result

        table_data.append([
            result["url"],
            features["email_count"],
            features["keyword_hits"],
            features["link_count"],
            score,
            level
        ])

    table = Table(table_data, colWidths=[150, 50, 60, 60, 60, 60])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ]))

    content.append(table)
    content.append(Spacer(1, 20))

    # ---------------- GRAPH ----------------
    if highest_result:
        graph_file = generate_graph(
            highest_result["features"],
            highest_result["score"],
            highest_result["level"]
        )

        content.append(Paragraph("Risk Visualization", heading_style))
        content.append(Spacer(1, 10))
        content.append(Image(graph_file, width=400, height=250))
        content.append(Spacer(1, 20))

    # ---------------- DETAILED FINDINGS ----------------
    content.append(Paragraph("Detailed Findings", heading_style))
    content.append(Spacer(1, 10))

    for result in results:
        features = result["features"]
        score = result["score"]
        level = result["level"]

        # Risk color
        if level == "Low":
            risk_color = "green"
        elif level == "Medium":
            risk_color = "orange"
        else:
            risk_color = "red"

        emails = features.get("emails", [])
        keywords = features.get("keywords_found", [])
        links = features.get("links", [])

        email_text = ", ".join([f"<font color='blue'>{e}</font>" for e in emails]) if emails else "None"
        keyword_text = ", ".join([f"<font color='red'>{k}</font>" for k in keywords]) if keywords else "None"
        link_text = "<br/>".join(links[:5]) if links else "None"

        # -------- GET REMEDIATION --------
        remediations = get_remediation(features, level)
        remediation_text = "<br/>".join([f"• {r}" for r in remediations])

        detail = f"""
        <b>Target:</b> {result["url"]}<br/>
        <b>Emails:</b> {email_text}<br/>
        <b>Keywords:</b> {keyword_text}<br/>
        <b>Links (sample):</b><br/>{link_text}<br/>
        <b>Score:</b> <font color='{risk_color}'>{score}</font><br/>
        <b>Risk Level:</b> <font color='{risk_color}'>{level}</font><br/><br/>

        <b>Remediation:</b><br/>
        {remediation_text}
        """

        content.append(Paragraph(detail, normal_style))
        content.append(Spacer(1, 15))

    # ---------------- SUMMARY ----------------
    summary = f"""
    <b>Summary:</b><br/>
    Total Targets: {len(results)}<br/>
    Highest Score: {highest_score}<br/>
    Overall Risk: <font color='red'>{overall_level}</font>
    """

    content.append(Paragraph(summary, normal_style))
    content.append(Spacer(1, 15))

    # ---------------- BUILD ----------------
    doc.build(content)

    print("[+] Attractive PDF Report Generated with Remediation!")