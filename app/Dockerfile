FROM python:3.8.6-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Copy all our files into the image.
COPY requirements.txt requirements.txt

# Install our requirements.
RUN pip install --user --no-cache-dir -Ur requirements.txt

ENV PATH="/home/${APP_USER}/.local/bin:${PATH}"

# Remove gcc
RUN apt-get autoremove -y gcc

COPY . /code/

EXPOSE 8000

# Specify the command to run when the image is run.
CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
