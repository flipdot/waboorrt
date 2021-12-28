FROM docker:20.10

RUN apk add inotify-tools git redis curl

WORKDIR /app
COPY start.sh /app/start.sh

CMD ["sh", "start.sh"]