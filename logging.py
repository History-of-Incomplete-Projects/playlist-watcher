import json
from io import open
from error import MissingLogbookError

class Logging(object):
    def __init__(self):
        self.logbook_name = "logbook.json"
        self.logbook = {
            "playlists": [
            ]
        }

    def log_video(self, playlist, video):
        self.read_from_logbook()
        for logged_playlist in self.logbook["playlists"]:
            if logged_playlist["url"] == playlist.url:
                logged_playlist["downloaded_videos"].append(
                    {
                        "url": video.url,
                        "artist": video.artist,
                        "title": video.title
                    }
                )
        self.write_to_logbook()

    def load_logbook(self, playlist):
        try:
            self.read_from_logbook()
        except MissingLogbookError:
            self.write_to_logbook()
        for playlist_logged in self.logbook["playlists"]:
            if playlist.url == playlist_logged["url"]:
                logged_videos = playlist_logged["downloaded_videos"]
                return logged_videos
        self.init_playlist_log(playlist)
        return []
    
    def init_playlist_log(self, playlist):
        self.read_from_logbook()
        self.logbook["playlists"].append(
            {
                "url": playlist.url,
                "name": playlist.name,
                "include_video": playlist.include_video,
                "downloaded_videos": []
            }
        )
        self.write_to_logbook()
    
    def write_to_logbook(self):
        with open(self.logbook_name, 'w+', encoding='utf-8') as f:
            f.write(json.dumps(self.logbook, f, ensure_ascii=False, indent=4, sort_keys=True))
    
    def read_from_logbook(self):
        try:
            with open("logbook.json", encoding='utf-8') as f:
                self.logbook = json.load(f)
        except (OSError, IOError) as e:
            raise MissingLogbookError

