FROM python:slim-bullseye

ENV PYTHONUNBUFFERED=1

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "server1.py"] 