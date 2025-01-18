import os
import base64
import requests

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

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
        return None
    
    return access_token

SPOTIFY_ACCESS_TOKEN = get_spotify_access_token()

def search_songs(theme):
    """
    Searches Spotify for songs based on the given theme (or keyword).
    """
    if not SPOTIFY_ACCESS_TOKEN:
        print("Error: No Spotify access token available.")
        return []
    
    url = f"https://api.spotify.com/v1/search?q={theme}&type=track&limit=10"
    headers = {
        "Authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Failed to fetch songs: {response.status_code} - {response.text}")
        return []
    
    tracks = response.json().get("tracks", {}).get("items", [])
    songs = []
    
    for track in tracks:
        songs.append({
            "name": track['name'],
            "artist": track['artists'][0]['name'],
            "url": track['external_urls']['spotify']
        })
    
    return songs
