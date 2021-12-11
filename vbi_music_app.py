import json
from flask import Flask, request
from gevent.pywsgi import WSGIServer
from lib.vbi_lib import VbiLib
from lib.jwt_token import get_token
from sqlite_database.db_connection import *
app = Flask('__name__')
vbi_lib = VbiLib()

create_database()
create_tables()
load_songs()


@app.route('/signup', methods=['POST'])
def signup():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        signup_result = vbi_lib.validate_credentials(email, password)
        if signup_result[0]:
           if create_user(email, password):
               return {'status':201, 'message':'User registered'}
           else:
               return {'status':401, 'message':'email address already exists'}
        else:
           return {'status':400, 'message':signup_result[1]}
    except Exception as err:
        print(err)


@app.route('/auth/login', methods=['POST'])
def get_auth_token():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        valid_user = login_validation(email, password)
        if valid_user:
            jwt_token = get_token(email, password)
            return {'status':200, 'message':jwt_token}
        else:
            return {'status': 401, 'message': 'Invalid User'}
    except Exception as err:
        print(err)


@app.route('/get/all_songs', methods=['GET'])
def list_all_songs():
    try:
        token = request.headers['token']
        user_id = request.args.get('user_id')
        user = vbi_lib.token_validation(user_id, token)
        if user[0]:
            songs_list = get_all_songs()
            return {'status':200, 'message': songs_list}
        else:
            return user[1]
    except Exception as err:
        print(err)


@app.route('/search/songs', methods=['GET'])
def search_songs():
    try:
        token = request.headers['token']
        user_id = request.args.get('user_id')
        user = vbi_lib.token_validation(user_id, token)
        if user[0]:
            selected_word = request.args.get('song_search')
            response = get_searched_songs(selected_word)
            return {'status':200, 'message':response}
        else:
            return user[1]
    except Exception as err:
        print(err)


@app.route('/create/playlist', methods=['POST'])
def playlist_creation():
    try:
        token = request.headers['token']
        user_id = request.json.get('user_id')
        user = vbi_lib.token_validation(user_id, token)
        if user[0]:
            playlist_name = request.json.get('playlist_name')
            if playlist_name == '':
                return {'status':400, 'message': 'Playlist Name is not Valid'}
            else:
                playlist = create_playlist(playlist_name, user_id)
                if playlist == 1:
                    return {'status':201, 'message': 'Playlist Created'}
                else:
                    return {'status':401, 'message': 'Playlist already exists'}
        else:
            return user[1]
    except Exception as err:
        print(err)


@app.route('/add/playlist/songs',  methods=['POST'])
def add_songs_to_playlist():
    try:
        token = request.headers['token']
        user_id = request.json.get('user_id')
        user = vbi_lib.token_validation(user_id, token)
        if user[0]:
            playlist_id = request.json.get('playlist_id')
            song_id = request.json.get('song_id')
            playlist_songs = create_playlist_songs(playlist_id, user_id, song_id)
            if playlist_songs == 1:
                return {'status': 201, 'message': 'Song is added to the playlist'}
            elif playlist_songs == -1:
                return {'status': 401, 'message': 'Invalid song id or playlist id'}
            else:
                return {'status': 401, 'message': 'Song is already added'}
        else:
            return user[1]
    except Exception as err:
        print(err)


@app.route('/get/playlist/songs', methods=['GET'])
def get_playlist_songs():
    try:
        token = request.headers['token']
        user_id = request.args.get('user_id')
        user = vbi_lib.token_validation(user_id, token)
        if user[0]:
            playlist_id = request.args.get('playlist_id')
            songs_list = get_songs_from_playlist(playlist_id, user_id)  
            return {'status': 200, 'message': songs_list}
        else:
            return user[1]   
    except Exception as err:
        print(err)


@app.route('/shuffle/playlist', methods=['POST'])
def shuffle_playlist():
    try:
        token = request.headers['token']
        user_id = request.json.get('user_id')
        user = vbi_lib.token_validation(user_id, token)
        if user[0]:
            playlist_id = request.json.get('playlist_id')
            songs_list = get_songs_from_playlist(playlist_id, user_id)
            shuffled_songs = vbi_lib.get_shuffle_songs_list(songs_list)  
            return {'status': 200, 'message': shuffled_songs}
        else:
            return user[1]
    except Exception as err:
        print(err)


if __name__ == '__main__':
    with open('config/config.json') as config_file:
        config = json.load(config_file)
        http_port = config['port_no']
    http_server = WSGIServer(('', http_port), app)
    print('server starts on port ' + str(http_port))
    http_server.serve_forever()