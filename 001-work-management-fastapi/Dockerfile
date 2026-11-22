FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/python-lib-core

COPY requirements-docker.txt /tmp/requirements-docker.txt
RUN pip install --no-cache-dir -r /tmp/requirements-docker.txt \
    && useradd --system --uid 10001 --no-create-home app \
    && install -d -o app -g app /data

WORKDIR /app/python-web-fastapi
COPY python-lib-core/ /app/python-lib-core/
COPY python-web-fastapi/ /app/python-web-fastapi/

USER app
EXPOSE 3000
CMD ["python", "app.py"]
