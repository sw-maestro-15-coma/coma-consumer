class ShortsRequestMessage:
    def __init__(self,
                 video_id,
                 shorts_id,
                 top_title,
                 video_s3_url,
                 start_time,
                 end_time) -> None:
        self.video_id = video_id
        self.shorts_id = shorts_id
        self.top_title = top_title
        self.video_s3_url = video_s3_url
        self.start_time = start_time
        self.end_time = end_time
