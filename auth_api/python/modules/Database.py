from os import getenv
import mysql.connector
from hashlib import sha512

class Database:
    
    def __init__(self):

        try:
            self._connection = mysql.connector.connect(
                host=getenv('HOST'), 
                database=getenv('DB_NAME'), 
                user=getenv('DB_USER'), 
                password=getenv('PASS'))
            self._cursor = self._connection.cursor()
        
        except Exception as e:
            print("Error while connecting to MySQL", e)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cursor.close()
        self._connection.close()

    def query(self, sql, params=None):
        self._cursor.execute(sql, params or ())
        return self._cursor.fetchall()

    def get_user_info(self, username):
        query_result = self.query(
            "SELECT password, salt FROM users\
            WHERE username = '{}'".format(username))
        return query_result

    def is_valid_login(self, username, password):
        
        user_record = self.get_user_info(username)
        
        if not user_record.__len__() > 0: return False
        
        stored_password, salt, = (user_record[0])
        encoded_str = (password + salt).encode()
        hashed_pass = sha512(encoded_str).hexdigest()

        return stored_password == hashed_pass

    def get_user_role(self, username):
        query_response = self.query(
            "SELECT role FROM users WHERE username = '{}'"
            .format(username))
        if not query_response.__len__() > 0:
            return False
        else:
            role, = (query_response)
            return role
