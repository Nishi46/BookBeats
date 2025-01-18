def recommend_songs_from_themes(book_themes, song_database):
    """Matches the themes of the book to the themes in the song database."""
    recommended_songs = []
    
    for song in song_database:
        matched_themes = set(book_themes) & set(song['themes'])
        if matched_themes:
            recommended_songs.append({
                "name": song['name'],
                "artist": song['artist'],
                "matched_themes": list(matched_themes)
            })
    
    return recommended_songs
