from python:3.5.5-alpine3.4
RUN mkdir -p /opt/apps
WORKDIR /opt/apps
EXPOSE 5000
COPY run.py resources.py requirements.txt tests.py /opt/apps/
RUN pip install -r requirements.txt
CMD [ "python", "run.py" ]
