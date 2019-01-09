import youtube_dl
from playlist import Playlist
from sched import scheduler
from time import time, sleep
from logging import Logging
import json
from error import ExpectedInputPlaylistFileNotFoundError

class Runner(object):
    def __init__(self, youtube_dl_options, playlists_name, logbook_name, period=60):
        self.runner = youtube_dl.YoutubeDL(youtube_dl_options)
        self.playlists_name = playlists_name
        self.logger = Logging(logbook_name)
        self.period = period

    def run(self):
        s = scheduler(time, sleep)
        s.enter(self.period, 2, self.get_playlists, ())
        s.enter(self.period, 1, self.download_playlists, ())
        while True:
            s.run()

    def get_playlists(self):
        try:
            with open(self.playlists_name) as f:
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
