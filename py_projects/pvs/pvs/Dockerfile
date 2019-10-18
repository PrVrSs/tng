FROM python:3.7.3-slim-stretch

WORKDIR /pvs

RUN apt-get update

RUN apt-get -y install gcc

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

VOLUME [ "/pvs" ]

EXPOSE 8000

# CMD ["python", "-m", "pvs.__main__"]

CMD ["gunicorn", "pvs.__main__:init_app(\"pvs/config.ini\", \"--dev\")", "-c", "pvs/gunicorn.conf.py"]
