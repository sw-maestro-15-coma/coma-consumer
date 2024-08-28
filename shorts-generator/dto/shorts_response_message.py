
class ShortsResponseMessage:
    def __init__(self,
                 video_id: int,
                 shorts_id: int,
                 link: str) -> None:
        self.video_id = video_id
        self.shorts_id = shorts_id
        self.link = link