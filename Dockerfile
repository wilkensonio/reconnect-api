ARG PYTHON_VERSION=3.12.6
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app 
COPY . .env 
COPY . ./requirements.txt
COPY . .

RUN ls -la /app

RUN ls -la /app/api


# Install the application's dependencies.
RUN  pip install --no-cache-dir -r requirements.txt



EXPOSE 8000  

CMD python3 -m uvicorn api.main:app --host=0.0.0.0 --port=8000