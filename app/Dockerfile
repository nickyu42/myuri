FROM python:3.8.6-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

# Copy all our files into the image.
COPY requirements.txt requirements.txt

ENV PATH="/root/.local/bin:${PATH}"

# Install our requirements.
RUN pip install --user --no-cache-dir -Ur requirements.txt

COPY . /code/

EXPOSE 8000

# Specify the command to run when the image is run.
CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
