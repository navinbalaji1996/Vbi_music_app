import jwt

def get_token(email, password, secret_code):
    try:
        user_dict = {'email' : email, 'password': password}
        encoded_jwt = jwt.encode(user_dict, secret_code, algorithm="HS256")
        return encoded_jwt
    except Exception as err:
        print(err)
    

if __name__ == '__main__':
    get_token('navinbalaji1996' , 'juhubj')
    
    



