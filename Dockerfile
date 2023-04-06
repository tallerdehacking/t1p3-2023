FROM python:slim-bullseye

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "server1.py"] 