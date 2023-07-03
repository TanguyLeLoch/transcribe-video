from transcriber import YouTubeTranscriber

# get youtube video arg from command line
# youtube_url = sys.argv[1]
# youtube_url = "https://www.youtube.com/watch?v=pWpF8f9Hzl8"
youtube_url = "https://www.youtube.com/watch?v=pB10v0VFPu4"
my_transcriber = YouTubeTranscriber(youtube_url)

# for segment in my_transcriber.segments:
    # print(segment)


def extract_video_for_word(word):
    result = my_transcriber.get_sentences_with_word(word)
    if len(result) > 0:
        transcribtion = YouTubeTranscriber(result[0])
        transcribtion.get_shortest_video_with_word(result[0])


extract_video_for_word("je veux d'abord avoir un mot pour remercier")
extract_video_for_word("les")
extract_video_for_word("mère")
extract_video_for_word("merci")
extract_video_for_word("pour")
extract_video_for_word("vidéo")
extract_video_for_word("tiktok")

