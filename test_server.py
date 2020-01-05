from unittest import TestCase
from server import Server


def mock_start_response(status, headerlist):
    pass


class TestServer(TestCase):
    def setUp(self):
        self.server = Server()
        self.mock_start_response = mock_start_response
        self.empty_mock_env = {
            'PATH_INFO': '',
            'REQUEST_METHOD': 'GET'
        }
        self.mock_env = {
            'PATH_INFO': 'mock',
            'REQUEST_METHOD': 'GET'
        }

    def test_call_with_no_route(self):
        res = self.server(self.empty_mock_env, self.mock_start_response)
        self.assertIn(b'Route not found.', res)

    def test_call_with_route(self):
        @self.server.route('mock')
        def mock(req, res):  # pylint: disable=unused-variable
            res.text = 'mock route'

        response = self.server(self.mock_env, self.mock_start_response)
        self.assertIn(b'mock route', response)
