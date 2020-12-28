FROM python:3.8

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv sync

COPY * ./
COPY static/ static/
COPY templates/ templates/

EXPOSE 80
ENTRYPOINT ["pipenv", "run"]
CMD ["sh", "start.sh"]