import yt_dlp, boto3, cv2, json, requests
import logging

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)

def get_video_title(youtube_url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(youtube_url, download=False)
        return result.get('title')

def youtube_download(youtube_url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(youtube_url, download=True)
        return ydl.prepare_filename(result)


def upload_to_s3(file_name, bucket_name, s3_key):
    s3 = boto3.client('s3')
    s3.upload_file(file_name, bucket_name, s3_key)

def get_duration(filename):
    video = cv2.VideoCapture(filename)
    return video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)

def post_success_to_api(data):
    url = "https://api.cotuber.com/api/v1/message/video"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response

def post_fail_to_api(data):
    pass