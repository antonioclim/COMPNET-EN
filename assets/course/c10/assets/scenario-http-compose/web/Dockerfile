FROM python:3.12-slim

WORKDIR /app
COPY server.py /app/server.py
COPY index.html /app/index.html

EXPOSE 8000
CMD ["python", "server.py"]
