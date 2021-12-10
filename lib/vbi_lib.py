import re

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
        elif not any(map(str.islower, password)):
            return 0, 'Password must contain atleast one lower character'
        elif not any(map(str.isupper, password)):
            return 0, 'Password must contain atleast one upper character'
        elif not any(map(str.isdigit, password)):
            return 0, 'Password must contain atleast one Number'
        elif self.spl_char_pattern.search(password) == None:
            return 0, 'Password must contain atleast one Special character'
        return 1, 'Verified'


if __name__ == '__main__':
    vbi = VbiLib()
    print(vbi.validate_credentials('navinbalaji1996@gmail.com', 'NAVINBALA1@'))