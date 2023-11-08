import unittest
import requests


class Tester(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_upload(self):
        url = "http://localhost:8000/frames/upload"
        file_name = "aboba.png"
        files = {
            "upload_file": open(file_name)
        }
        data = {
            "id_rtsp": 100
        }

        response = requests.post(url=url, files=files)
        print(response)

    def test_add_service(self):
        url = "http://localhost:8000/services/add"
        data = {
            "name": "aboba"
        }
        response = requests.post(url=url, data=data)
        print(response)

    def test_add_admin(self):
        url = "http://localhost:8000/user/add"
        data = {
            "name": "aboba"
        }
        response = requests.post(url=url, data=data)
        print(response)
