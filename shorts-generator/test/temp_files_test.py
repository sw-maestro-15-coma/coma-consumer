import unittest
from unittest.mock import patch

from domain.temp_files import TempFiles


class TempFilesTest(unittest.TestCase):
    def test_top_title_null(self):
        with self.assertRaises(RuntimeError):
            TempFiles(
                uuid=1,
                top_title=None
            )

    @patch("domain.temp_files.TempFiles")
    def test_make_text_path_exception(self, MockTempFiles):
        MockTempFiles.__make_temp_text_path.side_effect=Exception("오류 발생")

        with self.assertRaises(RuntimeError):
            TempFiles(
                uuid=1,
                top_title="some_title"
            )


if __name__ == '__main__':
    unittest.main()
