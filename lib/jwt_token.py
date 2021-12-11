import jwt

def get_token(email, password, secret_code='vbi#123'):
    user_dict = {'email' : email, 'password': password}
    encoded_jwt = jwt.encode(user_dict, secret_code, algorithm="HS256")
    print(encoded_jwt)
    return encoded_jwt
    

if __name__ == '__main__':
    get_token('navinbalaji1996' , 'juhubj')
    
    



