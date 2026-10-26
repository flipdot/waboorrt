#!/bin/bash
set -euo pipefail

alembic upgrade head

if [ -n "$WEBSERVER_API_KEY" ]; then
  python manage.py create-api-key --key $WEBSERVER_API_KEY
fi
uvicorn --host 0.0.0.0 --port 80 --proxy-headers --forwarded-allow-ips="*" app:app
