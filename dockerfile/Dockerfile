FROM python:2.7-slim

WORKDIR /app

ADD . /app 

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD ["python","raspi/start_webserver.py"]
