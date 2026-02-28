FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir paho-mqtt==2.1.0

COPY mqtt_cli.py /app/mqtt_cli.py

ENTRYPOINT ["python", "/app/mqtt_cli.py"]
