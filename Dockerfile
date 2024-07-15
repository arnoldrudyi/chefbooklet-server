FROM python:3.11

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PROJECT_DIR="/cooking"

RUN apt-get update && \
    apt-get install -qy \
        cmake \
        build-essential \
        libhiredis-dev \
        libpq-dev

RUN mkdir /$PROJECT_DIR

WORKDIR $PROJECT_DIR
ADD . $PROJECT_DIR

RUN pip install --upgrade pip setuptools
ADD ./requirements.txt ./
ADD ./start.sh start
RUN chmod +x start

RUN mkdir logs
RUN pip install -r requirements.txt

CMD ["./start"]