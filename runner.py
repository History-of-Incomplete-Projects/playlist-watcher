import youtube_dl
from playlist import Playlist
from sched import scheduler
from time import time, sleep
from logging import Logging


class Runner(object):
    def __init__(self, youtube_dl_options, playlists, logbook_name):
        self.runner = youtube_dl.YoutubeDL(youtube_dl_options)
        self.playlists = playlists
        self.logger = Logging(logbook_name)

    def run(self, period=0):
        s = scheduler(time, sleep)
        s.enter(period, 1, self.download_playlists, ())
        while True:
            s.run()

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
