FROM python:3.10-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . .

CMD [ "python3", "main.py" ]
