FROM python:3.12.2-slim

RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry install --only main --no-root

COPY yarvet_syncronizer /yarvet_syncronizer

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["python", "-m", "yarvet_syncronizer"]