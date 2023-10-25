FROM python:3.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc make

COPY . .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip uninstall -y werkzeug \
    && pip install werkzeug==2.3.0 \
    && pip install cryptography

EXPOSE 5101

CMD ["make", "start"]