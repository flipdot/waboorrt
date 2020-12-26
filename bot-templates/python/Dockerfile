FROM python:3.8

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv sync

COPY ./ ./

EXPOSE 4000
ENTRYPOINT ["pipenv", "run"]
CMD ["python", "bot.py"]