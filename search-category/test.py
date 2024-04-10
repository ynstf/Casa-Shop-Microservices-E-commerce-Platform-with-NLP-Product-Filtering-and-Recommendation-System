import unittest
from server import app

class TestServer(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_server_runs(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome", response.data) 

if __name__ == '__main__':
    unittest.main()
