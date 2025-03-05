#!/usr/bin/env bash
FROM python:3.12

# handling GCP Secret
ARG GOOGLE_CREDENTIALS_BASE64
RUN mkdir -p /app/credentials
# ENV GOOGLE_APPLICATION_CREDENTIALS="./secrets/donna_secret.json"
ENV EMAIL_PASSWORD='xmtviazvfgslauub'
ENV EMAIL_ADDRESS='bhaikiizzat.69@gmail.com'

COPY . /app/ 
#you need to keep this different from port of application I guess this is port on which docker container is exposed
EXPOSE 5000 
WORKDIR /app/ 
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV ENV="production"


RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y  && pip install --upgrade pip && pip install -r requirements.txt 
CMD ["streamlit",  "run", "app.py", "--server.port", "8501"] 