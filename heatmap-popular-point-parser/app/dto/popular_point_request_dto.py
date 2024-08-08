from pydantic import BaseModel


class PopularPointRequestDTO(BaseModel):
    youtubeUrl: str
