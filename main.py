from transcriber import YouTubeTranscriber

# get youtube video arg from command line
# youtube_url = sys.argv[1]
youtube_url = "https://www.youtube.com/watch?v=pWpF8f9Hzl8"
my_transcriber = YouTubeTranscriber(youtube_url)

# for segment in my_transcriber.segments:
    # print(segment)


result = my_transcriber.get_sentences_with_word("française")

for segment in result:
    transcribtion = YouTubeTranscriber(segment)
    transcribtion.get_shortest_video_with_word("français")