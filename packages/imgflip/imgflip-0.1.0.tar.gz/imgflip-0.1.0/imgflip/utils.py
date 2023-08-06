import webbrowser
import requests


class ResponseImage(object):
    """docstring for ."""

    def __init__(self, url):
        super(ResponseImage, self).__init__()
        self.url = url

    def webbrowser(self):
        webbrowser.open(self.url, new=2)

    def save(self):
        pass


def get_memes(url='https://api.imgflip.com/get_memes'):
    r = requests.get(url)
    data = r.json()
    return data['data']['memes']


def caption_image(template_id, username, password, text0, text1, url='https://api.imgflip.com/caption_image'):
    data = {
        'template_id': template_id,
        'username': username,
        'password': password,
        'text0': text0,
        'text1': text1,
    }
    r = requests.post(url, data=data)
    return r.json()
