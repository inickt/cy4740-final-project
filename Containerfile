FROM python:3.9.1-slim-buster

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY src/ .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "proxy.py" ]
