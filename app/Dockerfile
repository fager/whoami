FROM tiangolo/uwsgi-nginx-flask:python3.6

LABEL "Maintainer"="Frank Agerholm" \
        "version"="0.1"


COPY . /app
RUN pip install -r /app/requirements.txt

