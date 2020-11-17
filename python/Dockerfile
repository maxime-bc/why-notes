FROM python:3

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP run.py
ENV FLASK_ENV development

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD flask run --host 0.0.0.0