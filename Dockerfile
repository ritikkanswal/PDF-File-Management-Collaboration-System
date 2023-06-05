FROM joyzoursky/python-chromedriver
ARG SSH_PRIVATE_KEY
RUN apt-get update
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN export DJANGO_SETTINGS_MODULE=pdf_management_collaboration_system.settings
