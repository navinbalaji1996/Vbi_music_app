# Vbi_music_app

Vbi_music App is an online Application which contains songs by default in which user can register an account, search songs, create playlist and add songs to the
playlist.


## Installation using Virtual Environment
* sudo add-apt-repository ppa:deadsnakes/ppa
* sudo apt-get update
* sudo apt-get install python3.6
* alias python3='/usr/bin/python3.6'
* sudo apt install python3.6-venv
* mkdir Vbi_music_app
* cd Vbi_music_app
* python3 -m venv vbi_virtual_environment
* source vbi_virtual_environment/bin/activate
* pip install -U setuptools pip
* pip3 install flask
<!__ (python3 -m pip install gevent) __>
* pip3 install gevent
<!__ (sudo apt install peewee) __>
* pip3 install peewee
* pip3 install pyjwt

## Api Table

### Notations

* ip = localhost (for testing local)
* port = 5000 (port no taken from config.json)
* uid = userid 
* token = jwt token
* song = songs to be searched(i.e "im" , "ch")
* pname = playlist_name
* pid = playlist id
* sid = song id


Purpose  |  url  | Parameters |  Json |  Headers | Method
--- | --- | --- | --- | --- | ---
Signup | http://ip:port/signup | - | {'email':email, 'password:password}  |  -  |  POST
For getting token |  http://ip:port/auth/login |  -  | {'email':email, 'password:password} | - |  POST
Get all songs | http://ip:port/get/all/songs   | - | -| {'token':token} |  GET
Songs search   | http://ip:port/search/songs  | {'song_search':song} |  -  | {'token':token} |  GET
Playlist creation | http://ip:port/create/playlist | -  | {'playlist_name':pname}  | {'token':token} |  POST
Add songs to playlist | http://ip:port/add/playlist/songs  |  -| {'playlist_id':pid, 'song_id':sid}   | {'token':token} |  POST
Get songs from specific playlist| http://ip:port/get/playlist/songs   | {'playlist_id':pid}|  - | {'token':token} |  GET
Shuffling Playlist | http://ip:port/shuffle/playlist |  - | {'playlist_id':pid}   | {'token':token} |  POST



## How to run
* Install the Virtual Environment as mentioned above
* source vbi_virtual_environment/bin/activate
* python3 vbi_music_app.py


## Note
* SongsList table will be loaded with default songs
* I didn't add virtual environment in .gitignore because if you faced any issues in installation, you can make use of this virtual environment
