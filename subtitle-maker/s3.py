import os

import boto3
from dataclasses import dataclass


__s3 = boto3.client(
    service_name='s3',
    region_name='ap-northeast-2',
    aws_access_key_id="AKIA6GBMEHUUKC7J7Y53",
    aws_secret_access_key="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"
)


def download_video(video_id: int, s3_url: str) -> str:
    parse_result = S3UrlParser(s3_url)
    video_path = f"{os.environ.get("video_path")}/{video_id}.{parse_result.extension}"

    __s3.download_file(
        parse_result.bucket_name,
        parse_result.object_key,
        video_path
    )

    return video_path


def delete_video(video_path: str):
    os.remove(video_path)


class S3UrlParser:
    bucket_name: str
    object_key: str
    extension: str

    def __init__(self, s3_url: str):
        self.__validate_url(s3_url)

        parts = s3_url.replace("https://", "").split('/')
        self.bucket_name = parts[0].split(".s3.ap-northeast-2")[0]
        self.object_key = '/'.join(parts[1:])
        self.extension = self.object_key.split('/')[-1].split('.')[-1]

    def __validate_url(self, s3_url: str):
        if ".s3.ap-northeast-2" not in s3_url:
            raise ValueError("잘못된 S3 URL입니다.")
