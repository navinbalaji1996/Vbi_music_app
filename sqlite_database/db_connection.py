import json
import peewee
from peewee import *


db = SqliteDatabase('sqlite_database/vbi_music_app.db')


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    email = CharField(primary_key=True)
    password = CharField()


class PlayList(BaseModel):
    playlist_id = IntegerField()
    playlist_name = CharField()


class SongsList(BaseModel):
    song_id = IntegerField(primary_key=True)
    song_name = CharField()


def create_database():
    db.connect()


def create_tables():
    db.create_tables([Users, PlayList,SongsList],safe=True)


def load_songs():
    if not SongsList.select().count():
        with open('config/config.json') as config_file:
            config = json.load(config_file)
        for index, each in enumerate(config['songs_list']):
            SongsList().create(song_id = index+1, song_name=each)


'''def load_users():
    for i in range(1,11):
        try:
            a= Users().create(username='navin', password='password' + str(i))
            print(a)
        except Exception as err:
            print(err)'''

def get_all_songs():
    response = []
    songs_list = SongsList.select()
    for each in songs_list:
        response.append(each.song_name)
    print(response)
    return response


def create_user(email, password):
    Users().create(email=email,password=password)


if __name__ == '__main__':
    create_database()
    create_tables()
    load_songs()
    load_users()

