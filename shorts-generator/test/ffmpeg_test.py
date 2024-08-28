import unittest

from domain.shorts_processor import ShortsProcessor
from dto.shorts_request import ShortsRequest
from object_factory import ObjectFactory


class MyTestCase(unittest.TestCase):
    def test_invalid_args(self):
        shorts_processor = ObjectFactory.shorts_processor()
        shorts_request = ShortsRequest(s3_url="abc.com",
                                       text_path="/",
                                       output_path="/",
                                       start="00:00:00",
                                       end="00:00:00")

        with self.assertRaises(RuntimeError):
            shorts_processor.execute(request=shorts_request)

if __name__ == '__main__':
    unittest.main()