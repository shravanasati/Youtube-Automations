from pytube import YouTube, Playlist
import validators
from os import getcwd
from os.path import join as join_path, getsize, exists
from multiprocessing import Process
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
                self.filepath = join_path("/" + filepath, title + format)
            else:
                print("No such directory in the system, hence the video would be downloaded in the current working directory: {}.".format(getcwd()))
                self.filepath = join_path("/" + getcwd(), title+format)
        else:
            self.filepath = join_path("/" + getcwd(), title+format)


    def show_progress(self, filesize):
        """
        Shows the download progress.
        """
        print("Starting show_progress...")
        sleep(10)
        print("Started")
        size_on_disk = getsize(self.filepath)
        while size_on_disk < filesize:
            size_on_disk = getsize(self.filepath)
            ratio = (size_on_disk / filesize) * 100
            print(f"{ratio}% download completed ({size_on_disk/1000000}MB/{filesize/1000000}MB).")
            sleep(10)


    def download_audio(self):
        """
        Download the given youtube video in audio format.
        """
        stream = self.yt.streams.filter(only_audio=True).get_audio_only()
        download_size = stream.filesize
        print("Downloading the audio {}...".format(self.yt.title))
        t1 = Process(target=stream.download, args=(self.filepath, ))
        t1.start()
        t2 = Process(target=self.show_progress, args=(download_size, ))
        t2.start()     
        t2.join()     
        t1.join()     
        if not t1.is_alive():
            print("Finished downloading the audio!")
            quit()
        
    def download_video(self, resolution:str="480p"):
        """
        Downloads the given youtube video in video format.
        """
        resolutions = {"2160p":313 ,"1440p":271, "1080p":299, "720p":22, "480p":135, "360p":18, "240p":133, "144p":160}

        stream = self.yt.streams.get_by_itag(resolutions[resolution])
        if stream == None:
            print(resolution, "resolution not available for this video, switching to default resolution.")
            stream = self.yt.streams.filter(only_video=True, adaptive=True).first()
        download_size = stream.filesize
        print("Downloading the video {}...".format(self.yt.title))

        p1 = Process(target=stream.download, args=(self.filepath, ))
        p2 = Process(target=self.show_progress, args=(download_size, ))
        p2.start()
        p1.start()
        p2.join()
        p1.join()
        if not p1.is_alive():
            print("Finished downloading the video!")
            quit()

if __name__ == "__main__":
    print("Welcome to the Youtube Video Downloader!")
    url = input("Enter the video url for the video you want to download: ")
    format = int(input("What do you want to download from the video:\n 1. Audio \n 2. Video \n"))
    filepath = input("Enter the optional file location (press enter if you dont want to specify file location): ")
    if filepath == "":
        filepath=None
    print("Wait while the video and location is being checked...")
    
    if format == 1:
        yt = YouTubeDownloader(url, filepath=filepath)
        yt.download_audio()
    elif format == 2:
        res = input("Enter desired resoulution for the video (example: '720p'): ")
        available_res = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]
        if res.strip() not in available_res:
            print("Invalid resolution! Resolutions can range in", available_res)
            quit()

        yt = YouTubeDownloader(url, filepath=filepath)
        yt.download_video(res.strip())

    else:
        print("Invalid input!")
        quit()

    print("Thanks for visiting!")