import os


class FileSystem:
    def make_dir_if_not_exists(self, dir_name: str) -> None:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)


    def extract_dir_name(self, full_path: str) -> str:
        return os.path.dirname(full_path)


    def write_text_to_file(self, file_path: str, content: str) -> None:
        with open(file_path, "w+t") as e:
            e.write(content)


    def remove_all_temp_files(self, path_list: list[str]) -> None:
        try:
            for path in path_list:
                if os.path.isfile(path):
                    os.remove(path)
        except Exception as e:
            raise RuntimeError(e)


    def extract_file_name(self, path: str) -> str:
        return os.path.basename(path)
