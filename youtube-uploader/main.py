import googleapiclient.discovery
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

from consumer import start_consume


def upload_to_youtube(access_token: str, title: str, description: str, file_path: str) -> None:
    api_service_name: str = "youtube"
    api_version: str = "v3"

    credentials: Credentials = Credentials(token=access_token)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": description,
                "title": title
            },
            "status": {
                "privacyStatus": "private"
            }
        },
        media_body=MediaFileUpload(filename=file_path)
    )
    response = request.execute()

    print(response)


def test_start():
    __access_token: str = input("google oauth2로부터 받은 access token을 입력하세요 : ")
    __file_path: str = input("업로드할 동영상의 절대 경로를 입력해주세요 : ")
    __title: str = input("업로드할 동영상 제목 : ")
    __description: str = input("업로드할 동영상 설명 : ")
    upload_to_youtube(__access_token, __title, __description, __file_path)


if __name__ == "__main__":
    start_consume()