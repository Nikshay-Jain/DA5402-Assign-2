FROM apache/airflow:2.10.5

USER root

# Install Postgresql
RUN apt-get update && apt-get install -y postgresql-client

# Install Firefox and GeckoDriver
RUN apt-get install -y \
    firefox-esr \
    wget \
    && wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz \
    && tar -xzf geckodriver-v0.30.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.30.0-linux64.tar.gz

USER airflow

COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt