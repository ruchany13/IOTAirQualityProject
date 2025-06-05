FROM python:3.13.3-slim

WORKDIR /user/src/app

COPY requirements.txt .

# used  --break-system-packages because there is conflict between apt and pip
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

COPY app.py .
RUN chmod u+x ./*.py

CMD ["python3" , "-u" ,"app.py"]