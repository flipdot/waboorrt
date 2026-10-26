FROM node AS frontend

WORKDIR /app

COPY frontend/package.json /app/package.json
COPY frontend/package-lock.json /app/package-lock.json
RUN npm ci

COPY frontend /app
RUN npm run build

FROM python:3.8

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./
COPY --from=frontend /app/dist static/webapp

EXPOSE 80
CMD ["./start.sh"]