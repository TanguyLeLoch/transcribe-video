import os
import time
import moviepy.editor as mp
import whisper
import yt_dlp

print("Loading model...")
MODEL = whisper.load_model("tiny")


class YouTubeTranscriber:
    def __init__(self, video_address):
        if self.is_youtube(video_address):
            self.download_video(video_address)
            self.video_path = "video.mp4"
        else:
            self.video_path = video_address

        self.audio_path = "audio.wav"
        self.transcribed_text = ""
        self.segments = []
        self.separate_sentences()

    @staticmethod
    def download_video(video_url):
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': 'video.mp4',
        }
        # delete video file if exists
        try:
            os.remove("video.mp4")
        except:
            pass

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    @staticmethod
    def is_youtube(video_address):
        check = video_address.find("youtube.com/watch?v=")
        return check != -1

    def separate_sentences(self):
        # Load Whisper model

        # Load video file
        video = mp.VideoFileClip(self.video_path)
        # Extract audio from the video
        audio = video.audio
        # Save extracted audio to WAV file
        audio.write_audiofile(self.audio_path)
        begin_time = time.time()
        local_time = time.localtime(begin_time)
        formatted_time = time.strftime("%H:%M:%S", local_time)
        print("Transcribing...\n starting time: ", formatted_time)
        # Transcribe speech from the audio file
        result = MODEL.transcribe(self.audio_path)
        print("Time taken: ", time.time() - begin_time)
        # Access the transcribed text
        self.transcribed_text = result["text"]
        # Get the individual sentences or words with their timings
        self.segments = result["segments"]

    def get_sentences_with_word(self, word):
        count = 0
        files_created = []
        for segment in self.segments:
            text = segment["text"]
            if word.lower() in text.lower():
                file = self.create_sub_video(word + str(count), segment["start"], segment["end"])
                files_created.append(file)
                count += 1
        return files_created

    def create_sub_video(self, word, start, end):
        video = mp.VideoFileClip(self.video_path)

        sub_video = video.subclip(start, end)
        sub_video.write_videofile(word + ".mp4",
                                  codec='libx264',
                                  audio_codec='aac',
                                  temp_audiofile='temp-audio.m4a',
                                  remove_temp=True)

        return word + ".mp4"

    def get_shortest_video_with_word(self, word):
        while True:
            video = mp.VideoFileClip(self.video_path)
            # remove the last second of the video
            video_shorter = video.subclip(0, video.duration - 1)
            # save the video
            video_shorter.write_videofile("temp.mp4",
                                          codec='libx264',
                                          audio_codec='aac',
                                          temp_audiofile='temp-audio.m4a',
                                          remove_temp=True)
            # transcribe the video
            temp_transcriber = YouTubeTranscriber("temp.mp4")
            # get the segments with the word
            segments = temp_transcriber.get_sentences_with_word(word)
            # if there are segments with the word, return the video
            if len(segments) > 0:
                # rename temp.mp4 to the word
                os.rename("temp.mp4", self.video_path)
            else:
                return
