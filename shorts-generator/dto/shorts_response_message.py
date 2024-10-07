
class ShortsResponseMessage:
    def __init__(self,
                 shorts_id: int,
                 shorts_link: str,
                 thumbnail_link: str) -> None:
        self.shortsId = shorts_id
        self.s3Url = shorts_link
        self.thumbnailUrl = thumbnail_link