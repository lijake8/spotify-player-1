from flask import Flask, request, jsonify, session, redirect
from flask_cors import CORS
import os
from flask_session import Session
import spotipy
from dotenv import load_dotenv
import random

#In[0]: allow api keys to be pulled from .env file
def configure():
    load_dotenv()

configure()

#In[1]: set up flask app and session
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64) #sets the secret key for the Flask application. The secret key is used to encrypt session cookies and other sensitive data
app.config['SESSION_TYPE'] = 'filesystem' #sets the session type for the Flask application to be stored on the file system. By default, Flask uses a client-side session, but here it is configured to use server-side sessions stored on the file system. https://stackoverflow.com/questions/68902836/what-is-the-difference-between-client-side-based-sessions-and-server-side-sessio
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

CORS(app)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

SCOPES_LIST = ['user-read-currently-playing', 'playlist-modify-private']
SCOPES_STR = ' '.join(SCOPES_LIST)
SCOPES_URL = '+'.join(SCOPES_LIST)

auth_code = ''
auth_manager = None
cache_handler = None


def mocked_get_from_spotify():
    return {
        'mocked_data': {
            'name': 'jake',
            'age': 21,
            'major': ['computer science', 'business'],
            'example spotify data': True
        }
    }

@app.route("/api/mocked", methods=['GET'])
def mocked():
    third_party_data = mocked_get_from_spotify()
    return third_party_data

@app.route("/api/logininfo", methods=['GET'])
def logininfo():
    # #store the token info in the session framework provided by flask; then create a SpotifyOAuth object
    # cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session) 
    # auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID, 
    #                                            client_secret=CLIENT_SECRET, 
    #                                            redirect_uri=REDIRECT_URI,
    #                                            scope=SCOPES_STR,
    #                                            cache_handler=cache_handler,
    #                                            show_dialog=True)

    # logged_in = False
    # auth_url = None

    # if request.args.get("code"): #access parameter '?code=' in the URL
    #     # Step 2. Being redirected from Spotify auth page
    #     print('GETTING ACCESS TOKEN GIVEN CODE!!!!!!')
    #     auth_manager.get_access_token(request.args.get("code"))
    #     logged_in = True

    # elif not auth_manager.validate_token(cache_handler.get_cached_token()): #elif???
    #     # Step 1. Display spotify sign in link when no token
    #     # auth_url = auth_manager.get_authorize_url()
    #     # https://accounts.spotify.com/authorize?client_id=9688e06282ff4043a95d46dee1f7467d&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A5000&scope=user-read-currently-playing+playlist-modify-private&show_dialog=True
    #     # https://accounts.spotify.com/authorize?client_id=9688e06282ff4043a95d46dee1f7467d&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fplayer&scope=user-read-currently-playing+playlist-modify-private&show_dialog=True
        
    #     server_redirect_uri = 'http://localhost:3000/player'
    #     #convert server_redirect_uri to url string
    #     server_redirect_uri = server_redirect_uri.replace(':', '%3A')
    #     server_redirect_uri = server_redirect_uri.replace('/', '%2F')

    #     auth_url = f'https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={server_redirect_uri}&scope={SCOPES_URL}&show_dialog=True'
    #     logged_in = False





    server_redirect_uri = 'http://localhost:3000/player'
    #convert server_redirect_uri to url string
    server_redirect_uri = server_redirect_uri.replace(':', '%3A')
    server_redirect_uri = server_redirect_uri.replace('/', '%2F')

    auth_url = f'https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={server_redirect_uri}&scope={SCOPES_URL}&show_dialog=True'
    logged_in = False





    return {
        'logged_in': logged_in,
        'auth_url': auth_url
    }


@app.route('/api/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    # Process the received data
    auth_code = data['authCode']
    print('received auth code', auth_code)

    # #store the token info in the session framework provided by flask; then create a SpotifyOAuth object
    # cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session) 
    # print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    # auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID, 
    #                                            client_secret=CLIENT_SECRET, 
    #                                            redirect_uri=REDIRECT_URI,
    #                                            scope=SCOPES_STR,
    #                                            cache_handler=cache_handler,
    #                                            show_dialog=True)
    
    # print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
    # # use auth code to get access tokenif request.args.get("code"):
    # if request.args.get("code"):
    #     auth_manager.get_access_token(auth_code)
    #     return redirect('/api/')
    return 'data received'

@app.route('/api')
def index():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session) 
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID, 
                                               client_secret=CLIENT_SECRET, 
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPES_STR,
                                               cache_handler=cache_handler,
                                               show_dialog=True)
    
    auth_manager.get_access_token(auth_code)
    
    # Step 3. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    print('me', spotify.me()["display_name"])

    return {
        'name': spotify.me()["display_name"]
    }


@app.route('/api/random-number')
def generate_random_number():
    # Generate a random number
    random_number = random.randint(1, 100)

    # Return the random number as a JSON response
    return {
        'number': random_number
    }
    



if __name__ == "__main__":
    app.run(debug=True)