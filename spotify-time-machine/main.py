import requests, spotipy, pprint
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

answer = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD:")
list = []
URL = f"https://www.billboard.com/charts/hot-100/{answer}/"
response = requests.get(URL)
page_text = response.text

soup = BeautifulSoup(page_text, "html.parser")

songs_names = soup.select(".o-chart-results-list__item h3.c-title")
songs_names_updated = [song.getText().strip() for song in songs_names]
print(songs_names_updated)
print(songs_names_updated[99])


CLIENT_ID = "your ID"
CLIENT_SECRET = "your Secret"
scope = "playlist-modify-private"


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_secret=CLIENT_SECRET,
                                                                              client_id=CLIENT_ID))

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, redirect_uri="http://example.com", client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET, show_dialog=True, cache_path="token.txt"))
user_id = sp.current_user()["id"]
song_uri_list = []
year = answer.split("-")[0]
for song in songs_names_updated:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uri_list.append(uri)
    except IndexError:
        print(f"{song} - sorry, this one doesn't exist in Spotify.")

playlist = sp.user_playlist_create(user=user_id, name=f"{answer} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uri_list)