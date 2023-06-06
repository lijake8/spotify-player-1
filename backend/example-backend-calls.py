import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import os
from dotenv import load_dotenv

# CLIENT_ID = ''
# CLIENT_SECRET = ''
# REDIRECT_URI = 'http://localhost:8888'

# CLIENT_ID = os.environ.get('spotifyClientID')
# print('client id', CLIENT_ID)
# CLIENT_SECRET = os.environ.get('spotifyClientSecret')
# print('client secret', CLIENT_SECRET)
def configure():
    load_dotenv()

configure()

print('----------------------')
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),
                                               client_secret=os.getenv('CLIENT_SECRET'),
                                               redirect_uri=os.getenv('REDIRECT_URI'),
                                               scope="user-library-read"))

# example getting saved tracks
results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " - ", track['name'])

print('------------------------------------------------')

# example showing how to get 30 second samples and cover art for the top 10 tracks for Led Zeppelin
artist_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET')))
results = spotify.artist_top_tracks(artist_uri)

for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()
