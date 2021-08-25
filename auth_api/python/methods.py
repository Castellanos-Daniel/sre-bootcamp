from os import getenv
from modules.Database import Database
import jwt
# These functions need to be implemented


class Token:

    def generate_token(self, username, password):

        with Database() as db:
            isLogged = db.is_valid_login(username, password)

        if isLogged:
            with Database() as db:
                role = db.get_user_role(username)

            token = jwt.encode({"role": role}, getenv('SECRET'))

            response = token
        else:
            response = False

        return response


class Restricted:

    def access_data(self, authorization):
        try:
            jwt.decode(authorization, getenv('SECRET'), algorithms='HS256')
            return "You are under protected data"
        except Exception as e:
            print(e)
            return False
        # return authorization
