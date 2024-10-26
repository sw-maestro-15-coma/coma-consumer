from pydantic import BaseModel


class Subtitle(BaseModel):
    start: int
    end: int
    subtitle: str


class RequestDto(BaseModel):
    draftId: int
    subtitleList: list[Subtitle]
