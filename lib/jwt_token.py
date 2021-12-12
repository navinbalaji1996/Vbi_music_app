import jwt
import time
from datetime import datetime, timedelta, timezone


def get_token(email, user_id, secret_code):
    try:
        dt = datetime.now(tz=timezone.utc) + timedelta(hours=2)           
        user_dict = {'email' : email, 'user_id': user_id, "exp": dt}
        encoded_jwt = jwt.encode(user_dict, secret_code, algorithm="HS256")
        return encoded_jwt
    except Exception as err:
        print(err)
   

def decode_token(token, secret_code):
    try:         
        decoded_jwt = jwt.decode(token, secret_code, algorithms="HS256")
        return 1, decoded_jwt['user_id']
    except jwt.ExpiredSignatureError:
        return 0, 'Jwt Token Expired'
    except jwt.InvalidTokenError:
        return 0, 'Invalid Jwt Token'
    except Exception as err:
        print(err)
    
    



