import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from spellchecker import SpellChecker  

nlp = spacy.load("en_core_web_sm")
spell = SpellChecker()  

def correct_spelling(text):
    """Corrects spelling mistakes in the input text."""
    words = text.split()
    corrected_words = [spell.correction(word) if word not in spell else word for word in words]
    return " ".join(corrected_words)

def preprocess_text(text):
    """Cleans, corrects spelling, and preprocesses the input text."""
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters and digits
    text = correct_spelling(text)  # Correct spelling errors
    doc = nlp(text)
    lemmatized_text = " ".join([token.lemma_ for token in doc if not token.is_stop])  # Lemmatize
    return lemmatized_text
def extract_themes_from_text(text, top_n=20):
    """Extract themes (keywords) from the book using TF-IDF."""
    cleaned_text = preprocess_text(text)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([cleaned_text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray().flatten()
    sorted_scores = sorted(zip(scores, feature_names), reverse=True, key=lambda x: x[0])
    themes = [word for _, word in sorted_scores[:top_n]]
    return themes

def extract_named_entities(text):
    """Extract named entities (e.g., people, places, concepts) using spaCy."""
    doc = nlp(text)
    entities = set([ent.text for ent in doc.ents])
    return list(entities)
