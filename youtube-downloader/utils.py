import yt_dlp, boto3, cv2, json
 
def youtube_download(youtube_url):
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(youtube_url, download=True)
            return ydl.prepare_filename(result)
    except Exception as e:
        print(f"[youtube-downloader] {e}")


def upload_to_s3(file_name, bucket_name, s3_key):
    try:
        s3 = boto3.client('s3')
        s3.upload_file(file_name, bucket_name, s3_key)
        print(f"[youtube-downloader] video uploaded {file_name} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"[youtube-downloader] {e}")

def get_duration(filename):
    video = cv2.VideoCapture(filename)
    return video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)