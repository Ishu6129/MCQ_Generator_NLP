import numpy as np
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("en_core_web_sm")

def summarize(text, max_sentences):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]

    if len(sentences) <= max_sentences:
        return text

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(sentences)

    sentence_scores = np.sum(tfidf_matrix.toarray(), axis=1)

    ranked_sentences = sorted(
        ((sentence_scores[i], s) for i, s in enumerate(sentences)),
        reverse=True
    )

    return " ".join(s for _, s in ranked_sentences[:max_sentences])
    