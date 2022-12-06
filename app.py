from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import utils
import time
import spotipy
import pandas as pd
import json

app = Flask(__name__)

app.secret_key = 'secretkey'
app.config['SESSION_COOKIE_NAME'] = 'Partify Cookie'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    sp_oauth = utils.create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)

@app.route('/authorize')
def authorize():
    #return 'this is user page'
    sp_oauth = utils.create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for("getUserProfile"))

@app.route('/userPage', methods=['GET', 'POST'])
def getUserProfile():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    Auth = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    # results = sp.current_user_saved_tracks()
    # for item in results['items']:
    #     track = item['track']
    #     return(track['name'] + ' - ' + track['artists'][0]['name'])
    profile = utils.get_user_profile(Auth)
    playlists = utils.get_user_playlist(Auth)
    return render_template(
        'user.html',
        username = profile['display_name'],
        playlistNames = list(playlists.keys()),
        )

@app.route('/groupPage', methods=['GET', 'POST'])
def groupPage():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    Auth = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    if request.method == 'POST':
        inputSearch = request.form.get('newSongName')
        songs = utils.search_song(inputSearch, Auth)
        return jsonify(songs)
    else:
        playlistId = request.args['playlist']
        songsInPlaylist = utils.get_song_In_Playlist(playlistId, Auth)
        return render_template(
            'group.html',
            songsInPlaylist = songsInPlaylist
            )

@app.route('/returnSongsInPlaylist')
def getAllSongs():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    Auth = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    utils.create_user_playlist(Auth)
    utils.add_song_to_playlist(Auth, "5xwBIieMMFUmLDgvG4DjFe")
    # return utils.get_song_In_Playlist("3io6HS2WQqDybZ825bY41T", Auth)
    return 'ok'

@app.route('/createPlaylists')
def createPlaylist():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    Auth = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    utils.create_user_playlist(Auth)
    return utils.get_user_playlist(Auth)

@app.route('/playlists')
def getPlaylist():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    Auth = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    return utils.get_user_playlist(Auth)

@app.route('/getSongs')
def getSongs():
    session['token_info'], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect('/')
    Auth = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    playlistId = request.args['playlist']
    return str(utils.get_song_In_Playlist(playlistId, Auth))

# Checks to see if token is valid and gets a new token if not
def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = utils.create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    print(session.get("token_info"))
    return token_info, token_valid

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')



if __name__ == '__main__':
    app.debug = True
    app.run(port=3000, debug=True)