import re
from random import choice
from sqlite_database.db_connection import *
from .jwt_token import get_token

class VbiLib:


    def __init__(self):
        self.spl_char_pattern = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        self.email_pattern = re.compile('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}')


    def validate_credentials(self, email, password):
        if email == '': 
            return 0, 'email cannot be empty'
        elif not self.email_pattern.match(email):
            return 0, 'email address is not valid'
        elif len(password) < 8:
            return 0, 'Password must contain atleast 8 characters'
        elif not password[0].isalpha():
            return 0, 'Password should starts with Alphabet'
        elif not any(map(str.islower, password)):
            return 0, 'Password must contain atleast one lower character'
        elif not any(map(str.isupper, password)):
            return 0, 'Password must contain atleast one upper character'
        elif not any(map(str.isdigit, password)):
            return 0, 'Password must contain atleast one Number'
        elif self.spl_char_pattern.search(password) == None:
            return 0, 'Password must contain atleast one Special character'
        return 1, 'Verified'

    def token_validation(self, user_id, secret_key, token):
        user_details = get_user_by_id(user_id)
        if user_details[0]:
            generated_token = get_token(user_details[1][0], user_details[1][1], secret_key)
            if token == generated_token:
                return 1,''
            else:
                return 0, {'status':401, 'message':'Access token is denied'}
        else:
            return 0, {'status':400, 'message':'Invalid User id'}

    def get_shuffle_songs_list(self, songs_list):
        shuffled_list = []
        for i in range(len(songs_list)):
            ran = choice([each for each in songs_list if each not in shuffled_list])
            shuffled_list.append(ran)
        return shuffled_list


if __name__ == '__main__':
    vbi = VbiLib()
    print(vbi.get_shuffle_songs_list([1,2,3]))