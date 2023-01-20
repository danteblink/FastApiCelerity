FROM tiangolo/uvicorn-gunicorn:python3.8

COPY ./app /app

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN apt update
RUN apt-get -y install libzbar0
RUN apt-get -y install ffmpeg
RUN apt-get -y install poppler-utils
RUN apt-get -y install swig
RUN apt-get -y install libpulse-dev libasound2-dev
RUN apt-get -y install wget
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get -y install ./google-chrome-stable_current_amd64.deb
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install