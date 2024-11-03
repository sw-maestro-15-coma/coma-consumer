from pydantic import BaseModel


class Subtitle:
    def __init__(self, start: int, end: int, subtitle: str):
        self.start = start
        self.end = end
        self.subtitle = subtitle
