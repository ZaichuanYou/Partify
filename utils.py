import spotipy
from spotipy import util
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import pyqrcode
import png
from pyqrcode import QRCode
import json

def getToken(username, scope):
    token = util.prompt_for_user_token(username,scope=scope,client_id='2c33c1c77b5346438eae177739954110',client_secret='5fd21bbeef534e91ab441448b96493ee', redirect_uri="http://localhost:8888/callback/")
    return token

def getClient():
    return SpotifyClientCredentials(client_id="2c33c1c77b5346438eae177739954110", client_secret="5fd21bbeef534e91ab441448b96493ee")

def getAuth(token):
    sp = spotipy.Spotify(token)
    return sp

def getSongURIInPlaylist(playlists_uri, sp):

    track = []
    track.append(sp.playlist_tracks(playlists_uri)['items'])

    track_uri = []
    for t in track:
        if not t==None:
            for a in t:
                track_uri.append(a["track"]["uri"])
    
    return track_uri

def getSongInPlaylist(playlists_uri, sp):
    track = []
    track.append(sp.playlist_tracks(playlists_uri)['items'])

    track_data = []
    for t in track:
        if not t==None:
            for a in t:
                track_data.append(a["track"])
    
    return track_data

def getPlayerPlaylistStat(playlists, sp):
    playlists_uri = []
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
            playlists_uri.append(playlist['uri'])
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

    track_uri = []
    for a in playlists_uri:
        track_uri.append(getSongURIInPlaylist(a, sp))


    song_stat = pd.DataFrame(columns=list(sp.audio_features(track_uri[0])[0].keys()))
    temp = sp.audio_features(track_uri[0])[0]
    print(temp)
    song_stat = pd.concat([pd.DataFrame(temp, index=[0]), song_stat], axis = 0, ignore_index=True)

    for uri in track_uri:
        song_stat = pd.concat([song_stat, pd.DataFrame(sp.audio_features(uri)[0], index=[0])], axis=0, ignore_index=True)

    song_stat.drop('track_href', axis=1, inplace=True)
    song_stat.drop('uri', axis=1, inplace=True)
    song_stat.drop('id', axis=1, inplace=True)
    song_stat.drop('type', axis=1, inplace=True)
    song_stat.drop('analysis_url', axis=1, inplace=True)
    return song_stat

def createQRcode(url):
    qrCode = pyqrcode.create(url)
  
    # Create and save the svg file naming "myqr.svg"
    qrCode.svg("myqr.svg", scale = 8)
    
    # Create and save the png file naming "myqr.png"
    qrCode.png('myqr.png', scale = 6)

def encodeJson(dict):
    encoded = json.dumps(dict)
    return encoded