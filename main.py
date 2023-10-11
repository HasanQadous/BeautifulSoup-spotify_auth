from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

date = input("what year you would like to travel to in YYY-MM-DD format?")
year = date.split("-")[0]

spotify_id = "66246bb48e3b457c9cece27272bc1dcf"
spotify_secret = "83b3c86f5d4d4912859a4a8dd9c9ad7f"

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
web_html = response.text

soup = BeautifulSoup(web_html, "html.parser")

songs_list = [song.get_text().strip() for song in soup.select("li ul li h3")]

sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=spotify_id,
        client_secret=spotify_secret,
        show_dialog=True,
        cache_path="token.txt",
        username="Hasan Tariq"
        ))

user_id = sp.current_user()["id"]

songs_uri = []

for song in songs_list:
        result = sp.search(q=f"track:{song} year:{year}", type="track")

        try:
                uri = result["tracks"]["items"][0]["uri"]
                songs_uri.append(uri)
        except IndexError:
                print(f"{song} doesnt exist")
playlist = sp.user_playlist_create(user=user_id, name=f"{date} 100 Billboard", public="false")

sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uri)







