"""
    shorts_url : https://video-process-test-bucket.s3.ap-northeast-2.amazonaws.com/process/231130773470705504765574391372778964972.mp4
"""
import uuid
import boto3
from botocore.client import BaseClient

__s3_client: BaseClient = boto3.client('s3')

def get_file_from_url(shorts_url: str) -> str:
    bucket_name: str = "video-process-test-bucket"
    unique_id: int = uuid.uuid4().int
    file_name: str = f"/files/{unique_id}.mp4"

    parsed_url: list[str] = shorts_url.split("/")
    object_name: str = f"{parsed_url[3]}/{parsed_url[4]}"

    __s3_client.download_file(bucket_name, object_name, file_name)

    return file_name