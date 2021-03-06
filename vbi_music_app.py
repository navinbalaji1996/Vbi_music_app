import json
from flask import Flask, request
from gevent.pywsgi import WSGIServer
from lib.vbi_lib import VbiLib
from lib.jwt_token import get_token, decode_token
from lib.logger import setup_logger
from sqlite_database.db_connection import *
app = Flask('__name__')
vbi_lib = VbiLib()

create_database()
create_tables()
load_songs()

with open('config/config.json') as config_file:
    config = json.load(config_file)

debug_log = setup_logger('debug', 'debug.log')


@app.route('/signup', methods=['POST'])
def signup():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        signup_result = vbi_lib.validate_credentials(email, password)
        if signup_result[0]:
           if create_user(email, password):
               debug_log.info('User registered')
               return {'status':201, 'message':'User registered'}
           else:
               debug_log.info('Email Address already exists')
               return {'status':401, 'message':'email address already exists'}
        else:
            debug_log.info(signup_result[1])
            return {'status':400, 'message':signup_result[1]}
    except Exception as err:
        print(err)
        debug_log.error(str(err))


@app.route('/auth/login', methods=['POST'])
def get_auth_token():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        user_id = get_user_id(email, password)
        if user_id[0]:
            jwt_token = get_token(email, user_id[1], config['secret_key'])
            debug_log.info('Jwt Token generated')
            return {'status':200, 'message':jwt_token}
        else:
            debug_log.info('Invalid Credentails for getting token')
            return {'status': 401, 'message': 'Invalid User'}
    except Exception as err:
        print(err)
        debug_log.error(str(err))


@app.route('/get/all/songs', methods=['GET'])
def list_all_songs():
    try:
        token = request.headers['token']
        user = decode_token(token, config['secret_key'])
        if user[0]:
            songs_list = get_all_songs()
            debug_log.info('Fetched all songs list')
            return {'status':200, 'message': songs_list}
        else:
            debug_log.info(user[1])
            return {'status':401, 'message':user[1]}
    except Exception as err:
        print(err)
        debug_log.error(str(err))


@app.route('/search/songs', methods=['GET'])
def search_songs():
    try:
        token = request.headers['token']
        user = decode_token(token, config['secret_key'])
        if user[0]:
            selected_word = request.args.get('song_search')
            response = get_searched_songs(selected_word)
            debug_log.info('Songs search is done')
            return {'status':200, 'message':response}
        else:
            debug_log.info(user[1])
            return {'status':401, 'message':user[1]}
    except Exception as err:
        print(err)
        debug_log.error(str(err))


@app.route('/create/playlist', methods=['POST'])
def playlist_creation():
    try:
        token = request.headers['token']
        user = decode_token(token, config['secret_key'])
        if user[0]:
            playlist_name = request.json.get('playlist_name')
            if playlist_name == '':
                debug_log.info('playlist name entered is not valid')
                return {'status':400, 'message': 'Playlist Name is not Valid'}
            else:
                playlist = create_playlist(playlist_name, user[1])
                if playlist == 1:
                    debug_log.info('playlist created successfully')
                    return {'status':201, 'message': 'Playlist Created'}
                else:
                    debug_log.info('playlist already exists')
                    return {'status':401, 'message': 'Playlist already exists'}
        else:
            debug_log.info(user[1])
            return {'status':401, 'message':user[1]}
    except Exception as err:
        print(err)
        debug_log.error(str(err))


@app.route('/add/playlist/songs',  methods=['POST'])
def add_songs_to_playlist():
    try:
        token = request.headers['token']
        user = decode_token(token, config['secret_key'])
        if user[0]:
            playlist_id = request.json.get('playlist_id')
            song_id = request.json.get('song_id')
            playlist_songs = create_playlist_songs(playlist_id, user[1], song_id)
            if playlist_songs == 1:
                debug_log.info('Song is added to the playlist')
                return {'status': 201, 'message': 'Song is added to the playlist'}
            elif playlist_songs == -1:
                debug_log.info('Invalid song id or playlist id')
                return {'status': 401, 'message': 'Invalid song id or playlist id'}
            else:
                debug_log.info('Song is already added')
                return {'status': 401, 'message': 'Song is already added'}
        else:
            debug_log.info(user[1])
            return {'status':401, 'message':user[1]}
    except Exception as err:
        print(err)
        debug_log.error(str(err))


@app.route('/get/playlist/songs', methods=['GET'])
def get_playlist_songs():
    try:
        token = request.headers['token']
        user = decode_token(token, config['secret_key'])
        if user[0]:
            playlist_id = request.args.get('playlist_id')
            songs_list = get_songs_from_playlist(playlist_id, user[1])
            if songs_list[0]:
                debug_log.info('Song for playlist is fetched')
                return {'status': 200, 'message': songs_list[1]}
            else:
                return {'status':400, 'message': songs_list[1]}
        else:
            debug_log.info(user[1])
            return {'status':401, 'message':user[1]}   
    except Exception as err:
        print(err)
        debug_log.error(str(err))


@app.route('/shuffle/playlist', methods=['POST'])
def shuffle_playlist():
    try:
        token = request.headers['token']
        user = decode_token(token, config['secret_key'])
        if user[0]:
            playlist_id = request.json.get('playlist_id')
            songs_list = get_songs_from_playlist(playlist_id, user[1])
            if songs_list[0]:
                shuffled_songs = vbi_lib.get_shuffle_songs_list(songs_list[1]) 
                debug_log.info('Songs for the playlist is shuffled') 
                return {'status': 200, 'message': shuffled_songs}
            else:
                return {'status':400, 'message': songs_list[1]}
        else:
            debug_log.info(user[1])
            return {'status':401, 'message':user[1]}
    except Exception as err:
        print(err)
        debug_log.error(str(err))


if __name__ == '__main__':
    with open('config/config.json') as config_file:
        config = json.load(config_file)
        http_port = config['port_no']
    http_server = WSGIServer(('', http_port), app)
    print('server starts on port ' + str(http_port))
    http_server.serve_forever()