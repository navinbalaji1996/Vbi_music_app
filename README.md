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


 Purpose        |  url                           | Parameters        |  Json                |   Headers       | Method  |   Response
______________  |________________________________|___________________|______________________|_________________|_________|______________________________
  Signup        |  http://ip:port/signup         |      -            | {'email':email,      |        -        |  POST   |   {'status' : status_code,   
                |                                |                   |   'password:password}|                 |         |     'message' : return msg}  
________________|________________________________|___________________|______________________|_________________|_________|______________________________
 For getting    |  http://ip:port/auth/login     |      -            | {'email':email,      |        -        |  POST   |   {'status' : status_code,   
    token       |                                |                   | 'password:password}  |                 |         |   'message' : return msg}    
________________|________________________________|___________________|______________________|_________________|_________|______________________________
 Get all songs  | http://ip:port/get/all/songs   | {'user_id' : uid} |        -             | {'token':token} |  GET    |   {'status' : status_code,   
                |                                |                   |                      |                 |         |   'message' : return msg}    
________________|________________________________|___________________|______________________|_________________|_________|______________________________
 Songs search   | http://ip:port/search/songs    | {'user_id' : uid, |         -            | {'token':token} |  GET    |   {'status' : status_code,   
                |                                |  'song_search':   |                      |                 |         |    'message' : return msg}  
                |                                |       song}       |                      |                 |         |                              
________________|________________________________|___________________|______________________|_________________|_________|______________________________
   Playlist     | http://ip:port/create/playlist |      -            | {'user_id' : uid,    | {'token':token} |  POST   |   {'status' : status_code,   
   creation     |                                |                   |  'playlist_name':    |                 |         |     'message' : return msg}  
                |                                |                   |      pname           |                 |         |                             
________________|________________________________|___________________|______________________|_________________|_________|______________________________
  Add songs to  | http://ip:port/add/playlist/   |       -           | {'user_id' : uid,    | {'token':token} |  POST   |    {'status' : status_code,  
    playlist    |                       songs    |                   |  'playlist_id':pid,  |                 |         |     'message' : return msg} |               |                                |                   |   'song_id': sid}    |                 |         | 
________________|________________________________|___________________|______________________|_________________|_________|______________________________
 Get songs from | http://ip:port/get/playlist/   | {'user_id' : uid, |         -            | {'token':token} |  GET    |    {'status' : status_code,  
   specific     |                        songs   | 'playlist_id':pid}|                      |                 |         |    'message' : return msg}   
   playlist     |                                |                   |                      |                 |         |                              
________________|________________________________|___________________|______________________|_________________|_________|______________________________
    Shuffling   | http://ip:port/shuffle/playlist|       -           | {'user_id' : uid,    | {'token':token} |  POST   |   {'status' : status_code,   
     Playlist   |                                |                   | 'playlist_id':pid}   |                 |         |    'message' : return msg}   


