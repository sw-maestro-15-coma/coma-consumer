FROM python:3.12-slim AS builder

#COPY model.zip /model.zip

RUN apt-get update
RUN apt-get install -y unzip
RUN apt-get install -y git
RUN apt-get install -y ffmpeg

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD https://video-process-test-bucket.s3.ap-northeast-2.amazonaws.com/model.zip /model.zip
RUN unzip model.zip


FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/bin/ffmpeg /usr/bin/ffmpeg
COPY --from=builder . /app

COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
COPY s3.py /app/s3.py
COPY subtitle.py /app/subtitle.py
COPY whisper_subtitle_generator.py /app/whisper_subtitle_generator.py
COPY convert_audio.py /app/convert_audio.py

ENV audio_path /app/audio
ENV model_path /app/model
ENV video_path /app/video

RUN mkdir "$audio_path" "$video_path"

ENTRYPOINT ["python3", "main.py"]
