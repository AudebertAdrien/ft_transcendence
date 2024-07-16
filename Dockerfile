FROM python:3.12.4

WORKDIR /ft_transcendence

RUN apt update && apt upgrade -y
RUN apt install -y	vim 

COPY requirements.txt .
COPY manage.py .

RUN python3 -m venv venv
RUN venv/bin/pip3 install --upgrade pip
RUN venv/bin/pip3 install --no-cache-dir -r requirements.txt

COPY . .

#RUN venv/bin/python3 manage.py migrate --noinput
#RUN venv/bin/python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
