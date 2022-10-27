import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config

# spotipy authentication
client_id = config.client_id
client_secret = config.client_secret
redirect_url = 'http://example.com'
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth
    (client_id=client_id,
     client_secret=client_secret,
     redirect_uri='http://example.com',
     scope="playlist-modify-private",
     show_dialog=True,
     cache_path='token.txt'))
user_id = sp.current_user()["id"]

# scraping billboard
user_input = input('Which Year do you want travel to? Type date in this format YYYY-MM-DD: ')
bill_board_url = f' https://www.billboard.com/charts/hot-100/{user_input}'
response = requests.get(url=bill_board_url)
bill_board_webpage = response.text

soup = BeautifulSoup(bill_board_webpage, 'html.parser')
all_songs = soup.find_all(name="h3", id="title-of-a-story", class_="u-line-height-125")
song_titles = [song.get_text().strip() for song in all_songs]

song_uris = []
year = user_input.split("-")[0]

# searching for songs to extract their uri
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")

    try:
        song_uri = result["tracks"]["items"][0]["uri"]
        song_name = result["tracks"]["items"][0]["name"]
        song_uris.append(song_uri)

    except IndexError:
        print(f'{song} is not available')

# creating a playlist
new_playlists = sp.user_playlist_create(user_id,
                                        f'Time Machine {user_input}',
                                        public=False,
                                        description=f'Best of {user_input}')
playlist_id = new_playlists['id']

all_playlist = sp.playlist_add_items(playlist_id, song_uris)
print(new_playlists)
