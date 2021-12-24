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

COPY * ./
COPY static/ static/
COPY --from=frontend /app/dist static/webapp
COPY templates/ templates/
COPY account/ account/
COPY authentication/ authentication/
COPY internal internal/
COPY legacy/ legacy/
COPY migrations/ migrations/

EXPOSE 80
ENTRYPOINT ["pipenv", "run"]
CMD ["sh", "start.sh"]