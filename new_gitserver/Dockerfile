FROM golang:1-alpine AS build
COPY ./ /app
WORKDIR /app
RUN go build

FROM alpine
COPY --from=build /app/gitserver /app
WORKDIR /app
EXPOSE 2222
CMD ["./gitserver"]
