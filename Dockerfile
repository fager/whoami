FROM python:3.5-jessie

LABEL "Maintainer"="Alexandre Maldémé" \
        "version"="0.1"


# Add the app in /opt
ADD . /opt

# Working directory for "CMD"
WORKDIR /opt

# Set Flask env variables
ENV FLASK_APP=app.py \
    FLASK_DEBUG=1

# By default Flask use port 5000
EXPOSE 5000

# Install Flask via pip
RUN pip install flask

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]