FROM python:3

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP run.py
ENV FLASK_ENV development

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD bash -c 'while !</dev/tcp/postgresql/5432; do sleep 1; done; flask run --host 0.0.0.0'
