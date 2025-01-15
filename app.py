from flask import Flask, request, jsonify
from recommendation_engine import nlp
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# API Keys from environment variables
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Function to get Spotify access token
def get_spotify_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}",
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")

SPOTIFY_ACCESS_TOKEN = get_spotify_access_token()

@app.route("/search_book", methods=["GET"])
def search_book():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Book query is required"}), 400

    # Fetch book details from Google Books API
    google_books_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}"
    response = requests.get(google_books_url)
    data = response.json()

    if "items" not in data:
        return jsonify({"error": "No books found"}), 404

    # Extract book details
    book = data["items"][0]
    title = book["volumeInfo"].get("title", "Unknown Title")
    description = book["volumeInfo"].get("description", "")
    genre = book["volumeInfo"].get("categories", ["General"])[0]

    # Use NLP to extract mood/genre from description
    mood = nlp.analyze_text(description)

    # Fetch Spotify playlist based on mood/genre
    spotify_url = f"https://api.spotify.com/v1/search?q={mood}&type=playlist&limit=1"
    headers = {"Authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"}
    spotify_response = requests.get(spotify_url, headers=headers)
    spotify_data = spotify_response.json()

    if not spotify_data["playlists"]["items"]:
        return jsonify({"error": "No playlists found"}), 404

    playlist = spotify_data["playlists"]["items"][0]
    playlist_name = playlist["name"]
    playlist_url = playlist["external_urls"]["spotify"]

    return jsonify({
        "book_title": title,
        "mood": mood,
        "playlist_name": playlist_name,
        "playlist_url": playlist_url,
    })

if __name__ == "__main__":
    app.run(debug=True)
