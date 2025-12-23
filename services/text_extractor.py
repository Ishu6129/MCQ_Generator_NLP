import pdfplumber
import docx
from io import BytesIO

def extractText(file_bytes, filename):
    extension = filename.rsplit(".", 1)[1].lower()
    if extension == "pdf":
        text = ""
        pdf = pdfplumber.open(BytesIO(file_bytes))
        try:
            for page in pdf.pages:
                text += page.extract_text() or ""
        finally:
            pdf.close()
        return text

    if extension == "docx":
        doc = docx.Document(BytesIO(file_bytes))
        return " ".join(p.text for p in doc.paragraphs)

    if extension == "txt":
        return file_bytes.decode("utf-8", errors="ignore")

    return ""
