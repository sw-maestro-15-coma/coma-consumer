import os
import ffmpeg


def convert_audio(video_id: int, video_path: str) -> str:
    audio_path = f"{os.environ.get("audio_path")}/{video_id}.mp3"
    ffmpeg.input(video_path).output(audio_path).run()

    return audio_path


def delete_audio(audio_path: str):
    os.remove(audio_path)
