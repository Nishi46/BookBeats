import requests
from flask import Flask, render_template, request, jsonify
from analyzer import analyze_book_and_recommend_music
from spotify import get_spotify_recommendations
app = Flask(__name__)

# Google Books API URL template
GOOGLE_BOOKS_API_KEY = 'AIzaSyAvkr6DdSr-0tZ362oyCMmQMdbPdnagYsg'

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Book search route
@app.route('/search_book', methods=['GET'])
def search_book():
    query = request.args.get('q')
    
    if not query:
        return jsonify({"error": "Book query is required!"}), 400

    # Fetch book details from Google Books API
    google_books_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}"
    response = requests.get(google_books_url)
    
    if response.status_code == 200:
        book_data = response.json()
        
        # Check if any book was found
        if 'items' in book_data:
            book_info = book_data['items'][0]  # Get the first book result
            title = book_info['volumeInfo']['title']
            author = book_info['volumeInfo'].get('authors', ['Unknown'])[0]
            description = book_info['volumeInfo'].get('description', '')

            # Analyze the book and get music recommendations
            result = analyze_book_and_recommend_music(description)
            result['book_title'] = title
            result['book_author'] = author
            return jsonify(result)
        else:
            return jsonify({"error": "No books found for this query!"}), 404
    else:
        return jsonify({"error": "Failed to fetch data from Google Books API"}), 500

if __name__ == '__main__':
    app.run(debug=True)
