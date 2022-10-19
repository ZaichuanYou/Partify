import spotipy
from spotipy import util
import utils
import pandas as pd

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
client = utils.getClient()
spotify = spotipy.Spotify(client_credentials_manager=client)
username = "oju0v757td6ecnvja774t086p"
scope = "playlist-read-private playlist-modify-private user-top-read"
token = utils.getToken(username, scope)

"""results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])
    
lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

spotify = spotipy.Spotify(client_credentials_manager=client)
results = spotify.artist_top_tracks(lz_uri)

for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()"""


sp = spotipy.Spotify(token)

"""playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
"""
playlists_u = sp.user_playlists(user=username)
playlists_uri = []
while playlists_u:
    for i, playlist in enumerate(playlists_u['items']):
        print("%4d %s %s" % (i + 1 + playlists_u['offset'], playlist['uri'],  playlist['name']))
        playlists_uri.append(playlist['uri'])
    if playlists_u['next']:
        playlists_u = sp.next(playlists_u)
    else:
        playlists_u = None

track = []
for a in playlists_uri:
    track.append(sp.playlist_tracks(a)['items'])

track_uri = []
for t in track:
    if not t==None:
        for a in t:
            track_uri.append(a["track"]["uri"])


song_stat = pd.DataFrame(columns=list(sp.audio_features(track_uri[0])[0].keys()))
temp = sp.audio_features(track_uri[0])[0]
print(temp)
song_stat = pd.concat([pd.DataFrame(temp, index=[0]), song_stat], axis = 0, ignore_index=True)
print(song_stat)

for uri in track_uri:
    song_stat = pd.concat([song_stat, pd.DataFrame(sp.audio_features(uri)[0], index=[0])], axis=0, ignore_index=True)

song_stat.drop('track_href', axis=1, inplace=True)
song_stat.drop('uri', axis=1, inplace=True)
song_stat.drop('id', axis=1, inplace=True)
song_stat.drop('type', axis=1, inplace=True)
song_stat.drop('analysis_url', axis=1, inplace=True)
print(song_stat)
song_stat.to_csv("data.csv")