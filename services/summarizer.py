import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("en_core_web_sm")

def summarize(text, max_sentences=8):
    doc = nlp(text)

    sentences = [
        sent.text.strip()
        for sent in doc.sents
        if len(sent.text.strip()) > 30
    ]

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(sentences)

    sentence_scores = tfidf_matrix.sum(axis=1).A1

    ranked_sentences = sorted(
        zip(sentence_scores, sentences),
        reverse=True
    )

    summary = " ".join(
        sentence for _, sentence in ranked_sentences[:max_sentences]
    )

    return summary
