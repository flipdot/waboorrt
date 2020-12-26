FROM ubuntu:20.04

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get -y update && apt-get install -y openssh-server git sudo
RUN ssh-keygen -A
RUN mkdir -p /run/sshd

WORKDIR /git

COPY sshd_config /etc/ssh/sshd_config
COPY start.sh /start.sh
COPY newbot.sh /usr/local/bin/newbot

VOLUME /git
EXPOSE 22
CMD ["sh", "/start.sh"]
