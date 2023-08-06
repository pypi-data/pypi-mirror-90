import os
import json
import unittest
from unittest import mock

from imgflip.api import Client
from imgflip.utils import ResponseImage


class MockResponse:
    def __init__(self, json_data_file, status_code):
        with open(json_data_file) as json_file:
            self.json_data = json.load(json_file)
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_get_memes(*args, **kwargs):
    json_data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'utils', 'get_memes.json')
    return MockResponse(json_data_file, 200)


def mocked_caption_image(*args, **kwargs):
    json_data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'utils', 'caption_image.json')
    return MockResponse(json_data_file, 200)


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client('username', 'password', 'http://localhost/')

    @mock.patch('requests.get', side_effect=mocked_get_memes)
    def test_get_memes(self, mock_get):
        memes = self.client.get_memes()
        self.assertIsInstance(memes, list)

    @mock.patch('requests.post', side_effect=mocked_caption_image)
    def test_caption_image(self, mock_get):
        image = self.client.caption_image(id=0, text0='test', text1='test')
        self.assertIsInstance(image, ResponseImage)


if __name__ == '__main__':
    unittest.main()
