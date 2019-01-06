class Video(object):
    def __init__(self, url, artist, title):
        self.url = url
        self.artist = artist
        self.title = title

    def download(self, runner, include_video=True):
        runner.download([self.url])
