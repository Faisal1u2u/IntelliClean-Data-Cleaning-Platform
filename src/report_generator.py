from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os


class ReportGenerator:

    def __init__(self, df, summary):
        self.df = df
        self.summary = summary

    def generate_pdf(self):

        os.makedirs("../reports", exist_ok=True)

        file_path = "../reports/data_cleaning_report.pdf"
        doc = SimpleDocTemplate(file_path, pagesize=A4)

        elements = []
        styles = getSampleStyleSheet()

        # Title
        elements.append(Paragraph("<b>Automated Data Cleaning Report</b>", styles["Title"]))
        elements.append(Spacer(1, 0.3 * inch))

        # Date
        elements.append(Paragraph(f"Generated on: {datetime.now()}", styles["Normal"]))
        elements.append(Spacer(1, 0.3 * inch))

        # Dataset Info
        elements.append(Paragraph(f"Total Records After Cleaning: {len(self.df)}", styles["Normal"]))
        elements.append(Spacer(1, 0.3 * inch))

        # Summary Table (first few rows)
        summary_data = [self.summary.columns.tolist()] + self.summary.head().values.tolist()
        table = Table(summary_data)
        table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        elements.append(Paragraph("<b>Summary Statistics</b>", styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(table)
        elements.append(Spacer(1, 0.5 * inch))

        # Add Images
        elements.append(Paragraph("<b>Sales Distribution</b>", styles["Heading2"]))
        elements.append(Image("../reports/sales_distribution.png", width=5 * inch, height=3 * inch))
        elements.append(Spacer(1, 0.5 * inch))

        elements.append(Paragraph("<b>Revenue by City</b>", styles["Heading2"]))
        elements.append(Image("../reports/revenue_by_city.png", width=5 * inch, height=3 * inch))

        doc.build(elements)

import logging
logging.info("PDF Report Generated Successfully.")