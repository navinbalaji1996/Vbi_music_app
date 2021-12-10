import json
from flask import Flask, request
from gevent.pywsgi import WSGIServer
from lib.vbi_lib import VbiLib
from sqlite_database.db_connection import *
app = Flask('__name__')
vbi_lib = VbiLib()

create_database()
create_tables()
load_songs()



@app.route('/signup', methods=['POST'])
def signup():
    email = request.args.get('email')
    password = request.args.get('password')
    signup_result = vbi_lib.validate_credentials(email, password)
    print(signup_result)
    if signup_result[0]:
        create_user(email, password)
        return {'status':200, 'Message':'success'}
    else:
        return {'status':201, 'Message':signup_result[1]}



@app.route('/login', methods=['GET'])
def login():
    return "Login"


@app.route('/get/all_songs', methods=['GET'])
def list_all_songs():
    songs_list = get_all_songs()
    return {'status':200, 'message': songs_list}


@app.route('/create/playlist', methods=['POST'])
def create_playlist():
    return "Create Playlist"


@app.route('/shuffle/playlist', methods=['POST'])
def shuffle_playlist():
    return "Shuffle Playlist"


if __name__ == '__main__':
    with open('config/config.json') as config_file:
        config = json.load(config_file)
        http_port = config['port_no']
    http_server = WSGIServer(('', http_port), app)
    print('server starts on port ' + str(http_port))
    http_server.serve_forever()