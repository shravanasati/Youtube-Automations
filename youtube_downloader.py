from pytube import YouTube, Playlist
import validators
from os import getcwd
from os.path import join as join_path, getsize, exists
from threading import Thread
from time import sleep
import re

class YouTubeDownloader(YouTube, Playlist):
    """
    Interface to download youtube videos using pytube module.
    """
    def __init__(self, video_url, format=".mp4", filepath=None):
        """
        Constructor.
        """
        self.video_url = video_url
        self.format = format

        valid = validators.url(self.video_url)
        if valid != True:
            print("Invalid video url!")
            quit()

        if self.format not in [".mp3", ".mp4"]:
            print("Invalid format! Format can either be mp3 or mp4.")
            quit()

        self.yt = YouTube(self.video_url)
        removals = re.compile(r'''[.?*/|\:;]''')
        title = self.yt.title
        title = re.sub(removals, "", title)
        if filepath != None:
            if exists(filepath):
                self.filepath = join_path(filepath, title + format)
            raise FileNotFoundError("No such directory in the system")
        else:
            self.filepath = join_path(getcwd(), title+format)


    def show_progress(self, filesize):
        """
        Shows the download progress.
        """
        size_on_disk = getsize(self.filepath)
        while size_on_disk < filesize:
            size_on_disk = getsize(self.filepath)
            ratio = round(size_on_disk / filesize) * 100
            print(f"{ratio}% download completed ({size_on_disk/1000000}MB/{filesize/1000000}MB).")
            sleep(10)

    def download_audio(self):
        """
        Download the given youtube video in audio format.
        """
        stream = self.yt.streams.filter(only_audio=True).get_audio_only()
        download_size = stream.filesize
        print("Downloading the audio {}...".format(self.yt.title))
        t1 = Thread(target=stream.download)
        t1.start()
        self.show_progress(download_size)
        if not t1.is_alive():
            print("Done!")

    def download_video(self, resolution:str="480p"):
        """
        Downloads the given youtube video in video format.
        """
        resolutions = {"2160p":313 ,"1440p":271, "1080p":299, "720p":22, "480p":135, "360p":18}

        stream = self.yt.streams.get_by_itag(resolutions[resolution])
        if stream == None:
            print(resolution, "resolution not available for this video, switching to default resolution.")
            stream = self.yt.streams.filter(only_video=True, adaptive=True)
        download_size = stream.filesize
        print("Downloading the video {}...".format(self.yt.title))
        t1 = Thread(target=stream.download)
        t1.start()
        sleep(5)
        self.show_progress(download_size)
        if not t1.is_alive():
            print("Done!")

yt = YouTubeDownloader("https://www.youtube.com/watch?v=UUF231bR5YY")
yt.download_video(resolution="720p")