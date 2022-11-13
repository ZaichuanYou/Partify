import json
import spotipy
from spotipy import util
import utils
import pandas as pd

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
client = utils.getClient()
spotify = spotipy.Spotify(client_credentials_manager=client)
username = "oju0v757td6ecnvja774t086p"
scope = "playlist-read-private playlist-modify-private playlist-modify-public user-read-private user-read-email"
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


sp = utils.getAuth(token)
#print(utils.search_song("Dream", spotify))

playlists_u = sp.user_playlists(user=username)
print(utils.get_user_playlist(sp))

temp = utils.encodeJson(temp)
# Writing to sample.json
with open("test.json", "w") as outfile:
    outfile.write(temp)
utils.getPlayerPlaylistStat(playlists_u, sp)"""

sp = utils.getAuth(token)
#utils.create_user_playlist(sp)
#utils.delete_user_playlist(sp)
playlist_id = ""
playlists_u = sp.user_playlists(user=utils.get_user_id(sp))['items']
for playlist in playlists_u:
    if playlist["name"] == "Partify":
        playlist_id = playlist["id"]
song_id = utils.search_song("dream", sp)[0]['id']
print(song_id)
#utils.add_song_to_playlist(sp, song_id)
songs = utils.get_song_In_Playlist(playlist_id, sp)
song_id = utils.get_songid_by_name(sp, "Dream On")
utils.remove_song_from_playlist(sp, song_id)