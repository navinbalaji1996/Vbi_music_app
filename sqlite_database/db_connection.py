import peewee
from peewee import *


db = SqliteDatabase('vbi_music_app.db')


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
	username = CharField(primary_key=True)
	password = CharField()


class PlayList(BaseModel):
	playlist_id = IntegerField()
	playlist_name = CharField()


class SongsList(BaseModel):
	song_id = IntegerField()
	song_name = CharField()


def create_database():
	db.connect()


def create_tables():
	db.create_tables([Users, PlayList,SongsList],safe=True)


def load_songs():
	for i in range(1, 11):
		SongsList().create(song_id = i, song_name = 'Song' + str(i))

def load_users():
	for i in range(1,11):
		try:
		    a= Users().create(username='navin', password='password' + str(i))
		    print(a)
		except Exception as err:
			print(err)

def create_user():
	pass


if __name__ == '__main__':
	create_database()
	create_tables()
	load_songs()
	load_users()

