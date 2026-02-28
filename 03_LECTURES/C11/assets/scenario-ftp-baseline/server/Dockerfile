FROM python:3.12-slim

WORKDIR /app

# pyftpdlib is required by ftp_server.py (FTP server implementation).
RUN pip install --no-cache-dir pyftpdlib

# The actual server script is bind-mounted by docker-compose for easy editing.
CMD ["python", "ftp_server.py"]
