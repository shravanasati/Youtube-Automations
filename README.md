# YouTube - Automations
The **YouTube - Automations** repo is a collection of the following two YouTube automations scripts:
* **YouTube Channel Tracker**
* **YouTube Downloader**


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

The channel ID is the highlighted part of the URL, present just after the **channel** parameter.
Paste it as the value for ```channel_id``` variable.

### Channel name
Pretty obvious, the name of the channel you want to track (```channel_name```).


# Youtube Downloader
The **Youtube Downloader** is an interface to download youtube videos with the help of [```pytube```](https://github.com/nficano/pytube) module. You can download any Youtube video by providing just the video url, download location, the desired format and resolution.

## Features
* Download any YouTube video in desired format (audio/video)
* Download the video in desired resolution
* Watch the download progress
* Efficient exception handling

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

Run the command ```pip install -r requirements.txt``` to install all these dependencies at once.

You are good to go!
