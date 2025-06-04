# I don't use Python as a base image because of size. When build with Python size is 1.2 GB, with ubuntu like 500 MB
FROM ubuntu:latest

WORKDIR /user/src/app

COPY requirements.txt .

# libgpiod2 necessearry for control GPIO
RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get install -y libgpiod2 && \ 
    apt install -y python3-pip

# used  --break-system-packages because there is conflict between apt and pip
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

COPY app.py .
RUN chmod u+x ./*.py

CMD ["python3" , "-u" ,"app.py"]