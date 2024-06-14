FROM python:3.12.4-slim-bookworm AS build-stage

COPY requirements.txt ./

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


FROM python:3.12.4-slim-bookworm AS serve-stage

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y --no-install-recommends \
    build-essential \
    nginx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

COPY default.conf /etc/nginx/conf.d/default.conf

COPY --from=build-stage /wheels ./wheels

RUN pip install --no-cache ./wheels/*

EXPOSE 8000

CMD sh -c "uvicorn main:app --host 127.0.0.1 --port 8000 & nginx -g 'daemon off;'"