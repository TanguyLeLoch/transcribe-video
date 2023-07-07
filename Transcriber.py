import os
import time
import moviepy.editor as mp
import yt_dlp
import stable_whisper


# print("Loading model...")
# MODEL = whisper.load_model("large")
# MODEL = stable_whisper.load_model('large')

class Transcriber:

    def __init__(self, address):
        self.result = None
        if self.is_json(address):
            self.result = stable_whisper.WhisperResult('audio.json')
        elif self.is_youtube(address):
            self.from_youtube(address)
        else:
            self.from_video(address)

        self.audio_path = "audio.wav"

        self.result.save_as_json('audio.json')

    @staticmethod
    def is_youtube(video_address):
        check = video_address.find("youtube.com/watch?v=")
        return check != -1

    @staticmethod
    def is_json(address):
        return address.find(".json") != -1

    def from_youtube(self, address):
        video_path = "video.mp4"
        self.download_video(address, video_path)
        self.from_video(video_path)

    @staticmethod
    def download_video(video_url, output_path):
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': output_path,
        }
        # delete video file if exists
        try:
            os.remove(output_path)
        except:
            pass

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    def from_video(self, address):
        video = mp.VideoFileClip(address)
        audio = video.audio
        audio.write_audiofile("audio.wav")
        MODEL = stable_whisper.load_model('large')
        self.result = MODEL.transcribe('audio.wav')

    def create_srt_file(self):
        self.result.split_by_length(max_words=4, force_len=True)
        self.result.to_srt_vtt('audio.srt')
