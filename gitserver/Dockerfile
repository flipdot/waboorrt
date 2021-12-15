FROM ubuntu:20.04

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get -y update && apt-get install -y openssh-server
RUN ssh-keygen -A
###########################################################################################
# if you touch anything above everyone will get certificate warnings when using git / ssh #
#                                      think twice                                        #
###########################################################################################

RUN apt-get install -y sudo redis-tools
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y gitolite3
RUN mkdir -p /run/sshd
# RUN git config --global user.email "com@flipdot.org"; git config --global user.name "flipbot"

COPY bot-templates /app/bot-templates
COPY sshd_config /etc/ssh/sshd_config
COPY start.sh /start.sh
COPY newbot.sh /usr/local/bin/newbot
COPY post-receive.sh /app/post-receive.sh
RUN chmod +x /app/post-receive.sh
RUN chmod +x /usr/local/bin/newbot
RUN mkdir -p /botbuilder
RUN chmod 777 /botbuilder

# COPY gitolite.conf /app/post-receive.sh
COPY gitolite.rc /app/gitolite.rc
RUN sudo adduser --system --shell /bin/bash --group --disabled-password --home /home/git git

# Volume used to store all Gitolite data (keys, config and repositories), initialized on first run
VOLUME /home/git

# Volume used to store SSH host keys, generated on first run
VOLUME /etc/ssh/keys

EXPOSE 22
CMD ["sh", "/start.sh"]
