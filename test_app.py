from unittest import TestCase

from app import app

def mock_start_response(status, headerlist):
    pass

home_env = {
    'PATH_INFO': '/home',
    'REQUEST_METHOD': 'GET'
}

other_env = {
    'PATH_INFO': '/other',
    'REQUEST_METHOD': 'GET'
}

class TestApp(TestCase):
    def test_home_route(self):
        response = app(home_env, mock_start_response)
        self.assertIn(b'Home page', response)
    
    def test_other_route(self):
        response = app(other_env, mock_start_response)
        self.assertIn(b'Other page', response)