import spotipy
from spotipy import util
import utils

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
client = utils.getClient()
spotify = spotipy.Spotify(client_credentials_manager=client)
username = "oju0v757td6ecnvja774t086p"
scope = "playlist-read-private playlist-modify-private"
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
    print()
"""

sp = spotipy.Spotify(token)
"""
playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None"""

playlists_u = sp.user_playlists(user=username)
while playlists_u:
    for i, playlist in enumerate(playlists_u['items']):
        print("%4d %s %s" % (i + 1 + playlists_u['offset'], playlist['uri'],  playlist['name']))
    if playlists_u['next']:
        playlists_u = sp.next(playlists_u)
    else:
        playlists_u = None