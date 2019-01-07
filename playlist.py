import youtube_dl
from video import Video


class Playlist(object):
    def __init__(self, url, name, include_video=True):
        self.url = url
        self.name = name
        self.include_video = include_video
        self.downloaded = []

    def get_videos(self, runner):
        self.playlist = runner.extract_info(self.url, download=False)
        videos = [
            Video(vid["webpage_url"], vid["artist"], vid["title"])
            for vid in self.playlist["entries"]
        ]
        return videos
