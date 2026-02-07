FROM python:3.12-slim

WORKDIR /app
RUN pip install --no-cache-dir paho-mqtt==2.1.0

COPY actuator.py /app/actuator.py

CMD ["python", "actuator.py"]
