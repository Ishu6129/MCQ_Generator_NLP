from fpdf import FPDF
from io import BytesIO

def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)

    pdf_string = pdf.output(dest="S").encode("latin-1")

    pdf_bytes = BytesIO(pdf_string)
    pdf_bytes.seek(0)

    return pdf_bytes