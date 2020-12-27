FROM docker:20.10

RUN apk add inotify-tools git

WORKDIR /app
COPY start.sh /app/start.sh

VOLUME /git /botbuilder
CMD ["sh", "start.sh"]