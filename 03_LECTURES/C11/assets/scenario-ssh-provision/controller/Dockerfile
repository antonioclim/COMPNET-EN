FROM python:3.12-slim

WORKDIR /app

# paramiko is required by provision.py for SSH automation.
RUN pip install --no-cache-dir paramiko

# Scripts are bind-mounted by docker-compose for easy editing.
CMD ["python", "provision.py"]
