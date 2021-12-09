from flask import Flask
app = Flask('__name__')
from gevent.pywsgi import WSGIServer



@app.route('/get/all_songs', methods=['GET'])
def list_all_songs():
    return "all Songs"


@app.route('/create/playlist', methods=['POST'])
def create_playlist():
    return "Create Playlist"


@app.route('/shuffle/playlist', methods=['POST'])
def shuffle_playlist():
    return "Shuffle Playlist"


if __name__ == '__main__':
    http_port = "5000"
    http_server = WSGIServer(('', int(http_port)), app)
    print('server starts on port ' + http_port)
    http_server.serve_forever()