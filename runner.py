import youtube_dl
import json
from playlist import Playlist
from sched import scheduler
from time import time, sleep
from logging import Logging
from error import ExpectedInputPlaylistFileNotFoundError

class Runner(object):
    def __init__(self, youtube_dl_options):
        self.runner = youtube_dl.YoutubeDL(youtube_dl_options)
        self.playlists = []
        self.logger = Logging()

    def run(self, period=0):
        s = scheduler(time, sleep)
        s.enter(period, 1, self.get_playlists, ())
        s.enter(period, 2, self.download_playlists, ())
        while True:
            s.run()

    def get_playlists(self):
        try:
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
        except (OSError, IOError) as e:
            raise ExpectedInputPlaylistFileNotFoundError

    def download_playlists(self):
        for playlist in self.playlists:
            downloaded_videos = self.logger.load_logbook(playlist)
            videos = playlist.get_videos(self.runner)
            for video in videos:
                downloaded = False
                for downloaded_video in downloaded_videos:
                    if downloaded_video["url"] == video.url:
                        downloaded = True
                        break
                if not downloaded:
                    video.download(self.runner)
                    self.logger.log_video(playlist, video)

    