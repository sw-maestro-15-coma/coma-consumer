FROM python:3.12-slim AS builder

#COPY model.zip /model.zip

RUN apt-get update && \
    apt-get install -y wget unzip && \
    apt-get install -y git

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN wget -O model.zip "https://video-process-test-bucket.s3.ap-northeast-2.amazonaws.com/model.zip" && \
    unzip model.zip


FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /model /app/model

COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
COPY s3.py /app/s3.py
COPY subtitle.py /app/subtitle.py
COPY whisper_subtitle_generator.py /app/whisper_subtitle_generator.py
COPY convert_audio.py /app/convert_audio.py

ENV audio_path /app/audio
ENV model_path /app/model
ENV video_path /app/video

RUN mkdir "$audio_path" "$model_path" "$video_path"

ENTRYPOINT ["python3", "main.py"]
