FROM python:3.12-slim

WORKDIR /app

# dnspython is required by query.py for explicit resolver control and TTL visibility.
RUN pip install --no-cache-dir dnspython

# The actual script is bind-mounted by docker-compose for easy editing.
CMD ["python", "query.py"]
