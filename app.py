from flask import Flask, render_template, request, jsonify
from recommendation_engine import nlp
import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
#print(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

def get_spotify_access_token():
    """
    Retrieves an access token for Spotify API calls.

    Uses the client id and secret to request an access token, which is then
    extracted from the response and returned. If the request fails or the
    access token is not found in the response, an error message is printed
    and None is returned.

    Returns:
        str: The access token, or None if there was an error.
    """
    url = "https://accounts.spotify.com/api/token"
    
    client_credentials = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"    
    encoded_credentials = base64.b64encode(client_credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        print(f"Failed to get access token: {response.status_code} - {response.text}")
        return None
    access_token = response.json().get("access_token")
    if not access_token:
        print(f"Error: Access token not found in response: {response.json()}")
    
    return access_token

SPOTIFY_ACCESS_TOKEN = get_spotify_access_token()

@app.route("/")
def index():
    """
    Render the main HTML page (frontend)

    This route is responsible for rendering the main HTML page that makes up
    the frontend of the application. The rendered page will include a form
    for the user to enter the title of a book, and a button to submit the form.

    The page will also include JavaScript code that will capture the form
    submission event, send a request to the /search_book endpoint, and then
    display the recommended playlist on the page.
    """
    return render_template("index.html")
  
@app.route("/search_book", methods=["GET"])
def search_book():

    """
    Handles GET requests to the /search_book endpoint.

    This route is responsible for fetching book data from the Google Books API
    and then using the book's description to determine a mood, which is then
    used to fetch a list of songs from the Spotify API. The list of songs is
    returned to the caller as JSON.

    The request must include a query parameter called "q", which should contain
    the title of the book to search for. If the query parameter is missing, this
    route will return a 400 error with a JSON response containing an error
    message.

    If the request is successful, the response will include the title of the
    book, the mood that was determined from the book's description, and a list
    of recommended songs. The songs will be listed in the "recommended_songs"
    key, and will be an array of objects with the following keys:
        song_name: The title of the song
        song_url: The URL of the song on Spotify
    """
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Book query is required"}), 400
    google_books_url = f"https://www.googleapis.com/books/v1/volumes?q={query}:keyes&key=AIzaSyAvkr6DdSr-0tZ362oyCMmQMdbPdnagYsg"
    response = requests.get(google_books_url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from Google Books"}), 500

    data = response.json()
    if "items" not in data:
        return jsonify({"error": "No books found"}), 404

    book = data["items"][0]
    title = book["volumeInfo"].get("title", "Unknown Title")
    description = book["volumeInfo"].get("description", "")
    genre = book["volumeInfo"].get("categories", ["General"])[0]

    mood = nlp.analyze_text(description)

    spotify_url = f"https://api.spotify.com/v1/search?q={mood}&type=track&limit=10"
    headers = {"Authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"}
    spotify_response = requests.get(spotify_url, headers=headers)
    spotify_data = spotify_response.json()
    print(spotify_data)

    if "tracks" not in spotify_data or not spotify_data["tracks"]["items"]:
        return jsonify({"error": "No songs found for the mood/genre"}), 404

    songs = []
    for track in spotify_data["tracks"]["items"]:
        song_name = track["name"]
        song_url = track["external_urls"]["spotify"]
        songs.append({"song_name": song_name, "song_url": song_url})

    return jsonify({
        "book_title": title,
        "mood": mood,
        "recommended_songs": songs,
    })

if __name__ == "__main__":
    app.run(debug=True)

