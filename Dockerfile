FROM python:3.10-bullseye

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION 1.3.2

RUN pip install "poetry==$POETRY_VERSION" && poetry config virtualenvs.create false

WORKDIR /tmp

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi

WORKDIR /bot

ENTRYPOINT [ "watchmedo", "auto-restart", "--debug-force-polling", "python", "--", "-m", "kwenta.bot" ]
