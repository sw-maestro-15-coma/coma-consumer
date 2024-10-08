import unittest


class UrlParsingTest(unittest.TestCase):
    def test_parsing(self):
        url: str = "https://video-process-test-bucket.s3.ap-northeast-2.amazonaws.com/process/231130773470705504765574391372778964972.mp4"

        parsed_url: list[str] = url.split("/")
        for s in parsed_url:
            print(s)

        self.assertEqual(len(parsed_url), 5)

    def test_make_object_name(self):
        url: str = "https://video-process-test-bucket.s3.ap-northeast-2.amazonaws.com/process/231130773470705504765574391372778964972.mp4"

        expected_object_name: str = "process/231130773470705504765574391372778964972.mp4"

        parsed_url: list[str] = url.split("/")
        object_name: str = f"{parsed_url[3]}/{parsed_url[4]}"

        self.assertEqual(expected_object_name, object_name)


if __name__ == '__main__':
    unittest.main()
