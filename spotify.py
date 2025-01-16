import requests
from app import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import base64
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


def get_spotify_recommendations(mood):
    access_token = get_spotify_access_token()
    
    mood_string = " ".join(mood)
    url = f"https://api.spotify.com/v1/recommendations?seed_genres={mood_string}&limit=10"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        recommendations = response.json()
        songs = [
            {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "url": track["external_urls"]["spotify"]
            }
            for track in recommendations["tracks"]
        ]
        return songs
    else:
        return None