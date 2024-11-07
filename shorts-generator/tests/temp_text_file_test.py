import unittest

from domain.temp_text_file import TempTextFile
from tests.mock_file_system import MockFileSystem


class TempTextFileTest(unittest.TestCase):
    def test_something(self):
        temp_text_file = TempTextFile(MockFileSystem())

        ext: str = temp_text_file.get_text_path().split(".")[1]

        self.assertEqual(ext, "txt")


if __name__ == '__main__':
    unittest.main()
