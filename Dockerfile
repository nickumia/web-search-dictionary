FROM python:latest

# Config and Setup
ENV GECKODRIVER_VER v0.30.0
ENV FIREFOX_VER 97.0
WORKDIR /boc

# Install Firefox
RUN set -x \
   && apt update \
   && apt upgrade -y \
   && apt install -y \
       firefox-esr
RUN set -x \
   && apt install -y \
       libx11-xcb1 \
       libdbus-glib-1-2 \
   && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
   && tar -jxf firefox-* \
   && mv firefox /opt/ \
   && chmod 755 /opt/firefox \
   && chmod 755 /opt/firefox/firefox

# Install geckodriver
RUN curl -f -L https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz | tar xvz \
	&& mv geckodriver /usr/bin/

# Dependencies
COPY requirements.txt dev-requirements.txt setup.py /boc/
COPY websearchdict/ /boc/websearchdict/

RUN pip install --no-cache-dir -r requirements.txt -r dev-requirements.txt
