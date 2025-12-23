import google.generativeai as genai
from config import MCQ_API_KEY,GEMINI_MODEL_NAME


genai.configure(api_key=MCQ_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL_NAME)

def generate_ai_mcqs(summary_text, number_of_questions):
    prompt = f"""
You MUST follow the format EXACTLY.
DO NOT write explanations.
DO NOT write paragraphs.
DO NOT omit option labels.

Generate EXACTLY {number_of_questions} MCQs.

STRICT FORMAT (NO DEVIATION):

## MCQ
Question: <question>
A) <option A>
B) <option B>
C) <option C>
D) <option D>
Correct Answer: <A/B/C/D>

If the format is not followed, the answer is INVALID.

Text:
{summary_text}
"""
    return model.generate_content(prompt).text.strip()
