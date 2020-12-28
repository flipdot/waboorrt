FROM node AS frontend

COPY frontend /app

WORKDIR /app

RUN npm ci
RUN npm run build


FROM python:3.8

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv sync

COPY * ./
COPY static/ static/
COPY --from=frontend /app/dist static/webapp
COPY templates/ templates/

EXPOSE 80
ENTRYPOINT ["pipenv", "run"]
CMD ["sh", "start.sh"]