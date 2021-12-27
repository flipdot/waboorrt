FROM node AS frontend

WORKDIR /app

COPY frontend/package.json /app/package.json
COPY frontend/package-lock.json /app/package-lock.json
RUN npm ci

COPY frontend /app
RUN npm run build

FROM python:3.8

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv sync

COPY ./ ./
COPY --from=frontend /app/dist static/webapp

EXPOSE 80
ENTRYPOINT ["pipenv", "run"]
CMD ["sh", "start.sh"]