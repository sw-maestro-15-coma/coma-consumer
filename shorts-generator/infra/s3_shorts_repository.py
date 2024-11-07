import os.path
from typing import AnyStr, LiteralString
from venv import logger

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from config import Config
from domain.id_generator import IdGenerator
from domain.shorts_repository import ShortsRepository

class S3ShortsRepository(ShortsRepository):
    def __init__(self) -> None:
        self.__s3_bucket_name = Config.s3_bucket_name()
        self.client: BaseClient = boto3.client("s3",
                             region_name=Config.region(),
                             aws_access_key_id=Config.aws_access_key(),
                             aws_secret_access_key=Config.aws_secret_key())


    def download_shorts(self, s3_url: str) -> str:
        try:
            input_path = f"{Config.input_path()}/{IdGenerator.make_id()}.mp4"
            self.client.download_file(self.__s3_bucket_name, self.__extract_key(s3_url), input_path)

            return input_path

        except ClientError as e:
            logger.error(e)
            raise


    def post_shorts(self, output_path: str) -> str:
        try:
            file_name: AnyStr = self.__extract_file_name(output_path)
            self.client.upload_file(output_path, self.__s3_bucket_name, 'shorts/' + file_name)

            return Config.s3_url() + '/shorts/' + file_name
        except ClientError as e:
            logger.error(e)
            raise


    def post_thumbnail(self, thumbnail_path: str) -> str:
        try:
            file_name: AnyStr = self.__extract_file_name(thumbnail_path)
            self.client.upload_file(thumbnail_path, self.__s3_bucket_name, 'thumbnail/' + file_name)

            return Config.s3_url() + '/thumbnail/' + file_name
        except ClientError as e:
            logger.error(e)
            raise

    @staticmethod
    def __extract_file_name(path: str) -> AnyStr:
        return os.path.basename(path)


    @staticmethod
    def __extract_key(s3_url: str) -> str:
        splited: list[str] = s3_url.replace("s3://", "").split("/")

        return f"{splited[1]}/{splited[2]}"

