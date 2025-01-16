import re
import nltk
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

nltk.download("punkt")
nltk.download("stopwords")

# Sentiment Analysis using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    sentiment = "positive" if polarity > 0 else "negative" if polarity < 0 else "neutral"
    return sentiment, polarity, subjectivity

# Topic Modeling using LDA for Thematic Analysis
def analyze_themes(text):
    vectorizer = CountVectorizer(stop_words="english")
    X = vectorizer.fit_transform([text])

    lda = LatentDirichletAllocation(n_components=1, random_state=42)
    lda.fit(X)

    terms = vectorizer.get_feature_names_out()
    topic_keywords = [terms[i] for i in lda.components_.argsort()[0, -10:]]
    
    return " ".join(topic_keywords)

# Analyze Narrative Pace: Based on sentence length
def analyze_pace(text):
    sentences = nltk.sent_tokenize(text)
    sentence_lengths = [len(sentence.split()) for sentence in sentences]
    avg_length = sum(sentence_lengths) / len(sentence_lengths)
    pace = "slow" if avg_length > 20 else "fast"
    return pace

# Mood Mapping based on Sentiment, Themes, and Pace
def map_mood(sentiment, themes, pace):
    mood = []

    if sentiment == "positive":
        mood.append("uplifting")
    elif sentiment == "negative":
        mood.append("melancholy")
    
    if "adventure" in themes or "journey" in themes:
        mood.append("epic")
    elif "love" in themes or "romance" in themes:
        mood.append("romantic")
    
    if pace == "fast":
        mood.append("energetic")
    else:
        mood.append("reflective")
    
    return mood

# Function to analyze the book and generate music recommendations
def analyze_book_and_recommend_music(book_text):
    preprocessed_text = preprocess_text(book_text)
    
    sentiment, polarity, subjectivity = analyze_sentiment(preprocessed_text)
    themes = analyze_themes(preprocessed_text)
    pace = analyze_pace(preprocessed_text)
    
    mood = map_mood(sentiment, themes, pace)
    
    recommended_songs = get_spotify_recommendations(mood)
    
    return {
        "sentiment": sentiment,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "themes": themes,
        "pace": pace,
        "mood": mood,
        "recommended_songs": recommended_songs
    }

def preprocess_text(text):
    return re.sub(r"[^\w\s]", "", text.lower())
