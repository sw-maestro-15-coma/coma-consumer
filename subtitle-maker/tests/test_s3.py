from unittest import TestCase
from s3 import S3UrlParser
from subtitle import SubtitleResult, Subtitle


class MyTestCase(TestCase):
    def test_parse(self):
        """s3urlparser를 생성하면 url의 요소들을 파싱할 수 있어야 한다"""
        # given
        s3_url = "s3://video-process-bucket/origin/Gzs1qNmTcYY.webm"

        # when
        result = S3UrlParser(s3_url)

        # then
        self.assertEqual(result.bucket_name, "video-process-bucket")
        self.assertEqual(result.object_key, "origin/Gzs1qNmTcYY.webm")
        self.assertEqual(result.extension, "webm")

    def test_parse_invalid_url(self):
        """잘못된 s3urlparser를 생성하면 ValueError를 발생시켜야 한다"""
        # given
        s3_url = "https://naver.com"

        # when
        with self.assertRaises(ValueError):
            S3UrlParser(s3_url)

    def test_to_json(self):
        """SubtitleResult를 json으로 변환할 수 있어야 한다"""
        obj = SubtitleResult(subtitles=[Subtitle(start=0, end=1, subtitle="hello")])
        print(list(map(lambda x: x.__dict__, obj.subtitles)))
        self.assertEqual(obj.__dict__,  [{"start": 0, "end": 1, "subtitle": "hello"}])
