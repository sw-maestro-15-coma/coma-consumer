
class ShortsRequest:
    def __init__(self,
                 s3_url:str,
                 text_path:str,
                 start:str,
                 end:str) -> None:
        self.s3_url = s3_url
        self.text_path = text_path
        self.start = start
        self.end = end