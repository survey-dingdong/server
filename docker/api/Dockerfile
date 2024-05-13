FROM python:3.11.9-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1

FROM base AS builder

# Install poetry
RUN python -m pip install --upgrade pip && pip install poetry
RUN apt-get update && apt-get install -y gcc

# Install python dependencies in /.venv
COPY pyproject.toml .
RUN POETRY_VIRTUALENVS_IN_PROJECT=1 poetry install

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=builder /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

#Dockerize
ENV DOCKERIZE_VERSION v0.7.0
RUN apt-get update && apt-get install -y wget \
    && wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

WORKDIR /survey-dingdong
