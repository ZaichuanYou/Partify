from flask import url_for
import spotipy
from spotipy import util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import pyqrcode
from pyqrcode import QRCode
import json
import numpy as np
from Tianyi import rediction_classifier

def getToken(username, scope):
    token = util.prompt_for_user_token(username,scope=scope,client_id='2c33c1c77b5346438eae177739954110',client_secret='5fd21bbeef534e91ab441448b96493ee', redirect_uri="http://localhost:8888/callback/")
    return token

def getClient():
    return SpotifyClientCredentials(client_id="2c33c1c77b5346438eae177739954110", client_secret="5fd21bbeef534e91ab441448b96493ee")

def create_spotify_oauth():
    return SpotifyOAuth(
            client_id="2c33c1c77b5346438eae177739954110",
            client_secret="5fd21bbeef534e91ab441448b96493ee",
            redirect_uri=url_for('authorize', _external=True),
            # scope="user-library-read"
            scope="user-library-read playlist-read-private playlist-modify-private playlist-modify-public user-read-private user-read-email")
    

def getAuth(token):
    Auth = spotipy.Spotify(token)
    return Auth

def get_SongURI_In_Playlist(playlists_uri, Auth):

    track = []
    track.append(Auth.playlist_tracks(playlists_uri)['items'])

    track_uri = []
    for t in track:
        if not t==None:
            for a in t:
                track_uri.append(a["track"]["uri"])
    
    return track_uri

def get_song_In_Playlist(playlists_uri, Auth):
    track = []
    track.append(Auth.playlist_tracks(playlists_uri)['items'])

    track_data = []
    for t in track:
        if not t==None:
            for a in t:
                track_data.append(a["track"])
    
    return track_data

def get_user_playlist(Auth):
    playlists_u = Auth.user_playlists(user=get_user_id(Auth))
    result = {}
    for playlist in playlists_u['items']:
        temp_dict = {}
        temp_dict['images'] = playlist['images']
        temp_dict['description'] = playlist['description']
        temp_dict['id'] = playlist['id']
        result[playlist['name']] = temp_dict
    
    return result

def get_songid_by_name(Auth, name):
    playlist_id = ""
    playlists_u = Auth.user_playlists(user=get_user_id(Auth))['items']
    for playlist in playlists_u:
        if playlist["name"] == "Partify":
            playlist_id = playlist["id"]
    songs = get_song_In_Playlist(playlist_id, Auth)
    song_id = ""
    for song in songs:
        if song["name"] == name:
            song_id = song["id"]
    
    return song_id

def get_user_playlist_stat(playlists, Auth):
    playlists_uri = []
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
            playlists_uri.append(playlist['uri'])
        if playlists['next']:
            playlists = Auth.next(playlists)
        else:
            playlists = None

    track_uri = []
    for a in playlists_uri:
        track_uri.append(get_SongURI_In_Playlist(a, Auth))
    track_uri = np.array(track_uri)


    stats = []

    for uri in track_uri:
        song_stat = pd.DataFrame(columns=list(Auth.audio_features(uri)[0].keys()))
        temp = Auth.audio_features(uri[0])[0]
        song_stat = pd.concat([pd.DataFrame(temp, index=[0]), song_stat], axis = 0, ignore_index=True)
        for song in uri:
            song_stat = pd.concat([song_stat, pd.DataFrame(Auth.audio_features(song)[0], index=[0])], axis=0, ignore_index=True)
        stats.append(song_stat)


    for song_stat in stats:
        song_stat.drop('track_href', axis=1, inplace=True)
        song_stat.drop('id', axis=1, inplace=True)
        song_stat.drop('type', axis=1, inplace=True)
        song_stat.drop('analysis_url', axis=1, inplace=True)

    return np.array(stats)


def drop_Feature(song_Feature):
    new_stat = {}
    new_stat['cover_art'] = song_Feature['album']['images']
    new_stat['artists'] = song_Feature['artists']
    new_stat['preview'] = song_Feature['preview_url']
    new_stat['name'] = song_Feature['name']
    new_stat['id'] = song_Feature['id']
    new_stat['album_name'] = song_Feature['album']['name']
    return new_stat

