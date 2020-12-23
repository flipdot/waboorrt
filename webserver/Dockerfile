FROM python:3.8

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv sync

COPY * ./

EXPOSE 80
ENTRYPOINT ["pipenv", "run"]
CMD ["gunicorn", "-w 2", "-b", "0.0.0.0:80", "app:app"]