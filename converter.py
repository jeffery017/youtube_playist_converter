import requests
from bs4 import BeautifulSoup
from pytube import Playlist, YouTube
import re
import pyperclip
import ssl
import asyncio

ssl._create_default_https_context = ssl._create_unverified_context

# 輸入 YouTube 播放清單的網址
# playlist_url = "https://www.youtube.com/playlist?list=PLuxlg1BYq9r2bYL4GBrCvCH7iTLRHSDxI"
# mode = 0 # disk:0, paste:1
# format = 1 # 0:txt, 1:md, 2:both

class Video:
    def __init__(self, title="", url="", length=0):
        self.title = title
        self.url = url
        self.length = length
    

# get video info
def getVideoRawDataFromPlaylist(playlist_url):
    try:
        # 使用 pytube 庫的 Playlist 類別來獲取播放清單的資訊
        playlist = Playlist(playlist_url)

        # 載入播放清單的資訊
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

        total_length = 0  # 總時長，以秒為單位
        # 抓取所有影片標題和網址
        videos = [Video(playlist.title, playlist_url)]
        for url in playlist.video_urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('title').string
            video = YouTube(url)  # 獲取影片資訊
            length = video.length
            total_length += length
            videos.append(Video(title, url, length))
        
        videos[0].length = total_length
        print('finish convert')
        return videos
    except:
        print('except video not found')
        return []




def formatTime(t:int):
    if t < 0: return "-"
    
    # 將總時長轉換為 hh:mm:ss 格式
    s = t % 60
    t //= 60
    m = t % 60
    t //= 60
    h = t
    return  f"{h:02d}:{m:02d}:{s:02d}"

def videosToTxt(videos:list[Video]): 
    return '\n'.join([video.title for video in videos])

def videosToTxtWithLength(videos:list[Video]): 
    return '\n'.join([f'{video.title} {video.length}' for video in videos])

def videosToMd(videos:list[Video]):
    return '\n'.join([f'[{video.title}]({video.url})' for video in videos])

def videosToMdWithLength(videos:list[Video]):
    return '\n'.join([f'[{video.title}]({video.url}) ( {video.length})' for video in videos])


def copyToClipboard(content):
    # 複製到Clipboard
    pyperclip.copy(content)
    pyperclip.paste()


def storeToDisk(title, path, content):
    try: 
        filepath =  path + title
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        return 0
    except:
        return -1

def convert(playlist_url, mode, format): 
    store = mode == 0
    md = format >= 1
    txt = format%2 == 0

    # 使用 pytube 庫的 Playlist 類別來獲取播放清單的資訊
    playlist = Playlist(playlist_url)

    # 載入播放清單的資訊
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")


    print("處理中...")
    total_duration = 0  # 總時長，以秒為單位
    # 抓取所有影片標題和網址
    video_info = []
    for url in playlist.video_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').string
        video = YouTube(url)  # 獲取影片資訊
        duration = video.length
        total_duration += duration
        video_info.append((title, url))

    # 將總時長轉換為 hh:mm:ss 格式
    hours = int(total_duration / 3600)
    minutes = int((total_duration % 3600) / 60)
    seconds = int(total_duration % 60)
    total_duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    playlist_name = playlist.title
    markdown_list = ""

    if md:
        
        for title, url in video_info:
            markdown_list += f"[{title[:-10]}]({url})\n"
        
        # 複製到Clipboard    
        pyperclip.copy(markdown_list)
        spam = pyperclip.paste()

        # 儲存影片標題和網址到md檔案
        if store:
            filename = f"./output/{playlist_name}.md"
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"[{playlist_name}]({playlist_url})\n")
                file.write(f"總時長：{total_duration_str}\n\n\n")
                file.write(markdown_list)


    if txt:
        txt_list = ""
        for title, url in video_info:
                txt_list += title + '\n'
        
        # 複製到Clipboard    
        pyperclip.copy(markdown_list)
        spam = pyperclip.paste()
        
        # 儲存影片標題到txt檔案
        if store:
            filename = f"./output/{playlist_name}.txt"
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"[{playlist_name}]({playlist_url})\n")
                file.write(f"總時長：{total_duration_str}\n\n\n")
                file.write(txt_list)
            

    print(f"已存到./output/{playlist_name}")