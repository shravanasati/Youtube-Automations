from pytube import YouTube, Playlist
import validators
from os import getcwd, chdir, getlogin, rename, mkdir
from os.path import join as join_path, getsize, exists, expanduser
from multiprocessing import Process
from time import sleep
import re
from shutil import move as move_file
from string import ascii_letters as alphabets
from random import choice as random_choice

class YouTubeDownloader():
    """
    Interface to download youtube videos using pytube module.
    """
    def __init__(self, video_url, type, filepath=None):
        """
        video_url = The URL of the Youtube video.

        type = Download type, either of 'audio' or 'video'.

        filepath = The file location where all the videos of the playlist will be saved. In the filepath, a new directory with the playlost name would be created.
        """
        chdir(join_path(expanduser("~"), "Downloads"))

        self.video_url = video_url
        self.format = ".mp4"
        self.type = type

        # * validating the url
        valid = validators.url(self.video_url)
        if valid != True:
            print("Invalid video url!")
            quit()

        # * initiating a yt object
        self.yt = YouTube(self.video_url)

        # * altering the video title for filepath since [.?*/,|\:;] are not allowed in a filename
        removals = re.compile(r'''[.?*/,|\:;]''')
        title = self.yt.title
        self.video_title = re.sub(removals, "", title)

        # * making a valid filename
        if filepath != None:
            if exists(filepath):
                self.filepath = filepath
            else:
                print("No such directory in the system, hence the video would be downloaded in the current working directory: {}.".format(getcwd()))
                self.filepath = getcwd()
        else:
            self.filepath = getcwd()

    @staticmethod
    def index_of_key(key, d:dict):
        """
        Returns the index of the key from the dictionary.
        """
        # * for getting the next resolution of the video in case the provided resolution is not availables
        for i, k in enumerate(d.keys()):
            if k == key:
                index = i
                return index

    def show_progress(self, filesize):
        """
        Shows the download progress and changes extension to mp3.
        """
        # * original filepath is where the video would be downloaded
        original_path = join_path(getcwd(), self.video_title + self.format)

        # * waiting for seconds until the file is created because sometimes the file is not created and then it results in FileNotFoundError
        while not exists(original_path):
            sleep(1)
        
        # * showing the download progress
        size_on_disk = getsize(original_path)
        while size_on_disk < filesize:
            size_on_disk = getsize(original_path)
            ratio = (size_on_disk / filesize) * 100
            print(f"{ratio:.2f}% download completed ({size_on_disk/1000000}MB/{filesize/1000000}MB).")
            sleep(5)

        # changing extension to mp3 if audio
        if self.type == "audio":
            rename(original_path, join_path(getcwd(), self.video_title + ".mp3"))
            self.format = ".mp3"

    def move_after_download(self):
        """
        Moves the downloaded file to its destined filepath.
        """
        if getcwd() == self.filepath:
            return None
            
        try:
            original_path = join_path(getcwd(), self.video_title + self.format)
            
            # * moving the file to self.filepath
            move_file(original_path, self.filepath)
            print("File moved to", self.filepath)

        except Exception as e:
            print(e)


    def download_audio(self):
        """
        Download the given youtube video in audio format.
        """
        try:
            # * getting the audio stream from pytube module
            stream = self.yt.streams.filter(only_audio=True).get_audio_only()
            if stream == None:
                print("Error: No audio stream available for this video!")
                quit()

            download_size = stream.filesize
            print("Downloading the audio {}...".format(self.video_title))

            # * starting two threads, one for the download and other for showing download progress
            t1 = Process(target=stream.download)
            t1.start()
            self.show_progress(download_size)

            # * if finished downloading the file
            print("Finished downloading the audio!")
            # * moving to the self.filepath
            self.move_after_download()
            quit()

        except Exception as e:
            print("Following error occured:", e)
            quit()
        

    def download_video(self, resolution:str="720p"):
        """
        Downloads the given youtube video in video format.
        """
        try:
            # * itags for different resolutions for mp4 downloads 
            resolutions = {"2160p":313 ,"1440p":271, "1080p":299, "720p":22, "480p":135, "360p":18, "240p":133, "144p":160}

            # * getting the stream for the requested resolution
            stream = self.yt.streams.get_by_itag(resolutions[resolution])

            # * `stream = None` means that the requested resolution is not available for the given video, hence switching to the next lower resolution
            while True:
                # * getting the next lower resolution
                next_index = self.index_of_key(resolution, resolutions) + 1
                if next_index > 7:
                    print("No video stream available for this video!")
                    quit()
                next_res = list(resolutions.keys())[next_index]
                print(f"{resolution} resolution not available for this video, switching to {next_res} resolution.")

                # * fetching the new stream until the resolution is correct
                stream = self.yt.streams.get_by_itag(resolutions[next_res])
                if stream != None:
                    print("\n")
                    break
                resolution = next_res


            download_size = stream.filesize
            print("Downloading the video {}...".format(self.video_title))

            # * starting two threads, one for the download and other for showing download progress
            p1 = Process(target=stream.download)
            p1.start()
            self.show_progress(download_size)
            self.move_after_download()

        except Exception as e:
            print(e)


