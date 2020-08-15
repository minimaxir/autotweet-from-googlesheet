FROM python:3.8.5-slim-buster

RUN apt-get -y update && apt-get -y install gcc

WORKDIR /

# Make changes to the requirements/app here.
# This Dockerfile order allows Docker to cache the checkpoint layer
# and improve build times if making changes.
RUN pip3 --no-cache-dir install starlette uvicorn tweepy gspread
COPY * /

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENTRYPOINT ["python3", "-X", "utf8", "app.py"]