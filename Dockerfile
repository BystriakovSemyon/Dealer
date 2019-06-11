FROM python:3.7

RUN pip install -r requirements.txt 

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./Dealer /app

CMD ["python", "watcher.py"]