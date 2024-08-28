FROM python:3.12

COPY . /app

RUN apt update && apt install -y locales
RUN locale-gen ko_KR.UTF-8
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

ADD extrabold.ttf /usr/share/fonts/truetype/extrabold.ttf
RUN apt install -y ffmpeg
RUN pip3 install -r /app/requirements.txt

ENTRYPOINT ["python3", "/app/main.py"]