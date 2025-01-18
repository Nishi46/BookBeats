import requests

GOOGLE_BOOKS_API_KEY = 'AIzaSyAvkr6DdSr-0tZ362oyCMmQMdbPdnagYsg'

def get_book_info(book_title, author_name=None):
    """
    Fetches the book info (like description) from Google Books API
    based on the book title.
    """
    base_url = "https://www.googleapis.com/books/v1/volumes"
    
    query = f"intitle:{book_title}"
    if author_name:
        query += f"+inauthor:{author_name}"
    
    params = {
        "q": query,
        "key": GOOGLE_BOOKS_API_KEY,
        "maxResults": 5  
    }
    
    response = requests.get(base_url, params=params)
    
  
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        print(f"Response Text: {response.text}")
        return {"error": "Failed to fetch book information"}
    if response.status_code == 200:
        data = response.json()
        
        if 'items' in data:
            book_info = data['items'][0]['volumeInfo'] 
            title = book_info.get('title', 'N/A')
            authors = book_info.get('authors', [])
            description = book_info.get('description', 'No description available.')
            preview_link = book_info.get('previewLink', None)
            
            return {
                "title": title,
                "authors": authors,
                "description": description,
                "preview_link": preview_link
            }
        else:
            return {"error": "No books found"}
    else:
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}

def get_full_text(book_title):
    """
    Fetches the full text of the book if available (public domain books).
    """
    book_info = get_book_info(book_title)
    preview_link = book_info.get('preview_link')
    
    if preview_link:
        return preview_link
    else:
        return book_info['description']
