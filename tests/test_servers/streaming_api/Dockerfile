FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn

# Copy server file
COPY server.py .

# Expose port
EXPOSE 8000

# Run the server
CMD ["python", "server.py"]
