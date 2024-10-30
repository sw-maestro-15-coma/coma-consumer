FROM python:3.12-slim

COPY . /app
RUN mkdir output
RUN mkdir text
RUN mkdir thumbnail
RUN mkdir subtitle

RUN apt update && apt install -y locales && apt clean
RUN locale-gen ko_KR.UTF-8
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

RUN pip3 install -r /app/requirements.txt

ENTRYPOINT ["python3", "/app/main.py"]