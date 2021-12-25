FROM golang:1-alpine AS build
COPY ./ /app
WORKDIR /app
RUN go build
RUN go build hooks/post-receive.go

FROM alpine
RUN apk add git bash
COPY --from=build /app/gitserver /app/
COPY --from=build /app/post-receive /app/
WORKDIR /app
EXPOSE 2222
CMD ["./gitserver"]
