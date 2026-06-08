# Build a container that serves the FastAPI app.
# Build:  docker build -t resume-matcher-api .
# Run:    docker run -p 8000:8000 resume-matcher-api   (docs at http://localhost:8000/docs)

FROM python:3.14-slim

# Don't write .pyc files; flush logs straight to the container output.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements FIRST and install them as their own layer. Docker caches
# this layer, so it only reinstalls dependencies when requirements.txt changes,
# not every time you edit the source code. This is why dependency install and
# code copy are separate steps.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the application code.
COPY . .

EXPOSE 8000

# 0.0.0.0 (not 127.0.0.1) so the API is reachable from outside the container.
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
