FROM golang:1-alpine AS build
WORKDIR /app
COPY ./ ./
RUN go build

FROM alpine
WORKDIR /app
COPY --from=build /app/gitserver ./
EXPOSE 2222
CMD ["./gitserver"]
