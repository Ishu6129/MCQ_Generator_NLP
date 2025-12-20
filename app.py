from flask import Flask,request,render_template
from PyPDF2 import PdfReader
import spacy
import random
from collections import Counter



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
        page_text=pdf_reader.pages[page_num].extract_text()
        text+=page_text
    return text

@app.route("/",methods=['POST','GET'])
def index():
    if request.method=="POST":
        text=''
        if "uploaded_files" in request.files:
            files=request.files.getlist("uploaded_files")
            for file in files:
                if file.filename.endswith(".pdf"):
                    text+=process_pdf(file)
                    print(text)
                elif file.filename.endswith(".txt"):
                    text+=file.read().decode('utf-8')
                else:
                    return "<script>alert('Unsupported file type'); window.location.href='/';</script>"

        num_questions=int(request.form['num_questions'])
        mcqs=generate_mcqs(text,num_questions)
        mcq_with_index=[(i+1,mcq) for i,mcq in enumerate(mcqs)]
        return render_template('mcqs.html',mcqs=mcq_with_index) 
    
    return render_template('index.html')


if __name__=="__main__":
    app.run(host="0.0.0.0", port=3000)
