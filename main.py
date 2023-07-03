import time

import moviepy.editor as mp

import whisper

# Load Whisper model
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
# Transcribe speech from the audio file
result = model.transcribe(audio_path)

print("Time taken: ", time.time() - beginTime)


# Access the transcribed text
transcribed_text = result["text"]

# Print the transcribed text
print(transcribed_text)
