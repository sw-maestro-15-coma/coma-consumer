import boto3


__s3 = boto3.client('s3')


def download_video(video_id: int, s3_url: str) -> str:
    bucket_name, object_key = __extract_s3_info(s3_url)
    video_path = f"/video/{video_id}.mp4"
    __s3.download_file(bucket_name, object_key, video_path)

    return video_path


def __extract_s3_info(s3_url: str) -> tuple[str, str]:
    if not s3_url.startswith("https://"):
        raise ValueError("잘못된 S3 URL입니다.")

    parts = s3_url.replace("https://", "").split('/')
    bucket_name = parts[0]
    object_key = '/'.join(parts[1:])

    return bucket_name, object_key
