import json
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


sp = utils.getAuth(token)


playlists_u = sp.user_playlists(user=username)
temp = utils.getSongInPlaylist(playlists_u['items'][0]['uri'], sp)[0]
print(temp.keys())
temp = utils.encodeJson(temp)
# Writing to sample.json
with open("test.json", "w") as outfile:
    outfile.write(temp)
#utils.getPlayerPlaylistStat(playlists_u, sp)