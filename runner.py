import youtube_dl
import json
from playlist import Playlist
from sched import scheduler
from time import time, sleep


class Runner(object):
    def __init__(self, youtube_dl_options):
        self.runner = youtube_dl.YoutubeDL(youtube_dl_options)
        self.playlists = []

    def run(self, period=60):
        s = scheduler(time, sleep)
        s.enter(period, 1, self.get_playlists, ())
        s.enter(period, 2, self.download_playlists, ())
        while True:
            s.run()

    def get_playlists(self):
        with open("playlists.json") as f:
            playlists = json.load(f)
            self.playlists = [
                Playlist(
                    playlist["playlist"]["url"],
                    playlist["playlist"]["name"],
                    playlist["include_video"],
                )
                for playlist in playlists["playlists"]
            ]

    def download_playlists(self):
        for playlist in self.playlists:
            videos = playlist.get_videos(self.runner)
            for video in videos:
                video.download(self.runner)
