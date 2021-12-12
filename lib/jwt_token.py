import jwt
import time
from datetime import datetime, timedelta, timezone


def get_token(email, password, secret_code):
    try:
        dt = datetime.now(tz=timezone.utc) + timedelta(hours=2)           
        user_dict = {'email' : email, 'password': password, "exp": dt}
        encoded_jwt = jwt.encode(user_dict, secret_code, algorithm="HS256")
        return encoded_jwt
    except Exception as err:
        print(err)
   

def decode_token(token, secret_code):
    try:         
        decoded_jwt = jwt.decode(token, secret_code, algorithms="HS256")
        return 1, decoded_jwt
    except jwt.ExpiredSignatureError:
        return 0, 'Jwt Token Expired'
    except jwt.InvalidTokenError:
        return 0, 'Invalid Token'
    except Exception as err:
        print(err)


if __name__ == '__main__':
    token = get_token('navinbalaji1996@gmail.com' , 'Navin@123', "vbi#123")
    time.sleep(2)
    print(decode_token(token, 'vbi#123'))
    
    



