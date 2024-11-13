FROM node:lts-slim
WORKDIR /
COPY . .
RUN npm install && npm install typescript -g
RUN tsc
RUN apt update && apt install -y ffmpeg
RUN mkdir /node_modules/ffprobe-static/bin/linux/arm64
RUN cp /usr/bin/ffprobe /node_modules/ffprobe-static/bin/linux/arm64/ffprobe
ENTRYPOINT ["node", "/dist/main.js"]
EXPOSE 7000