def search_song(song_name, auth):
    result = auth.search(q=song_name, type="track", limit=10)['tracks']['items']
    result_list = []
    for song in result:
        result_list.append(drop_Feature(song))
    return result_list

def add_song_to_playlist(Auth, song_id):
    playlist_id = ""
    playlists_u = Auth.user_playlists(user=get_user_id(Auth))['items']
    for playlist in playlists_u:
        if playlist["name"] == "Partify":
            playlist_id = playlist["id"]
    Auth.user_playlist_add_tracks(get_user_id(Auth), playlist_id, [song_id])

def remove_song_from_playlist(Auth, song_id):
    playlist_id = ""
    playlists_u = Auth.user_playlists(user=get_user_id(Auth))['items']
    for playlist in playlists_u:
        if playlist["name"] == "Partify":
            playlist_id = playlist["id"]
    Auth.user_playlist_remove_all_occurrences_of_tracks(get_user_id(Auth), playlist_id, [song_id])

def get_user_id(Auth):
    """
    Get id of user which can be use as the only identification of user
    """
    return Auth.current_user()["id"]

def get_user_profile(Auth):
    """
    Example output: {'country': 'US', 'display_name': 'oju0v757td6ecnvja774t086p', 
    'email': 'zxy456@case.edu', 'explicit_content': {'filter_enabled': False, 'filter_locked': False}, 
    'external_urls': {'spotify': 'https://open.spotify.com/user/oju0v757td6ecnvja774t086p'}, 
    'followers': {'href': None, 'total': 0}, 'href': 'https://api.spotify.com/v1/users/oju0v757td6ecnvja774t086p', 
    'id': 'oju0v757td6ecnvja774t086p', 'images': [], 'product': 'premium', 'type': 'user', 
    'uri': 'spotify:user:oju0v757td6ecnvja774t086p'}
    """
    profile = Auth.current_user()
    return profile

def create_user_playlist(Auth):
    Auth.user_playlist_create(get_user_id(Auth), "Partify", public=True, description="Playlist for the party!")

def delete_user_playlist(Auth):
    playlist_id = ""
    playlists_u = Auth.user_playlists(user=get_user_id(Auth))['items']
    for playlist in playlists_u:
        if playlist["name"] == "Partify":
            playlist_id = playlist["id"]
    Auth.user_playlist_unfollow(get_user_id(Auth), playlist_id)

def recommend(Auth):
    """
    Return a list of songs
    """
    recomend_machine = rediction_classifier()
    playlists_u = Auth.user_playlists(user=get_user_id(Auth))
    stat = get_user_playlist_stat(playlists_u, Auth)


    try:
        recomend_machine.classifier_selection(stat[:-2])
        uris = recomend_machine.predict(stat[-1], stat, 5)
    except:
        uris=[]
        for list in stat[1:]:
            for uri in list["uri"]:
                if not uri in uris and len(uris)<6:
                    uris.append(uri)
        print(uris)
    result = Auth.tracks(uris)["tracks"]
    result_list = []
    for track in result:
        result_list.append(drop_Feature(track))
    return result_list

def get_song(Auth, id):
    result = Auth.track(id)
    return drop_Feature(result)

def get_partify(Auth):
    playlist_id = ""
    playlists_u = Auth.user_playlists(user=get_user_id(Auth))['items']
    for playlist in playlists_u:
        if playlist["name"] == "Partify":
            playlist_id = playlist["id"]
    return playlist_id

def user_follow(Auth, playlist_id):
    Auth.user_playlist_follow_playlist(get_user_id(Auth, playlist_id))

def createQRcode(url):
    qrCode = pyqrcode.create(url)
    qrCode.png("Partify.png")

def encodeJson(dict):
    encoded = json.dumps(dict)
    return encoded
