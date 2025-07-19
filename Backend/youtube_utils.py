import os
from yt_dlp import YoutubeDL
from hashlib import md5

AUDIO_CACHE_DIR = "cache/audio"

def download_audio(video_url):
    os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)
    video_id = md5(video_url.encode()).hexdigest()
    audio_path_no_ext = os.path.join(AUDIO_CACHE_DIR, video_id)  # no .mp3 extension yet
    final_audio_path = audio_path_no_ext + ".mp3"

    if os.path.exists(final_audio_path):
        return final_audio_path

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": audio_path_no_ext + ".%(ext)s",  # let yt_dlp handle extension
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "keepvideo": False,
        "quiet": False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    return final_audio_path
