import re
import io
import requests
from PyPDF2 import PdfReader

def getDriveId(link):
    patterns = [
        r"/d/([a-zA-Z0-9_-]+)",
        r"id=([a-zA-Z0-9_-]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1) # gives the matched pattern only not full link
    return None

def readFromLink(drive_link):
    file_id = getDriveId(drive_link)
    if not file_id:
        return ""

    # for google docs
    doc_url = f"https://docs.google.com/document/d/{file_id}/export?format=txt"
    response = requests.get(doc_url)
    if response.status_code == 200 and "DOCTYPE" not in response.text:
        return response.text

    # for pdf
    pdf_url = f"https://drive.google.com/uc?id={file_id}&export=download"
    pdf_bytes = requests.get(pdf_url).content
    reader = PdfReader(io.BytesIO(pdf_bytes))

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    return text
