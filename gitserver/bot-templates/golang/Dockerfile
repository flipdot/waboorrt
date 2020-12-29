FROM golang:alpine

WORKDIR /app
COPY ./ ./

RUN ["go", "build", "-o", "bot", "."]

EXPOSE 4000
CMD ["./bot"]
