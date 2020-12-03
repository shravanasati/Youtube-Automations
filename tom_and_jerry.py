from requests import get as rget
from json import loads as jloads
from webbrowser import open_new_tab
from random import randint

def watch_tom_and_jerry():
    # youtube api key
    api_key = ""
    playlist_id = "PLbEif3LMBbrxFaXONS-1Uf51G0hkzQ3j4" 

    # api search url
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=110&playlistId={playlist_id}&key={api_key}"

    # opening the text file which contains all the video ids for videos that are watched
    f =  open('watched.txt', 'a+')
    fc = f.read().split("\n")

    try:
        print("Loading...")
        # getting results from the youtube api and parsing the data
        r = rget(url).text
        parser = jloads(r)

        while True:
            # checking if the video id the api returned is in the text file, because if it is, then you won't want to see the same video again
            videoId = (parser['items'][randint(0, 108)]['contentDetails']['videoId'])
            if videoId in fc:
                continue
            else:
                break

        # opening the browser for watching the video 
        videoURl = f"https://www.youtube.com/watch?v={videoId}"
        print("Successful!")
        open_new_tab(videoURl)

        # appending the video id for the video watched 
        f.write(videoId+"\n")
        f.close()

    except Exception as e:
        print(e)

if __name__ == "__main__":
    watch_tom_and_jerry()