class PlaylistDownloader():
    """
    Base class for downloading playlists using Playlst class of pytube.
    """
    def __init__(self, playlist_url, type, filepath) -> None:
        """
        playlist_url = URL to the playlist on Youtube.
        
        type = Download type, whether audio or video.

        filepath = The file location where all the videos of the playlist will be saved. In the filepath, a new directory with the playlost name would be created.
        """
        self.playlist_url = playlist_url
        self.type = type

        # * validating the url
        valid = validators.url(self.playlist_url)
        if valid != True:
            print("Invalid playlist url!")
            quit()

        
        # * initialising playlist object
        self.plt = Playlist(playlist_url)

        # * altering the playlist title for filepath since [.?*/,|\:;] are not allowed in a filename
        playlist_name = self.plt.title
        removals = re.compile(r'''[.?*/,|\:;]''')
        self.playlist_name = re.sub(removals, "", playlist_name)

        # * checking the filepath
        if filepath != None:
            if exists(filepath):
                self.filepath = join_path(filepath, playlist_name)
            else:
                print("No such directory in the system, hence the video would be downloaded in the current working directory: {}.".format(getcwd()))
                self.filepath = join_path(getcwd(), playlist_name)
        else:
            self.filepath = join_path(getcwd(), playlist_name)

        while True:
            try:
                mkdir(join_path(filepath, self.playlist_name))
                break
            except FileExistsError:
                new_folder_name = join_path(filepath, self.playlist_name) + "" + random_choice(alphabets)
                print(f"Path '{join_path(filepath, self.playlist_name)}' already exists, hence making new folder with name {new_folder_name}.")
                mkdir(new_folder_name)
                break

    def download_all_videos(self, resolution:str="720p"):
        for vid in self.plt.video_urls:
            yt = YouTubeDownloader(vid, "video", self.filepath)
            yt.download_video(resolution)

    def download_all_audio(self):
        for vid in self.plt.video_urls():
            yt =YouTubeDownloader(vid, "audio", self.filepath)
            yt.download_audio()


if __name__ == "__main__":
    print("Welcome to the Youtube Video Downloader!")

    playlist_or_video = int(input("What to download? \n 1. Video \n 2. Playlist \n"))
    
    if playlist_or_video == 1:
        url = input("Enter the video url for the video you want to download: ")

        format = int(input("What do you want to download from the video:\n 1. Audio \n 2. Video \n"))

        filepath = input("Enter the optional file location (press enter if you dont want to specify file location): ")

        if filepath == "":
            filepath = None

        if format == 1:
            print("\nWait while the download is being started...")
            yt = YouTubeDownloader(url, "audio", filepath=filepath)
            yt.download_audio()

        elif format == 2:
            res = input("Enter desired resoulution for the video (example: '720p'): ").strip()
            available_res = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]

            if res not in available_res:
                print("Invalid resolution! Resolutions can range in", available_res)
                quit()

            print("Wait while the download is being started...")

            yt = YouTubeDownloader(url, "video", filepath=filepath)
            yt.download_video(res)

        else:
            print("Invalid input!")
            quit()


    elif playlist_or_video == 2:
        url = input("Enter the playlist url for the playlist you want to download: ")

        format = int(input("What do you want to download from the playlist:\n 1. Audio \n 2. Video \n"))

        filepath = input("Enter the optional file location (press enter if you dont want to specify file location): ")

        if filepath == "":
            filepath = None

        if format == 1:
            print("\nWait while the download is being started...")
            plt = PlaylistDownloader(url, "audio", filepath=filepath)
            plt.download_all_audio()

        elif format == 2:
            res = input("Enter desired resoulution for the video (example: '720p'): ").strip()
            available_res = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]

            if res not in available_res:
                print("Invalid resolution! Resolutions can range in", available_res)
                quit()

            print("Wait while the download is being started...")

            plt = PlaylistDownloader(url, "video", filepath=filepath)
            plt.download_all_videos(res)

        else:
            print("Invalid input!")
            quit()


    else:
        print("Invalid input!")

    print("Thanks for visiting!")