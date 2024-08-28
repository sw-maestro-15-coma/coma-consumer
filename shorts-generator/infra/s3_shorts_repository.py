from venv import logger

import boto3
from botocore.exceptions import ClientError

from domain.shorts_repository import ShortsRepository

class S3ShortsRepository(ShortsRepository):
    def __init__(self):
        self.__s3_bucket_name = "video-process-test-bucket"
        self.__s3_bucket_url = "https://video-process-test-bucket.s3.ap-northeast-2.amazonaws.com/"
        self.client = boto3.client("s3",
                             region_name="ap-northeast-2",
                             aws_access_key_id='AKIA6GBMEHUUKC7J7Y53',
                             aws_secret_access_key='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')

    def post_shorts(self, output_path: str, file_name: str) -> None:
        try:
            response = self.client.upload_file(output_path, self.__s3_bucket_name, 'process/' + file_name)
        except ClientError as e:
            logger.error(e)
            raise