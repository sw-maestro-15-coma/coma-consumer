from venv import logger

import boto3
from botocore.exceptions import ClientError

from config import Config
from domain.shorts_repository import ShortsRepository

class S3ShortsRepository(ShortsRepository):
    def __init__(self) -> None:
        self.__s3_bucket_name = Config.s3_bucket_name()
        self.client = boto3.client("s3",
                             region_name=Config.region(),
                             aws_access_key_id=Config.aws_access_key(),
                             aws_secret_access_key=Config.aws_secret_key())

    def post_shorts(self, output_path: str, file_name: str) -> str:
        try:
            self.client.upload_file(output_path, self.__s3_bucket_name, 'process/' + file_name)

            return self.__s3_bucket_name + 'process/' + file_name
        except ClientError as e:
            logger.error(e)
            raise