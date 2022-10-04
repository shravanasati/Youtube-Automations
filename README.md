# YouTube - Automations
The **YouTube - Automations** repo is a collection of the following three YouTube automations scripts:
* **YouTube Channel Tracker**
* **YouTube Downloader**
* **Youtube Channel Like ratio**

# YouTube Channel Tracker

## Overview

The **YouTube Channel Tracker** is a simple python script that opens Youtube when your favorite Youtuber uploads a new video. In this way, you can watch your favorite Youtuber's new video as soon as it is published! It uses the [YouTube API](https://console.developers.google.com/apis/api/youtube.googleapis.com) to accomplish this task. It also automatically likes the video!

## Setup
You'll need three things to get this script working:
* YouTube API Key
* Channel ID of the YouTube channel you want to track
* Channel name of the YouTube channel you want to track

*Note: Provide each of this thing in the code respectively.*

### YouTube API Key
YouTube API key is the base of this script. Get the API key from [here](https://console.developers.google.com/apis/api/youtube.googleapis.com). It is used to get the data from the YouTube API.

Paste it as the value for ```api_key``` variable.

### Channel ID
You would have to provide the channel ID of the youtube channel you want to track. 

For example:


![Channel ID](example.png)


The channel ID is the highlighted part of the URL, present just after the **channel** parameter. You'll get such url when you visit a Youtube channel's home page.
Paste it as the value for ```channel_id``` variable.

### Channel name
Pretty obvious, the name of the channel you want to track (```channel_name```).


# Youtube Downloader
The **Youtube Downloader** is an interface to download youtube videos with the help of [```pytube```](https://github.com/pytube/pytube) module. You can download any Youtube video by providing just the video url, download location, the desired format and resolution.

## Features
* Download any YouTube video in desired format (audio/video)
* Download the video in desired resolution
* Download playlists as a whole, again in desired format and resolution
* Watch the download progress
* Efficient exception handling

# Youtube Channel Like ratio
The **Youtube Channel Like ratio** computes the average like ratio of any Youtube channel by fetching the video ids of the 25 latest videos that's been uploaded on the channel and extracting the number of likes and dislikes from [this link](https://returnyoutubedislikeapi.com/votes?videoId={video_id}). It uses ``scrapetube`` package to fetch the video ids of the channel. Note that you need to pass the channel ID as a parameter to the ```get_video_ids``` function.


# Installation
## Using Git
Type the following command in your Git Bash:

- For SSH:
```git clone git@github.com:Shravan-1908/Youtube-Automations.git```
- For HTTPS: ```git clone https://github.com/Shravan-1908/Youtube-Automations.git```

The whole repository would be cloned in the directory you opened the Git Bash in.

## Using GitHub ZIP download
You can alternatively download the repository as a zip file using the GitHub **Download ZIP** feature. 

*External modules used-*
- win10toast 
- pyttsx3
- pyautogui
- validators
- requests
- pytube
- scrapetube

Run the command ```pip install -r requirements.txt``` to install all these dependencies at once.

You are good to go!
