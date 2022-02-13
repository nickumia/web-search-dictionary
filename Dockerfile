FROM python:latest

# Config and Setup
WORKDIR /boc

# Dependencies
COPY requirements.txt dev-requirements.txt setup.py /boc/
COPY wsd/ /boc/wsd/

RUN pip install --no-cache-dir -r requirements.txt -r dev-requirements.txt
