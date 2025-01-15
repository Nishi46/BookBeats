import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import re

nltk.download("punkt")
nltk.download("stopwords")

def analyze_text(text):
    # Preprocess text
    text = re.sub(r"[^\w\s]", "", text.lower())
    words = word_tokenize(text)
    words = [word for word in words if word not in stopwords.words("english")]

    keywords_to_moods = {
        "love": "romance",
        "adventure": "adventure",
        "war": "epic",
        "space": "sci-fi",
        "magic": "fantasy",
        "mystery": "mystery",
        "crime": "thriller",
        "sad": "melancholy",
        "happy": "uplifting",
    }

    mood_counter = Counter()
    for word in words:
        for keyword, mood in keywords_to_moods.items():
            if keyword in word:
                mood_counter[mood] += 1

    if mood_counter:
        return mood_counter.most_common(1)[0][0]
    return "general"
