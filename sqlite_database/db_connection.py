import json
import peewee
import re
from lib.logger import setup_logger
from peewee import *


db = SqliteDatabase('sqlite_database/vbi_music_app.db', pragmas={'foreign_keys': 1})
debug_log = setup_logger('debug', 'debug.log')


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    user_id = IntegerField(primary_key=True)
    email = CharField(unique=True)
    password = CharField()


class SongsList(BaseModel):
    song_id = IntegerField(primary_key=True)
    song_name = CharField()


class PlayList(BaseModel):
    playlist_id = IntegerField(primary_key=True)
    playlist_name = CharField()
    user_id = ForeignKeyField(Users, backref='playlist')


class PlayListSongs(BaseModel):
    playlist_song_id = IntegerField(primary_key=True)
    playlist_id = ForeignKeyField(PlayList, backref='PlayListSongs')
    song_id = ForeignKeyField(SongsList, backref='PlayListSongs')
    user_id = ForeignKeyField(Users, backref='PlayListSongs')



def create_database():
    db.connect()


def create_tables():
    db.create_tables([Users, SongsList, PlayList, PlayListSongs],safe=True)


def load_songs():
    if not SongsList.select().count():
        with open('config/config.json') as config_file:
            config = json.load(config_file)
        for index, each in enumerate(config['songs_list']):
            SongsList().create(song_id = index+1, song_name=each)


def get_all_songs():
    response = []
    songs_list = SongsList.select()
    for each in songs_list:
        response.append(each.song_name)
    return response


def login_validation(email, password):
    valid_user = Users.select().where(Users.email == email,Users.password == password).count()
    if valid_user:
        return 1
    return 0


def get_searched_songs(selected_word):
    response = []
    songs_list = SongsList.select()
    for each in songs_list:
        if re.search(selected_word, each.song_name):
            response.append(each.song_name)
    return response


def create_user(email, password):
    try:
        Users().create(email=email,password=password)
        return 1
    except Exception as err:
        debug_log.error(str(err))
        return 0



def create_playlist(playlist_name, user_id):
    try:
        playlist = PlayList.select().where(PlayList.playlist_name == playlist_name,PlayList.user_id == user_id).count()
        if playlist:
            return 0
        else:
            PlayList().create(playlist_name = playlist_name, user_id = user_id)
            return 1
    except Exception as err:
        print(err)
        debug_log.error(str(err))


def create_playlist_songs(playlist_id, user_id, song_id):
    try:
        playlist_song = PlayListSongs().select().where(PlayListSongs.playlist_id == playlist_id, PlayListSongs.user_id == user_id, PlayListSongs.song_id == song_id).count()
        if playlist_song:
            return 0
        else:
            PlayListSongs().create(playlist_id = playlist_id, user_id = user_id, song_id = song_id)
            return 1
    except Exception as err:
        print(err)
        debug_log.error(str(err))
        return -1

def get_songs_from_playlist(playlist_id, user_id):
    try:
        songs = PlayListSongs().select().where(PlayListSongs.playlist_id == playlist_id, PlayListSongs.user_id == user_id)
        songs_list = []
        for each in songs:
            song = SongsList().select().where(SongsList.song_id == each)
            songs_list.append(song[0].song_name)
        return songs_list
    except Exception as err:
        print(err)
        debug_log.error(str(err))


def get_user_by_id(user_id):
    try:
        user = Users.select().where(Users.user_id == user_id)
        if user.count():
            return 1, (user[0].email, user[0].password)
        else:
            return 0, ''
    except Exception as err:
        print(err)
        debug_log.error(str(err))



if __name__ == '__main__':
    create_database()
    create_tables()
    load_songs()
    load_users()

