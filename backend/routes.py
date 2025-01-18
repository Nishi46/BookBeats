from backend import app
from flask import render_template, request
from backend.book_api import get_book_info
from backend.theme_extractor import extract_themes_from_text
from backend.spotify_client import search_songs

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    error = None
    book_name = None
    
    if request.method == "POST":
        book_name = request.form["book_name"]
        
        book_info = get_book_info(book_name)
        
        if "error" in book_info:
            error = book_info["error"]
        else:
            themes = extract_themes_from_text(book_info["description"])
            print(themes)
            recommendations = search_songs(" ".join(themes))
    
    return render_template("index.html", book_name=book_name, recommendations=recommendations, error=error)
