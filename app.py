from flask import Flask,request,render_template
from PyPDF2 import PdfReader
import spacy
import random
import requests
from collections import Counter
import io
import re



app=Flask(__name__)

nlp = spacy.load("en_core_web_sm")
import random
from collections import Counter

def generate_mcqs(text, num_questions=5):
    if not text:
        return []
    
    doc = nlp(text)
    
    sentences = [sent.text for sent in doc.sents]
    selected_sentences = random.sample(
        sentences, min(num_questions, len(sentences))
    )
    
    mcqs = []
    for sentence in selected_sentences:
        sent_doc = nlp(sentence)
        nouns = [token.text for token in sent_doc if token.pos_ == "NOUN" and not token.is_stop]

        if len(nouns) < 2:
            continue

        subject = Counter(nouns).most_common(1)[0][0]
        question = sentence.replace(subject, "_____", 1)

        distractors = list(set(nouns) - {subject})
        while len(distractors) < 3:
            distractors.append("None")
        options = [subject] + random.sample(distractors, 3)
        random.shuffle(options)

        correct_answer = chr(65 + options.index(subject))

        mcqs.append((question, options, correct_answer))

    return mcqs

def process_pdf(file):
    text=""
    pdf_reader=PdfReader(file)
    for page_num in range(len(pdf_reader.pages)):
        page_text = pdf_reader.pages[page_num].extract_text()
        if page_text:
            text += page_text

    return text

def extract_drive_file_id(link):
    patterns = [
        r"https://drive.google.com/file/d/([a-zA-Z0-9_-]+)",
        r"https://drive.google.com/open\?id=([a-zA-Z0-9_-]+)",
        r"https://docs.google.com/document/d/([a-zA-Z0-9_-]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1)
    return None


def process_drive_file(drive_link):
    file_id = extract_drive_file_id(drive_link)
    if not file_id:
        return ""

    # If uploaded link is of Doc
    doc_url = f"https://docs.google.com/document/d/{file_id}/export?format=txt"
    response = requests.get(doc_url)

    if response.status_code == 200 and "DOCTYPE" not in response.text:
        return response.text

    # If uploaded link is of pdf
    pdf_url = f"https://drive.google.com/uc?id={file_id}&export=download"
    pdf_response = requests.get(pdf_url)

    pdf_file = io.BytesIO(pdf_response.content)
    reader = PdfReader(pdf_file)

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    return text


@app.route("/",methods=['POST','GET'])
def index():
    if request.method=="POST":
        text=''
        
        files = request.files.getlist("uploaded_files")
        for file in files:
            if file.filename.endswith(".pdf"):
                text += process_pdf(file)
            elif file.filename.endswith(".txt"):
                text += file.read().decode("utf-8")

        # Link
        drive_link = request.form.get("drive_link")
        if drive_link:
            text += process_drive_file(drive_link)

        if not text.strip():
            return "<script>alert('No valid text found');window.location.href='/';</script>"

        num_questions=int(request.form['num_questions'])
        mcqs=generate_mcqs(text,num_questions)
        mcq_with_index=[(i+1,mcq) for i,mcq in enumerate(mcqs)]
        return render_template('mcqs.html',mcqs=mcq_with_index) 
    
    return render_template('index.html')


if __name__=="__main__":
    app.run(host="0.0.0.0", port=3000)
