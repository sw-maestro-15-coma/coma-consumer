
class ShortsResponseMessage:
    def __init__(self,
                 video_id: int,
                 shorts_id: int,
                 shorts_link: str,
                 thumbnail_link: str) -> None:
        self.video_id = video_id
        self.shorts_id = shorts_id
        self.shorts_link = shorts_link
        self.thumbnail_link = thumbnail_link