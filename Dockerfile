FROM python:3.12-bookworm

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y tzdata

ENV TZ=Asia/Seoul

RUN pip install --upgrade pip && pip install poetry && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
