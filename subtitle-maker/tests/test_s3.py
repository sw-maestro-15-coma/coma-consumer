from unittest import TestCase
from s3 import S3UrlParser


class MyTestCase(TestCase):
    def test_parse(self):
        """s3urlparser를 생성하면 url의 요소들을 파싱할 수 있어야 한다"""
        # given
        s3_url = "https://video-process-test-bucket.s3.ap-northeast-2.amazonaws.com/origin/599903428704431693.webm"

        # when
        result = S3UrlParser(s3_url)

        # then
        self.assertEqual(result.bucket_name, "video-process-test-bucket")
        self.assertEqual(result.object_key, "origin/599903428704431693.webm")
        self.assertEqual(result.extension, "webm")

    def test_parse_invalid_url(self):
        """잘못된 s3urlparser를 생성하면 ValueError를 발생시켜야 한다"""
        # given
        s3_url = "https://naver.com"

        # when
        with self.assertRaises(ValueError):
            S3UrlParser(s3_url)