FROM python:3.8

COPY --from=ghcr.io/astral-sh/uv:0.13.5@sha256:a12ede1e6dc90d3b3e600d0901731e71f0ab0f4d72683ea097b76c19c43cc8df /uv /uvx /bin/

WORKDIR /app

ENV UV_FROZEN=1
COPY pyproject.toml uv.lock ./
RUN uv sync

COPY ./ ./

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 80
CMD ["python", "app.py"]
