from fastapi import APIRouter

from dto.popular_point_request_dto import PopularPointRequestDTO
from ..service.heatmap import get_popular_point_by_heatmap

from ..domain.youtube_crawler import YoutubeCrawler

router = APIRouter(
    prefix="/video",
    tags=["video"],
)


@router.post("/{video_id}/popular-point")
async def extract_popular_point(video_id: int, data: PopularPointRequestDTO):
    crawler = YoutubeCrawler()
    heatmap = crawler.get_most_replayed_heatmap(data.youtubeUrl)
    popular_point = get_popular_point_by_heatmap(heatmap)
    return {"videoId": video_id, "popularPoint": popular_point}


@router.get("/{video_id}/subtitle")
async def extract_subtitle(video_id: int):
    # 자막 기능은 현재 구현되어 있지 않습니다.
    return {"videoId": video_id}
