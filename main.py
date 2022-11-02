import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    billboard_year = input("what year you would like to travel to in YYYY-MM-DD format:")
    URL = f"https://www.billboard.com/charts/hot-100/{billboard_year}"
    res = requests.get(URL)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    gallery_data = soup.findAll(name="li", class_="o-chart-results-list__item")
    songs_list = []
    for gallery in gallery_data:
        song_data = gallery.find(name="h3", id="title-of-a-story")
        if song_data is not None:
            songs_list.append(song_data.string.strip())
    scope = "playlist-modify-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    playlist_name = f"{billboard_year} top billboard songs"
    playlist = sp.user_playlist_create(name=playlist_name, user=sp.current_user()["id"] ,public=False)
    songs_uri = []
    for song in songs_list:
        song_uri = sp.search(q=song, limit=1, type='track')['tracks']['items'][0]['uri']
        songs_uri.append(song_uri)
    sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uri)
