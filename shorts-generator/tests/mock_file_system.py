
class MockFileSystem:
    def __init__(self) -> None: # for mocking
        pass

    def make_dir_if_not_exists(self, dir_name: str) -> None: # for mocking
        pass


    def extract_dir_name(self, full_path: str) -> str: # for mocking
        return "/dirname"


    def write_text_to_file(self, file_path: str, content: str) -> None: # for mocking
        pass


    def remove_all_temp_files(self, path_list: list[str]) -> None: # for mocking
        pass
