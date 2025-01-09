#!/bin/bash

uv run python manage.py migrate && \
uv run gunicorn --log-level debug --access-logfile - --error-logfile - base.asgi:application -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --workers 4 --threads 2