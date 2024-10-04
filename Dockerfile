FROM python:3.12-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install poetry && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev

COPY . .

# For development
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
