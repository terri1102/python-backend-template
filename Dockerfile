FROM python:3.12-bookworm

WORKDIR /usr/src/app

RUN pip install --upgrade pip && pip install poetry && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
