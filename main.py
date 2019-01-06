from __future__ import unicode_literals
from runner import Runner

ydl_opts = {
    "quiet": True,
    "outtmpl": "./youtube/%(title)s.%(ext)s"
}

if __name__ == "__main__":
    runner = Runner(ydl_opts)
    runner.run()
