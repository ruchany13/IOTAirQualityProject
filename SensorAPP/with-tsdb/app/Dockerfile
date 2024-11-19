FROM ubuntu:latest

WORKDIR /user/src/app

COPY requirements.txt .

# libgpiod2 necessearry for control GPIO
RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get install -y libgpiod2 && \ 
    apt install -y python3-pip

RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# influxdb connection variables
ENV TOKEN=
ENV ORG=
ENV HOST=
ENV BUCKET=

COPY app.py .
RUN chmod u+x ./*.py

CMD ["python3" , "-u" ,"app.py"]