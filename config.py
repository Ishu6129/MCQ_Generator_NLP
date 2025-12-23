import os
ALLOWED_EXTENSIONS = {"pdf", "txt", "docx"}
MAX_TEXT_CHAR_LIMIT = 3000
MAX_SUMMARY_SENTENCES = 8
MCQ_API_KEY = os.getenv("MCQ_API_KEY")
GEMINI_MODEL_NAME = "gemini-2.5-flash"
if not MCQ_API_KEY:
    raise ValueError(
        "MCQ_API_KEY environment variable not set. "
        "Please configure it before running the app."
    )
