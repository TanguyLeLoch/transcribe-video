import sys
import time

import moviepy.editor as mp
import whisper
import yt_dlp


def download_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'video.mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def check_url():
    check = youtube_url.find("youtube.com/watch?v=")
    if check == -1:
        print("Invalid URL")
        exit()


# get youtube video arg from command line
youtube_url = sys.argv[1]
check_url()

# download video
download_video(youtube_url)

# Load Whisper model
print("Loading model...")
model = whisper.load_model("base")

# # Load video file
video_path = "video.mp4"
video = mp.VideoFileClip(video_path)

# # Extract audio from the video
audio = video.audio

# Set audio file path for transcription
audio_path = "audio.wav"

# Save extracted audio to WAV file
audio.write_audiofile(audio_path)

beginTime = time.time()
print("Transcribing...\n starting time: ", beginTime)
# Transcribe speech from the audio file
result = model.transcribe(audio_path)

print("Time taken: ", time.time() - beginTime)

# Access the transcribed text
transcribed_text = result["text"]

# Print the transcribed text
print(transcribed_text)
