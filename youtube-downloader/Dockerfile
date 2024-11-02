FROM python:3.12-slim

# Set the working directory
COPY . /app

# Set the locale
RUN apt update && apt install -y locales
RUN locale-gen ko_KR.UTF-8
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

# Install yt-dlp
RUN apt install -y yt-dlp
RUN apt install -y ffmpeg
# Install python dependencies
RUN pip3 install -r /app/requirements.txt

# Run the main.py
ENTRYPOINT ["python3", "/app/main.py"]