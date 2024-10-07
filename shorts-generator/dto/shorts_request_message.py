from dto.subtitle import Subtitle


class ShortsRequestMessage:
    def __init__(self,
                 shorts_id: int,
                 top_title: str,
                 video_s3_url: str,
                 start_time: int,
                 end_time: int,
                 subtitle_list: list[Subtitle]) -> None:
        self.shorts_id = shorts_id
        self.top_title = top_title
        self.video_s3_url = video_s3_url
        self.start_time = start_time
        self.end_time = end_time
        self.subtitle_list = subtitle_list
