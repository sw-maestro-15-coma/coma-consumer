FROM python:3.12

RUN mkdir files

COPY . .

RUN apt update && apt install -y locales
RUN locale-gen ko_KR.UTF-8
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]