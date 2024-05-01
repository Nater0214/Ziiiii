# Setup
FROM python:3.12.3
WORKDIR /bot

# Install firefox and ffmpeg
RUN apt-get update -y
RUN apt-get install -y firefox-esr ffmpeg

# Instal pip requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy files
COPY . .

# Command
CMD python3 main.py
