from application.shorts_service import ShortsService
from domain.id_generator import IdGenerator
from domain.shorts_processor import ShortsProcessor
from domain.shorts_repository import ShortsRepository
from domain.shorts_result_sender import ShortsResultSender
from domain.shorts_thumbnail_maker import ShortsThumbnailMaker
from infra.ffmpeg_shorts_processor import FfmpegShortsProcessor
from infra.ffmpeg_shorts_thumbnail_maker import FfmpegShortsThumbnailMaker
from infra.rabbitmq_consumer import RabbitMQConsumer
from infra.s3_shorts_repository import S3ShortsRepository
from infra.simple_shorts_result_sender import SimpleShortsResultSender


class ObjectFactory:
    @classmethod
    def rabbitmq_consumer(cls) -> RabbitMQConsumer:
        return RabbitMQConsumer(shorts_service=cls.shorts_service(),
                                shorts_result_sender=cls.shorts_result_sender())

    @classmethod
    def shorts_service(cls) -> ShortsService:
        return ShortsService(shorts_processor=cls.shorts_processor(),
                             shorts_repository=cls.shorts_repository(),
                             shorts_thumbnail_maker=cls.shorts_thumbnail_maker())

    @classmethod
    def shorts_processor(cls) -> ShortsProcessor:
        return FfmpegShortsProcessor()

    @classmethod
    def shorts_repository(cls) -> ShortsRepository:
        return S3ShortsRepository()

    @classmethod
    def shorts_result_sender(cls) -> ShortsResultSender:
        return SimpleShortsResultSender()

    @classmethod
    def shorts_thumbnail_maker(cls) -> ShortsThumbnailMaker:
        return FfmpegShortsThumbnailMaker()