FROM python:alpine 
RUN pip install flask flask_restful requests pyyaml
RUN apk update;apk upgrade;apk add bash
COPY exporter/ exporter/
WORKDIR /exporter
EXPOSE 5002
CMD python exporter.py