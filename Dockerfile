FROM python:3.12.4

WORKDIR /ft_transcendence

RUN apt update && apt upgrade -y

COPY requirements.txt .
COPY manage.py .

RUN python3 -m venv venv
RUN venv/bin/pip3 install --upgrade pip
RUN venv/bin/pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000
