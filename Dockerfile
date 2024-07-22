FROM python:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /transcendence

RUN apt update && apt upgrade -y
RUN apt install -y	vim 

COPY requirements.txt .

RUN python3 -m venv venv
RUN venv/bin/pip3 install --upgrade pip
RUN venv/bin/pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files during the build
RUN venv/bin/python manage.py collectstatic --noinput

EXPOSE 80

# CMD ["venv/bin/python", "manage.py", "runserver", "0.0.0.0:80"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "80", "pong.asgi:application"]