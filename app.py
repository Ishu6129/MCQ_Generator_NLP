from flask import Flask, render_template, request, send_file
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()

from config import *
from services import (
    extractText,
    readFromLink,
    summarize,
    generatClassicMcqs,
    generate_ai_mcqs,
    generate_pdf
)
from services.ai_parser import parse_ai_mcqs
MAX_AI_MCQS = 15

generated_pdf_cache = {}

def is_allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        combined_text = ""

        # Uploaded File
        uploaded_file = request.files.get("file")
        if uploaded_file and is_allowed_file(uploaded_file.filename, ALLOWED_EXTENSIONS):
            file_bytes = uploaded_file.read()
            combined_text += extractText(file_bytes, uploaded_file.filename)

        # Link Files
        drive_link = request.form.get("drive_link")
        if drive_link:
            combined_text += readFromLink(drive_link)

        if not combined_text.strip():
            return "<script>alert('No valid text provided');history.back()</script>"

       
        limited_text = combined_text[:MAX_TEXT_CHAR_LIMIT]
        number_of_questions = int(request.form["num_questions"])
        selected_mode = request.form["mode"]

        # If Ai selected
        if selected_mode == "ai":
            if number_of_questions > MAX_AI_MCQS:
                return (
                    "<script>"
                    "alert('AI mode supports a maximum of 15 MCQs only.');"
                    "history.back();"
                    "</script>"
                )

            summary_text = summarize(limited_text, MAX_SUMMARY_SENTENCES)
            raw_ai_output = generate_ai_mcqs(summary_text, number_of_questions)
            parsed_mcqs = parse_ai_mcqs(raw_ai_output)

            if not parsed_mcqs:
                return "<script>alert('AI failed to generate valid MCQs');history.back()</script>"

            generated_pdf_cache["latest"] = generate_pdf(raw_ai_output)

            return render_template(
                "results.html",
                mcqs=parsed_mcqs
            )
        manual_mcqs = generatClassicMcqs(limited_text, number_of_questions)

        return render_template(
            "mcqs.html",
            mcqs=enumerate(manual_mcqs, 1)
        )

    return render_template("index.html")

@app.route("/download/pdf")
def download_pdf():
    pdf_file = generated_pdf_cache.get("latest")

    if not pdf_file:
        return "No PDF available", 404

    return send_file(
        pdf_file,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="mcqs.pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
