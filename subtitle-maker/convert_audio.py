import ffmpeg


def convert_audio(video_id: int, video_path: str) -> str:
    audio_path = f"/Users/octoping/Documents/audio/{video_id}.mp3"
    ffmpeg.input(video_path).output(audio_path).run()

    return audio_path
