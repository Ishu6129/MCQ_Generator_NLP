import spacy
import random
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def generatClassicMcqs(text, number_of_questions):
    document = nlp(text)
    sentences = [sentence.text for sentence in document.sents]

    selected_sentences = random.sample(
        sentences,
        min(number_of_questions, len(sentences))
    )

    mcqs = []

    for sentence in selected_sentences:
        parsed_sentence = nlp(sentence)
        nouns = [
            token.text for token in parsed_sentence
            if token.pos_ == "NOUN" and not token.is_stop
        ]

        if len(nouns) < 2:
            continue

        correct_answer = Counter(nouns).most_common(1)[0][0]
        question_text = sentence.replace(correct_answer, "_____", 1)

        distractors = list(set(nouns) - {correct_answer})
        while len(distractors) < 3:
            distractors.append("None")

        options = [correct_answer] + random.sample(distractors, 3)
        random.shuffle(options)

        correct_option = chr(65 + options.index(correct_answer))
        mcqs.append((question_text, options, correct_option))

    return mcqs
