import unittest
from Transcriber import Transcriber


class TranscriberTests(unittest.TestCase):
    def setUp(self):
        # self.transcriber = Transcriber("audio.json")
        self.transcriber = Transcriber("1688880064729201.mp4")

    def test_create_srt_file(self):
        self.transcriber.create_srt_file()


if __name__ == '__main__':
    unittest.main()
