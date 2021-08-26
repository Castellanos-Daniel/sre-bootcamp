import unittest
from methods import Token, Restricted
from dotenv import load_dotenv, find_dotenv


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.convert = Token()
        self.validate = Restricted()
        load_dotenv(find_dotenv())
        self.test_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiYWRtaW4ifQ.BmcZ8aB5j8wLSK8CqdDwkGxZfFwM1X1gfAIN7cXOx9w'

    def test_generate_token(self):
        self.assertEqual(self.test_token,
                         self.convert.generate_token('admin', 'secret'))

    def test_generate_token_failsafe(self):
        self.assertEqual(False,
                         self.convert.generate_token('fake_user', 'incorrect_pass'))

    def test_access_data(self):
        self.assertEqual('You are under protected data',
                         self.validate.access_data(self.test_token))

    def test_access_data_failsafe(self):
        self.assertEqual(False,
                         self.validate.access_data('falseToken'))


if __name__ == '__main__':
    unittest.main()
