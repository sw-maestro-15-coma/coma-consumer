import boto3


__s3 = boto3.client(
    service_name='s3',
    region_name='ap-northeast-2',
    aws_access_key_id="AKIA6GBMEHUUKC7J7Y53",
    aws_secret_access_key="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"
)


def download_video(video_id: int, s3_url: str) -> str:
    bucket_name, object_key, extension = __extract_s3_info(s3_url)
    video_path = f"/Users/octoping/{video_id}.{extension}"
    __s3.download_file(bucket_name, object_key, video_path)

    return video_path


def __extract_s3_info(s3_url: str) -> tuple[str, str, str]:
    if not s3_url.startswith("https://"):
        raise ValueError("잘못된 S3 URL입니다.")

    parts = s3_url.replace("https://", "").split('/')
    bucket_name = parts[0].split(".s3.ap-northeast-2")[0]
    object_key = '/'.join(parts[1:])
    extension = object_key.split('/')[-1].split('.')[-1]

    return bucket_name, object_key, extension
