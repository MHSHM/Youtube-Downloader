import sys

from pytube import YouTube
from pytube.cli import on_progress
from pytube import Playlist
import os
import subprocess

from scipy.constants import bar

save_path = "F:\\HYPE!!!"

print("input 1 to download  video/videos")
print("input 2 to download a playlist")

choice = int(input("Choice: "))


def progress_func(stream, chunk, bytes_remaining):
    curr = stream.filesize - bytes_remaining
    percent = (curr / stream.filesize) * 100.0
    format_float = "{:.2f}".format(percent)
    sys.stdout.write("Downloading... " + str(format_float) + '%\n')
    sys.stdout.flush()


def MergeAudioVideo(yt):
    video_path = save_path + "\\" + "video.mp4"
    audio_path = save_path + "\\" + "audio.mp4"
    subprocess.run("ffmpeg -i {} -i {} -c copy {}".format(video_path, audio_path, save_path + "\\" + "out.mp4"))
    os.remove(audio_path)
    os.remove(video_path)
    special_chars = ["\\", "/", ":", "*", "?", "/", "<", ">", "|"]
    video_title = yt.title
    for char in video_title:
        if char in special_chars:
            video_title = video_title.replace(char, "")
    os.rename(save_path + "\\" + "out.mp4", save_path + "\\" + "{}.mp4".format(video_title))


def Download(urls):
    i = 1
    for ele in links:
        yt = YouTube(ele[0], on_progress_callback=progress_func)
        print("{}- {}".format(i, yt.title))
        yt.streams.filter(adaptive=True) \
            .filter(file_extension="mp4") \
            .filter(res=ele[1]) \
            .first().download(output_path=save_path, filename="video.mp4")
        stream = yt.streams.filter(only_audio=True).filter(file_extension="mp4").filter(abr="128kbps")
        if stream is None:
            yt.streams.filter(only_audio=True) \
                .filter(file_extension="mp4") \
                .first().download(output_path=save_path, filename="audio.mp4")
        else:
            stream.first().download(output_path=save_path, filename="audio.mp4")
        MergeAudioVideo(yt)
        i += 1

links = []

if choice == 1:

    while True:
        i_url = input("URL: ")
        if i_url == "exit":
            break
        res = input("Resolution i.e. 1080p: ")
        links.append([i_url, res])

    Download(links)

elif choice == 2:
    i_url = input("Playlist: ")
    res = input("Resolution: ")
    p = Playlist(i_url)
    links = []
    for url in p.video_urls:
        links.append([url, res])
    Download(links)
