FROM python:3.12

RUN apt-get update

RUN pip install --upgrade pip
RUN pip install uv

RUN mkdir /app

COPY pyproject.toml /app/
COPY uv.lock /app/

WORKDIR /app

RUN uv pip install -r pyproject.toml

COPY . /app

EXPOSE 8000

VOLUME /app/storage

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
