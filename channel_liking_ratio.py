import scrapetube
import requests
from dataclasses import dataclass

@dataclass
class Video:
    video_id: str
    likes: int
    dislikes: int
    def ratio(self):
        return self.likes / self.dislikes

def get_video_data(video_id):
    url = f"https://returnyoutubedislikeapi.com/votes?videoId={video_id}"
    resp = requests.get(url).json()
    return Video(video_id, resp['likes'], resp['dislikes'])

def get_video_ids(channelID, n = 10):
    print("getting video ids")
    videos = scrapetube.get_channel(channelID)
    ids = []
    for video in videos:
        ids.append(video['videoId'])
        if len(ids) == n:
            break

    return ids

data = [get_video_data(i).ratio() for i in get_video_ids("UCCezIgC97PvUuR4_gbFUs5g")]
print(sum(data)/len(data))

