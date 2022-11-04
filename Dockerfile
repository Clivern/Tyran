FROM python:3.12

RUN apt-get update

RUN pip install --upgrade pip

RUN mkdir /app

COPY requirements.freeze.txt /app/

WORKDIR /app

RUN pip install -r requirements.freeze.txt

COPY . /app

EXPOSE 8000

VOLUME /app/storage

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
