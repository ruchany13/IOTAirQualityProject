FROM ubuntu:latest

WORKDIR /user/src/app

COPY requirements.txt .

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y libgpiod2
RUN apt install -y python3-pip
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

ENV TOKEN=
ENV ORG=
ENV HOST=
ENV BUCKET=

COPY app.py .
RUN chmod u+x ./*.py

CMD ["python3" , "-u" ,"app.py"]