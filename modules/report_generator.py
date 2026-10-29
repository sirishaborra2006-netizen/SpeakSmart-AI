from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(results, transcript):

    pdf_file = "reports/speech_report.pdf"

    doc = SimpleDocTemplate(pdf_file)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("SpeakSmart AI Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Total Words: {results['total_words']}", styles["Normal"]))
    content.append(Paragraph(f"Filler Words: {results['filler_count']}", styles["Normal"]))
    content.append(Paragraph(f"Confidence: {results['confidence_score']}%", styles["Normal"]))
    content.append(Paragraph(f"WPM: {results['wpm']}", styles["Normal"]))
    content.append(
    Paragraph(
        f"Duration: {results.get('speech_duration', results.get('duration', 0))} sec",
        styles["Normal"]
    )
)

    content.append(Spacer(1, 12))
    content.append(Paragraph("Transcript", styles["Heading2"]))
    content.append(Paragraph(transcript, styles["Normal"]))

    doc.build(content)

    return pdf_file