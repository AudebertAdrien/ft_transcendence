FROM python:3.8

WORKDIR /ft_transcendence

EXPOSE 8000

ENTRYPOINT ["tail", "-f", "/dev/null"]
