# Use the Python 3 official image
# https://hub.docker.com/_/python
FROM python:3.12-slim

# Run in unbuffered mode and set default port
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Create and change to the app directory.
WORKDIR /app

# Copy local code to the container image.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./

# Railway requires listening on 0.0.0.0 and $PORT
EXPOSE 8080

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080", "--workers", "2"]