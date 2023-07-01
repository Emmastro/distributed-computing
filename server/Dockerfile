FROM python:3.10-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python3 manage.py collectstatic --noinput
RUN python3 manage.py migrate

# Load Demo data

RUN python3 manage.py loaddata fixtures/demo_data.json

ENV PORT=8000
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 server.wsgi:application
