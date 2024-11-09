FROM python:3.12-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y unzip
RUN apt-get install -y git
RUN apt-get install -y ffmpeg
RUN apt-get install -y libgomp1


ADD https://video-process-test-bucket.s3.ap-northeast-2.amazonaws.com/model.zip /app/model.zip
RUN unzip model.zip
RUN rm model.zip

COPY requirements.txt .

COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
COPY s3.py /app/s3.py
COPY subtitle.py /app/subtitle.py
COPY whisper_subtitle_generator.py /app/whisper_subtitle_generator.py
COPY convert_audio.py /app/convert_audio.py
COPY rearrange_subtitle.py /app/rearrange_subtitle.py

RUN pip install --no-cache-dir -r requirements.txt

ENV audio_path /app/audio
ENV model_path /app/model
ENV video_path /app/video

RUN mkdir "$audio_path" "$video_path"

ENTRYPOINT ["python3", "main.py"]
