from __future__ import unicode_literals
from urllib.parse import urlparse       # Get parameter from url

import moviepy.editor as mp             # Used to convert movie to mp3 and cut to right frame
import youtube_dl
import os


class MyLogger(object):
    def debug(self, msg):
        print("dbg: " + msg)

    def warning(self, msg):
        pass
        # print("warning: " + msg)

    def error(self, msg):
        print("error: " + msg)


def my_hook(d):
    # print("list status: " + str(d['status']))         apparently only "finished" and "downloading"

    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


class Downloader(object):
    """Wrapper for the youtube_dl module
        only_audio: extract audio as mp3
        keep_video: keep the video as well as audio
    """
    def __init__(self, url, only_audio=False, keep_video=False, cut=False, cut_from=0, cut_until=0):
        self.url = url
        self.video_key = urlparse(url).query.split('=')[1]  # TODO: Make this work for other than standard youtube.com...v=xxxxxx urls

        self.only_audio = only_audio
        self.keep_video = keep_video
        self.cut = cut
        self.cut_from = cut_from                # TODO: Checks if the video is longer than
        self.cut_until = cut_until              # ......the parameter for the checks

        self.basic_opts = {
            'outtmpl': '%(id)s',                # name the file the ID of the video
            'noplaylist': True,                 # only download single song, not playlist
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }

#        if only_audio:
#            self.basic_opts['postprocessors'] = [{
#                'key': 'FFmpegExtractAudio',
#                'preferredcodec': 'mp3',
#                'preferredquality': '192',
#            }]


    def get_formats(self):
        with youtube_dl.YoutubeDL(self.basic_opts) as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            # print(info_dict)
            # TODO: parse info_dict for formats
            return None


    def download(self):
        with youtube_dl.YoutubeDL(self.basic_opts) as ydl:
            ret_val = ydl.download([self.url])

        if self.only_audio:
            if self.cut:
                clip = mp.VideoFileClip(self.video_key).subclip(self.cut_from, self.cut_until)
            else:
                clip = mp.VideoFileClip(self.video_key)

            clip.audio.write_audiofile(self.video_key + ".mp3")

            if not self.keep_video:
                os.remove(self.video_key)


d = Downloader('https://www.youtube.com/watch?v=CppiJUbC8BI', only_audio=True, keep_video=False, cut=True, cut_from=33, cut_until=5*60+10)
d.download()