FROM python:3.13.3-slim

WORKDIR /user/src/app

COPY requirements.txt .

#Install required packages for gcc and RPIO
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libgpiod2 && \
    # Clean unnecesearry repos
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# used  --break-system-packages because there is conflict between apt and pip
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

COPY app.py .
RUN chmod u+x ./*.py

CMD ["python3" , "-u" ,"app.py"]