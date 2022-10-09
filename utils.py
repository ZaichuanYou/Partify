import spotipy
from spotipy import util
from spotipy.oauth2 import SpotifyClientCredentials

def getToken(username, scope):
    token = util.prompt_for_user_token(username,scope=scope,client_id='2c33c1c77b5346438eae177739954110',client_secret='5fd21bbeef534e91ab441448b96493ee', redirect_uri="http://localhost:8888/callback/")
    return token

def getClient():
    return SpotifyClientCredentials(client_id="2c33c1c77b5346438eae177739954110", client_secret="5fd21bbeef534e91ab441448b96493ee")