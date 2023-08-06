from imgflip.utils import ResponseImage, get_memes, caption_image


class Client(object):
    """docstring for Client."""

    def __init__(self, username='', password='', root_url='https://api.imgflip.com/'):
        super(Client, self).__init__()
        self.username = username
        self.password = password
        self.urls = {
            'get_memes': root_url + 'get_memes',
            'caption_image': root_url + 'caption_image',
        }
        self.memes = []

    def get_memes(self, update=False):
        if len(self.memes) == 0 or update:
            self.memes = get_memes(url=self.urls['get_memes'])
        return self.memes

    def caption_image(self, id=None, index=-1, **kwargs):
        if id is None:
            if len(self.memes) == 0:
                self.get_memes()
            print(len(self.memes), index, index in range(len(self.memes)))
            if index in range(len(self.memes)):
                id = self.memes[index].get('id')

        if id is None:
            print('Error')

        text0 = kwargs.get('text0')
        text1 = kwargs.get('text1')
        data = caption_image(id, self.username, self.password, text0, text1, url=self.urls['caption_image'])
        return ResponseImage(data['data']['url'])
